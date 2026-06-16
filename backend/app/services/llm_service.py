"""
LLM Service
Handles text generation using Google Gemini API
Provides explanations for recipe recommendations
"""

import json
import logging
import re
import time
from typing import List, Optional, Dict, Any
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from app.config import settings
from app.models.recipe import Recipe

# Setup logger
logger = logging.getLogger(__name__)


def _strip_code_fences(raw: str) -> str:
    """Remove markdown code fences from LLM output."""
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3].rstrip()
    if raw.startswith("json"):
        raw = raw[4:].lstrip()
    return raw


def _normalize_llm_json(text: str) -> str:
    """Convert Python-style literals to valid JSON."""
    text = re.sub(r'\bNone\b', 'null', text)
    text = re.sub(r'\bTrue\b', 'true', text)
    text = re.sub(r'\bFalse\b', 'false', text)
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)
    return text


class LLMService:
    """
    Service for generating explanations using Google Gemini API
    Provides personalized recipe recommendation explanations
    """

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self.fallback_model = getattr(settings, "GEMINI_FALLBACK_MODEL", None)
        self.max_tokens = settings.GEMINI_MAX_TOKENS
        self.temperature = settings.GEMINI_TEMPERATURE
        self.enabled = settings.GEMINI_ENABLED
        self.client: Optional[genai.Client] = None
        self._model_loaded = False

    def _load_model(self):
        """Initialize Gemini API client"""
        if not self.enabled:
            logger.debug("LLM service is disabled")
            return

        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            logger.warning("LLM explanations will be disabled")
            self.enabled = False
            return

        if not self._model_loaded:
            try:
                logger.info(f"Initializing Gemini API: {self.model_name}")
                self.client = genai.Client(api_key=self.api_key)
                self._model_loaded = True
                logger.info(f"Gemini client initialized for model: {self.model_name}")
            except Exception as e:
                logger.exception(f"Error initializing Gemini API: {e}")
                logger.warning("LLM explanations will be disabled")
                self.enabled = False
                self._model_loaded = False
                raise

    def is_available(self) -> bool:
        """Check if LLM service is available and ready"""
        return self.enabled and self._model_loaded and self.client is not None

    def _get_quota_delay(self, msg: str) -> float:
        """Extract retry delay (seconds) from a Gemini 429 error message."""
        match = re.search(r'retry in (\d+(?:\.\d+)?)s', msg, re.I)
        return min(float(match.group(1)) if match else 20, 60)

    def _try_with_model(self, model_name: str, prompt: str, config, max_retries: int, is_last_model: bool):
        """Attempt generation with one model, retrying on quota errors.

        Returns the API response on success, None to signal 'try next model',
        or raises on a non-retryable error.
        """
        for attempt in range(max_retries + 1):
            try:
                return self.client.models.generate_content(
                    model=model_name, contents=prompt, config=config
                )
            except ClientError as e:
                if e.code != 429:
                    raise
                if attempt < max_retries:
                    delay = self._get_quota_delay(str(e))
                    logger.warning(f"Gemini quota (429), {delay:.0f}s sonra tekrar deniyor...")
                    time.sleep(delay)
                elif not is_last_model:
                    logger.info(f"Ana model kota aşıldı, fallback ({self.fallback_model}) deneniyor...")
                    return None
                else:
                    logger.warning("Gemini API kota aşıldı (429)")
                    raise
        return None

    def _try_generate_with_retry(self, prompt: str, config: types.GenerateContentConfig, max_retries: int = 1):
        """429 quota hatasında retry ve model fallback dene."""
        models_to_try = [self.model_name]
        if self.fallback_model and self.model_name != self.fallback_model:
            models_to_try.append(self.fallback_model)

        for i, model_name in enumerate(models_to_try):
            result = self._try_with_model(model_name, prompt, config, max_retries, i == len(models_to_try) - 1)
            if result is not None:
                return result

    # Interaction type → human-readable Turkish label for prompt injection
    _HISTORY_LABELS: Dict[str, str] = {
        "like": "beğendi",
        "cook": "daha önce pişirdi",
        "save": "kaydetmişti",
        "skip": "atladı",
    }

    def _build_history_note(self, user_history: Dict[str, str]) -> str:
        """Build the personalization note from user interaction history."""
        liked = [t for t, a in user_history.items() if a in ("like", "cook", "save")]
        skipped = [t for t, a in user_history.items() if a == "skip"]
        note = ""
        if liked:
            note += f"\nKullanıcı geçmişte şu tarifleri beğendi/pişirdi: {', '.join(liked[:5])}."
        if skipped:
            note += f"\nKullanıcı şu tarifleri daha önce atladı (ilgilenmedi): {', '.join(skipped[:5])}."
        return note

    def _build_preferences_part(self, user_preferences: Dict[str, Any]) -> Optional[str]:
        """Return a formatted context string for dietary preferences, or None if none active."""
        active_prefs = []
        if user_preferences.get('vegan'):
            active_prefs.append('Vegan')
        if user_preferences.get('vegetarian') and not user_preferences.get('vegan'):
            active_prefs.append('Vejetaryen')
        if user_preferences.get('glutenFree'):
            active_prefs.append('Glutensiz')
        if user_preferences.get('dairyFree'):
            active_prefs.append('Süt Ürünü İçermez')
        if user_preferences.get('nutAllergy'):
            active_prefs.append('Kuruyemiş İçermez')
        return f"**Diyet Tercihleri:** {', '.join(active_prefs)}" if active_prefs else None

    def _build_recipe_note(self, recipe: Recipe, user_history: Optional[Dict[str, str]]) -> str:
        """Return a bracketed history note for a recipe, or empty string."""
        if not user_history:
            return ""
        interaction = user_history.get(recipe.Title)
        label = self._HISTORY_LABELS.get(interaction, "") if interaction else ""
        return f" [Kullanıcı bu tarifi daha önce {label}]" if label else ""

    def _build_prompt(
        self,
        user_ingredients: List[str],
        recommended_recipes: List[Recipe],
        user_preferences: Optional[Dict[str, Any]] = None,
        excluded_ingredients: Optional[List[str]] = None,
        user_history: Optional[Dict[str, str]] = None,
    ) -> str:
        """Build prompt for Gemini API, optionally injecting user history context."""
        history_note = self._build_history_note(user_history) if user_history else ""

        system_prompt = f"""Sen profesyonel bir Türk şefisin ve kullanıcının yemek alışkanlıklarını hatırlayan kişisel şefisin. Kullanıcıya elindeki malzemelere en uygun tarifi neden önerdiğini, malzemelerin uyumunu vurgulayarak, samimi ve iştah açıcı bir Türkçe ile açıkla.{history_note}

Kurallar:
- Türkçe yaz, samimi ve sıcak bir dil kullan.
- Düz metin yaz, markdown işaretleri (###, **, * vb.) KULLANMA.
- En fazla 3-4 cümle yaz. Kısa, öz ve iştah açıcı ol.
- Malzemelerin birbirleriyle neden iyi uyum sağladığını vurgula.
- Eğer kullanıcının daha önce beğendiği tarifler önerildiyse bunu sıcak bir dille belirt.
- Her tarifi tek tek listeleme, genel bir şef notu ver.
"""

        context_parts = [f"**Mevcut Malzemeler:** {', '.join(user_ingredients)}"]

        if user_preferences:
            pref_part = self._build_preferences_part(user_preferences)
            if pref_part:
                context_parts.append(pref_part)

        if excluded_ingredients:
            context_parts.append(f"**Hariç Tutulan Malzemeler:** {', '.join(excluded_ingredients)}")

        recipes_text = "\n\nÖnerilen Tarifler:\n"
        for i, recipe in enumerate(recommended_recipes[:3], 1):
            ingredients_text = recipe.Cleaned_Ingredients or recipe.Ingredients
            ingredients_clean = ingredients_text.replace('[', '').replace(']', '').replace("'", '')
            recipe_note = self._build_recipe_note(recipe, user_history)
            recipes_text += f"\n{i}. {recipe.Title}{recipe_note} - Malzemeler: {ingredients_clean[:200]}\n"

        prompt = f"""{system_prompt}
---

Kullanıcı Bilgisi:
{chr(10).join(context_parts)}
{recipes_text}

---

Bu tariflerin neden önerildiğini kısaca özetle. Düz metin yaz, markdown kullanma."""

        return prompt

    def generate_explanation(
        self,
        user_ingredients: List[str],
        recommended_recipes: List[Recipe],
        user_preferences: Optional[Dict[str, Any]] = None,
        excluded_ingredients: Optional[List[str]] = None,
        user_history: Optional[Dict[str, str]] = None,
    ) -> Optional[str]:
        """Generate explanation for recipe recommendations using Gemini API"""
        if not recommended_recipes:
            logger.warning("No recipes provided for explanation generation")
            return None

        if not self.enabled:
            logger.debug("LLM service is disabled, skipping explanation generation")
            return None

        if not self.api_key:
            logger.debug("GEMINI_API_KEY not found, skipping explanation generation")
            return None

        try:
            if not self._model_loaded:
                self._load_model()

            if not self.is_available():
                logger.warning("LLM model could not be loaded, skipping explanation generation")
                return None

            prompt = self._build_prompt(
                user_ingredients=user_ingredients,
                recommended_recipes=recommended_recipes,
                user_preferences=user_preferences,
                excluded_ingredients=excluded_ingredients,
                user_history=user_history,
            )

            logger.debug(f"Generating explanation for {len(recommended_recipes)} recipes")

            config = types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )
            response = self._try_generate_with_retry(prompt, config, max_retries=0)
            explanation = response.text.strip()

            logger.debug(f"Explanation generated: {len(explanation)} characters")

            return explanation

        except ClientError as e:
            if e.code == 429:
                logger.warning("Gemini API kota aşıldı, açıklama atlanıyor")
            else:
                logger.exception(f"Gemini API client error: {e}")
            return None
        except Exception as e:
            logger.exception(f"Error generating explanation: {e}")
            logger.warning("Returning None for explanation")
            return None

    def _parse_llm_json(self, raw: str) -> Optional[Dict[str, Any]]:
        """Parse and normalize LLM JSON output, with regex fallback on failure."""
        normalized = _normalize_llm_json(raw)
        try:
            return json.loads(normalized)
        except json.JSONDecodeError as parse_err:
            match = re.search(r'\{[\s\S]*\}', raw)
            if match:
                try:
                    return json.loads(_normalize_llm_json(match.group(0)))
                except json.JSONDecodeError:
                    pass
            logger.warning(
                f"LLM JSON parse failed ({parse_err}), raw response:\n{raw}\n"
                "returning empty substitutions"
            )
            return None

    def generate_substitutions(
        self,
        recipe_title: str,
        missing_ingredients: List[str],
        available_ingredients: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate ingredient substitution suggestions using Gemini API.

        Returns a dict like:
            {"substitutions": {"süt": ["badem sütü", "yulaf sütü"]}, "explanation": "..."}
        or None on failure.
        """
        if not missing_ingredients:
            return {"substitutions": {}, "explanation": None}

        if not self.enabled or not self.api_key:
            logger.debug("LLM service unavailable, skipping substitution generation")
            return None

        try:
            if not self._model_loaded:
                self._load_model()
            if not self.is_available():
                return None

            subs_example = {ing: ["ikame1", "ikame2"] for ing in missing_ingredients[:2]}
            example_str = json.dumps({"substitutions": subs_example, "explanation": "Örnek açıklama"}, ensure_ascii=False)

            prompt = f"""Sen profesyonel bir Türk mutfağı şefisin. Sadece geçerli JSON döndür, başka metin yazma.

Tarif: {recipe_title}
Eksik malzemeler: {', '.join(missing_ingredients)}
Mevcut malzemeler: {', '.join(available_ingredients) if available_ingredients else 'Yok'}

Her eksik malzeme için 1-3 ikame öner (Türk mutfağına uygun). Örnek format:
{example_str}

Yanıtın SADECE bu JSON formatında olsun, tırnak ve virgüllere dikkat et."""

            # thinking_budget=0: JSON üretimi için thinking devre dışı — daha hızlı ve ucuz
            config = types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=2048,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            )
            response = self._try_generate_with_retry(prompt, config)

            raw = _strip_code_fences(response.text.strip())
            result = self._parse_llm_json(raw)

            if result is None:
                return {"substitutions": {}, "explanation": "İkame önerileri şu an yüklenemedi."}

            logger.debug(f"Substitutions generated for {len(missing_ingredients)} ingredients")
            return result

        except ClientError as e:
            if e.code == 429:
                logger.warning("Gemini API kota aşıldı, ikame önerileri boş döndürülüyor")
            else:
                logger.exception(f"Gemini API client error: {e}")
            return {"substitutions": {}, "explanation": None}
        except Exception as e:
            logger.exception(f"Error generating substitutions: {e}")
            return {"substitutions": {}, "explanation": None}

    def get_model_info(self) -> dict:
        """Get information about the LLM service"""
        return {
            "model_name": self.model_name,
            "loaded": self._model_loaded,
            "enabled": self.enabled,
            "has_api_key": bool(self.api_key),
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }


# Singleton instance
llm_service = LLMService()
