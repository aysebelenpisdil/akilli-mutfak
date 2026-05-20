This file is a merged representation of a subset of the codebase, containing specifically included files, combined into a single document by Repomix.
The content has been processed where comments have been removed, content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: src/**/*, backend/**/*, package.json, requirements.txt, vite.config.ts, README.md
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Code comments have been removed from supported file types
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
backend/
  app/
    middleware/
      __init__.py
      auth.py
      rate_limiter.py
    models/
      __init__.py
      auth.py
      feedback.py
      fridge.py
      recipe.py
      shopping_list.py
    routes/
      __init__.py
      auth.py
      feedback.py
      fridge.py
      recipes.py
      shopping_list.py
      user_preferences.py
    services/
      __init__.py
      auth_service.py
      cf_service.py
      database_service.py
      email_service.py
      embedding_service.py
      faiss_service.py
      llm_service.py
      rag_pipeline.py
      recipe_service.py
      reranker_service.py
      tfidf_service.py
    utils/
      __init__.py
      cache.py
      helpers.py
    __init__.py
    config.py
    database.py
    main.py
  data/
    recipe_index_metadata.json
    recipe_index.faiss
    recipes.json
    recipes.ts
  evaluation/
    __init__.py
    baselines.py
    dataset.py
    metrics.py
    reporter.py
    runner.py
    systems.py
  scripts/
    build_faiss_index.py
    build_tfidf_index.py
    copy_variant_images.py
    download_manual_images.py
    download_models.py
    download_recipe_images.py
    evaluate_recommendations.py
    seed_users.py
    set_supabase_password.py
  tests/
    __init__.py
    conftest.py
    test_auth.py
    test_evaluation_metrics.py
    test_feedback.py
    test_fridge.py
    test_health.py
    test_recipes.py
    test_shopping_list.py
    test_survey.py
    test_tfidf_service.py
    test_user_preferences.py
  .env.example
  .gitignore
  .python-version
  pytest.ini
  requirements.txt
src/
  components/
    Navbar.tsx
    RecipeImage.tsx
    RecipeSurvey.tsx
  constants/
    ingredientData.ts
  data/
    calorieData.json
    cleanedIngredients.json
    recipes.ts
  hooks/
    useIngredientSearch.ts
  lib/
    supabase.ts
  pages/
    FridgePage.tsx
    LoginPage.tsx
    PreferencesPage.tsx
    ProfilePage.tsx
    RecipeDetailPage.tsx
    RecipesPage.tsx
    ShoppingListPage.tsx
  store/
    AuthContext.tsx
    FridgeContext.tsx
    RecipeContext.tsx
    ShoppingListContext.tsx
  tests/
    calorieEstimator.test.ts
    helpers.test.ts
    recipeFilter.test.ts
    setup.ts
    shoppingList.test.ts
    utils.test.ts
  utils/
    api.ts
    calorieEstimator.ts
    dietaryRules.ts
    helpers.ts
    ingredientNormalizer.ts
    recipeFilter.ts
  App.tsx
  index.css
  index.tsx
  types.ts
  vite-env.d.ts
package.json
README.md
vite.config.ts
```

# Files

## File: backend/app/middleware/__init__.py
````python

````

## File: backend/app/middleware/auth.py
````python
async def get_current_user(request: Request) -> dict
⋮----
session_id = request.cookies.get("session_id")
⋮----
user = await auth_service.validate_session(session_id)
⋮----
async def get_optional_user(request: Request) -> Optional[dict]
````

## File: backend/app/middleware/rate_limiter.py
````python
limiter = Limiter(key_func=get_remote_address)
````

## File: backend/app/models/__init__.py
````python

````

## File: backend/app/models/fridge.py
````python
class Ingredient(BaseModel)
⋮----
name: str
⋮----
class FridgeRequest(BaseModel)
⋮----
ingredients: List[str]
⋮----
class FridgeResponse(BaseModel)
⋮----
success: bool
message: str
````

## File: backend/app/models/shopping_list.py
````python
class ShoppingListItem(BaseModel)
⋮----
name: str
display_name: str
purchased: bool = False
from_recipes: List[str] = []
⋮----
class ShoppingListPayload(BaseModel)
⋮----
items: List[ShoppingListItem]
````

## File: backend/app/routes/__init__.py
````python

````

## File: backend/app/routes/fridge.py
````python
router = APIRouter(prefix="/fridge", tags=["fridge"])
⋮----
@router.get("/ingredients", response_model=dict)
async def get_ingredients(user: dict = Depends(get_current_user))
⋮----
ingredients = await database_service.get_fridge_ingredients(user["id"])
⋮----
@router.post("/ingredients", response_model=FridgeResponse)
async def save_ingredients(request: FridgeRequest, user: dict = Depends(get_current_user))
````

## File: backend/app/routes/shopping_list.py
````python
router = APIRouter(prefix="/shopping-list", tags=["shopping-list"])
⋮----
@router.get("/items")
async def get_items(user: dict = Depends(get_current_user))
⋮----
items = await database_service.get_shopping_list(user["id"])
⋮----
@router.post("/items")
async def save_items(payload: ShoppingListPayload, user: dict = Depends(get_current_user))
````

## File: backend/app/routes/user_preferences.py
````python
router = APIRouter(prefix="/user", tags=["user"])
⋮----
class PreferencesPayload(BaseModel)
⋮----
dietary: dict
excluded: list[str]
⋮----
@router.get("/preferences")
async def get_preferences(user: dict = Depends(get_current_user))
⋮----
@router.post("/preferences")
async def save_preferences(body: PreferencesPayload, user: dict = Depends(get_current_user))
````

## File: backend/app/services/__init__.py
````python

````

## File: backend/app/services/auth_service.py
````python
logger = logging.getLogger(__name__)
⋮----
serializer = URLSafeTimedSerializer(settings.SESSION_SECRET)
⋮----
def _as_str(val)
⋮----
class AuthService
⋮----
async def create_or_get_user(self, email: str) -> dict
⋮----
result = await conn.execute(
row = result.mappings().fetchone()
⋮----
user_id = str(uuid.uuid4())
now = datetime.utcnow()
⋮----
async def generate_magic_link(self, user_id: str) -> str
⋮----
token = serializer.dumps(user_id, salt="magic-link")
expires_at = datetime.utcnow() + timedelta(seconds=settings.MAGIC_LINK_EXPIRY)
⋮----
async def verify_magic_link(self, token: str) -> dict | None
⋮----
user_id = serializer.loads(token, salt="magic-link", max_age=settings.MAGIC_LINK_EXPIRY)
⋮----
link = result.mappings().fetchone()
⋮----
user = result.mappings().fetchone()
⋮----
async def create_session(self, user_id: str) -> str
⋮----
session_id = str(uuid.uuid4())
expires_at = datetime.utcnow() + timedelta(days=settings.SESSION_EXPIRY_DAYS)
⋮----
async def validate_session(self, session_id: str) -> dict | None
⋮----
expires_at = row["expires_at"]
⋮----
expires_at = datetime.fromisoformat(expires_at)
⋮----
async def logout(self, session_id: str)
⋮----
auth_service = AuthService()
````

## File: backend/app/services/cf_service.py
````python
logger = logging.getLogger(__name__)
⋮----
_WEIGHTS: Dict[str, float] = {
⋮----
CF_MAX_DELTA = 0.20
⋮----
TOP_N_SIMILAR = 5
⋮----
def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float
⋮----
shared = set(a) & set(b)
⋮----
dot = sum(a[k] * b[k] for k in shared)
mag_a = math.sqrt(sum(x * x for x in a.values()))
mag_b = math.sqrt(sum(x * x for x in b.values()))
denom = mag_a * mag_b
⋮----
class CFService
⋮----
async def _fetch_all_interaction_vectors(self) -> Dict[str, Dict[str, float]]
⋮----
result = await conn.execute(
rows = result.fetchall()
⋮----
vectors: Dict[str, Dict[str, float]] = {}
⋮----
weight = _WEIGHTS.get(itype, 0.0)
⋮----
existing = vectors[user_id].get(recipe_title, 0.0)
⋮----
all_vectors = await self._fetch_all_interaction_vectors()
⋮----
user_vec = all_vectors.get(user_id)
⋮----
# Benzer kullanıcıları bul (kendisi hariç)
similarities: List[tuple] = []
⋮----
sim = _cosine(user_vec, other_vec)
⋮----
top_similar = similarities[:top_n_similar]
⋮----
# Aday tarifler için ağırlıklı CF skoru
candidate_set = set(candidate_titles)
raw_scores: Dict[str, float] = {}
⋮----
other_vec = all_vectors[other_id]
⋮----
# Kullanıcı zaten bu tarifte etkileşim yapmışsa CF'den çıkar
⋮----
# [0, CF_MAX_DELTA] aralığına normalize et
max_raw = max(raw_scores.values())
⋮----
cf_deltas = {
⋮----
cf_service = CFService()
````

## File: backend/app/services/email_service.py
````python
logger = logging.getLogger(__name__)
⋮----
def send_magic_link(to_email: str, token: str) -> bool
⋮----
smtp_user = str(settings.SMTP_USER).strip()
smtp_password = str(settings.SMTP_PASSWORD).replace(" ", "").strip()
from_email = (settings.SMTP_FROM or settings.SMTP_USER).strip()
magic_link_url = f"{settings.FRONTEND_URL}/
⋮----
subject = "Buzdolabı Şefi - Giriş Bağlantınız"
⋮----
plain_text = f"""Merhaba,
⋮----
html = f"""<!DOCTYPE html>
⋮----
msg = MIMEMultipart("alternative")
````

## File: backend/app/services/embedding_service.py
````python
logger = logging.getLogger(__name__)
⋮----
class EmbeddingService
⋮----
def __init__(self)
⋮----
def _load_model(self)
⋮----
def _prepare_recipe_text(self, recipe: Recipe) -> str
⋮----
"""
        Combine recipe fields into a single text for embedding.
        Format: Tarif: {Başlık}. Malzemeler: {malzeme1}, {malzeme2}, ...
        Instructions are intentionally excluded — they introduce noise that
        degrades ingredient-based similarity matching in L2 space.
        """
title = recipe.Title or ""
⋮----
ingredients_text = recipe.Cleaned_Ingredients or recipe.Ingredients or ""
ingredients_clean = (
⋮----
def encode_recipe(self, recipe: Recipe) -> np.ndarray
⋮----
"""
        Generate embedding for a single recipe

        Args:
            recipe: Recipe object

        Returns:
            numpy array of shape (dimension,)
        """
⋮----
recipe_text = self._prepare_recipe_text(recipe)
embedding = self.model.encode(recipe_text, convert_to_numpy=True)
⋮----
def encode_recipes_batch(self, recipes: List[Recipe], batch_size: int = 32) -> np.ndarray
⋮----
"""
        Generate embeddings for multiple recipes (batch processing)
        More efficient than encoding one by one

        Args:
            recipes: List of Recipe objects
            batch_size: Number of recipes to process at once

        Returns:
            numpy array of shape (num_recipes, dimension)
        """
⋮----
# Prepare all recipe texts
recipe_texts = [self._prepare_recipe_text(recipe) for recipe in recipes]
⋮----
# Encode in batches for efficiency
embeddings = self.model.encode(
⋮----
def encode_text(self, text: str) -> np.ndarray
⋮----
"""
        Generate embedding for arbitrary text (e.g., user query)

        Args:
            text: Input text string

        Returns:
            numpy array of shape (dimension,)
        """
⋮----
embedding = self.model.encode(text, convert_to_numpy=True)
⋮----
def get_model_info(self) -> dict
⋮----
"""Get information about the loaded model"""
⋮----
embedding_service = EmbeddingService()
````

## File: backend/app/services/faiss_service.py
````python
FAISS_AVAILABLE = True
⋮----
faiss = None
FAISS_AVAILABLE = False
⋮----
logger = logging.getLogger(__name__)
⋮----
class FAISSService
⋮----
def __init__(self)
⋮----
def _create_index(self)
⋮----
index_type = settings.FAISS_INDEX_TYPE
⋮----
index = faiss.IndexFlatL2(self.dimension)
⋮----
index = faiss.IndexFlatIP(self.dimension)
⋮----
def build_index(self, embeddings: np.ndarray, recipes: List[Recipe]) -> bool
⋮----
# Validate inputs
⋮----
# Create index
index = self._create_index()
⋮----
# Normalize embeddings for L2 distance (optional, but recommended)
# For cosine similarity, we'd normalize, but for L2 we keep as-is
embeddings_normalized = embeddings.astype('float32')
⋮----
# Add vectors to index
⋮----
# Save index
⋮----
# Save to disk
⋮----
def _save_index(self)
⋮----
"""Save index and metadata to disk"""
⋮----
# Ensure directory exists
⋮----
# Save FAISS index
⋮----
# Save metadata
metadata = {
⋮----
def load_index(self) -> bool
⋮----
"""
        Load FAISS index from disk

        Returns:
            True if successful, False otherwise
        """
⋮----
# Check file size (basic validation)
file_size = self.index_path.stat().st_size
⋮----
# Load FAISS index
⋮----
# Validate index
⋮----
# Load metadata
⋮----
metadata = json.load(f)
⋮----
# Validate metadata
⋮----
# Load embeddings (for reference, not required for search)
embeddings_path = self.index_path.parent / 'recipe_embeddings.npy'
⋮----
def is_loaded(self) -> bool
⋮----
"""
        Check if FAISS index is loaded and ready for search

        Returns:
            True if index is loaded, False otherwise
        """
⋮----
def _ensure_index_loaded(self)
⋮----
"""
        Ensure index is loaded before search

        Raises:
            RuntimeError: If index cannot be loaded
        """
⋮----
error_msg = (
⋮----
"""
        Search for similar vectors

        Args:
            query_vector: Query embedding of shape (dimension,)
            k: Number of results to return

        Returns:
            Tuple of (distances, indices)
            - distances: Array of shape (k,) - L2 distances (lower is better)
            - indices: Array of shape (k,) - Recipe indices

        Raises:
            RuntimeError: If index is not loaded
            ValueError: If query vector has wrong shape or dimension
        """
⋮----
# Validate query vector
⋮----
# Validate k
⋮----
k = self.index.ntotal
⋮----
# Reshape query to (1, dimension) for FAISS
query_reshaped = query_vector.reshape(1, -1).astype('float32')
⋮----
# Search
⋮----
"""
        Search for recipes similar to a text query

        Args:
            text: Query text (e.g., "chicken pasta recipe")
            k: Number of results to return
            embedding_service: EmbeddingService instance to encode text

        Returns:
            Tuple of (distances, indices)

        Raises:
            ValueError: If text is empty or embedding_service is None
            RuntimeError: If encoding or search fails






























        Search for recipes similar to a list of ingredients

        Args:
            ingredients: List of ingredient names
            k: Number of results to return
            embedding_service: EmbeddingService instance to encode text

        Returns:
            Tuple of (distances, indices)

        Raises:
            ValueError: If ingredients list is empty
            RuntimeError: If search fails


















Get information about the loaded index"""
⋮----
faiss_service = FAISSService()
````

## File: backend/app/services/reranker_service.py
````python
logger = logging.getLogger(__name__)
⋮----
class RerankerService
⋮----
def __init__(self)
⋮----
def _load_model(self)
⋮----
def _prepare_recipe_text(self, recipe: Recipe) -> str
⋮----
title = recipe.Title or ""
⋮----
ingredients_text = recipe.Cleaned_Ingredients or recipe.Ingredients or ""
ingredients_clean = (
⋮----
instructions = recipe.Instructions or ""
words = instructions.split()
⋮----
instructions = ' '.join(words[:300]) + '...'
⋮----
def _prepare_query_text(self, ingredients: List[str]) -> str
⋮----
"""
        Prepare query text from ingredients for reranking.
        Mirrors the FAISS query format so query and document share the same language space.
        """
⋮----
def is_loaded(self) -> bool
⋮----
"""
        Check if reranker model is loaded and ready

        Returns:
            True if model is loaded, False otherwise
        """
⋮----
"""
        Re-rank recipes based on query relevance using cross-encoder

        Args:
            query: Query text (e.g., "Recipe with chicken, pasta, tomato")
            recipes: List of Recipe objects to re-rank
            top_k: Number of top results to return

        Returns:
            List of tuples (Recipe, relevance_score) sorted by score (descending)
            Scores are normalized to 0-1 range (higher is better)
        """
⋮----
# Return recipes with dummy scores
⋮----
# Fallback: return recipes with dummy scores
⋮----
# Prepare query-recipe pairs
pairs = []
⋮----
recipe_text = self._prepare_recipe_text(recipe)
⋮----
# Score pairs using cross-encoder (batch processing)
scores = self.model.predict(
⋮----
# Normalize scores to 0-1 range (sigmoid for cross-encoder outputs)
⋮----
normalized_scores = 1 / (1 + np.exp(-scores))  # Sigmoid normalization
⋮----
# Create (recipe, score) pairs
recipe_scores = list(zip(recipes, normalized_scores))
⋮----
# Sort by score (descending)
⋮----
# Return top-k
top_results = recipe_scores[:top_k]
⋮----
query = self._prepare_query_text(ingredients)
⋮----
def get_model_info(self) -> dict
⋮----
reranker_service = RerankerService()
````

## File: backend/app/services/tfidf_service.py
````python
logger = logging.getLogger(__name__)
⋮----
def _clean_ingredients_text(raw: str) -> str
⋮----
class TFIDFService
⋮----
"""
    TF-IDF inverted index over recipe Cleaned_Ingredients.

    Recipe sırası recipe_service._load_recipes() ile deterministik şekilde belirlenir;
    FAISS index ile birebir aynı sıradadır (idx i → aynı tarif).
    """
⋮----
def __init__(self, vectorizer_path: str, matrix_path: str)
⋮----
self._matrix = None  # scipy sparse (n_recipes × vocab)
⋮----
def build_index(self, recipes) -> None
⋮----
"""Tariflerin Cleaned_Ingredients'ından TF-IDF matrisi oluştur ve diske kaydet."""
documents = [_clean_ingredients_text(r.Cleaned_Ingredients) for r in recipes]
⋮----
token_pattern=r"(?u)\b\w\w+\b",  # Unicode-aware — Türkçe ç/ğ/ı/ö/ş/ü
⋮----
sublinear_tf=True,   # log(1+tf) — kısa belgeler için daha dengeli
⋮----
def load_index(self) -> bool
⋮----
"""Diskten yükle. Başarılıysa True döner."""
⋮----
def is_loaded(self) -> bool
⋮----
cosine similarity = sparse dot product.
indices: shape (k,) — recipe index'leri
````

## File: backend/app/utils/__init__.py
````python

````

## File: backend/app/utils/cache.py
````python
class SimpleCache
⋮----
def __init__(self)
⋮----
def _generate_key(self, prefix: str, data: Any) -> str
⋮----
data_str = json.dumps(data, sort_keys=True)
hash_key = hashlib.md5(data_str.encode()).hexdigest()
⋮----
def get(self, key: str) -> Optional[Any]
⋮----
"""Get value from cache if not expired"""
⋮----
# Check expiry
⋮----
# Expired, remove from cache
⋮----
def set(self, key: str, value: Any, ttl_seconds: int = 300)
⋮----
"""Set value in cache with TTL (default 5 minutes)"""
⋮----
def clear(self)
⋮----
"""Clear all cache"""
⋮----
def size(self) -> int
⋮----
"""Get cache size"""
⋮----
cache = SimpleCache()
````

## File: backend/app/utils/helpers.py
````python
logger = logging.getLogger(__name__)
⋮----
def parse_ingredient_list(ingredients_str: str) -> List[str]
⋮----
valid_json = ingredients_str.replace("'", '"')
⋮----
def get_ingredient_image_url(name: str) -> str
⋮----
def get_recipe_image_url(image_name: str) -> str
````

## File: backend/app/__init__.py
````python

````

## File: backend/data/recipe_index_metadata.json
````json
{
  "index_type": "IndexFlatL2",
  "metric": "L2",
  "dimension": 384,
  "num_vectors": 532,
  "recipes": [
    {
      "index": 0,
      "title": "Karnıyarık",
      "image_name": "karniyarik"
    },
    {
      "index": 1,
      "title": "İmam Bayıldı",
      "image_name": "imam-bayildi"
    },
    {
      "index": 2,
      "title": "Mercimek Çorbası",
      "image_name": "mercimek-corbasi"
    },
    {
      "index": 3,
      "title": "Kuru Fasulye",
      "image_name": "kuru-fasulye"
    },
    {
      "index": 4,
      "title": "Lahmacun",
      "image_name": "lahmacun"
    },
    {
      "index": 5,
      "title": "Mantı",
      "image_name": "manti"
    },
    {
      "index": 6,
      "title": "Hünkar Beğendi",
      "image_name": "hunkar-begendi"
    },
    {
      "index": 7,
      "title": "Çılbır",
      "image_name": "cilbir"
    },
    {
      "index": 8,
      "title": "İçli Köfte",
      "image_name": "icli-kofte"
    },
    {
      "index": 9,
      "title": "Etli Nohut Yemeği",
      "image_name": "etli-nohut"
    },
    {
      "index": 10,
      "title": "Zeytinyağlı Yaprak Sarma",
      "image_name": "zeytinyagli-yaprak-sarma"
    },
    {
      "index": 11,
      "title": "Şakşuka",
      "image_name": "saksuka"
    },
    {
      "index": 12,
      "title": "Zeytinyağlı Barbunya",
      "image_name": "zeytinyagli-barbunya"
    },
    {
      "index": 13,
      "title": "Kısır",
      "image_name": "kisir"
    },
    {
      "index": 14,
      "title": "Menemen",
      "image_name": "menemen"
    },
    {
      "index": 15,
      "title": "Adana Kebap",
      "image_name": "adana-kebap"
    },
    {
      "index": 16,
      "title": "Sütlaç",
      "image_name": "sutlac"
    },
    {
      "index": 17,
      "title": "Baklava",
      "image_name": "baklava"
    },
    {
      "index": 18,
      "title": "Türlü",
      "image_name": "turlu"
    },
    {
      "index": 19,
      "title": "Ezogelin Çorbası",
      "image_name": "ezogelin-corbasi"
    },
    {
      "index": 20,
      "title": "Tas Kebabı",
      "image_name": "tas-kebabi"
    },
    {
      "index": 21,
      "title": "Patlıcan Musakka",
      "image_name": "patlican-musakka"
    },
    {
      "index": 22,
      "title": "Pilav Üstü Kuru Fasulye",
      "image_name": "pilav-ustu-kuru-fasulye"
    },
    {
      "index": 23,
      "title": "Ispanaklı Yumurta",
      "image_name": "ispanakli-yumurta"
    },
    {
      "index": 24,
      "title": "Ali Nazik Kebap",
      "image_name": "ali-nazik-kebap"
    },
    {
      "index": 25,
      "title": "Vegan Mercimek Köftesi (Vegan)",
      "image_name": "vegan-mercimek-koftesi"
    },
    {
      "index": 26,
      "title": "Vegan Karnıyarık (Vegan)",
      "image_name": "vegan-karniyarik"
    },
    {
      "index": 27,
      "title": "Vegan Menemen (Vegan)",
      "image_name": "vegan-menemen"
    },
    {
      "index": 28,
      "title": "Vegan Çılbır (Vegan)",
      "image_name": "vegan-cilbir"
    },
    {
      "index": 29,
      "title": "Glutensiz Lahmacun (Glutensiz)",
      "image_name": "glutensiz-lahmacun"
    },
    {
      "index": 30,
      "title": "Glutensiz Mercimek Çorbası (Glutensiz)",
      "image_name": "glutensiz-mercimek-corbasi"
    },
    {
      "index": 31,
      "title": "Glutensiz İçli Köfte (Glutensiz)",
      "image_name": "glutensiz-icli-kofte"
    },
    {
      "index": 32,
      "title": "Yulaf Sütlü Sütlaç (Vegan & Glutensiz)",
      "image_name": "yulaf-sutlu-sutlac"
    },
    {
      "index": 33,
      "title": "Laktozsuz Sütlaç (Süt Ürünü Yok)",
      "image_name": "laktozsuz-sutlac"
    },
    {
      "index": 34,
      "title": "Vejetaryen Kuru Fasulye (Vejetaryen)",
      "image_name": "vejetaryen-kuru-fasulye"
    },
    {
      "index": 35,
      "title": "Vejetaryen Mantı (Vejetaryen)",
      "image_name": "vejetaryen-manti"
    },
    {
      "index": 36,
      "title": "Vejetaryen Pide (Vejetaryen)",
      "image_name": "vejetaryen-pide"
    },
    {
      "index": 37,
      "title": "Glutensiz Kısır (Glutensiz)",
      "image_name": "glutensiz-kisir"
    },
    {
      "index": 38,
      "title": "Glutensiz Ezogelin Çorbası (Glutensiz)",
      "image_name": "glutensiz-ezogelin-corbasi"
    },
    {
      "index": 39,
      "title": "Süt Ürünsüz Hünkar Beğendi (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-hunkar-begendi"
    },
    {
      "index": 40,
      "title": "Vegan Yaprak Sarma (Vegan)",
      "image_name": "vegan-yaprak-sarma"
    },
    {
      "index": 41,
      "title": "Vejetaryen Ispanaklı Börek (Vejetaryen)",
      "image_name": "vejetaryen-ispanakli-borek"
    },
    {
      "index": 42,
      "title": "Kuruyemişsiz Aşure (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-asure"
    },
    {
      "index": 43,
      "title": "Glutensiz Patates Köftesi (Glutensiz & Vejetaryen)",
      "image_name": "glutensiz-patates-koftesi"
    },
    {
      "index": 44,
      "title": "Vegan Mercimek Çorbası (Vegan & Glutensiz)",
      "image_name": "vegan-mercimek-corbasi"
    },
    {
      "index": 45,
      "title": "Vejetaryen Patlıcan Musakka (Vejetaryen)",
      "image_name": "vejetaryen-patlican-musakka"
    },
    {
      "index": 46,
      "title": "Süt Ürünsüz Menemen (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-menemen"
    },
    {
      "index": 47,
      "title": "Vegan Baklava (Vegan)",
      "image_name": "vegan-baklava"
    },
    {
      "index": 48,
      "title": "Kuruyemişsiz Baklava (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-baklava"
    },
    {
      "index": 49,
      "title": "Glutensiz Mücver (Glutensiz & Vejetaryen)",
      "image_name": "glutensiz-mucver"
    },
    {
      "index": 50,
      "title": "Yayla Çorbası",
      "image_name": "yayla-corbasi"
    },
    {
      "index": 51,
      "title": "Tarhana Çorbası",
      "image_name": "tarhana-corbasi"
    },
    {
      "index": 52,
      "title": "İşkembe Çorbası",
      "image_name": "iskembe-corbasi"
    },
    {
      "index": 53,
      "title": "Toyga Çorbası",
      "image_name": "toyga-corbasi"
    },
    {
      "index": 54,
      "title": "Lebeniye Çorbası",
      "image_name": "lebeniye-corbasi"
    },
    {
      "index": 55,
      "title": "Analı Kızlı Çorbası",
      "image_name": "anali-kizli-corbasi"
    },
    {
      "index": 56,
      "title": "Düğün Çorbası",
      "image_name": "dugun-corbasi"
    },
    {
      "index": 57,
      "title": "Süleymaniye Çorbası",
      "image_name": "suleymaniye-corbasi"
    },
    {
      "index": 58,
      "title": "Yüksük Çorbası",
      "image_name": "yuksuk-corbasi"
    },
    {
      "index": 59,
      "title": "Beyran Çorbası",
      "image_name": "beyran-corbasi"
    },
    {
      "index": 60,
      "title": "Zeytinyağlı Enginar",
      "image_name": "zeytinyagli-enginar"
    },
    {
      "index": 61,
      "title": "Zeytinyağlı Kereviz",
      "image_name": "zeytinyagli-kereviz"
    },
    {
      "index": 62,
      "title": "Zeytinyağlı Pırasa",
      "image_name": "zeytinyagli-pirasa"
    },
    {
      "index": 63,
      "title": "Zeytinyağlı Taze Fasulye",
      "image_name": "zeytinyagli-taze-fasulye"
    },
    {
      "index": 64,
      "title": "Zeytinyağlı Bakla",
      "image_name": "zeytinyagli-bakla"
    },
    {
      "index": 65,
      "title": "Zeytinyağlı Börülce",
      "image_name": "zeytinyagli-borulce"
    },
    {
      "index": 66,
      "title": "Haydari",
      "image_name": "haydari"
    },
    {
      "index": 67,
      "title": "Acılı Ezme",
      "image_name": "acili-ezme"
    },
    {
      "index": 68,
      "title": "Patlıcan Salatası",
      "image_name": "patlican-salatasi"
    },
    {
      "index": 69,
      "title": "Çoban Salatası",
      "image_name": "coban-salatasi"
    },
    {
      "index": 70,
      "title": "Atom Salatası",
      "image_name": "atom-salatasi"
    },
    {
      "index": 71,
      "title": "Gavurdağı Salatası",
      "image_name": "gavurdagi-salatasi"
    },
    {
      "index": 72,
      "title": "Humus",
      "image_name": "humus"
    },
    {
      "index": 73,
      "title": "Babaganuş",
      "image_name": "babaganus"
    },
    {
      "index": 74,
      "title": "Muhammara",
      "image_name": "muhammara"
    },
    {
      "index": 75,
      "title": "Glutensiz Tarhana Çorbası (Glutensiz)",
      "image_name": "glutensiz-tarhana-corbasi"
    },
    {
      "index": 76,
      "title": "Vegan Yayla Çorbası (Vegan)",
      "image_name": "vegan-yayla-corbasi"
    },
    {
      "index": 77,
      "title": "Vegan Düğün Çorbası (Vegan & Glutensiz)",
      "image_name": "vegan-dugun-corbasi"
    },
    {
      "index": 78,
      "title": "Süt Ürünsüz Toyga Çorbası (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-toyga-corbasi"
    },
    {
      "index": 79,
      "title": "Glutensiz Düğün Çorbası (Glutensiz)",
      "image_name": "glutensiz-dugun-corbasi"
    },
    {
      "index": 80,
      "title": "Vegan Tarhana Çorbası (Vegan & Glutensiz)",
      "image_name": "vegan-tarhana-corbasi"
    },
    {
      "index": 81,
      "title": "Vegan Enginar (Vegan)",
      "image_name": "vegan-enginar"
    },
    {
      "index": 82,
      "title": "Vegan Kereviz (Vegan)",
      "image_name": "vegan-kereviz"
    },
    {
      "index": 83,
      "title": "Vegan Zeytinyağlı Taze Fasulye (Vegan)",
      "image_name": "vegan-zeytinyagli-taze-fasulye"
    },
    {
      "index": 84,
      "title": "Vegan Bakla (Vegan)",
      "image_name": "vegan-bakla"
    },
    {
      "index": 85,
      "title": "Laktozsuz Haydari (Süt Ürünü Yok)",
      "image_name": "laktozsuz-haydari"
    },
    {
      "index": 86,
      "title": "Vegan Humus (Vegan & Glutensiz)",
      "image_name": "vegan-humus"
    },
    {
      "index": 87,
      "title": "Vegan Babaganuş (Vegan & Glutensiz)",
      "image_name": "vegan-babaganus"
    },
    {
      "index": 88,
      "title": "Kuruyemişsiz Muhammara (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-muhammara"
    },
    {
      "index": 89,
      "title": "Glutensiz Muhammara (Glutensiz)",
      "image_name": "glutensiz-muhammara"
    },
    {
      "index": 90,
      "title": "Vejetaryen Yoğurtlu Semizotu (Vejetaryen)",
      "image_name": "vejetaryen-yogurtlu-semizotu"
    },
    {
      "index": 91,
      "title": "Vegan Semizotu Salatası (Vegan & Glutensiz)",
      "image_name": "vegan-semizotu-salatasi"
    },
    {
      "index": 92,
      "title": "Süt Ürünsüz Patlıcan Salatası (Süt Ürünü Yok & Glutensiz)",
      "image_name": "sut-urunsuz-patlican-salatasi"
    },
    {
      "index": 93,
      "title": "Kuruyemişsiz Gavurdağı Salatası (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-gavurdagi-salatasi"
    },
    {
      "index": 94,
      "title": "Vegan Pırasa (Vegan)",
      "image_name": "vegan-pirasa"
    },
    {
      "index": 95,
      "title": "Vejetaryen Kabak Çorbası (Vejetaryen)",
      "image_name": "vejetaryen-kabak-corbasi"
    },
    {
      "index": 96,
      "title": "Vegan Kabak Çorbası (Vegan & Glutensiz)",
      "image_name": "vegan-kabak-corbasi"
    },
    {
      "index": 97,
      "title": "Vegan Börülce Salatası (Vegan & Glutensiz)",
      "image_name": "vegan-borulce-salatasi"
    },
    {
      "index": 98,
      "title": "Glutensiz Lebeniye Çorbası (Glutensiz)",
      "image_name": "glutensiz-lebeniye-corbasi"
    },
    {
      "index": 99,
      "title": "Vegan Acılı Ezme (Vegan & Glutensiz)",
      "image_name": "vegan-acili-ezme"
    },
    {
      "index": 100,
      "title": "Kadınbudu Köfte",
      "image_name": "kadinbudu-kofte"
    },
    {
      "index": 101,
      "title": "İzmir Köfte",
      "image_name": "izmir-kofte"
    },
    {
      "index": 102,
      "title": "Tekirdağ Köfte",
      "image_name": "tekirdag-kofte"
    },
    {
      "index": 103,
      "title": "Sulu Köfte",
      "image_name": "sulu-kofte"
    },
    {
      "index": 104,
      "title": "Dalyan Köfte",
      "image_name": "dalyan-kofte"
    },
    {
      "index": 105,
      "title": "Etli Kapuska",
      "image_name": "etli-kapuska"
    },
    {
      "index": 106,
      "title": "Etli Güveç",
      "image_name": "etli-guvec"
    },
    {
      "index": 107,
      "title": "Orman Kebabı",
      "image_name": "orman-kebabi"
    },
    {
      "index": 108,
      "title": "İskender Kebap",
      "image_name": "iskender-kebap"
    },
    {
      "index": 109,
      "title": "Urfa Kebap",
      "image_name": "urfa-kebap"
    },
    {
      "index": 110,
      "title": "Beyti Kebap",
      "image_name": "beyti-kebap"
    },
    {
      "index": 111,
      "title": "Tavuk Şiş",
      "image_name": "tavuk-sis"
    },
    {
      "index": 112,
      "title": "Kuzu Şiş",
      "image_name": "kuzu-sis"
    },
    {
      "index": 113,
      "title": "Çoban Kavurma",
      "image_name": "coban-kavurma"
    },
    {
      "index": 114,
      "title": "Saç Kavurma",
      "image_name": "sac-kavurma"
    },
    {
      "index": 115,
      "title": "Testi Kebabı",
      "image_name": "testi-kebabi"
    },
    {
      "index": 116,
      "title": "Kağıt Kebabı",
      "image_name": "kagit-kebabi"
    },
    {
      "index": 117,
      "title": "Fırında Kuzu Tandır",
      "image_name": "firinda-kuzu-tandir"
    },
    {
      "index": 118,
      "title": "Fırında Köfte Patates",
      "image_name": "firinda-kofte-patates"
    },
    {
      "index": 119,
      "title": "Fırında Sebzeli Et",
      "image_name": "firinda-sebzeli-et"
    },
    {
      "index": 120,
      "title": "Fırında Tavuk Baget",
      "image_name": "firinda-tavuk-baget"
    },
    {
      "index": 121,
      "title": "Tepsi Kebabı",
      "image_name": "tepsi-kebabi"
    },
    {
      "index": 122,
      "title": "Hasan Paşa Köfte",
      "image_name": "hasan-pasa-kofte"
    },
    {
      "index": 123,
      "title": "Etli Biber Dolması",
      "image_name": "etli-biber-dolmasi"
    },
    {
      "index": 124,
      "title": "Fırında Kıymalı Patlıcan Kebap",
      "image_name": "firinda-kiymali-patlican-kebap"
    },
    {
      "index": 125,
      "title": "Glutensiz Kadınbudu Köfte (Glutensiz)",
      "image_name": "glutensiz-kadinbudu-kofte"
    },
    {
      "index": 126,
      "title": "Glutensiz İzmir Köfte (Glutensiz)",
      "image_name": "glutensiz-izmir-kofte"
    },
    {
      "index": 127,
      "title": "Glutensiz Tekirdağ Köfte (Glutensiz)",
      "image_name": "glutensiz-tekirdag-kofte"
    },
    {
      "index": 128,
      "title": "Glutensiz Fırında Köfte (Glutensiz)",
      "image_name": "glutensiz-firinda-kofte"
    },
    {
      "index": 129,
      "title": "Süt Ürünsüz İskender (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-iskender"
    },
    {
      "index": 130,
      "title": "Süt Ürünsüz Beyti Kebap (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-beyti-kebap"
    },
    {
      "index": 131,
      "title": "Süt Ürünsüz Orman Kebabı (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-orman-kebabi"
    },
    {
      "index": 132,
      "title": "Süt Ürünsüz Saç Kavurma (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-sac-kavurma"
    },
    {
      "index": 133,
      "title": "Vegan Sulu Köfte (Vegan)",
      "image_name": "vegan-sulu-kofte"
    },
    {
      "index": 134,
      "title": "Vegan Etli Güveç (Vegan)",
      "image_name": "vegan-etli-guvec"
    },
    {
      "index": 135,
      "title": "Vegan Tepsi Kebabı (Vegan)",
      "image_name": "vegan-tepsi-kebabi"
    },
    {
      "index": 136,
      "title": "Vegan Biber Dolması (Vegan)",
      "image_name": "vegan-biber-dolmasi"
    },
    {
      "index": 137,
      "title": "Vegan Fırında Sebzeli Kebap (Vegan & Glutensiz)",
      "image_name": "vegan-firinda-sebzeli-kebap"
    },
    {
      "index": 138,
      "title": "Vegan Kapuska (Vegan)",
      "image_name": "vegan-kapuska"
    },
    {
      "index": 139,
      "title": "Kuruyemişsiz Hasan Paşa Köfte (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-hasan-pasa-kofte"
    },
    {
      "index": 140,
      "title": "Glutensiz Sulu Köfte (Glutensiz)",
      "image_name": "glutensiz-sulu-kofte"
    },
    {
      "index": 141,
      "title": "Glutensiz Etli Güveç (Glutensiz)",
      "image_name": "glutensiz-etli-guvec"
    },
    {
      "index": 142,
      "title": "Süt Ürünsüz Fırında Kuzu Tandır (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-firinda-kuzu-tandir"
    },
    {
      "index": 143,
      "title": "Süt Ürünsüz Çoban Kavurma (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-coban-kavurma"
    },
    {
      "index": 144,
      "title": "Glutensiz Kağıt Kebabı (Glutensiz)",
      "image_name": "glutensiz-kagit-kebabi"
    },
    {
      "index": 145,
      "title": "Vegan Kağıt Kebabı (Vegan & Glutensiz)",
      "image_name": "vegan-kagit-kebabi"
    },
    {
      "index": 146,
      "title": "Glutensiz Tepsi Kebabı (Glutensiz)",
      "image_name": "glutensiz-tepsi-kebabi"
    },
    {
      "index": 147,
      "title": "Süt Ürünsüz Tavuk Şiş (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-tavuk-sis"
    },
    {
      "index": 148,
      "title": "Vegan Şiş Kebap (Vegan & Glutensiz)",
      "image_name": "vegan-sis-kebap"
    },
    {
      "index": 149,
      "title": "Glutensiz Dalyan Köfte (Glutensiz)",
      "image_name": "glutensiz-dalyan-kofte"
    },
    {
      "index": 150,
      "title": "Tavuk Sote",
      "image_name": "tavuk-sote"
    },
    {
      "index": 151,
      "title": "Fırında Tavuk Pirzola",
      "image_name": "firinda-tavuk-pirzola"
    },
    {
      "index": 152,
      "title": "Tavuk Döner",
      "image_name": "tavuk-doner"
    },
    {
      "index": 153,
      "title": "Kremalı Tavuk Makarna",
      "image_name": "kremali-tavuk-makarna"
    },
    {
      "index": 154,
      "title": "Tavuk Tandır",
      "image_name": "tavuk-tandir"
    },
    {
      "index": 155,
      "title": "Tavuk Pane",
      "image_name": "tavuk-pane"
    },
    {
      "index": 156,
      "title": "Fırında Tavuk Kanat",
      "image_name": "firinda-tavuk-kanat"
    },
    {
      "index": 157,
      "title": "Hindi Fırın",
      "image_name": "hindi-firin"
    },
    {
      "index": 158,
      "title": "Tavuk Güveç",
      "image_name": "tavuk-guvec"
    },
    {
      "index": 159,
      "title": "Hindi Sote",
      "image_name": "hindi-sote"
    },
    {
      "index": 160,
      "title": "Hamsi Tava",
      "image_name": "hamsi-tava"
    },
    {
      "index": 161,
      "title": "Fırında Somon",
      "image_name": "firinda-somon"
    },
    {
      "index": 162,
      "title": "Karides Güveç",
      "image_name": "karides-guvec"
    },
    {
      "index": 163,
      "title": "Tereyağlı Karides",
      "image_name": "tereyagli-karides"
    },
    {
      "index": 164,
      "title": "Kalamar Tava",
      "image_name": "kalamar-tava"
    },
    {
      "index": 165,
      "title": "Fırında Mezgit",
      "image_name": "firinda-mezgit"
    },
    {
      "index": 166,
      "title": "Balık Buğulama",
      "image_name": "balik-bugulama"
    },
    {
      "index": 167,
      "title": "Midye Dolma",
      "image_name": "midye-dolma"
    },
    {
      "index": 168,
      "title": "Midye Tava",
      "image_name": "midye-tava"
    },
    {
      "index": 169,
      "title": "Levrek Izgara",
      "image_name": "levrek-izgara"
    },
    {
      "index": 170,
      "title": "Somon Izgara",
      "image_name": "somon-izgara"
    },
    {
      "index": 171,
      "title": "Glutensiz Tavuk Pane (Glutensiz)",
      "image_name": "glutensiz-tavuk-pane"
    },
    {
      "index": 172,
      "title": "Glutensiz Kalamar Tava (Glutensiz)",
      "image_name": "glutensiz-kalamar-tava"
    },
    {
      "index": 173,
      "title": "Glutensiz Tavuk Sote (Glutensiz)",
      "image_name": "glutensiz-tavuk-sote"
    },
    {
      "index": 174,
      "title": "Süt Ürünsüz Tavuk Sote (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-tavuk-sote"
    },
    {
      "index": 175,
      "title": "Süt Ürünsüz Kremalı Tavuk (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-kremali-tavuk"
    },
    {
      "index": 176,
      "title": "Süt Ürünsüz Karides Sote (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-karides-sote"
    },
    {
      "index": 177,
      "title": "Süt Ürünsüz Karides Güveç (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-karides-guvec"
    },
    {
      "index": 178,
      "title": "Süt Ürünsüz Hindi Fırın (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-hindi-firin"
    },
    {
      "index": 179,
      "title": "Glutensiz Midye Tava (Glutensiz)",
      "image_name": "glutensiz-midye-tava"
    },
    {
      "index": 180,
      "title": "Glutensiz Fırında Somon (Glutensiz)",
      "image_name": "glutensiz-firinda-somon"
    },
    {
      "index": 181,
      "title": "Süt Ürünsüz Tavuk Döner (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-tavuk-doner"
    },
    {
      "index": 182,
      "title": "Kuruyemişsiz Midye Dolma (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-midye-dolma"
    },
    {
      "index": 183,
      "title": "Vegan Soya Tavuk Sote (Vegan)",
      "image_name": "vegan-soya-tavuk-sote"
    },
    {
      "index": 184,
      "title": "Vegan Mantarlı Kalamar (Vegan)",
      "image_name": "vegan-mantarli-kalamar"
    },
    {
      "index": 185,
      "title": "Vegan Tofu Balık (Vegan & Glutensiz)",
      "image_name": "vegan-tofu-balik"
    },
    {
      "index": 186,
      "title": "Vegan Soya Tavuk Güveç (Vegan)",
      "image_name": "vegan-soya-tavuk-guvec"
    },
    {
      "index": 187,
      "title": "Vegan Mantar Döner (Vegan)",
      "image_name": "vegan-mantar-doner"
    },
    {
      "index": 188,
      "title": "Vegan Karides Güveç (Vegan)",
      "image_name": "vegan-karides-guvec"
    },
    {
      "index": 189,
      "title": "Vejetaryen Balık Buğulama (Vejetaryen)",
      "image_name": "vejetaryen-balik-bugulama"
    },
    {
      "index": 190,
      "title": "Glutensiz Tavuk Güveç (Glutensiz)",
      "image_name": "glutensiz-tavuk-guvec"
    },
    {
      "index": 191,
      "title": "Glutensiz Hamsi Tava (Glutensiz)",
      "image_name": "glutensiz-hamsi-tava"
    },
    {
      "index": 192,
      "title": "Fırında Palamut",
      "image_name": "firinda-palamut"
    },
    {
      "index": 193,
      "title": "Balık Köfte",
      "image_name": "balik-kofte"
    },
    {
      "index": 194,
      "title": "Tavuklu Pilav",
      "image_name": "tavuklu-pilav"
    },
    {
      "index": 195,
      "title": "Fırında Tavuk Sarma",
      "image_name": "firinda-tavuk-sarma"
    },
    {
      "index": 196,
      "title": "Glutensiz Balık Köfte (Glutensiz)",
      "image_name": "glutensiz-balik-kofte"
    },
    {
      "index": 197,
      "title": "Vegan Mantarlı Tandır (Vegan)",
      "image_name": "vegan-mantarli-tandir"
    },
    {
      "index": 198,
      "title": "Süt Ürünsüz Tavuk Tandır (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-tavuk-tandir"
    },
    {
      "index": 199,
      "title": "Vegan Fırında Tofu Somon (Vegan & Glutensiz)",
      "image_name": "vegan-firinda-tofu-somon"
    },
    {
      "index": 200,
      "title": "Peynirli Poğaça",
      "image_name": "peynirli-pogaca"
    },
    {
      "index": 201,
      "title": "Patatesli Poğaça",
      "image_name": "patatesli-pogaca"
    },
    {
      "index": 202,
      "title": "Açma",
      "image_name": "acma"
    },
    {
      "index": 203,
      "title": "Simit",
      "image_name": "simit"
    },
    {
      "index": 204,
      "title": "Su Böreği",
      "image_name": "su-boregi"
    },
    {
      "index": 205,
      "title": "Sigara Böreği",
      "image_name": "sigara-boregi"
    },
    {
      "index": 206,
      "title": "Kol Böreği",
      "image_name": "kol-boregi"
    },
    {
      "index": 207,
      "title": "Ispanaklı Börek",
      "image_name": "ispanakli-borek"
    },
    {
      "index": 208,
      "title": "Kıymalı Pide",
      "image_name": "kiymali-pide"
    },
    {
      "index": 209,
      "title": "Kuşbaşılı Pide",
      "image_name": "kusbasili-pide"
    },
    {
      "index": 210,
      "title": "Kaşarlı Pide",
      "image_name": "kasarli-pide"
    },
    {
      "index": 211,
      "title": "Gözleme",
      "image_name": "gozleme"
    },
    {
      "index": 212,
      "title": "Kıymalı Mantı",
      "image_name": "kiymali-manti"
    },
    {
      "index": 213,
      "title": "Tepsi Böreği",
      "image_name": "tepsi-boregi"
    },
    {
      "index": 214,
      "title": "Glutensiz Peynirli Poğaça (Glutensiz)",
      "image_name": "glutensiz-peynirli-pogaca"
    },
    {
      "index": 215,
      "title": "Glutensiz Patatesli Poğaça (Glutensiz)",
      "image_name": "glutensiz-patatesli-pogaca"
    },
    {
      "index": 216,
      "title": "Vegan Patatesli Poğaça (Vegan)",
      "image_name": "vegan-patatesli-pogaca"
    },
    {
      "index": 217,
      "title": "Vegan Sigara Böreği (Vegan)",
      "image_name": "vegan-sigara-boregi"
    },
    {
      "index": 218,
      "title": "Glutensiz Sigara Böreği (Glutensiz)",
      "image_name": "glutensiz-sigara-boregi"
    },
    {
      "index": 219,
      "title": "Glutensiz Ispanaklı Börek (Glutensiz)",
      "image_name": "glutensiz-ispanakli-borek"
    },
    {
      "index": 220,
      "title": "Süt Ürünsüz Kol Böreği (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-kol-boregi"
    },
    {
      "index": 221,
      "title": "Vegan Kol Böreği (Vegan)",
      "image_name": "vegan-kol-boregi"
    },
    {
      "index": 222,
      "title": "Glutensiz Kıymalı Pide (Glutensiz)",
      "image_name": "glutensiz-kiymali-pide"
    },
    {
      "index": 223,
      "title": "Vegan Lahmacun (Vegan)",
      "image_name": "vegan-lahmacun"
    },
    {
      "index": 224,
      "title": "Glutensiz Vegan Lahmacun (Glutensiz & Vegan)",
      "image_name": "glutensiz-vegan-lahmacun"
    },
    {
      "index": 225,
      "title": "Vegan Mantı (Vegan)",
      "image_name": "vegan-manti"
    },
    {
      "index": 226,
      "title": "Glutensiz Mantı (Glutensiz)",
      "image_name": "glutensiz-manti"
    },
    {
      "index": 227,
      "title": "Glutensiz Simit (Glutensiz)",
      "image_name": "glutensiz-simit"
    },
    {
      "index": 228,
      "title": "Vegan Simit (Vegan)",
      "image_name": "vegan-simit"
    },
    {
      "index": 229,
      "title": "Süt Ürünsüz Gözleme (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-gozleme"
    },
    {
      "index": 230,
      "title": "Vegan Gözleme (Vegan)",
      "image_name": "vegan-gozleme"
    },
    {
      "index": 231,
      "title": "Glutensiz Gözleme (Glutensiz)",
      "image_name": "glutensiz-gozleme"
    },
    {
      "index": 232,
      "title": "Vegan Su Böreği (Vegan)",
      "image_name": "vegan-su-boregi"
    },
    {
      "index": 233,
      "title": "Glutensiz Su Böreği (Glutensiz)",
      "image_name": "glutensiz-su-boregi"
    },
    {
      "index": 234,
      "title": "Glutensiz Açma (Glutensiz)",
      "image_name": "glutensiz-acma"
    },
    {
      "index": 235,
      "title": "Vegan Açma (Vegan)",
      "image_name": "vegan-acma"
    },
    {
      "index": 236,
      "title": "Vegan Tepsi Böreği (Vegan)",
      "image_name": "vegan-tepsi-boregi"
    },
    {
      "index": 237,
      "title": "Süt Ürünsüz Kaşarlı Pide (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-kasarli-pide"
    },
    {
      "index": 238,
      "title": "Glutensiz Kaşarlı Pide (Glutensiz)",
      "image_name": "glutensiz-kasarli-pide"
    },
    {
      "index": 239,
      "title": "Glutensiz Vegan Mantı (Glutensiz & Vegan)",
      "image_name": "glutensiz-vegan-manti"
    },
    {
      "index": 240,
      "title": "Glutensiz Kol Böreği (Glutensiz)",
      "image_name": "glutensiz-kol-boregi"
    },
    {
      "index": 241,
      "title": "Vegan Pide (Vegan)",
      "image_name": "vegan-pide"
    },
    {
      "index": 242,
      "title": "Çiğ Börek",
      "image_name": "cig-borek"
    },
    {
      "index": 243,
      "title": "Zeytinli Poğaça",
      "image_name": "zeytinli-pogaca"
    },
    {
      "index": 244,
      "title": "Peynirli Gözleme",
      "image_name": "peynirli-gozleme"
    },
    {
      "index": 245,
      "title": "Karadeniz Pidesi",
      "image_name": "karadeniz-pidesi"
    },
    {
      "index": 246,
      "title": "Glutensiz Çiğ Börek (Glutensiz)",
      "image_name": "glutensiz-cig-borek"
    },
    {
      "index": 247,
      "title": "Vegan Zeytinli Poğaça (Vegan)",
      "image_name": "vegan-zeytinli-pogaca"
    },
    {
      "index": 248,
      "title": "Glutensiz Tepsi Böreği (Glutensiz)",
      "image_name": "glutensiz-tepsi-boregi"
    },
    {
      "index": 249,
      "title": "Süt Ürünsüz Peynirli Poğaça (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-peynirli-pogaca"
    },
    {
      "index": 250,
      "title": "Tereyağlı Pirinç Pilavı",
      "image_name": "tereyagli-pirinc-pilavi"
    },
    {
      "index": 251,
      "title": "Bulgur Pilavı",
      "image_name": "bulgur-pilavi"
    },
    {
      "index": 252,
      "title": "Firik Pilavı",
      "image_name": "firik-pilavi"
    },
    {
      "index": 253,
      "title": "İç Pilav",
      "image_name": "ic-pilav"
    },
    {
      "index": 254,
      "title": "Nohutlu Pirinç Pilavı",
      "image_name": "nohutlu-pirinc-pilavi"
    },
    {
      "index": 255,
      "title": "Domatesli Bulgur Pilavı",
      "image_name": "domatesli-bulgur-pilavi"
    },
    {
      "index": 256,
      "title": "Meyhane Pilavı",
      "image_name": "meyhane-pilavi"
    },
    {
      "index": 257,
      "title": "Maklube",
      "image_name": "maklube"
    },
    {
      "index": 258,
      "title": "Etli Nohut",
      "image_name": "etli-nohut-yemegi"
    },
    {
      "index": 259,
      "title": "Etli Kuru Fasulye",
      "image_name": "etli-kuru-fasulye-tencere"
    },
    {
      "index": 260,
      "title": "Barbunya Pilaki",
      "image_name": "barbunya-pilaki"
    },
    {
      "index": 261,
      "title": "Fava",
      "image_name": "fava"
    },
    {
      "index": 262,
      "title": "Fellah Köftesi",
      "image_name": "fellah-koftesi"
    },
    {
      "index": 263,
      "title": "Nohut Köftesi",
      "image_name": "nohut-koftesi"
    },
    {
      "index": 264,
      "title": "Yeşil Mercimek Yemeği",
      "image_name": "yesil-mercimek-yemegi"
    },
    {
      "index": 265,
      "title": "Börülce Salatası",
      "image_name": "borulce-salatasi"
    },
    {
      "index": 266,
      "title": "Kuru Bamya",
      "image_name": "kuru-bamya"
    },
    {
      "index": 267,
      "title": "Sade Pirinç Pilavı",
      "image_name": "sade-pirinc-pilavi"
    },
    {
      "index": 268,
      "title": "Mercimek Köftesi",
      "image_name": "mercimek-koftesi"
    },
    {
      "index": 269,
      "title": "Vegan Pirinç Pilavı (Vegan & Glutensiz)",
      "image_name": "vegan-pirinc-pilavi"
    },
    {
      "index": 270,
      "title": "Süt Ürünsüz Şehriyeli Pilav (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-sehriyeli-pilav"
    },
    {
      "index": 271,
      "title": "Glutensiz Pirinç Pilavı (Glutensiz)",
      "image_name": "glutensiz-pirinc-pilavi"
    },
    {
      "index": 272,
      "title": "Glutensiz Kinoa Pilavı (Glutensiz & Vegan)",
      "image_name": "glutensiz-kinoa-pilavi"
    },
    {
      "index": 273,
      "title": "Glutensiz Karabuğday Pilavı (Glutensiz)",
      "image_name": "glutensiz-karabugday-pilavi"
    },
    {
      "index": 274,
      "title": "Vegan Bulgur Pilavı (Vegan)",
      "image_name": "vegan-bulgur-pilavi"
    },
    {
      "index": 275,
      "title": "Vegan Domatesli Bulgur Pilavı (Vegan)",
      "image_name": "vegan-domatesli-bulgur-pilavi"
    },
    {
      "index": 276,
      "title": "Süt Ürünsüz Nohutlu Pilav (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-nohutlu-pilav"
    },
    {
      "index": 277,
      "title": "Vegan Nohut Yemeği (Vegan & Glutensiz)",
      "image_name": "vegan-nohut-pilaki"
    },
    {
      "index": 278,
      "title": "Vegan Kuru Fasulye (Vegan & Glutensiz)",
      "image_name": "vegan-kuru-fasulye-tencere"
    },
    {
      "index": 279,
      "title": "Vegan Barbunya Pilaki (Vegan & Glutensiz)",
      "image_name": "vegan-barbunya-pilaki"
    },
    {
      "index": 280,
      "title": "Glutensiz Fellah Köftesi (Glutensiz & Vegan)",
      "image_name": "glutensiz-fellah-koftesi"
    },
    {
      "index": 281,
      "title": "Glutensiz Nohut Köftesi (Glutensiz & Vegan)",
      "image_name": "glutensiz-nohut-koftesi"
    },
    {
      "index": 282,
      "title": "Vegan Fava (Vegan & Glutensiz)",
      "image_name": "vegan-fava"
    },
    {
      "index": 283,
      "title": "Vegan Yeşil Mercimek (Vegan & Glutensiz)",
      "image_name": "vegan-yesil-mercimek"
    },
    {
      "index": 284,
      "title": "Vegan Kuru Bamya (Vegan & Glutensiz)",
      "image_name": "vegan-kuru-bamya"
    },
    {
      "index": 285,
      "title": "Vegan Maklube (Vegan & Glutensiz)",
      "image_name": "vegan-maklube"
    },
    {
      "index": 286,
      "title": "Süt Ürünsüz Meyhane Pilavı (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-meyhane-pilavi"
    },
    {
      "index": 287,
      "title": "Glutensiz Mercimek Köftesi (Glutensiz & Vegan)",
      "image_name": "glutensiz-mercimek-koftesi"
    },
    {
      "index": 288,
      "title": "Vegan Firik Pilavı (Vegan)",
      "image_name": "vegan-firik-pilavi"
    },
    {
      "index": 289,
      "title": "Kuruyemişsiz İç Pilav (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-ic-pilav"
    },
    {
      "index": 290,
      "title": "Süt Ürünsüz Firik Pilavı (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-firik-pilavi"
    },
    {
      "index": 291,
      "title": "Glutensiz Vegan Kinoa Tabbule (Glutensiz & Vegan)",
      "image_name": "glutensiz-kinoa-tabbule"
    },
    {
      "index": 292,
      "title": "Patlıcanlı Pilav",
      "image_name": "patlicanli-pilav"
    },
    {
      "index": 293,
      "title": "Etli Bezelye",
      "image_name": "etli-bezelye"
    },
    {
      "index": 294,
      "title": "Nohutlu Bulgur Pilavı",
      "image_name": "nohutlu-bulgur-pilavi"
    },
    {
      "index": 295,
      "title": "Kıymalı Bulgur Pilavı",
      "image_name": "kiymali-bulgur-pilavi"
    },
    {
      "index": 296,
      "title": "Vegan Patlıcanlı Pilav (Vegan)",
      "image_name": "vegan-patlicanli-pilav"
    },
    {
      "index": 297,
      "title": "Vegan Bezelye Yemeği (Vegan & Glutensiz)",
      "image_name": "vegan-bezelye-yemegi"
    },
    {
      "index": 298,
      "title": "Glutensiz Nohutlu Kinoa Pilavı (Glutensiz & Vegan)",
      "image_name": "glutensiz-nohutlu-kinoa-pilavi"
    },
    {
      "index": 299,
      "title": "Süt Ürünsüz Bulgur Pilavı (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-bulgur-pilavi"
    },
    {
      "index": 300,
      "title": "Muhallebi",
      "image_name": "muhallebi"
    },
    {
      "index": 301,
      "title": "Kazandibi",
      "image_name": "kazandibi"
    },
    {
      "index": 302,
      "title": "Keşkül",
      "image_name": "keskul"
    },
    {
      "index": 303,
      "title": "Güllaç",
      "image_name": "gullac"
    },
    {
      "index": 304,
      "title": "Supangle",
      "image_name": "supangle"
    },
    {
      "index": 305,
      "title": "Tavuk Göğsü Tatlısı",
      "image_name": "tavuk-gogsu-tatlisi"
    },
    {
      "index": 306,
      "title": "Trileçe",
      "image_name": "trilece"
    },
    {
      "index": 307,
      "title": "Profiterol",
      "image_name": "profiterol"
    },
    {
      "index": 308,
      "title": "Dondurma",
      "image_name": "dondurma"
    },
    {
      "index": 309,
      "title": "Magnolya Tatlısı",
      "image_name": "magnolya-tatlisi"
    },
    {
      "index": 310,
      "title": "Panna Cotta",
      "image_name": "panna-cotta"
    },
    {
      "index": 311,
      "title": "Sütlü İrmik Tatlısı",
      "image_name": "sutlu-irmik-tatlisi"
    },
    {
      "index": 312,
      "title": "Sakızlı Muhallebi",
      "image_name": "sakizli-muhallebi"
    },
    {
      "index": 313,
      "title": "Fırında Sütlaç",
      "image_name": "firinda-sutlac"
    },
    {
      "index": 314,
      "title": "Vegan Muhallebi (Vegan & Glutensiz)",
      "image_name": "vegan-muhallebi"
    },
    {
      "index": 315,
      "title": "Vegan Kazandibi (Vegan)",
      "image_name": "vegan-kazandibi"
    },
    {
      "index": 316,
      "title": "Vegan Keşkül (Vegan & Glutensiz)",
      "image_name": "vegan-keskul"
    },
    {
      "index": 317,
      "title": "Laktozsuz Güllaç (Süt Ürünü Yok)",
      "image_name": "laktozsuz-gullac"
    },
    {
      "index": 318,
      "title": "Vegan Supangle (Vegan & Glutensiz)",
      "image_name": "vegan-supangle"
    },
    {
      "index": 319,
      "title": "Vejetaryen Yalancı Tavuk Göğsü (Vejetaryen & Glutensiz)",
      "image_name": "vejetaryen-yalanci-tavuk-gogsu"
    },
    {
      "index": 320,
      "title": "Vegan Yalancı Tavuk Göğsü (Vegan & Glutensiz)",
      "image_name": "vegan-yalanci-tavuk-gogsu"
    },
    {
      "index": 321,
      "title": "Süt Ürünsüz Trileçe (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-trilece"
    },
    {
      "index": 322,
      "title": "Vegan Dondurma (Vegan & Glutensiz)",
      "image_name": "vegan-dondurma"
    },
    {
      "index": 323,
      "title": "Vegan Magnolya (Vegan)",
      "image_name": "vegan-magnolya"
    },
    {
      "index": 324,
      "title": "Glutensiz Muhallebi (Glutensiz)",
      "image_name": "glutensiz-muhallebi"
    },
    {
      "index": 325,
      "title": "Glutensiz Supangle (Glutensiz)",
      "image_name": "glutensiz-supangle"
    },
    {
      "index": 326,
      "title": "Kuruyemişsiz Güllaç (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-gullac"
    },
    {
      "index": 327,
      "title": "Kuruyemişsiz Keşkül (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-keskul"
    },
    {
      "index": 328,
      "title": "Süt Ürünsüz Sakızlı Muhallebi (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-sakizli-muhallebi"
    },
    {
      "index": 329,
      "title": "Vegan Güllaç (Vegan)",
      "image_name": "vegan-gullac"
    },
    {
      "index": 330,
      "title": "Süt Ürünsüz Fırında Sütlaç (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-firinda-sutlac"
    },
    {
      "index": 331,
      "title": "Vegan Profiterol (Vegan)",
      "image_name": "vegan-profiterol"
    },
    {
      "index": 332,
      "title": "Süt Ürünsüz Dondurma (Süt Ürünü Yok & Glutensiz)",
      "image_name": "sut-urunsuz-dondurma"
    },
    {
      "index": 333,
      "title": "Glutensiz Kazandibi (Glutensiz)",
      "image_name": "glutensiz-kazandibi"
    },
    {
      "index": 334,
      "title": "Glutensiz Trileçe (Glutensiz)",
      "image_name": "glutensiz-trilece"
    },
    {
      "index": 335,
      "title": "Vegan Sütlaç (Vegan & Glutensiz)",
      "image_name": "vegan-sutlac-tatli"
    },
    {
      "index": 336,
      "title": "Vegan Panna Cotta (Vegan & Glutensiz)",
      "image_name": "vegan-panna-cotta"
    },
    {
      "index": 337,
      "title": "Süt Ürünsüz Magnolya (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-magnolya"
    },
    {
      "index": 338,
      "title": "Glutensiz Sütlü İrmik Tatlısı (Glutensiz)",
      "image_name": "glutensiz-sutlu-irmik-tatlisi"
    },
    {
      "index": 339,
      "title": "Vegan Çikolatalı Mus (Vegan & Glutensiz)",
      "image_name": "vegan-cikolatali-mus"
    },
    {
      "index": 340,
      "title": "Glutensiz Fırında Sütlaç (Glutensiz)",
      "image_name": "glutensiz-firinda-sutlac"
    },
    {
      "index": 341,
      "title": "Vegan Meyveli Dondurma (Vegan & Glutensiz)",
      "image_name": "vegan-meyveli-dondurma"
    },
    {
      "index": 342,
      "title": "Süt Ürünsüz Profiterol (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-profiterol"
    },
    {
      "index": 343,
      "title": "Aşure",
      "image_name": "asure"
    },
    {
      "index": 344,
      "title": "Çikolatalı Sufle",
      "image_name": "cikolatali-sufle"
    },
    {
      "index": 345,
      "title": "Keskül-i Fükaralı",
      "image_name": "keskul-i-fukarali"
    },
    {
      "index": 346,
      "title": "Çilekli Dondurma",
      "image_name": "cilekli-dondurma"
    },
    {
      "index": 347,
      "title": "Vegan Aşure (Vegan)",
      "image_name": "vegan-asure"
    },
    {
      "index": 348,
      "title": "Vegan Çikolatalı Sufle (Vegan & Glutensiz)",
      "image_name": "vegan-cikolatali-sufle"
    },
    {
      "index": 349,
      "title": "Süt Ürünsüz Çilekli Dondurma (Süt Ürünü Yok & Glutensiz)",
      "image_name": "sut-urunsuz-cilekli-dondurma"
    },
    {
      "index": 350,
      "title": "Antep Baklavası",
      "image_name": "antep-baklavasi"
    },
    {
      "index": 351,
      "title": "Kadayıf",
      "image_name": "kadayif"
    },
    {
      "index": 352,
      "title": "Şekerpare",
      "image_name": "sekerpare"
    },
    {
      "index": 353,
      "title": "Revani",
      "image_name": "revani"
    },
    {
      "index": 354,
      "title": "Tulumba Tatlısı",
      "image_name": "tulumba-tatlisi"
    },
    {
      "index": 355,
      "title": "Lokma Tatlısı",
      "image_name": "lokma-tatlisi"
    },
    {
      "index": 356,
      "title": "Künefe",
      "image_name": "kunefe"
    },
    {
      "index": 357,
      "title": "Kalburabastı",
      "image_name": "kalburabasti"
    },
    {
      "index": 358,
      "title": "Ekmek Kadayıfı",
      "image_name": "ekmek-kadayifi"
    },
    {
      "index": 359,
      "title": "Irmik Helvası",
      "image_name": "irmik-helvasi"
    },
    {
      "index": 360,
      "title": "Un Helvası",
      "image_name": "un-helvasi"
    },
    {
      "index": 361,
      "title": "Islak Kek",
      "image_name": "islak-kek"
    },
    {
      "index": 362,
      "title": "Havuçlu Tarçınlı Kek",
      "image_name": "havuclu-tarcinli-kek"
    },
    {
      "index": 363,
      "title": "Un Kurabiyesi",
      "image_name": "un-kurabiyesi"
    },
    {
      "index": 364,
      "title": "Mozaik Pasta",
      "image_name": "mozaik-pasta"
    },
    {
      "index": 365,
      "title": "Limonlu Kek",
      "image_name": "limonlu-kek"
    },
    {
      "index": 366,
      "title": "Kuruyemişsiz Sade Baklava (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-sade-baklava"
    },
    {
      "index": 367,
      "title": "Kuruyemişsiz Kadayıf (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-kadayif"
    },
    {
      "index": 368,
      "title": "Kuruyemişsiz Künefe (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-kunefe"
    },
    {
      "index": 369,
      "title": "Kuruyemişsiz Şekerpare (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-sekerpare"
    },
    {
      "index": 370,
      "title": "Kuruyemişsiz Kalburabastı (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-kalburabasti"
    },
    {
      "index": 371,
      "title": "Kuruyemişsiz İrmik Helvası (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-irmik-helvasi"
    },
    {
      "index": 372,
      "title": "Glutensiz Şekerpare (Glutensiz)",
      "image_name": "glutensiz-sekerpare"
    },
    {
      "index": 373,
      "title": "Glutensiz Revani (Glutensiz)",
      "image_name": "glutensiz-revani"
    },
    {
      "index": 374,
      "title": "Glutensiz Islak Kek (Glutensiz)",
      "image_name": "glutensiz-islak-kek"
    },
    {
      "index": 375,
      "title": "Glutensiz Havuçlu Kek (Glutensiz)",
      "image_name": "glutensiz-havuclu-kek"
    },
    {
      "index": 376,
      "title": "Vegan Revani (Vegan)",
      "image_name": "vegan-revani"
    },
    {
      "index": 377,
      "title": "Vegan Islak Kek (Vegan)",
      "image_name": "vegan-islak-kek"
    },
    {
      "index": 378,
      "title": "Vegan Lokma (Vegan)",
      "image_name": "vegan-lokma"
    },
    {
      "index": 379,
      "title": "Vegan Un Helvası (Vegan)",
      "image_name": "vegan-un-helvasi"
    },
    {
      "index": 380,
      "title": "Vegan Limonlu Kek (Vegan)",
      "image_name": "vegan-limonlu-kek"
    },
    {
      "index": 381,
      "title": "Vegan Un Kurabiyesi (Vegan)",
      "image_name": "vegan-un-kurabiyesi"
    },
    {
      "index": 382,
      "title": "Vegan Mozaik Pasta (Vegan)",
      "image_name": "vegan-mozaik-pasta"
    },
    {
      "index": 383,
      "title": "Süt Ürünsüz Baklava (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-baklava"
    },
    {
      "index": 384,
      "title": "Süt Ürünsüz Kadayıf (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-kadayif"
    },
    {
      "index": 385,
      "title": "Süt Ürünsüz Şekerpare (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-sekerpare"
    },
    {
      "index": 386,
      "title": "Süt Ürünsüz Islak Kek (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-islak-kek"
    },
    {
      "index": 387,
      "title": "Süt Ürünsüz İrmik Helvası (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-irmik-helvasi"
    },
    {
      "index": 388,
      "title": "Glutensiz Vegan Revani (Glutensiz & Vegan)",
      "image_name": "glutensiz-vegan-revani"
    },
    {
      "index": 389,
      "title": "Glutensiz Vegan Islak Kek (Glutensiz & Vegan)",
      "image_name": "glutensiz-vegan-islak-kek"
    },
    {
      "index": 390,
      "title": "Glutensiz Un Kurabiyesi (Glutensiz)",
      "image_name": "glutensiz-un-kurabiyesi"
    },
    {
      "index": 391,
      "title": "Vegan Havuçlu Kek (Vegan)",
      "image_name": "vegan-havuclu-kek"
    },
    {
      "index": 392,
      "title": "Sobiyet",
      "image_name": "sobiyet"
    },
    {
      "index": 393,
      "title": "Cevizli Kek",
      "image_name": "cevizli-kek"
    },
    {
      "index": 394,
      "title": "Kabak Tatlısı",
      "image_name": "kabak-tatlisi"
    },
    {
      "index": 395,
      "title": "Kemalpaşa Tatlısı",
      "image_name": "kemalpasa-tatlisi"
    },
    {
      "index": 396,
      "title": "Kuruyemişsiz Ekmek Kadayıfı (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-ekmek-kadayifi"
    },
    {
      "index": 397,
      "title": "Glutensiz Limonlu Kek (Glutensiz)",
      "image_name": "glutensiz-limonlu-kek"
    },
    {
      "index": 398,
      "title": "Süt Ürünsüz Künefe (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-kunefe"
    },
    {
      "index": 399,
      "title": "Vegan Kabak Tatlısı (Vegan & Glutensiz)",
      "image_name": "vegan-kabak-tatlisi"
    },
    {
      "index": 400,
      "title": "Kokoreç",
      "image_name": "kokorec"
    },
    {
      "index": 401,
      "title": "Sokak Midye Dolma",
      "image_name": "sokak-midye-dolma"
    },
    {
      "index": 402,
      "title": "Islak Hamburger",
      "image_name": "islak-hamburger"
    },
    {
      "index": 403,
      "title": "Tantuni",
      "image_name": "tantuni"
    },
    {
      "index": 404,
      "title": "Kumpir",
      "image_name": "kumpir"
    },
    {
      "index": 405,
      "title": "Döner Dürüm",
      "image_name": "doner-durum"
    },
    {
      "index": 406,
      "title": "Balık Ekmek",
      "image_name": "balik-ekmek"
    },
    {
      "index": 407,
      "title": "Kahvaltı Menemen",
      "image_name": "kahvalti-menemen"
    },
    {
      "index": 408,
      "title": "Kuymak",
      "image_name": "kuymak"
    },
    {
      "index": 409,
      "title": "Pişi",
      "image_name": "pisi"
    },
    {
      "index": 410,
      "title": "Sucuklu Yumurta",
      "image_name": "sucuklu-yumurta"
    },
    {
      "index": 411,
      "title": "Poşe Yumurtalı Çılbır",
      "image_name": "pose-yumurtali-cilbir"
    },
    {
      "index": 412,
      "title": "Sokak Simidi",
      "image_name": "sokak-simidi"
    },
    {
      "index": 413,
      "title": "Vegan Kokoreç (Vegan)",
      "image_name": "vegan-kokorec"
    },
    {
      "index": 414,
      "title": "Vegan Midye Dolma (Vegan)",
      "image_name": "vegan-midye-dolma"
    },
    {
      "index": 415,
      "title": "Vegan Tantuni (Vegan)",
      "image_name": "vegan-tantuni"
    },
    {
      "index": 416,
      "title": "Vegan Kumpir (Vegan & Glutensiz)",
      "image_name": "vegan-kumpir"
    },
    {
      "index": 417,
      "title": "Tofulu Vegan Menemen (Vegan & Glutensiz)",
      "image_name": "tofulu-vegan-menemen"
    },
    {
      "index": 418,
      "title": "Vegan Kuymak (Vegan & Glutensiz)",
      "image_name": "vegan-kuymak"
    },
    {
      "index": 419,
      "title": "Glutensiz Pişi (Glutensiz)",
      "image_name": "glutensiz-pisi"
    },
    {
      "index": 420,
      "title": "Glutensiz Islak Hamburger (Glutensiz)",
      "image_name": "glutensiz-islak-hamburger"
    },
    {
      "index": 421,
      "title": "Süt Ürünsüz Kumpir (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-kumpir"
    },
    {
      "index": 422,
      "title": "Süt Ürünsüz Kuymak (Süt Ürünü Yok & Glutensiz)",
      "image_name": "sut-urunsuz-kuymak"
    },
    {
      "index": 423,
      "title": "Süt Ürünsüz Çılbır (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-cilbir"
    },
    {
      "index": 424,
      "title": "Vejetaryen Menemen (Vejetaryen)",
      "image_name": "vejetaryen-menemen"
    },
    {
      "index": 425,
      "title": "Vegan Pişi (Vegan)",
      "image_name": "vegan-pisi"
    },
    {
      "index": 426,
      "title": "Vegan Susamlı Simit (Vegan)",
      "image_name": "vegan-susamli-simit"
    },
    {
      "index": 427,
      "title": "Glutensiz Susamlı Simit (Glutensiz)",
      "image_name": "glutensiz-susamli-simit"
    },
    {
      "index": 428,
      "title": "Vegan Islak Hamburger (Vegan)",
      "image_name": "vegan-islak-hamburger"
    },
    {
      "index": 429,
      "title": "Süt Ürünsüz Sucuklu Yumurta (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-sucuklu-yumurta"
    },
    {
      "index": 430,
      "title": "Adana Dürüm",
      "image_name": "adana-durum"
    },
    {
      "index": 431,
      "title": "Çiğ Köfte Dürüm",
      "image_name": "cig-kofte-durum"
    },
    {
      "index": 432,
      "title": "Dürüm Döner",
      "image_name": "durum-doner"
    },
    {
      "index": 433,
      "title": "Kaşarlı Tost",
      "image_name": "kasarli-tost"
    },
    {
      "index": 434,
      "title": "Sokak Usulü Acılı Ezme",
      "image_name": "sokak-usulu-acili-ezme"
    },
    {
      "index": 435,
      "title": "Sahanda Yumurta",
      "image_name": "sahanda-yumurta"
    },
    {
      "index": 436,
      "title": "Peynirli Pide",
      "image_name": "peynirli-pide"
    },
    {
      "index": 437,
      "title": "Boyoz",
      "image_name": "boyoz"
    },
    {
      "index": 438,
      "title": "Vegan Döner Dürüm (Vegan)",
      "image_name": "vegan-doner-durum"
    },
    {
      "index": 439,
      "title": "Glutensiz Tantuni (Glutensiz)",
      "image_name": "glutensiz-tantuni"
    },
    {
      "index": 440,
      "title": "Süt Ürünsüz Kaşarlı Tost (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-kasarli-tost"
    },
    {
      "index": 441,
      "title": "Vegan Boyoz (Vegan)",
      "image_name": "vegan-boyoz"
    },
    {
      "index": 442,
      "title": "Vegan Peynirli Pide (Vegan)",
      "image_name": "vegan-peynirli-pide"
    },
    {
      "index": 443,
      "title": "Glutensiz Vegan Pişi (Glutensiz & Vegan)",
      "image_name": "glutensiz-vegan-pisi"
    },
    {
      "index": 444,
      "title": "Süt Ürünsüz Sahanda Yumurta (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-sahanda-yumurta"
    },
    {
      "index": 445,
      "title": "Vegan Adana Dürüm (Vegan)",
      "image_name": "vegan-adana-durum"
    },
    {
      "index": 446,
      "title": "Glutensiz Çiğ Köfte Dürüm (Glutensiz & Vegan)",
      "image_name": "glutensiz-cig-kofte-durum"
    },
    {
      "index": 447,
      "title": "Süt Ürünsüz Pişi (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-pisi"
    },
    {
      "index": 448,
      "title": "Vejetaryen Kumpir (Vejetaryen)",
      "image_name": "vejetaryen-kumpir"
    },
    {
      "index": 449,
      "title": "Glutensiz Balık Ekmek (Glutensiz)",
      "image_name": "glutensiz-balik-ekmek"
    },
    {
      "index": 450,
      "title": "Perde Pilavı",
      "image_name": "perde-pilavi"
    },
    {
      "index": 451,
      "title": "Analıkızlı Çorbası",
      "image_name": "analikizli-corbasi"
    },
    {
      "index": 452,
      "title": "Höşmerim",
      "image_name": "hosmerim"
    },
    {
      "index": 453,
      "title": "Sütlü Nuriye",
      "image_name": "sutlu-nuriye"
    },
    {
      "index": 454,
      "title": "Maraş Tarhanası Çorbası",
      "image_name": "maras-tarhanasi-corbasi"
    },
    {
      "index": 455,
      "title": "Çeçil Peynirli Börek",
      "image_name": "cecil-peynirli-borek"
    },
    {
      "index": 456,
      "title": "Kayseri Mantısı",
      "image_name": "kayseri-mantisi"
    },
    {
      "index": 457,
      "title": "Bici Bici",
      "image_name": "bici-bici"
    },
    {
      "index": 458,
      "title": "Keledoş",
      "image_name": "keledos"
    },
    {
      "index": 459,
      "title": "Arabaşı Çorbası",
      "image_name": "arabasi-corbasi"
    },
    {
      "index": 460,
      "title": "Çırpma",
      "image_name": "cirpma"
    },
    {
      "index": 461,
      "title": "Gülüzar Çorbası",
      "image_name": "guluzar-corbasi"
    },
    {
      "index": 462,
      "title": "Tirit",
      "image_name": "tirit"
    },
    {
      "index": 463,
      "title": "Gendime Pilavı",
      "image_name": "gendime-pilavi"
    },
    {
      "index": 464,
      "title": "Hıngel",
      "image_name": "hingel"
    },
    {
      "index": 465,
      "title": "Kaygana",
      "image_name": "kaygana"
    },
    {
      "index": 466,
      "title": "Kirde",
      "image_name": "kirde"
    },
    {
      "index": 467,
      "title": "Mumbar Dolması",
      "image_name": "mumbar-dolmasi"
    },
    {
      "index": 468,
      "title": "Yağlama",
      "image_name": "yaglama"
    },
    {
      "index": 469,
      "title": "Lobik",
      "image_name": "lobik"
    },
    {
      "index": 470,
      "title": "Düğürcük Çorbası",
      "image_name": "dugurcuk-corbasi"
    },
    {
      "index": 471,
      "title": "Çullama",
      "image_name": "cullama"
    },
    {
      "index": 472,
      "title": "Ekşili Pilav",
      "image_name": "eksili-pilav"
    },
    {
      "index": 473,
      "title": "Katıklı Ekmek",
      "image_name": "katikli-ekmek"
    },
    {
      "index": 474,
      "title": "Vegan Perde Pilavı (Vegan)",
      "image_name": "vegan-perde-pilavi"
    },
    {
      "index": 475,
      "title": "Glutensiz Analıkızlı Çorbası (Glutensiz & Vegan)",
      "image_name": "glutensiz-analikizli-corbasi"
    },
    {
      "index": 476,
      "title": "Süt Ürünsüz Sütlü Nuriye (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-sutlu-nuriye"
    },
    {
      "index": 477,
      "title": "Vegan Keledoş (Vegan & Glutensiz)",
      "image_name": "vegan-keledos"
    },
    {
      "index": 478,
      "title": "Süt Ürünsüz Höşmerim (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-hosmerim"
    },
    {
      "index": 479,
      "title": "Glutensiz Kayseri Mantısı (Glutensiz)",
      "image_name": "glutensiz-kayseri-mantisi"
    },
    {
      "index": 480,
      "title": "Vegan Lobik (Vegan & Glutensiz)",
      "image_name": "vegan-lobik"
    },
    {
      "index": 481,
      "title": "Süt Ürünsüz Çırpma (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-cirpma"
    },
    {
      "index": 482,
      "title": "Vegan Gendime Pilavı (Vegan)",
      "image_name": "vegan-gendime-pilavi"
    },
    {
      "index": 483,
      "title": "Süt Ürünsüz Kaygana (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-kaygana"
    },
    {
      "index": 484,
      "title": "Vegan Ekşili Pilav (Vegan & Glutensiz)",
      "image_name": "vegan-eksili-pilav"
    },
    {
      "index": 485,
      "title": "Kuruyemişsiz Sütlü Nuriye (Kuruyemiş Alerjisi)",
      "image_name": "kuruyemissiz-sutlu-nuriye"
    },
    {
      "index": 486,
      "title": "Glutensiz Bici Bici (Glutensiz & Vegan)",
      "image_name": "glutensiz-bici-bici"
    },
    {
      "index": 487,
      "title": "Vegan Katıklı Ekmek (Vegan & Glutensiz)",
      "image_name": "vegan-katikli-ekmek"
    },
    {
      "index": 488,
      "title": "Süt Ürünsüz Tirit (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-tirit"
    },
    {
      "index": 489,
      "title": "Vegan Arabaşı Çorbası (Vegan)",
      "image_name": "vegan-arabasi-corbasi"
    },
    {
      "index": 490,
      "title": "Süt Ürünsüz Gülüzar Çorbası (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-guluzar-corbasi"
    },
    {
      "index": 491,
      "title": "Vegan Düğürcük Çorbası (Vegan)",
      "image_name": "vegan-dugurcuk-corbasi"
    },
    {
      "index": 492,
      "title": "Sırın",
      "image_name": "sirin"
    },
    {
      "index": 493,
      "title": "Ayran Aşı Çorbası",
      "image_name": "ayran-asi-corbasi"
    },
    {
      "index": 494,
      "title": "Glutensiz Hıngel (Glutensiz)",
      "image_name": "glutensiz-hingel"
    },
    {
      "index": 495,
      "title": "Vegan Çullama (Vegan)",
      "image_name": "vegan-cullama"
    },
    {
      "index": 496,
      "title": "Süt Ürünsüz Çeçil Peynirli Börek (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-cecil-peynirli-borek"
    },
    {
      "index": 497,
      "title": "Vegan Mumbar Dolması (Vegan)",
      "image_name": "vegan-mumbar-dolmasi"
    },
    {
      "index": 498,
      "title": "Glutensiz Maraş Tarhanası Çorbası (Glutensiz)",
      "image_name": "glutensiz-maras-tarhanasi"
    },
    {
      "index": 499,
      "title": "Süt Ürünsüz Yağlama (Süt Ürünü Yok)",
      "image_name": "sut-urunsuz-yaglama"
    },
    {
      "index": 500,
      "title": "Patates Köftesi",
      "image_name": "patates-koftesi"
    },
    {
      "index": 501,
      "title": "Sodalı Köfte",
      "image_name": "sodali-kofte"
    },
    {
      "index": 502,
      "title": "Mantarlı Tavuk",
      "image_name": "mantarli-tavuk"
    },
    {
      "index": 503,
      "title": "Mantar Sote",
      "image_name": "mantar-sote"
    },
    {
      "index": 504,
      "title": "Ispanaklı Fırın Patates",
      "image_name": "ispanakli-firin-patates"
    },
    {
      "index": 505,
      "title": "Fırında Soslu Karnabahar",
      "image_name": "firinda-soslu-karnabahar"
    },
    {
      "index": 506,
      "title": "Patates Oturtma",
      "image_name": "patates-oturtma"
    },
    {
      "index": 507,
      "title": "Patates Yatağında Soslu Köfte",
      "image_name": "patates-yataginda-soslu-kofte"
    },
    {
      "index": 508,
      "title": "Mantarlı Tavuk Sote",
      "image_name": "mantarli-tavuk-sote"
    },
    {
      "index": 509,
      "title": "Kaşarlı Tas Kebabı",
      "image_name": "kasarli-tas-kebabi"
    },
    {
      "index": 510,
      "title": "Sebzeli Misket Köfte",
      "image_name": "sebzeli-misket-kofte"
    },
    {
      "index": 511,
      "title": "Tavuklu Patates Karnıyarık",
      "image_name": "tavuklu-patates-karniyarik"
    },
    {
      "index": 512,
      "title": "Tavuk Kanat",
      "image_name": "tavuk-kanat"
    },
    {
      "index": 513,
      "title": "Patatesli Bezelyeli Tavuk",
      "image_name": "patatesli-bezelyeli-tavuk"
    },
    {
      "index": 514,
      "title": "Patatesli Tavuk Göğsü",
      "image_name": "patatesli-tavuk-gogsu"
    },
    {
      "index": 515,
      "title": "Karnabahar Shots",
      "image_name": "karnabahar-shots"
    },
    {
      "index": 516,
      "title": "Belen Tava",
      "image_name": "belen-tava"
    },
    {
      "index": 517,
      "title": "Patatesli Sulu Köfte",
      "image_name": "patatesli-sulu-kofte"
    },
    {
      "index": 518,
      "title": "Sultan Kebabı",
      "image_name": "sultan-kebabi"
    },
    {
      "index": 519,
      "title": "Kuru Patlıcan Dolması",
      "image_name": "kuru-patlican-dolmasi"
    },
    {
      "index": 520,
      "title": "Mantar Soslu Tavuk",
      "image_name": "mantar-soslu-tavuk"
    },
    {
      "index": 521,
      "title": "Fırın Karnabahar",
      "image_name": "firin-karnabahar"
    },
    {
      "index": 522,
      "title": "Soğan Dolması",
      "image_name": "sogan-dolmasi"
    },
    {
      "index": 523,
      "title": "Tavuk Köftesi",
      "image_name": "tavuk-koftesi"
    },
    {
      "index": 524,
      "title": "Zeytinyağlı Patlıcan Yemeği",
      "image_name": "zeytinyagli-patlican-yemegi"
    },
    {
      "index": 525,
      "title": "Köfte",
      "image_name": "kofte"
    },
    {
      "index": 526,
      "title": "Zeytinyağlı Kuru Dolma",
      "image_name": "zeytinyagli-kuru-dolma"
    },
    {
      "index": 527,
      "title": "Soslu Tavuk",
      "image_name": "soslu-tavuk"
    },
    {
      "index": 528,
      "title": "Mantar Kavurması",
      "image_name": "mantar-kavurmasi"
    },
    {
      "index": 529,
      "title": "Bayat Pide Kebabı",
      "image_name": "bayat-pide-kebabi"
    },
    {
      "index": 530,
      "title": "Taco",
      "image_name": "taco"
    },
    {
      "index": 531,
      "title": "Ödemiş Köftesi",
      "image_name": "odemis-koftesi"
    }
  ]
}
````

## File: backend/data/recipes.json
````json
[
  {
    "Title": "Karnıyarık",
    "Ingredients": "['4 adet patlıcan', '250 gram kıyma', '2 adet soğan', '2 adet domates', '2 adet sivri biber', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Patlıcanları alacalı soyun ve tuzlu suda bekletin.\nKıymayı soğanla kavurun.\nDoğranmış domates ve biberi ekleyin.\nBaharatları ilave edip karıştırın.\nPatlıcanları kızartın ve ortalarını yarın.\nİç harcı patlıcanların içine doldurun.\nÜzerine domates dilimi koyun.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "karniyarik",
    "Cleaned_Ingredients": "['patlıcan', 'kıyma', 'soğan', 'domates', 'sivri biber', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "İmam Bayıldı",
    "Ingredients": "['6 adet patlıcan', '3 adet soğan', '4 adet domates', '6 diş sarımsak', '1 su bardağı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Patlıcanları alacalı soyun ve tuzlu suda bekletin.\nSoğanları ince doğrayıp zeytinyağında kavurun.\nSarımsakları ekleyin.\nRendelenmiş domatesleri ilave edin.\nMaydanozu doğrayıp karışıma ekleyin.\nPatlıcanları yarıp içlerini açın.\nHarcı patlıcanların içine doldurun.\nÜzerine domates dilimleri koyun.\nKısık ateşte 45 dakika pişirin.",
    "Image_Name": "imam-bayildi",
    "Cleaned_Ingredients": "['patlıcan', 'soğan', 'domates', 'sarımsak', 'zeytinyağı', 'maydanoz', 'tuz', 'şeker']"
  },
  {
    "Title": "Mercimek Çorbası",
    "Ingredients": "['1.5 su bardağı kırmızı mercimek', '1 adet soğan', '1 adet havuç', '1 adet patates', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '6 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Mercimeği yıkayın.\nSoğan, havuç ve patatesi doğrayın.\nTencereye alıp su ekleyin.\nSalçayı ilave edin.\nYaklaşık 30 dakika pişirin.\nBlenderdan geçirin.\nTereyağını eritip üzerine gezdirin.\nKimyon ve karabiber serpin.",
    "Image_Name": "mercimek-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'soğan', 'havuç', 'patates', 'domates salçası', 'tereyağı', 'su', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Kuru Fasulye",
    "Ingredients": "['2 su bardağı kuru fasulye', '200 gram kuşbaşı dana eti', '2 adet soğan', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı tereyağı', '6 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Fasulyeleri bir gece önceden ıslatın.\nEti tereyağında kavurun.\nSoğanları ekleyip soteleyin.\nSalçaları ilave edin.\nFasulyeleri ve sıcak suyu ekleyin.\nKısık ateşte yaklaşık 1.5 saat pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "kuru-fasulye",
    "Cleaned_Ingredients": "['kuru fasulye', 'dana eti', 'soğan', 'domates salçası', 'biber salçası', 'tereyağı', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Lahmacun",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '300 gram kıyma', '2 adet soğan', '2 adet domates', '1 demet maydanoz', '2 adet sivri biber', '1 yemek kaşığı biber salçası', '1 çay kaşığı pul biber']",
    "Instructions": "Un, maya, tuz ve suyu yoğurun.\nHamuru 30 dakika dinlendirin.\nKıymayı soğan, domates, biber ve maydanozla karıştırın.\nSalça ve baharatları ekleyin.\nHamuru bezeler ayırıp ince açın.\nÜzerine harcı yayın.\n250 derece fırında 8-10 dakika pişirin.",
    "Image_Name": "lahmacun",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'tuz', 'su', 'kıyma', 'soğan', 'domates', 'maydanoz', 'sivri biber', 'biber salçası', 'pul biber']"
  },
  {
    "Title": "Mantı",
    "Ingredients": "['3 su bardağı un', '2 adet yumurta', '1 çay kaşığı tuz', '200 gram kıyma', '1 adet soğan', '2 su bardağı yoğurt', '3 diş sarımsak', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı pul biber', '1 çay kaşığı nane']",
    "Instructions": "Un, yumurta, tuz ve suyla hamur yoğurun.\n30 dakika dinlendirin.\nKıyma ve soğanı karıştırarak iç harç yapın.\nHamuru ince açıp kareler kesin.\nHer karenin ortasına harç koyup kapatın.\nKaynayan suda 15 dakika haşlayın.\nSarımsaklı yoğurdu hazırlayın.\nTereyağında salça ve pul biberi kızdırın.\nMantının üzerine yoğurt ve sos gezdirin.",
    "Image_Name": "manti",
    "Cleaned_Ingredients": "['un', 'yumurta', 'tuz', 'kıyma', 'soğan', 'yoğurt', 'sarımsak', 'tereyağı', 'domates salçası', 'pul biber', 'nane']"
  },
  {
    "Title": "Hünkar Beğendi",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '3 adet patlıcan', '2 adet soğan', '2 adet domates', '2 yemek kaşığı tereyağı', '2 yemek kaşığı un', '1.5 su bardağı süt', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kuzu etini soğanla kavurun.\nDoğranmış domatesleri ekleyin.\nSu ilave edip kısık ateşte pişirin.\nPatlıcanları közleyin ve kabuklarını soyun.\nEzin ve bir tencereye alın.\nAyrı bir tencerede tereyağı ve unu kavurun.\nSütü yavaş yavaş ekleyip beşamel yapın.\nPatlıcan püresiyle karıştırın.\nBeğendiyi tabağa yayıp üzerine eti koyun.",
    "Image_Name": "hunkar-begendi",
    "Cleaned_Ingredients": "['kuzu eti', 'patlıcan', 'soğan', 'domates', 'tereyağı', 'un', 'süt', 'tuz', 'karabiber']"
  },
  {
    "Title": "Çılbır",
    "Ingredients": "['4 adet yumurta', '2 su bardağı yoğurt', '2 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber', '1 yemek kaşığı sirke', '1 çay kaşığı tuz']",
    "Instructions": "Yoğurdu sarımsakla ezin.\nSuyu kaynatın ve sirke ekleyin.\nYumurtaları teker teker poşe yapın.\nTabağa sarımsaklı yoğurdu yayın.\nÜzerine poşe yumurtaları yerleştirin.\nTereyağını eritip pul biberle kızdırın.\nYumurtaların üzerine gezdirin.",
    "Image_Name": "cilbir",
    "Cleaned_Ingredients": "['yumurta', 'yoğurt', 'sarımsak', 'tereyağı', 'pul biber', 'sirke', 'tuz']"
  },
  {
    "Title": "İçli Köfte",
    "Ingredients": "['2 su bardağı ince bulgur', '1 su bardağı irmik', '250 gram kıyma', '2 adet soğan', '1 demet maydanoz', '3 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon']",
    "Instructions": "Bulguru ıslatıp irmikle yoğurun.\nKıymayı soğanla tereyağında kavurun.\nMaydanoz ve baharatları ekleyin.\nDış hamurdan ceviz büyüklüğünde parçalar koparın.\nOrtalarını oyup iç harcı doldurun.\nKapatıp şekil verin.\nKaynamış suda veya yağda pişirin.",
    "Image_Name": "icli-kofte",
    "Cleaned_Ingredients": "['ince bulgur', 'irmik', 'kıyma', 'soğan', 'maydanoz', 'tereyağı', 'tuz', 'karabiber', 'pul biber', 'kimyon']"
  },
  {
    "Title": "Etli Nohut Yemeği",
    "Ingredients": "['2 su bardağı nohut', '250 gram kuşbaşı dana eti', '2 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '5 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Nohudu bir gece önceden ıslatın.\nEti tereyağında kavurun.\nSoğanları ekleyip soteleyin.\nSalçayı ilave edip karıştırın.\nNohudu ve sıcak suyu ekleyin.\nKısık ateşte 1 saat pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "etli-nohut",
    "Cleaned_Ingredients": "['nohut', 'dana eti', 'soğan', 'domates salçası', 'tereyağı', 'su', 'tuz', 'karabiber']"
  },
  {
    "Title": "Zeytinyağlı Yaprak Sarma",
    "Ingredients": "['50 adet asma yaprağı', '1.5 su bardağı pirinç', '3 adet soğan', '2 adet domates', '1 demet dereotu', '1 demet nane', '1 su bardağı zeytinyağı', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Asma yapraklarını haşlayın.\nPirinci yıkayıp süzün.\nSoğanları ince doğrayıp zeytinyağında kavurun.\nPirinci ekleyin.\nDoğranmış domates, dereotu ve naneyi ilave edin.\nBaharatları ekleyip karıştırın.\nYaprakların içine harçtan koyup sarın.\nTencereye dizin, üzerine su ve limon suyu ekleyin.\nKısık ateşte 45 dakika pişirin.",
    "Image_Name": "zeytinyagli-yaprak-sarma",
    "Cleaned_Ingredients": "['asma yaprağı', 'pirinç', 'soğan', 'domates', 'dereotu', 'nane', 'zeytinyağı', 'limon', 'tuz', 'karabiber']"
  },
  {
    "Title": "Şakşuka",
    "Ingredients": "['3 adet patlıcan', '3 adet biber', '4 adet domates', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Patlıcanları ve biberleri küp küp doğrayın.\nZeytinyağında patlıcanları kavurun.\nBiberleri ekleyin.\nDoğranmış domates ve sarımsakları ilave edin.\nBaharatları ekleyin.\nKısık ateşte 20 dakika pişirin.",
    "Image_Name": "saksuka",
    "Cleaned_Ingredients": "['patlıcan', 'biber', 'domates', 'sarımsak', 'zeytinyağı', 'tuz', 'pul biber']"
  },
  {
    "Title": "Zeytinyağlı Barbunya",
    "Ingredients": "['2 su bardağı barbunya', '2 adet soğan', '2 adet havuç', '3 adet domates', '1 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Barbunya fasulyelerini bir gece ıslatın.\nSoğanları zeytinyağında kavurun.\nHavuç ve domatesleri ekleyin.\nFasulyeleri ilave edip su ekleyin.\nKısık ateşte 1 saat pişirin.\nSoğuk servis yapın.",
    "Image_Name": "zeytinyagli-barbunya",
    "Cleaned_Ingredients": "['barbunya', 'soğan', 'havuç', 'domates', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Kısır",
    "Ingredients": "['2 su bardağı ince bulgur', '2 yemek kaşığı domates salçası', '2 yemek kaşığı biber salçası', '4 adet yeşil soğan', '1 demet maydanoz', '1 adet limon', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı nar ekşisi', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon']",
    "Instructions": "Bulguru sıcak suyla ıslatın ve 15 dakika bekletin.\nSalçaları ve zeytinyağını ekleyip yoğurun.\nİnce doğranmış yeşil soğan ve maydanozu ekleyin.\nLimon suyu ve nar ekşisini ilave edin.\nBaharatları ekleyip karıştırın.\nSoğuk servis yapın.",
    "Image_Name": "kisir",
    "Cleaned_Ingredients": "['ince bulgur', 'domates salçası', 'biber salçası', 'yeşil soğan', 'maydanoz', 'limon', 'zeytinyağı', 'nar ekşisi', 'tuz', 'pul biber', 'kimyon']"
  },
  {
    "Title": "Menemen",
    "Ingredients": "['4 adet yumurta', '3 adet domates', '2 adet sivri biber', '1 adet soğan', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Soğanı tereyağında kavurun.\nBiberleri ekleyin.\nDoğranmış domatesleri ilave edin.\nDomatesler yumuşayınca yumurtaları kırın.\nYavaşça karıştırarak pişirin.\nBaharatları ekleyin.\nSıcak servis yapın.",
    "Image_Name": "menemen",
    "Cleaned_Ingredients": "['yumurta', 'domates', 'sivri biber', 'soğan', 'tereyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Adana Kebap",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '2 diş sarımsak', '1 yemek kaşığı biber salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon', '4 adet lavaş']",
    "Instructions": "Kıymayı soğan ve sarımsakla yoğurun.\nSalça ve baharatları ekleyip iyice karıştırın.\nBuzdolabında 2 saat dinlendirin.\nŞişlere sararak mangalda veya ızgarada pişirin.\nLavaş, soğan ve közlenmiş domates ile servis yapın.",
    "Image_Name": "adana-kebap",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'sarımsak', 'biber salçası', 'tuz', 'karabiber', 'pul biber', 'kimyon', 'lavaş']"
  },
  {
    "Title": "Sütlaç",
    "Ingredients": "['1 litre süt', '1 çay bardağı pirinç', '1 su bardağı toz şeker', '2 yemek kaşığı nişasta', '1 paket vanilya']",
    "Instructions": "Pirinçleri yıkayıp haşlayın.\nSütü ekleyin ve kaynatın.\nŞekeri ilave edin.\nNişastayı az sütte eritip tencereye ekleyin.\nVanilyayı ilave edin.\nKoyulaşana kadar karıştırarak pişirin.\nKaselere paylaştırın.\nFırında üzerini kızartın.",
    "Image_Name": "sutlac",
    "Cleaned_Ingredients": "['süt', 'pirinç', 'toz şeker', 'nişasta', 'vanilya']"
  },
  {
    "Title": "Baklava",
    "Ingredients": "['500 gram yufka', '250 gram tereyağı', '2 su bardağı ceviz', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Yufkaları tepsiye sererken aralarına eritilmiş tereyağı sürün.\nHer 3-4 yufkada bir ceviz serpin.\nTüm yufkaları serdikten sonra dilimleyin.\nKalan tereyağını üzerine gezdirin.\n170 derece fırında 45 dakika pişirin.\nŞeker ve suyu kaynatıp şerbet yapın.\nLimon suyu ekleyin.\nSıcak baklavanın üzerine soğuk şerbeti dökün.",
    "Image_Name": "baklava",
    "Cleaned_Ingredients": "['yufka', 'tereyağı', 'ceviz', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Türlü",
    "Ingredients": "['2 adet patlıcan', '2 adet kabak', '2 adet patates', '2 adet biber', '3 adet domates', '1 adet soğan', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Tüm sebzeleri büyük küpler halinde doğrayın.\nZeytinyağını tencereye alın.\nSoğan ve sarımsağı kavurun.\nSebzeleri ekleyin.\nBaharatları ilave edin.\nKısık ateşte veya 180 derece fırında 40 dakika pişirin.",
    "Image_Name": "turlu",
    "Cleaned_Ingredients": "['patlıcan', 'kabak', 'patates', 'biber', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'tuz', 'karabiber']"
  },
  {
    "Title": "Ezogelin Çorbası",
    "Ingredients": "['1 su bardağı kırmızı mercimek', '0.5 su bardağı pirinç', '0.5 su bardağı ince bulgur', '1 adet soğan', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı tereyağı', '6 su bardağı su', '1 çay kaşığı nane', '1 çay kaşığı pul biber', '1 çay kaşığı tuz']",
    "Instructions": "Mercimek, pirinç ve bulguru yıkayın.\nSu ile tencereye alın ve pişirin.\nAyrı bir tavada tereyağını eritin.\nSoğanı kavurun, salçaları ekleyin.\nSosu çorbaya ilave edin.\nBaharatları ekleyip 5 dakika daha pişirin.",
    "Image_Name": "ezogelin-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'pirinç', 'ince bulgur', 'soğan', 'domates salçası', 'biber salçası', 'tereyağı', 'su', 'nane', 'pul biber', 'tuz']"
  },
  {
    "Title": "Tas Kebabı",
    "Ingredients": "['500 gram kuşbaşı dana eti', '3 adet patates', '2 adet soğan', '2 adet domates', '2 adet sivri biber', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Eti tereyağında kavurun.\nSoğanları ekleyin.\nSalçayı ilave edin.\nSu ekleyip 30 dakika pişirin.\nPatatesleri ekleyin.\nDomates ve biberleri ilave edin.\nKısık ateşte 20 dakika daha pişirin.",
    "Image_Name": "tas-kebabi",
    "Cleaned_Ingredients": "['dana eti', 'patates', 'soğan', 'domates', 'sivri biber', 'tereyağı', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "Patlıcan Musakka",
    "Ingredients": "['4 adet patlıcan', '250 gram kıyma', '2 adet soğan', '3 adet domates', '2 adet sivri biber', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Patlıcanları halka halka kesin ve kızartın.\nKıymayı soğanla kavurun.\nDoğranmış domates ve biberleri ekleyin.\nBaharatları ilave edin.\nTepsiye patlıcan ve kıymalı harcı katlar halinde dizin.\nÜzerine domates dilimleri koyun.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "patlican-musakka",
    "Cleaned_Ingredients": "['patlıcan', 'kıyma', 'soğan', 'domates', 'sivri biber', 'zeytinyağı', 'tuz', 'karabiber']"
  },
  {
    "Title": "Pilav Üstü Kuru Fasulye",
    "Ingredients": "['2 su bardağı kuru fasulye', '200 gram kuşbaşı dana eti', '2 adet soğan', '2 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '2 su bardağı pirinç', '3 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Fasulyeleri bir gece ıslatın.\nEti tereyağında kavurun.\nSoğan ve salçayı ekleyin.\nFasulyeleri ve suyu ilave edip 1.5 saat pişirin.\nAyrı bir tencerede pirinci tereyağında kavurun.\nSu ve tuz ekleyip pilavı pişirin.\nPilavın üzerine fasulye dökün.",
    "Image_Name": "pilav-ustu-kuru-fasulye",
    "Cleaned_Ingredients": "['kuru fasulye', 'dana eti', 'soğan', 'domates salçası', 'tereyağı', 'pirinç', 'su', 'tuz', 'karabiber']"
  },
  {
    "Title": "Ispanaklı Yumurta",
    "Ingredients": "['500 gram ıspanak', '3 adet yumurta', '1 adet soğan', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Ispanakları yıkayıp doğrayın.\nSoğanı tereyağında kavurun.\nIspanakları ekleyip suyunu salana kadar pişirin.\nYumurtaları kırıp üzerine ekleyin.\nBaharatları serpin.\nYumurtalar pişene kadar bekleyin.",
    "Image_Name": "ispanakli-yumurta",
    "Cleaned_Ingredients": "['ıspanak', 'yumurta', 'soğan', 'tereyağı', 'tuz', 'pul biber']"
  },
  {
    "Title": "Ali Nazik Kebap",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '4 adet patlıcan', '2 su bardağı yoğurt', '3 diş sarımsak', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Patlıcanları közleyin ve kabuklarını soyun.\nEzin ve sarımsaklı yoğurtla karıştırın.\nKuzu etini tereyağında kavurun.\nSalça ve baharatları ekleyin.\nPatlıcanlı yoğurdu tabağa yayın.\nÜzerine kavurulmuş eti koyun.\nPul biberli tereyağı gezdirin.",
    "Image_Name": "ali-nazik-kebap",
    "Cleaned_Ingredients": "['kuzu eti', 'patlıcan', 'yoğurt', 'sarımsak', 'tereyağı', 'domates salçası', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Mercimek Köftesi (Vegan)",
    "Ingredients": "['2 su bardağı kırmızı mercimek', '1.5 su bardağı ince bulgur', '3 adet yeşil soğan', '1 demet maydanoz', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber', '1 adet limon']",
    "Instructions": "Mercimeği yıkayıp bol suda haşlayın.\nHaşlanan mercimeğin üzerine bulguru ekleyip kapağını kapatın.\n15 dakika demlendirin.\nSalçaları ve zeytinyağını ekleyip yoğurun.\nİnce doğranmış yeşil soğan ve maydanozu katın.\nBaharatları ve limon suyunu ekleyin.\nKöfte şekli verip servis yapın.",
    "Image_Name": "vegan-mercimek-koftesi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'ince bulgur', 'yeşil soğan', 'maydanoz', 'domates salçası', 'biber salçası', 'zeytinyağı', 'tuz', 'kimyon', 'pul biber', 'limon']"
  },
  {
    "Title": "Vegan Karnıyarık (Vegan)",
    "Ingredients": "['4 adet patlıcan', '1 su bardağı yeşil mercimek', '2 adet soğan', '2 adet domates', '2 adet sivri biber', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Patlıcanları alacalı soyun ve tuzlu suda bekletin.\nYeşil mercimeği önceden haşlayın.\nSoğanı zeytinyağında kavurun.\nDoğranmış domates ve biberi ekleyin.\nHaşlanmış mercimeği ilave edin.\nBaharatları ekleyin.\nPatlıcanları kızartıp ortalarını yarın.\nMercimekli harcı doldurun.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "vegan-karniyarik",
    "Cleaned_Ingredients": "['patlıcan', 'yeşil mercimek', 'soğan', 'domates', 'sivri biber', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Menemen (Vegan)",
    "Ingredients": "['300 gram tofu', '3 adet domates', '2 adet sivri biber', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '0.5 çay kaşığı zerdeçal', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Tofuyu ufalayın.\nSoğanı zeytinyağında kavurun.\nBiberleri ekleyin.\nDoğranmış domatesleri ilave edin.\nTofuyu ekleyip zerdeçalle renklendirin.\nBaharatları ekleyip 5 dakika daha pişirin.\nSıcak servis yapın.",
    "Image_Name": "vegan-menemen",
    "Cleaned_Ingredients": "['tofu', 'domates', 'sivri biber', 'soğan', 'zeytinyağı', 'zerdeçal', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Çılbır (Vegan)",
    "Ingredients": "['300 gram yumuşak tofu', '1 su bardağı soya yoğurdu', '2 diş sarımsak', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı pul biber', '1 yemek kaşığı sirke', '1 çay kaşığı zerdeçal', '1 çay kaşığı tuz']",
    "Instructions": "Tofuyu kalın dilimler halinde kesin.\nSirkeli suda hafifçe haşlayın.\nSoya yoğurdunu sarımsakla karıştırın.\nTabağa yoğurdu yayın.\nÜzerine tofu dilimlerini yerleştirin.\nZeytinyağını pul biberle kızdırın.\nÜzerine gezdirin.",
    "Image_Name": "vegan-cilbir",
    "Cleaned_Ingredients": "['tofu', 'soya yoğurdu', 'sarımsak', 'zeytinyağı', 'pul biber', 'sirke', 'zerdeçal', 'tuz']"
  },
  {
    "Title": "Glutensiz Lahmacun (Glutensiz)",
    "Ingredients": "['2 su bardağı mısır unu', '1 su bardağı pirinç unu', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '300 gram kıyma', '2 adet soğan', '2 adet domates', '1 demet maydanoz', '2 adet sivri biber', '1 yemek kaşığı biber salçası', '1 çay kaşığı pul biber']",
    "Instructions": "Mısır unu, pirinç unu, maya, tuz ve suyla hamur yoğurun.\n30 dakika dinlendirin.\nKıymayı soğan, domates, biber ve maydanozla karıştırın.\nSalça ve baharatları ekleyin.\nHamuru ince açın.\nÜzerine harcı yayın.\n250 derece fırında 10 dakika pişirin.",
    "Image_Name": "glutensiz-lahmacun",
    "Cleaned_Ingredients": "['mısır unu', 'pirinç unu', 'yaş maya', 'tuz', 'su', 'kıyma', 'soğan', 'domates', 'maydanoz', 'sivri biber', 'biber salçası', 'pul biber']"
  },
  {
    "Title": "Glutensiz Mercimek Çorbası (Glutensiz)",
    "Ingredients": "['1.5 su bardağı kırmızı mercimek', '1 adet soğan', '1 adet havuç', '1 adet patates', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '6 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Mercimeği yıkayın.\nSoğan, havuç ve patatesi doğrayın.\nTencereye alıp su ekleyin.\nSalçayı ilave edin.\n30 dakika pişirin.\nBlenderdan geçirin.\nTereyağını eritip üzerine gezdirin.\nKimyon ve karabiber serpin.",
    "Image_Name": "glutensiz-mercimek-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'soğan', 'havuç', 'patates', 'domates salçası', 'tereyağı', 'su', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Glutensiz İçli Köfte (Glutensiz)",
    "Ingredients": "['2 su bardağı haşlanmış patates', '1 su bardağı mısır unu', '250 gram kıyma', '2 adet soğan', '1 demet maydanoz', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon']",
    "Instructions": "Haşlanmış patatesleri ezin.\nMısır ununu ekleyip yoğurun.\nKıymayı soğanla tereyağında kavurun.\nMaydanoz ve baharatları ekleyin.\nDış hamurdan parçalar koparıp içini oyun.\nİç harcı doldurup kapatın.\nKaynamış suda haşlayın veya fırınlayın.",
    "Image_Name": "glutensiz-icli-kofte",
    "Cleaned_Ingredients": "['patates', 'mısır unu', 'kıyma', 'soğan', 'maydanoz', 'tereyağı', 'tuz', 'karabiber', 'pul biber', 'kimyon']"
  },
  {
    "Title": "Yulaf Sütlü Sütlaç (Vegan & Glutensiz)",
    "Ingredients": "['1 litre yulaf sütü', '1 çay bardağı pirinç', '1 su bardağı toz şeker', '2 yemek kaşığı mısır nişastası', '1 paket vanilya']",
    "Instructions": "Pirinçleri yıkayıp haşlayın.\nYulaf sütünü ekleyip kaynatın.\nŞekeri ilave edin.\nNişastayı az yulaf sütünde eritip ekleyin.\nVanilyayı ilave edin.\nKoyulaşana kadar pişirin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "yulaf-sutlu-sutlac",
    "Cleaned_Ingredients": "['yulaf sütü', 'pirinç', 'toz şeker', 'mısır nişastası', 'vanilya']"
  },
  {
    "Title": "Laktozsuz Sütlaç (Süt Ürünü Yok)",
    "Ingredients": "['1 litre badem sütü', '1 çay bardağı pirinç', '1 su bardağı toz şeker', '2 yemek kaşığı mısır nişastası', '1 paket vanilya']",
    "Instructions": "Pirinçleri yıkayıp haşlayın.\nBadem sütünü ekleyip kaynatın.\nŞekeri ilave edin.\nNişastayı az badem sütünde eritip ekleyin.\nVanilyayı ilave edin.\nKoyulaşana kadar pişirin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "laktozsuz-sutlac",
    "Cleaned_Ingredients": "['badem sütü', 'pirinç', 'toz şeker', 'mısır nişastası', 'vanilya']"
  },
  {
    "Title": "Vejetaryen Kuru Fasulye (Vejetaryen)",
    "Ingredients": "['2 su bardağı kuru fasulye', '2 adet soğan', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı zeytinyağı', '6 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Fasulyeleri bir gece önceden ıslatın.\nSoğanları zeytinyağında kavurun.\nSalçaları ilave edin.\nFasulyeleri ve sıcak suyu ekleyin.\nKısık ateşte 1.5 saat pişirin.\nBaharatları ekleyin.",
    "Image_Name": "vejetaryen-kuru-fasulye",
    "Cleaned_Ingredients": "['kuru fasulye', 'soğan', 'domates salçası', 'biber salçası', 'zeytinyağı', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vejetaryen Mantı (Vejetaryen)",
    "Ingredients": "['3 su bardağı un', '2 adet yumurta', '1 çay kaşığı tuz', '2 adet patates', '1 adet soğan', '2 su bardağı yoğurt', '3 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber', '1 çay kaşığı nane']",
    "Instructions": "Un, yumurta, tuz ve suyla hamur yoğurun.\n30 dakika dinlendirin.\nHaşlanmış patatesleri ezin, soğanla karıştırın.\nHamuru ince açıp kareler kesin.\nHer karenin ortasına patatesli harç koyup kapatın.\nKaynayan suda 15 dakika haşlayın.\nSarımsaklı yoğurdu hazırlayın.\nTereyağında pul biberi kızdırın.\nMantının üzerine yoğurt ve sos gezdirin.",
    "Image_Name": "vejetaryen-manti",
    "Cleaned_Ingredients": "['un', 'yumurta', 'tuz', 'patates', 'soğan', 'yoğurt', 'sarımsak', 'tereyağı', 'pul biber', 'nane']"
  },
  {
    "Title": "Vejetaryen Pide (Vejetaryen)",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '200 gram beyaz peynir', '200 gram kaşar peyniri', '2 adet yumurta', '1 demet maydanoz']",
    "Instructions": "Un, maya, tuz ve suyla hamur yoğurun.\n30 dakika dinlendirin.\nPeynirleri ufalayıp maydanozla karıştırın.\nHamuru pide şeklinde açın.\nİçine peynirli harcı koyun.\nKenarlarını kıvırın.\nÜzerine yumurta sarısı sürün.\n220 derece fırında 15 dakika pişirin.",
    "Image_Name": "vejetaryen-pide",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'tuz', 'su', 'beyaz peynir', 'kaşar peyniri', 'yumurta', 'maydanoz']"
  },
  {
    "Title": "Glutensiz Kısır (Glutensiz)",
    "Ingredients": "['2 su bardağı karabuğday', '2 yemek kaşığı domates salçası', '2 yemek kaşığı biber salçası', '4 adet yeşil soğan', '1 demet maydanoz', '1 adet limon', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı nar ekşisi', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon']",
    "Instructions": "Karabuğdayı haşlayıp süzün.\nSalçaları ve zeytinyağını ekleyip karıştırın.\nİnce doğranmış yeşil soğan ve maydanozu ekleyin.\nLimon suyu ve nar ekşisini ilave edin.\nBaharatları ekleyip karıştırın.\nSoğuk servis yapın.",
    "Image_Name": "glutensiz-kisir",
    "Cleaned_Ingredients": "['karabuğday', 'domates salçası', 'biber salçası', 'yeşil soğan', 'maydanoz', 'limon', 'zeytinyağı', 'nar ekşisi', 'tuz', 'pul biber', 'kimyon']"
  },
  {
    "Title": "Glutensiz Ezogelin Çorbası (Glutensiz)",
    "Ingredients": "['1 su bardağı kırmızı mercimek', '0.5 su bardağı pirinç', '1 adet soğan', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı tereyağı', '6 su bardağı su', '1 çay kaşığı nane', '1 çay kaşığı pul biber', '1 çay kaşığı tuz']",
    "Instructions": "Mercimek ve pirinci yıkayın.\nSu ile tencereye alıp pişirin.\nAyrı bir tavada tereyağını eritin.\nSoğanı kavurun, salçaları ekleyin.\nSosu çorbaya ilave edin.\nBaharatları ekleyip 5 dakika daha pişirin.",
    "Image_Name": "glutensiz-ezogelin-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'pirinç', 'soğan', 'domates salçası', 'biber salçası', 'tereyağı', 'su', 'nane', 'pul biber', 'tuz']"
  },
  {
    "Title": "Süt Ürünsüz Hünkar Beğendi (Süt Ürünü Yok)",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '4 adet patlıcan', '2 adet soğan', '2 adet domates', '2 yemek kaşığı zeytinyağı', '1 su bardağı mısır unu', '1.5 su bardağı et suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kuzu etini soğanla zeytinyağında kavurun.\nDoğranmış domatesleri ekleyin.\nSu ilave edip kısık ateşte pişirin.\nPatlıcanları közleyin ve kabuklarını soyun.\nEzin ve bir tencereye alın.\nAyrı bir tencerede zeytinyağı ve mısır ununu kavurun.\nEt suyunu yavaş yavaş ekleyip koyulaştırın.\nPatlıcan püresiyle karıştırın.\nTabağa beğendiyi yayıp üzerine eti koyun.",
    "Image_Name": "sut-urunsuz-hunkar-begendi",
    "Cleaned_Ingredients": "['kuzu eti', 'patlıcan', 'soğan', 'domates', 'zeytinyağı', 'mısır unu', 'et suyu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Yaprak Sarma (Vegan)",
    "Ingredients": "['50 adet asma yaprağı', '1.5 su bardağı pirinç', '3 adet soğan', '2 adet domates', '1 demet dereotu', '1 demet nane', '1 su bardağı zeytinyağı', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Asma yapraklarını haşlayın.\nPirinci yıkayıp süzün.\nSoğanları ince doğrayıp zeytinyağında kavurun.\nPirinci ekleyin.\nDoğranmış domates, dereotu ve naneyi ilave edin.\nBaharatları ekleyip karıştırın.\nYaprakların içine harçtan koyup sarın.\nTencereye dizin, su ve limon suyu ekleyin.\nKısık ateşte 45 dakika pişirin.",
    "Image_Name": "vegan-yaprak-sarma",
    "Cleaned_Ingredients": "['asma yaprağı', 'pirinç', 'soğan', 'domates', 'dereotu', 'nane', 'zeytinyağı', 'limon', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vejetaryen Ispanaklı Börek (Vejetaryen)",
    "Ingredients": "['6 adet yufka', '500 gram ıspanak', '200 gram beyaz peynir', '2 adet yumurta', '0.5 su bardağı zeytinyağı', '0.5 su bardağı yulaf sütü', '1 çay kaşığı tuz']",
    "Instructions": "Ispanakları yıkayıp doğrayın.\nPeyniri ufalayıp ıspanakla karıştırın.\nYumurtayı, zeytinyağını ve yulaf sütünü ayrı bir kapta çırpın.\nYufkaları tepsiye sererken aralarına sıvı karışımı sürün.\nHer 2 yufkada bir ıspanaklı harç serpin.\nÜst yufkayı serdikten sonra kalan sıvıyı gezdirin.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "vejetaryen-ispanakli-borek",
    "Cleaned_Ingredients": "['yufka', 'ıspanak', 'beyaz peynir', 'yumurta', 'zeytinyağı', 'yulaf sütü', 'tuz']"
  },
  {
    "Title": "Kuruyemişsiz Aşure (Kuruyemiş Alerjisi)",
    "Ingredients": "['1 su bardağı buğday', '0.5 su bardağı nohut', '0.5 su bardağı kuru fasulye', '1 su bardağı toz şeker', '0.5 su bardağı kuru kayısı', '0.5 su bardağı kuru üzüm', '0.5 su bardağı kuru incir', '2 yemek kaşığı nişasta', '1 yemek kaşığı gül suyu', '8 su bardağı su', '1 çay kaşığı tarçın']",
    "Instructions": "Buğday, nohut ve fasulyeyi bir gece ıslatın.\nAyrı ayrı haşlayın.\nKuru meyveleri doğrayıp ılık suda bekletin.\nBüyük bir tencerede hepsini birleştirin.\nŞekeri ve suyu ekleyip kaynatın.\nNişastayı az suda eritip ilave edin.\nGül suyunu ekleyin.\nKaselere paylaştırıp tarçın serpin.",
    "Image_Name": "kuruyemissiz-asure",
    "Cleaned_Ingredients": "['buğday', 'nohut', 'kuru fasulye', 'toz şeker', 'kuru kayısı', 'kuru üzüm', 'kuru incir', 'nişasta', 'gül suyu', 'su', 'tarçın']"
  },
  {
    "Title": "Glutensiz Patates Köftesi (Glutensiz & Vejetaryen)",
    "Ingredients": "['5 adet patates', '1 su bardağı mısır unu', '1 adet yumurta', '1 adet soğan', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', 'kızartma yağı']",
    "Instructions": "Patatesleri haşlayıp ezin.\nMısır unu, yumurta ve baharatları ekleyin.\nİnce doğranmış soğan ve maydanozu ilave edin.\nYoğurun ve köfte şekli verin.\nKızgın yağda kızartın.\nKağıt havlu üzerinde fazla yağını alın.",
    "Image_Name": "glutensiz-patates-koftesi",
    "Cleaned_Ingredients": "['patates', 'mısır unu', 'yumurta', 'soğan', 'maydanoz', 'tuz', 'karabiber', 'pul biber', 'kızartma yağı']"
  },
  {
    "Title": "Vegan Mercimek Çorbası (Vegan & Glutensiz)",
    "Ingredients": "['1.5 su bardağı kırmızı mercimek', '1 adet soğan', '1 adet havuç', '1 adet patates', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '6 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Mercimeği yıkayın.\nSoğan, havuç ve patatesi doğrayın.\nTencereye alıp su ekleyin.\nSalçayı ilave edin.\n30 dakika pişirin.\nBlenderdan geçirin.\nZeytinyağını ısıtıp kimyon ve pul biber ekleyin.\nÜzerine gezdirin.",
    "Image_Name": "vegan-mercimek-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'soğan', 'havuç', 'patates', 'domates salçası', 'zeytinyağı', 'su', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Vejetaryen Patlıcan Musakka (Vejetaryen)",
    "Ingredients": "['4 adet patlıcan', '1 su bardağı yeşil mercimek', '2 adet soğan', '3 adet domates', '2 adet sivri biber', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Patlıcanları halka halka kesin ve kızartın.\nYeşil mercimeği önceden haşlayın.\nSoğanı zeytinyağında kavurun.\nDoğranmış domates ve biberleri ekleyin.\nHaşlanmış mercimeği ilave edin.\nTepsiye patlıcan ve mercimekli harcı katlar halinde dizin.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "vejetaryen-patlican-musakka",
    "Cleaned_Ingredients": "['patlıcan', 'yeşil mercimek', 'soğan', 'domates', 'sivri biber', 'zeytinyağı', 'tuz', 'karabiber']"
  },
  {
    "Title": "Süt Ürünsüz Menemen (Süt Ürünü Yok)",
    "Ingredients": "['4 adet yumurta', '3 adet domates', '2 adet sivri biber', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Soğanı zeytinyağında kavurun.\nBiberleri ekleyin.\nDoğranmış domatesleri ilave edin.\nDomatesler yumuşayınca yumurtaları kırın.\nYavaşça karıştırarak pişirin.\nBaharatları ekleyin.\nSıcak servis yapın.",
    "Image_Name": "sut-urunsuz-menemen",
    "Cleaned_Ingredients": "['yumurta', 'domates', 'sivri biber', 'soğan', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Baklava (Vegan)",
    "Ingredients": "['500 gram yufka', '200 gram margarin', '2 su bardağı tahin', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Yufkaları tepsiye sererken aralarına eritilmiş margarin sürün.\nHer 3-4 yufkada bir tahin yayın.\nTüm yufkaları serdikten sonra dilimleyin.\nKalan margarini üzerine gezdirin.\n170 derece fırında 45 dakika pişirin.\nŞeker ve suyu kaynatıp şerbet yapın.\nLimon suyu ekleyin.\nSıcak baklavanın üzerine soğuk şerbeti dökün.",
    "Image_Name": "vegan-baklava",
    "Cleaned_Ingredients": "['yufka', 'margarin', 'tahin', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Kuruyemişsiz Baklava (Kuruyemiş Alerjisi)",
    "Ingredients": "['500 gram yufka', '250 gram tereyağı', '2 su bardağı tahin', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Yufkaları tepsiye sererken aralarına eritilmiş tereyağı sürün.\nHer 3-4 yufkada bir tahin yayın.\nTüm yufkaları serdikten sonra dilimleyin.\nKalan tereyağını üzerine gezdirin.\n170 derece fırında 45 dakika pişirin.\nŞeker ve suyu kaynatıp şerbet yapın.\nLimon suyu ekleyin.\nSıcak baklavanın üzerine soğuk şerbeti dökün.",
    "Image_Name": "kuruyemissiz-baklava",
    "Cleaned_Ingredients": "['yufka', 'tereyağı', 'tahin', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Glutensiz Mücver (Glutensiz & Vejetaryen)",
    "Ingredients": "['3 adet kabak', '2 adet yumurta', '1 su bardağı mısır unu', '1 demet dereotu', '100 gram beyaz peynir', '3 adet yeşil soğan', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı']",
    "Instructions": "Kabakları rendeleyin ve tuzlayıp suyunu sıkın.\nYumurta, mısır unu ve ufalanmış peyniri ekleyin.\nDereotu ve yeşil soğanı doğrayıp ilave edin.\nBaharatları ekleyip karıştırın.\nKaşıkla alıp kızgın yağda kızartın.\nKağıt havlu üzerinde süzün.",
    "Image_Name": "glutensiz-mucver",
    "Cleaned_Ingredients": "['kabak', 'yumurta', 'mısır unu', 'dereotu', 'beyaz peynir', 'yeşil soğan', 'tuz', 'karabiber', 'kızartma yağı']"
  },
  {
    "Title": "Yayla Çorbası",
    "Ingredients": "['2 su bardağı yoğurt', '1 adet yumurta', '1 yemek kaşığı un', '0.5 su bardağı pirinç', '6 su bardağı su', '2 yemek kaşığı tereyağı', '1 çay kaşığı nane', '1 çay kaşığı tuz']",
    "Instructions": "Pirinci yıkayıp suda haşlayın.\nYoğurt, yumurta ve unu çırpın.\nHaşlanmış pirincin suyundan azar azar ekleyerek ısıtın.\nYoğurtlu karışımı tencereye aktarın.\nSürekli karıştırarak kaynatın.\nTereyağında naneyi kızdırıp üzerine gezdirin.",
    "Image_Name": "yayla-corbasi",
    "Cleaned_Ingredients": "['yoğurt', 'yumurta', 'un', 'pirinç', 'su', 'tereyağı', 'nane', 'tuz']"
  },
  {
    "Title": "Tarhana Çorbası",
    "Ingredients": "['3 yemek kaşığı tarhana', '1 yemek kaşığı domates salçası', '1 yemek kaşığı tereyağı', '5 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Tarhanayı bir miktar suda ıslatın.\nTereyağını eritip salçayı kavurun.\nIslatılmış tarhanayı ekleyin.\nKalan suyu ilave edip karıştırın.\nKısık ateşte 20 dakika pişirin.\nPul biber serperek servis yapın.",
    "Image_Name": "tarhana-corbasi",
    "Cleaned_Ingredients": "['tarhana', 'domates salçası', 'tereyağı', 'su', 'tuz', 'pul biber']"
  },
  {
    "Title": "İşkembe Çorbası",
    "Ingredients": "['500 gram işkembe', '2 yemek kaşığı un', '2 yemek kaşığı tereyağı', '2 adet yumurta sarısı', '1 adet limon', '6 su bardağı su', '3 diş sarımsak', '2 yemek kaşığı sirke', '1 çay kaşığı tuz']",
    "Instructions": "İşkembeyi temizleyip haşlayın.\nİnce şeritler halinde doğrayın.\nTereyağında unu kavurun.\nHaşlama suyunu ekleyip kaynatın.\nDoğranmış işkembeyi ilave edin.\nYumurta sarısı ve limon suyunu çırpıp çorbaya ekleyin.\nSarımsaklı sirke ile servis yapın.",
    "Image_Name": "iskembe-corbasi",
    "Cleaned_Ingredients": "['işkembe', 'un', 'tereyağı', 'yumurta sarısı', 'limon', 'su', 'sarımsak', 'sirke', 'tuz']"
  },
  {
    "Title": "Toyga Çorbası",
    "Ingredients": "['1 su bardağı nohut', '0.5 su bardağı buğday', '2 su bardağı yoğurt', '1 adet yumurta', '1 yemek kaşığı un', '6 su bardağı su', '2 yemek kaşığı tereyağı', '1 çay kaşığı nane', '1 çay kaşığı tuz']",
    "Instructions": "Nohut ve buğdayı bir gece ıslatın.\nHaşlayın.\nYoğurt, yumurta ve unu çırpın.\nHaşlama suyundan ekleyerek ısıtın.\nTencereye aktarıp nohut ve buğdayla karıştırın.\nKaynatın.\nTereyağında nane kızdırıp üzerine gezdirin.",
    "Image_Name": "toyga-corbasi",
    "Cleaned_Ingredients": "['nohut', 'buğday', 'yoğurt', 'yumurta', 'un', 'su', 'tereyağı', 'nane', 'tuz']"
  },
  {
    "Title": "Lebeniye Çorbası",
    "Ingredients": "['200 gram kıyma', '0.5 su bardağı pirinç', '2 su bardağı yoğurt', '1 adet yumurta', '1 yemek kaşığı un', '1 adet soğan', '6 su bardağı su', '2 yemek kaşığı tereyağı', '1 çay kaşığı nane', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kıymayı baharatla yoğurup küçük köfteler yapın.\nPirinci yıkayıp suda haşlayın.\nYoğurt, yumurta ve unu çırpın.\nPirinçli suya yavaşça ekleyin.\nKöfteleri çorbaya bırakın.\nPişene kadar karıştırarak kaynatın.\nTereyağında nane kızdırıp gezdirin.",
    "Image_Name": "lebeniye-corbasi",
    "Cleaned_Ingredients": "['kıyma', 'pirinç', 'yoğurt', 'yumurta', 'un', 'soğan', 'su', 'tereyağı', 'nane', 'tuz', 'karabiber']"
  },
  {
    "Title": "Analı Kızlı Çorbası",
    "Ingredients": "['200 gram kıyma', '0.5 su bardağı pirinç', '1 su bardağı kırmızı mercimek', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '7 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı nane']",
    "Instructions": "Kıymayı yoğurup minik köfteler yapın.\nMercimeği yıkayıp suda haşlayın.\nPirinci ekleyin.\nAyrı tavada tereyağını eritip salçayı kavurun.\nSosu çorbaya ekleyin.\nKöfteleri çorbaya bırakıp pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "anali-kizli-corbasi",
    "Cleaned_Ingredients": "['kıyma', 'pirinç', 'kırmızı mercimek', 'soğan', 'domates salçası', 'tereyağı', 'su', 'tuz', 'pul biber', 'nane']"
  },
  {
    "Title": "Düğün Çorbası",
    "Ingredients": "['300 gram kuşbaşı kuzu eti', '1 adet yumurta sarısı', '1 adet limon', '2 yemek kaşığı un', '2 yemek kaşığı tereyağı', '7 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kuzu etini suda haşlayın.\nAyrı bir kapta tereyağı ve unu kavurun.\nEt suyunu ekleyip pişirin.\nYumurta sarısı ve limon suyunu çırpın.\nÇorbadan bir miktar ekleyerek ısıtın.\nTencereye aktarıp karıştırın.\nPul biberli tereyağı gezdirin.",
    "Image_Name": "dugun-corbasi",
    "Cleaned_Ingredients": "['kuzu eti', 'yumurta sarısı', 'limon', 'un', 'tereyağı', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Süleymaniye Çorbası",
    "Ingredients": "['300 gram kuşbaşı dana eti', '2 adet yumurta sarısı', '1 adet limon', '2 yemek kaşığı un', '2 yemek kaşığı tereyağı', '7 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Dana etini suda haşlayın ve doğrayın.\nTereyağı ve unu kavurun.\nEt suyunu yavaş yavaş ekleyin.\nYumurta sarıları ve limon suyunu çırpın.\nÇorbadan miktar alıp ısıtın.\nTencereye aktarıp eti ekleyin.\nKaynamadan servis yapın.",
    "Image_Name": "suleymaniye-corbasi",
    "Cleaned_Ingredients": "['dana eti', 'yumurta sarısı', 'limon', 'un', 'tereyağı', 'su', 'tuz', 'karabiber']"
  },
  {
    "Title": "Yüksük Çorbası",
    "Ingredients": "['2 su bardağı un', '1 adet yumurta', '1 su bardağı kırmızı mercimek', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '6 su bardağı su', '1 çay kaşığı nane', '1 çay kaşığı tuz']",
    "Instructions": "Un ve yumurtayla sert hamur yoğurun.\nMinik parçalar koparıp parmakla bastırarak şekil verin.\nMercimeği suda haşlayın.\nTereyağında soğan ve salçayı kavurun.\nÇorbaya ekleyin.\nHamur parçalarını çorbaya atın.\nPişene kadar kaynatın.\nNane serpin.",
    "Image_Name": "yuksuk-corbasi",
    "Cleaned_Ingredients": "['un', 'yumurta', 'kırmızı mercimek', 'soğan', 'domates salçası', 'tereyağı', 'su', 'nane', 'tuz']"
  },
  {
    "Title": "Beyran Çorbası",
    "Ingredients": "['500 gram kuzu but', '1 su bardağı pirinç', '4 diş sarımsak', '2 yemek kaşığı tereyağı', '8 su bardağı su', '1 çay kaşığı pul biber', '1 çay kaşığı karabiber', '1 çay kaşığı tuz']",
    "Instructions": "Kuzu etini gece boyunca kısık ateşte haşlayın.\nEti didikleyin.\nPirinci yıkayıp et suyunda haşlayın.\nSarımsakları ezin ve ekleyin.\nDidiklenmiş eti çorbaya koyun.\nTereyağında pul biberi kızdırıp gezdirin.",
    "Image_Name": "beyran-corbasi",
    "Cleaned_Ingredients": "['kuzu but', 'pirinç', 'sarımsak', 'tereyağı', 'su', 'pul biber', 'karabiber', 'tuz']"
  },
  {
    "Title": "Zeytinyağlı Enginar",
    "Ingredients": "['6 adet enginar', '2 adet havuç', '1 adet soğan', '1 adet limon', '1 su bardağı bezelye', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker', '1 demet dereotu']",
    "Instructions": "Enginarları temizleyip limonlu suda bekletin.\nSoğanı zeytinyağında kavurun.\nHavuçları doğrayıp ekleyin.\nEnginarları tencereye dizin.\nBezelyeleri ve dereotunu ilave edin.\nŞeker, tuz ve limon suyunu ekleyin.\nSu ilave edip kısık ateşte 40 dakika pişirin.\nSoğuk servis yapın.",
    "Image_Name": "zeytinyagli-enginar",
    "Cleaned_Ingredients": "['enginar', 'havuç', 'soğan', 'limon', 'bezelye', 'zeytinyağı', 'tuz', 'şeker', 'dereotu']"
  },
  {
    "Title": "Zeytinyağlı Kereviz",
    "Ingredients": "['4 adet kereviz', '2 adet havuç', '2 adet patates', '1 adet soğan', '1 adet limon', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Kerevizleri soyup limonlu suda bekletin.\nSoğanı zeytinyağında kavurun.\nHavuç ve patatesleri doğrayıp ekleyin.\nKerevizleri ilave edin.\nŞeker, tuz ve limon suyu ekleyin.\nSu ilave edip kısık ateşte 45 dakika pişirin.\nSoğuk servis yapın.",
    "Image_Name": "zeytinyagli-kereviz",
    "Cleaned_Ingredients": "['kereviz', 'havuç', 'patates', 'soğan', 'limon', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Zeytinyağlı Pırasa",
    "Ingredients": "['4 adet pırasa', '2 adet havuç', '1 su bardağı pirinç', '1 adet limon', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Pırasaları temizleyip halka halka doğrayın.\nZeytinyağında kavurun.\nHavuçları doğrayıp ekleyin.\nYıkanmış pirinci ilave edin.\nLimon suyu, tuz ve şekeri ekleyin.\nSu ilave edip kısık ateşte 30 dakika pişirin.\nSoğuk servis yapın.",
    "Image_Name": "zeytinyagli-pirasa",
    "Cleaned_Ingredients": "['pırasa', 'havuç', 'pirinç', 'limon', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Zeytinyağlı Taze Fasulye",
    "Ingredients": "['500 gram taze fasulye', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Fasulyeleri ayıklayıp doğrayın.\nSoğanı zeytinyağında kavurun.\nSarımsakları ekleyin.\nDoğranmış domatesleri ilave edin.\nFasulyeleri ekleyin.\nTuz ve şekeri ilave edin.\nSu ekleyip kısık ateşte 40 dakika pişirin.\nSoğuk veya ılık servis yapın.",
    "Image_Name": "zeytinyagli-taze-fasulye",
    "Cleaned_Ingredients": "['taze fasulye', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Zeytinyağlı Bakla",
    "Ingredients": "['1 kilo taze bakla', '2 adet soğan', '1 demet dereotu', '1 adet limon', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Baklaları ayıklayın.\nSoğanları zeytinyağında kavurun.\nBaklaları ekleyin.\nDereotunu doğrayıp ilave edin.\nTuz, şeker ve limon suyunu ekleyin.\nSu ilave edip kısık ateşte 35 dakika pişirin.\nSoğuk servis yapın.",
    "Image_Name": "zeytinyagli-bakla",
    "Cleaned_Ingredients": "['taze bakla', 'soğan', 'dereotu', 'limon', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Zeytinyağlı Börülce",
    "Ingredients": "['2 su bardağı kuru börülce', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '0.5 su bardağı zeytinyağı', '1 adet limon', '1 çay kaşığı tuz']",
    "Instructions": "Börülceyi bir gece ıslatın.\nHaşlayıp süzün.\nSoğanı zeytinyağında kavurun.\nSarımsakları ekleyin.\nDoğranmış domatesleri ilave edin.\nBörülceyi ekleyip az su ilave edin.\nKısık ateşte 25 dakika pişirin.\nLimon sıkıp soğuk servis yapın.",
    "Image_Name": "zeytinyagli-borulce",
    "Cleaned_Ingredients": "['börülce', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'limon', 'tuz']"
  },
  {
    "Title": "Haydari",
    "Ingredients": "['3 su bardağı süzme yoğurt', '100 gram beyaz peynir', '3 diş sarımsak', '1 demet dereotu', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı pul biber', '1 çay kaşığı nane', '1 çay kaşığı tuz']",
    "Instructions": "Süzme yoğurdu bir kaba alın.\nBeyaz peyniri ufalayıp ekleyin.\nSarımsakları ezin ve ilave edin.\nDereotunu doğrayıp karıştırın.\nNane ve tuzu ekleyin.\nÜzerine zeytinyağı ve pul biber gezdirip servis yapın.",
    "Image_Name": "haydari",
    "Cleaned_Ingredients": "['süzme yoğurt', 'beyaz peynir', 'sarımsak', 'dereotu', 'zeytinyağı', 'pul biber', 'nane', 'tuz']"
  },
  {
    "Title": "Acılı Ezme",
    "Ingredients": "['4 adet domates', '2 adet sivri biber', '1 adet soğan', '1 demet maydanoz', '2 yemek kaşığı biber salçası', '1 yemek kaşığı nar ekşisi', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı sumak']",
    "Instructions": "Domatesleri, biberleri ve soğanı çok ince doğrayın.\nMaydanozu ince kıyın.\nSalçayı ekleyin.\nNar ekşisi ve zeytinyağını ilave edin.\nBaharatları ekleyip iyice karıştırın.\nSoğuk servis yapın.",
    "Image_Name": "acili-ezme",
    "Cleaned_Ingredients": "['domates', 'sivri biber', 'soğan', 'maydanoz', 'biber salçası', 'nar ekşisi', 'zeytinyağı', 'tuz', 'pul biber', 'sumak']"
  },
  {
    "Title": "Patlıcan Salatası",
    "Ingredients": "['3 adet patlıcan', '2 adet domates', '1 adet sivri biber', '2 diş sarımsak', '1 adet limon', '3 yemek kaşığı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz']",
    "Instructions": "Patlıcanları közleyin.\nKabuklarını soyup ezin.\nDomates ve biberleri közleyip doğrayın.\nSarımsakları ezin.\nHepsini karıştırın.\nLimon suyu ve zeytinyağını ekleyin.\nMaydanoz serperek servis yapın.",
    "Image_Name": "patlican-salatasi",
    "Cleaned_Ingredients": "['patlıcan', 'domates', 'sivri biber', 'sarımsak', 'limon', 'zeytinyağı', 'maydanoz', 'tuz']"
  },
  {
    "Title": "Çoban Salatası",
    "Ingredients": "['3 adet domates', '2 adet salatalık', '2 adet sivri biber', '1 adet soğan', '1 demet maydanoz', '1 adet limon', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz']",
    "Instructions": "Domatesleri, salatalıkları ve biberleri küp küp doğrayın.\nSoğanı ince ince doğrayın.\nMaydanozu kıyın.\nHepsini bir kase de karıştırın.\nLimon suyu ve zeytinyağını ekleyin.\nTuzlayıp servis yapın.",
    "Image_Name": "coban-salatasi",
    "Cleaned_Ingredients": "['domates', 'salatalık', 'sivri biber', 'soğan', 'maydanoz', 'limon', 'zeytinyağı', 'tuz']"
  },
  {
    "Title": "Atom Salatası",
    "Ingredients": "['4 adet yeşil domates', '4 adet sivri biber', '2 adet soğan', '3 diş sarımsak', '2 yemek kaşığı biber salçası', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı nar ekşisi', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Yeşil domatesleri ve biberleri ince doğrayın.\nSoğanı ve sarımsakları doğrayın.\nHepsini karıştırın.\nSalça, nar ekşisi ve zeytinyağını ekleyin.\nMaydanozu kıyıp ilave edin.\nBaharatlarla tatlandırıp servis yapın.",
    "Image_Name": "atom-salatasi",
    "Cleaned_Ingredients": "['yeşil domates', 'sivri biber', 'soğan', 'sarımsak', 'biber salçası', 'zeytinyağı', 'nar ekşisi', 'maydanoz', 'tuz', 'pul biber']"
  },
  {
    "Title": "Gavurdağı Salatası",
    "Ingredients": "['3 adet domates', '2 adet salatalık', '1 adet soğan', '3 adet ceviz', '1 yemek kaşığı nar ekşisi', '2 yemek kaşığı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı sumak', '1 çay kaşığı tuz']",
    "Instructions": "Domatesleri ve salatalıkları küp doğrayın.\nSoğanı ince doğrayın.\nCevizleri kırın.\nMaydanozu kıyın.\nHepsini karıştırın.\nNar ekşisi, zeytinyağı ve sumak ekleyin.\nTuzlayıp servis yapın.",
    "Image_Name": "gavurdagi-salatasi",
    "Cleaned_Ingredients": "['domates', 'salatalık', 'soğan', 'ceviz', 'nar ekşisi', 'zeytinyağı', 'maydanoz', 'sumak', 'tuz']"
  },
  {
    "Title": "Humus",
    "Ingredients": "['2 su bardağı nohut', '3 yemek kaşığı tahin', '2 diş sarımsak', '1 adet limon', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber']",
    "Instructions": "Nohudu bir gece ıslatıp haşlayın.\nSüzüp blendere alın.\nTahin, sarımsak ve limon suyunu ekleyin.\nZeytinyağı ve tuzu ilave edin.\nPürüzsüz olana kadar çekin.\nTabağa yayıp kimyon ve pul biber serpin.\nZeytinyağı gezdirip servis yapın.",
    "Image_Name": "humus",
    "Cleaned_Ingredients": "['nohut', 'tahin', 'sarımsak', 'limon', 'zeytinyağı', 'tuz', 'kimyon', 'pul biber']"
  },
  {
    "Title": "Babaganuş",
    "Ingredients": "['3 adet patlıcan', '2 yemek kaşığı tahin', '2 diş sarımsak', '1 adet limon', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 demet maydanoz']",
    "Instructions": "Patlıcanları közleyin.\nKabuklarını soyup ezin.\nTahin ve sarımsağı ekleyin.\nLimon suyunu ilave edin.\nZeytinyağı ve tuzu ekleyip karıştırın.\nKimyon serpin.\nMaydanozla süsleyip servis yapın.",
    "Image_Name": "babaganus",
    "Cleaned_Ingredients": "['patlıcan', 'tahin', 'sarımsak', 'limon', 'zeytinyağı', 'tuz', 'kimyon', 'maydanoz']"
  },
  {
    "Title": "Muhammara",
    "Ingredients": "['4 adet kırmızı biber', '1 su bardağı ceviz', '3 yemek kaşığı nar ekşisi', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı biber salçası', '1 dilim bayat ekmek', '1 çay kaşığı kimyon', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Kırmızı biberleri közleyip kabuklarını soyun.\nEkmeği ıslatıp sıkın.\nHepsini blendere alın.\nCeviz, nar ekşisi ve salçayı ekleyin.\nZeytinyağını ilave edin.\nBaharatlarla birlikte çekin.\nTabağa alıp zeytinyağı gezdirin.",
    "Image_Name": "muhammara",
    "Cleaned_Ingredients": "['kırmızı biber', 'ceviz', 'nar ekşisi', 'zeytinyağı', 'biber salçası', 'bayat ekmek', 'kimyon', 'tuz', 'pul biber']"
  },
  {
    "Title": "Glutensiz Tarhana Çorbası (Glutensiz)",
    "Ingredients": "['3 yemek kaşığı glutensiz tarhana', '1 yemek kaşığı domates salçası', '1 yemek kaşığı tereyağı', '5 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Glutensiz tarhanayı bir miktar suda ıslatın.\nTereyağını eritip salçayı kavurun.\nIslatılmış tarhanayı ekleyin.\nKalan suyu ilave edip karıştırın.\nKısık ateşte 20 dakika pişirin.\nPul biber serperek servis yapın.",
    "Image_Name": "glutensiz-tarhana-corbasi",
    "Cleaned_Ingredients": "['glutensiz tarhana', 'domates salçası', 'tereyağı', 'su', 'tuz', 'pul biber']"
  },
  {
    "Title": "Vegan Yayla Çorbası (Vegan)",
    "Ingredients": "['2 su bardağı soya yoğurdu', '2 yemek kaşığı mısır nişastası', '0.5 su bardağı pirinç', '6 su bardağı su', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı nane', '1 çay kaşığı tuz']",
    "Instructions": "Pirinci yıkayıp suda haşlayın.\nSoya yoğurdunu nişasta ile çırpın.\nHaşlama suyundan azar azar ekleyerek ısıtın.\nYoğurtlu karışımı tencereye aktarın.\nSürekli karıştırarak kaynatın.\nZeytinyağında naneyi kızdırıp üzerine gezdirin.",
    "Image_Name": "vegan-yayla-corbasi",
    "Cleaned_Ingredients": "['soya yoğurdu', 'mısır nişastası', 'pirinç', 'su', 'zeytinyağı', 'nane', 'tuz']"
  },
  {
    "Title": "Vegan Düğün Çorbası (Vegan & Glutensiz)",
    "Ingredients": "['1 su bardağı kırmızı mercimek', '1 adet havuç', '1 adet patates', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '1 adet limon', '6 su bardağı su', '1 çay kaşığı zerdeçal', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Mercimeği yıkayın.\nSebzeleri doğrayıp suda haşlayın.\nSalçayı ekleyin.\nBlenderdan geçirin.\nLimon suyunu ilave edin.\nZeytinyağında pul biber ve zerdeçalı kızdırıp gezdirin.",
    "Image_Name": "vegan-dugun-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'havuç', 'patates', 'soğan', 'domates salçası', 'zeytinyağı', 'limon', 'su', 'zerdeçal', 'tuz', 'pul biber']"
  },
  {
    "Title": "Süt Ürünsüz Toyga Çorbası (Süt Ürünü Yok)",
    "Ingredients": "['1 su bardağı nohut', '0.5 su bardağı buğday', '2 su bardağı soya yoğurdu', '1 yemek kaşığı mısır nişastası', '6 su bardağı su', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı nane', '1 çay kaşığı tuz']",
    "Instructions": "Nohut ve buğdayı bir gece ıslatın.\nHaşlayın.\nSoya yoğurdunu nişasta ile çırpın.\nHaşlama suyundan ekleyerek ısıtın.\nTencereye aktarıp nohut ve buğdayla karıştırın.\nKaynatın.\nZeytinyağında nane kızdırıp gezdirin.",
    "Image_Name": "sut-urunsuz-toyga-corbasi",
    "Cleaned_Ingredients": "['nohut', 'buğday', 'soya yoğurdu', 'mısır nişastası', 'su', 'zeytinyağı', 'nane', 'tuz']"
  },
  {
    "Title": "Glutensiz Düğün Çorbası (Glutensiz)",
    "Ingredients": "['300 gram kuşbaşı kuzu eti', '1 adet yumurta sarısı', '1 adet limon', '2 yemek kaşığı mısır nişastası', '2 yemek kaşığı tereyağı', '7 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kuzu etini suda haşlayın.\nMısır nişastasını az suda eritin.\nEt suyuna ekleyip kaynatın.\nYumurta sarısı ve limon suyunu çırpın.\nÇorbadan bir miktar ekleyerek ısıtın.\nTencereye aktarıp karıştırın.\nTereyağında pul biber kızdırıp gezdirin.",
    "Image_Name": "glutensiz-dugun-corbasi",
    "Cleaned_Ingredients": "['kuzu eti', 'yumurta sarısı', 'limon', 'mısır nişastası', 'tereyağı', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Tarhana Çorbası (Vegan & Glutensiz)",
    "Ingredients": "['3 yemek kaşığı glutensiz tarhana', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '5 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Glutensiz tarhanayı suda ıslatın.\nZeytinyağında salçayı kavurun.\nIslatılmış tarhanayı ekleyin.\nSuyu ilave edip karıştırın.\nKısık ateşte 20 dakika pişirin.\nPul biber serpin.",
    "Image_Name": "vegan-tarhana-corbasi",
    "Cleaned_Ingredients": "['glutensiz tarhana', 'domates salçası', 'zeytinyağı', 'su', 'tuz', 'pul biber']"
  },
  {
    "Title": "Vegan Enginar (Vegan)",
    "Ingredients": "['6 adet enginar', '2 adet havuç', '1 adet soğan', '1 adet limon', '1 su bardağı bezelye', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker', '1 demet dereotu']",
    "Instructions": "Enginarları temizleyip limonlu suda bekletin.\nSoğanı zeytinyağında kavurun.\nHavuçları doğrayıp ekleyin.\nEnginarları tencereye dizin.\nBezelyeleri ve dereotunu ilave edin.\nŞeker, tuz ve limon suyunu ekleyin.\nSu ilave edip kısık ateşte 40 dakika pişirin.\nSoğuk servis yapın.",
    "Image_Name": "vegan-enginar",
    "Cleaned_Ingredients": "['enginar', 'havuç', 'soğan', 'limon', 'bezelye', 'zeytinyağı', 'tuz', 'şeker', 'dereotu']"
  },
  {
    "Title": "Vegan Kereviz (Vegan)",
    "Ingredients": "['4 adet kereviz', '2 adet havuç', '2 adet patates', '1 adet soğan', '1 adet limon', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Kerevizleri soyup limonlu suda bekletin.\nSoğanı zeytinyağında kavurun.\nHavuç ve patatesleri doğrayıp ekleyin.\nKerevizleri ilave edin.\nŞeker, tuz ve limon suyu ekleyin.\nSu ilave edip kısık ateşte 45 dakika pişirin.\nSoğuk servis yapın.",
    "Image_Name": "vegan-kereviz",
    "Cleaned_Ingredients": "['kereviz', 'havuç', 'patates', 'soğan', 'limon', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Vegan Zeytinyağlı Taze Fasulye (Vegan)",
    "Ingredients": "['500 gram taze fasulye', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Fasulyeleri ayıklayıp doğrayın.\nSoğanı zeytinyağında kavurun.\nSarımsakları ekleyin.\nDoğranmış domatesleri ilave edin.\nFasulyeleri ekleyin.\nTuz ve şekeri ilave edin.\nSu ekleyip kısık ateşte 40 dakika pişirin.",
    "Image_Name": "vegan-zeytinyagli-taze-fasulye",
    "Cleaned_Ingredients": "['taze fasulye', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Vegan Bakla (Vegan)",
    "Ingredients": "['1 kilo taze bakla', '2 adet soğan', '1 demet dereotu', '1 adet limon', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Baklaları ayıklayın.\nSoğanları zeytinyağında kavurun.\nBaklaları ekleyin.\nDereotunu doğrayıp ilave edin.\nTuz, şeker ve limon suyunu ekleyin.\nSu ilave edip kısık ateşte 35 dakika pişirin.\nSoğuk servis yapın.",
    "Image_Name": "vegan-bakla",
    "Cleaned_Ingredients": "['taze bakla', 'soğan', 'dereotu', 'limon', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Laktozsuz Haydari (Süt Ürünü Yok)",
    "Ingredients": "['3 su bardağı soya yoğurdu', '3 diş sarımsak', '1 demet dereotu', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı pul biber', '1 çay kaşığı nane', '1 çay kaşığı tuz']",
    "Instructions": "Soya yoğurdunu süzgeçte 2 saat süzün.\nBir kaba alın.\nSarımsakları ezin ve ekleyin.\nDereotunu doğrayıp karıştırın.\nNane ve tuzu ekleyin.\nÜzerine zeytinyağı ve pul biber gezdirip servis yapın.",
    "Image_Name": "laktozsuz-haydari",
    "Cleaned_Ingredients": "['soya yoğurdu', 'sarımsak', 'dereotu', 'zeytinyağı', 'pul biber', 'nane', 'tuz']"
  },
  {
    "Title": "Vegan Humus (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı nohut', '3 yemek kaşığı tahin', '2 diş sarımsak', '1 adet limon', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber']",
    "Instructions": "Nohudu bir gece ıslatıp haşlayın.\nSüzüp blendere alın.\nTahin, sarımsak ve limon suyunu ekleyin.\nZeytinyağı ve tuzu ilave edin.\nPürüzsüz olana kadar çekin.\nTabağa yayıp kimyon ve pul biber serpin.\nZeytinyağı gezdirin.",
    "Image_Name": "vegan-humus",
    "Cleaned_Ingredients": "['nohut', 'tahin', 'sarımsak', 'limon', 'zeytinyağı', 'tuz', 'kimyon', 'pul biber']"
  },
  {
    "Title": "Vegan Babaganuş (Vegan & Glutensiz)",
    "Ingredients": "['3 adet patlıcan', '2 yemek kaşığı tahin', '2 diş sarımsak', '1 adet limon', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 demet maydanoz']",
    "Instructions": "Patlıcanları közleyin.\nKabuklarını soyup ezin.\nTahin ve sarımsağı ekleyin.\nLimon suyunu ilave edin.\nZeytinyağı ve tuzu ekleyip karıştırın.\nKimyon serpin.\nMaydanozla süsleyip servis yapın.",
    "Image_Name": "vegan-babaganus",
    "Cleaned_Ingredients": "['patlıcan', 'tahin', 'sarımsak', 'limon', 'zeytinyağı', 'tuz', 'kimyon', 'maydanoz']"
  },
  {
    "Title": "Kuruyemişsiz Muhammara (Kuruyemiş Alerjisi)",
    "Ingredients": "['4 adet kırmızı biber', '3 yemek kaşığı tahin', '3 yemek kaşığı nar ekşisi', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı biber salçası', '1 dilim bayat ekmek', '1 çay kaşığı kimyon', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Kırmızı biberleri közleyip kabuklarını soyun.\nEkmeği ıslatıp sıkın.\nHepsini blendere alın.\nTahin, nar ekşisi ve salçayı ekleyin.\nZeytinyağını ilave edin.\nBaharatlarla birlikte çekin.\nTabağa alıp zeytinyağı gezdirin.",
    "Image_Name": "kuruyemissiz-muhammara",
    "Cleaned_Ingredients": "['kırmızı biber', 'tahin', 'nar ekşisi', 'zeytinyağı', 'biber salçası', 'bayat ekmek', 'kimyon', 'tuz', 'pul biber']"
  },
  {
    "Title": "Glutensiz Muhammara (Glutensiz)",
    "Ingredients": "['4 adet kırmızı biber', '1 su bardağı ceviz', '3 yemek kaşığı nar ekşisi', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı biber salçası', '1 çay kaşığı kimyon', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Kırmızı biberleri közleyip kabuklarını soyun.\nBlendere alın.\nCeviz, nar ekşisi ve salçayı ekleyin.\nZeytinyağını ilave edin.\nBaharatlarla birlikte çekin.\nTabağa alıp zeytinyağı gezdirin.",
    "Image_Name": "glutensiz-muhammara",
    "Cleaned_Ingredients": "['kırmızı biber', 'ceviz', 'nar ekşisi', 'zeytinyağı', 'biber salçası', 'kimyon', 'tuz', 'pul biber']"
  },
  {
    "Title": "Vejetaryen Yoğurtlu Semizotu (Vejetaryen)",
    "Ingredients": "['2 demet semizotu', '2 su bardağı yoğurt', '3 diş sarımsak', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Semizotlarını yıkayıp ayıklayın.\nKaynayan suda 2 dakika haşlayın.\nSüzüp soğutun.\nYoğurdu sarımsakla ezin.\nSemizotlarını tabağa yayın.\nÜzerine sarımsaklı yoğurt dökün.\nZeytinyağı ve pul biber gezdirin.",
    "Image_Name": "vejetaryen-yogurtlu-semizotu",
    "Cleaned_Ingredients": "['semizotu', 'yoğurt', 'sarımsak', 'zeytinyağı', 'tuz', 'pul biber']"
  },
  {
    "Title": "Vegan Semizotu Salatası (Vegan & Glutensiz)",
    "Ingredients": "['2 demet semizotu', '2 adet domates', '1 adet salatalık', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '1 adet limon', '1 çay kaşığı sumak', '1 çay kaşığı tuz']",
    "Instructions": "Semizotlarını yıkayıp ayıklayın.\nDomates ve salatalığı doğrayın.\nSoğanı ince doğrayın.\nHepsini karıştırın.\nLimon suyu ve zeytinyağını ekleyin.\nSumak ve tuz serpin.",
    "Image_Name": "vegan-semizotu-salatasi",
    "Cleaned_Ingredients": "['semizotu', 'domates', 'salatalık', 'soğan', 'zeytinyağı', 'limon', 'sumak', 'tuz']"
  },
  {
    "Title": "Süt Ürünsüz Patlıcan Salatası (Süt Ürünü Yok & Glutensiz)",
    "Ingredients": "['3 adet patlıcan', '2 adet domates', '1 adet sivri biber', '2 diş sarımsak', '1 adet limon', '3 yemek kaşığı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz']",
    "Instructions": "Patlıcanları közleyin.\nKabuklarını soyup ezin.\nDomates ve biberleri közleyip doğrayın.\nSarımsakları ezin.\nHepsini karıştırın.\nLimon suyu ve zeytinyağını ekleyin.\nMaydanoz serperek servis yapın.",
    "Image_Name": "sut-urunsuz-patlican-salatasi",
    "Cleaned_Ingredients": "['patlıcan', 'domates', 'sivri biber', 'sarımsak', 'limon', 'zeytinyağı', 'maydanoz', 'tuz']"
  },
  {
    "Title": "Kuruyemişsiz Gavurdağı Salatası (Kuruyemiş Alerjisi)",
    "Ingredients": "['3 adet domates', '2 adet salatalık', '1 adet soğan', '1 yemek kaşığı nar ekşisi', '2 yemek kaşığı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı sumak', '1 çay kaşığı tuz']",
    "Instructions": "Domatesleri ve salatalıkları küp doğrayın.\nSoğanı ince doğrayın.\nMaydanozu kıyın.\nHepsini karıştırın.\nNar ekşisi, zeytinyağı ve sumak ekleyin.\nTuzlayıp servis yapın.",
    "Image_Name": "kuruyemissiz-gavurdagi-salatasi",
    "Cleaned_Ingredients": "['domates', 'salatalık', 'soğan', 'nar ekşisi', 'zeytinyağı', 'maydanoz', 'sumak', 'tuz']"
  },
  {
    "Title": "Vegan Pırasa (Vegan)",
    "Ingredients": "['4 adet pırasa', '2 adet havuç', '1 su bardağı pirinç', '1 adet limon', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Pırasaları temizleyip halka halka doğrayın.\nZeytinyağında kavurun.\nHavuçları doğrayıp ekleyin.\nYıkanmış pirinci ilave edin.\nLimon suyu, tuz ve şekeri ekleyin.\nSu ilave edip kısık ateşte 30 dakika pişirin.\nSoğuk servis yapın.",
    "Image_Name": "vegan-pirasa",
    "Cleaned_Ingredients": "['pırasa', 'havuç', 'pirinç', 'limon', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Vejetaryen Kabak Çorbası (Vejetaryen)",
    "Ingredients": "['3 adet kabak', '1 adet soğan', '1 adet patates', '2 yemek kaşığı tereyağı', '4 su bardağı su', '1 su bardağı süt', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kabak, soğan ve patatesi doğrayın.\nTereyağında kavurun.\nSu ekleyip 25 dakika pişirin.\nBlenderdan geçirin.\nSütü ekleyip kaynatın.\nBaharatlarla tatlandırın.",
    "Image_Name": "vejetaryen-kabak-corbasi",
    "Cleaned_Ingredients": "['kabak', 'soğan', 'patates', 'tereyağı', 'su', 'süt', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Kabak Çorbası (Vegan & Glutensiz)",
    "Ingredients": "['3 adet kabak', '1 adet soğan', '1 adet patates', '2 yemek kaşığı zeytinyağı', '4 su bardağı su', '1 su bardağı yulaf sütü', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı zerdeçal']",
    "Instructions": "Kabak, soğan ve patatesi doğrayın.\nZeytinyağında kavurun.\nSu ekleyip 25 dakika pişirin.\nBlenderdan geçirin.\nYulaf sütünü ekleyip kaynatın.\nBaharatlarla tatlandırın.",
    "Image_Name": "vegan-kabak-corbasi",
    "Cleaned_Ingredients": "['kabak', 'soğan', 'patates', 'zeytinyağı', 'su', 'yulaf sütü', 'tuz', 'karabiber', 'zerdeçal']"
  },
  {
    "Title": "Vegan Börülce Salatası (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı kuru börülce', '2 adet domates', '1 adet soğan', '1 demet maydanoz', '3 yemek kaşığı zeytinyağı', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı sumak']",
    "Instructions": "Börülceyi bir gece ıslatıp haşlayın.\nSüzüp soğutun.\nDomates ve soğanı doğrayın.\nMaydanozu kıyın.\nHepsini karıştırın.\nLimon suyu ve zeytinyağını ekleyin.\nSumak ve tuz serpin.",
    "Image_Name": "vegan-borulce-salatasi",
    "Cleaned_Ingredients": "['börülce', 'domates', 'soğan', 'maydanoz', 'zeytinyağı', 'limon', 'tuz', 'sumak']"
  },
  {
    "Title": "Glutensiz Lebeniye Çorbası (Glutensiz)",
    "Ingredients": "['200 gram kıyma', '0.5 su bardağı pirinç', '2 su bardağı yoğurt', '1 adet yumurta', '1 yemek kaşığı mısır nişastası', '1 adet soğan', '6 su bardağı su', '2 yemek kaşığı tereyağı', '1 çay kaşığı nane', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kıymayı baharatla yoğurup küçük köfteler yapın.\nPirinci yıkayıp suda haşlayın.\nYoğurt, yumurta ve nişastayı çırpın.\nPirinçli suya yavaşça ekleyin.\nKöfteleri çorbaya bırakın.\nPişene kadar karıştırarak kaynatın.\nTereyağında nane kızdırıp gezdirin.",
    "Image_Name": "glutensiz-lebeniye-corbasi",
    "Cleaned_Ingredients": "['kıyma', 'pirinç', 'yoğurt', 'yumurta', 'mısır nişastası', 'soğan', 'su', 'tereyağı', 'nane', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Acılı Ezme (Vegan & Glutensiz)",
    "Ingredients": "['4 adet domates', '2 adet sivri biber', '1 adet soğan', '1 demet maydanoz', '2 yemek kaşığı biber salçası', '1 yemek kaşığı nar ekşisi', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı sumak']",
    "Instructions": "Domatesleri, biberleri ve soğanı çok ince doğrayın.\nMaydanozu ince kıyın.\nSalçayı ekleyin.\nNar ekşisi ve zeytinyağını ilave edin.\nBaharatları ekleyip iyice karıştırın.\nSoğuk servis yapın.",
    "Image_Name": "vegan-acili-ezme",
    "Cleaned_Ingredients": "['domates', 'sivri biber', 'soğan', 'maydanoz', 'biber salçası', 'nar ekşisi', 'zeytinyağı', 'tuz', 'pul biber', 'sumak']"
  },
  {
    "Title": "Kadınbudu Köfte",
    "Ingredients": "['300 gram kıyma', '0.5 su bardağı pirinç', '1 adet soğan', '2 adet yumurta', '0.5 su bardağı un', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı']",
    "Instructions": "Pirinci haşlayın.\nKıyma, soğan, maydanoz ve baharatlarla karıştırın.\n1 yumurtayı ekleyip yoğurun.\nOvaller şekil verin ve buzdolabında 30 dakika dinlendirin.\nKalan yumurtayı çırpın, köfteleri una bulayıp yumurtaya batırın.\nKızgın yağda kızartın.",
    "Image_Name": "kadinbudu-kofte",
    "Cleaned_Ingredients": "['kıyma', 'pirinç', 'soğan', 'yumurta', 'un', 'maydanoz', 'tuz', 'karabiber', 'kızartma yağı']"
  },
  {
    "Title": "İzmir Köfte",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '2 diş sarımsak', '3 adet patates', '3 adet domates', '2 adet sivri biber', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Kıyma, soğan, sarımsak ve baharatlarla köfte harcı hazırlayın.\nKöfteleri şekillendirin.\nZeytinyağında hafif kızartın.\nPatatesleri dilimleyip kızartın.\nTepsiye köfte ve patatesleri dizin.\nDomates, biber ve salçalı sosu hazırlayıp üzerine dökün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "izmir-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'sarımsak', 'patates', 'domates', 'sivri biber', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Tekirdağ Köfte",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '2 dilim bayat ekmek', '1 adet yumurta', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber']",
    "Instructions": "Bayat ekmeği ıslatıp sıkın.\nKıyma, soğan, ekmek ve yumurtayı karıştırın.\nBaharatları ekleyip iyice yoğurun.\nBuzdolabında 1 saat dinlendirin.\nYassı köfteler şekillendirin.\nIzgarada veya tavada pişirin.",
    "Image_Name": "tekirdag-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'bayat ekmek', 'yumurta', 'tuz', 'karabiber', 'kimyon', 'pul biber']"
  },
  {
    "Title": "Sulu Köfte",
    "Ingredients": "['400 gram kıyma', '0.5 su bardağı pirinç', '1 adet soğan', '1 adet yumurta', '2 adet patates', '2 adet havuç', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '6 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı nane']",
    "Instructions": "Kıyma, pirinç, soğan ve yumurtayla köfte harcı hazırlayın.\nBaharatları ekleyip yoğurun.\nKüçük köfteler şekillendirin.\nPatates ve havuçları doğrayın.\nSıcak suya salçaları ekleyip kaynatın.\nSebzeleri atın.\nKöfteleri tencereye bırakın.\nKısık ateşte 30 dakika pişirin.",
    "Image_Name": "sulu-kofte",
    "Cleaned_Ingredients": "['kıyma', 'pirinç', 'soğan', 'yumurta', 'patates', 'havuç', 'domates salçası', 'biber salçası', 'su', 'tuz', 'karabiber', 'nane']"
  },
  {
    "Title": "Dalyan Köfte",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '1 demet maydanoz', '2 dilim bayat ekmek', '1 adet yumurta', '1 yemek kaşığı biber salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Bayat ekmeği ıslatıp sıkın.\nKıyma, soğan, maydanoz, ekmek ve yumurtayı karıştırın.\nSalça ve baharatları ekleyip yoğurun.\n1 saat buzdolabında dinlendirin.\nOval köfteler yapıp ızgarada pişirin.",
    "Image_Name": "dalyan-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'maydanoz', 'bayat ekmek', 'yumurta', 'biber salçası', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Etli Kapuska",
    "Ingredients": "['500 gram beyaz lahana', '250 gram kıyma', '1 adet soğan', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Lahanayı ince ince doğrayın.\nKıymayı zeytinyağında kavurun.\nSoğanı ekleyip soteleyin.\nSalçaları ilave edin.\nLahanayı ekleyip karıştırın.\nKısık ateşte suyunu salıp çekene kadar 30 dakika pişirin.\nBaharatları ekleyin.",
    "Image_Name": "etli-kapuska",
    "Cleaned_Ingredients": "['beyaz lahana', 'kıyma', 'soğan', 'domates salçası', 'biber salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Etli Güveç",
    "Ingredients": "['500 gram kuşbaşı dana eti', '2 adet patlıcan', '2 adet biber', '2 adet domates', '2 adet patates', '1 adet soğan', '3 diş sarımsak', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Eti zeytinyağında kavurun.\nSoğan ve sarımsağı ekleyin.\nSalçayı ilave edin.\nSebzeleri büyük doğrayıp güvece dizin.\nEti üzerine koyun.\nBaharatları serpin.\nAz su ekleyin.\n180 derece fırında 1 saat pişirin.",
    "Image_Name": "etli-guvec",
    "Cleaned_Ingredients": "['dana eti', 'patlıcan', 'biber', 'domates', 'patates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Orman Kebabı",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '10 adet arpacık soğan', '3 adet patates', '2 adet havuç', '2 adet sivri biber', '2 adet domates', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kuzu etini tereyağında kavurun.\nArpacık soğanları ekleyin.\nSalçayı ilave edin.\nSebzeleri büyük doğrayıp tencereye alın.\nAz su ekleyin.\nKısık ateşte 1.5 saat pişirin.",
    "Image_Name": "orman-kebabi",
    "Cleaned_Ingredients": "['kuzu eti', 'arpacık soğan', 'patates', 'havuç', 'sivri biber', 'domates', 'tereyağı', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "İskender Kebap",
    "Ingredients": "['500 gram kuzu döner eti', '4 adet pide', '3 su bardağı yoğurt', '3 adet domates', '3 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Pideleri dilimleyip tabağa dizin.\nDöner etini pidelerin üzerine yerleştirin.\nDomatesleri rendeleyin, salçayla kaynatıp sos yapın.\nSosu etin üzerine gezdirin.\nYoğurdu yanına koyun.\nTereyağını kızdırıp pul biberle etin üzerine dökün.",
    "Image_Name": "iskender-kebap",
    "Cleaned_Ingredients": "['kuzu döner eti', 'pide', 'yoğurt', 'domates', 'tereyağı', 'domates salçası', 'tuz', 'pul biber']"
  },
  {
    "Title": "Urfa Kebap",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '2 diş sarımsak', '1 yemek kaşığı biber salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '4 adet lavaş']",
    "Instructions": "Kıymayı soğan ve sarımsakla yoğurun.\nSalça ve baharatları ekleyip karıştırın.\nBuzdolabında 2 saat dinlendirin.\nŞişlere sararak mangalda veya ızgarada pişirin.\nLavaş ve közlenmiş sebzelerle servis yapın.",
    "Image_Name": "urfa-kebap",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'sarımsak', 'biber salçası', 'tuz', 'karabiber', 'pul biber', 'lavaş']"
  },
  {
    "Title": "Beyti Kebap",
    "Ingredients": "['500 gram kıyma', '2 diş sarımsak', '1 yemek kaşığı biber salçası', '4 adet lavaş', '2 su bardağı yoğurt', '2 yemek kaşığı tereyağı', '2 adet domates', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kıyma, sarımsak, salça ve baharatlarla harç hazırlayın.\nŞişlere sarıp ızgarada pişirin.\nLavaşa sarın ve dilimleyin.\nDomates sosunu hazırlayın.\nTabağa dizin, sos dökün.\nYoğurdu yanına koyun.\nTereyağını pul biberle kızdırıp gezdirin.",
    "Image_Name": "beyti-kebap",
    "Cleaned_Ingredients": "['kıyma', 'sarımsak', 'biber salçası', 'lavaş', 'yoğurt', 'tereyağı', 'domates', 'domates salçası', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Tavuk Şiş",
    "Ingredients": "['600 gram tavuk göğsü', '2 adet sivri biber', '1 adet soğan', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı yoğurt', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 çay kaşığı pul biber']",
    "Instructions": "Tavukları kuşbaşı doğrayın.\nYoğurt, zeytinyağı ve baharatlarla marine edin.\nBuzdolabında 2 saat bekletin.\nBiber ve soğanla şişlere dizin.\nIzgarada veya fırında pişirin.",
    "Image_Name": "tavuk-sis",
    "Cleaned_Ingredients": "['tavuk göğsü', 'sivri biber', 'soğan', 'zeytinyağı', 'yoğurt', 'tuz', 'karabiber', 'kekik', 'pul biber']"
  },
  {
    "Title": "Kuzu Şiş",
    "Ingredients": "['600 gram kuzu but', '2 adet sivri biber', '1 adet soğan', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı yoğurt', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Kuzu etini kuşbaşı doğrayın.\nYoğurt, zeytinyağı ve baharatlarla marine edin.\nBuzdolabında en az 4 saat bekletin.\nBiber ve soğanla şişlere dizin.\nMangalda veya ızgarada pişirin.",
    "Image_Name": "kuzu-sis",
    "Cleaned_Ingredients": "['kuzu but', 'sivri biber', 'soğan', 'zeytinyağı', 'yoğurt', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Çoban Kavurma",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '2 adet sivri biber', '2 adet domates', '1 adet soğan', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kuzu etini tereyağında yüksek ateşte kavurun.\nSoğanı ekleyip soteleyin.\nBiberleri ilave edin.\nDoğranmış domatesleri ekleyin.\nBaharatları serpin.\nBirkaç dakika daha pişirip servis yapın.",
    "Image_Name": "coban-kavurma",
    "Cleaned_Ingredients": "['kuzu eti', 'sivri biber', 'domates', 'soğan', 'tereyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Saç Kavurma",
    "Ingredients": "['500 gram kuşbaşı dana eti', '3 adet sivri biber', '3 adet domates', '2 adet soğan', '3 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kekik']",
    "Instructions": "Sacı veya geniş tavayı kızdırın.\nTereyağını eritip eti kavurun.\nSoğan ve sarımsakları ekleyin.\nBiberleri ilave edin.\nDomatesleri ekleyip birkaç dakika pişirin.\nBaharatları serpin.\nSıcak servis yapın.",
    "Image_Name": "sac-kavurma",
    "Cleaned_Ingredients": "['dana eti', 'sivri biber', 'domates', 'soğan', 'sarımsak', 'tereyağı', 'tuz', 'karabiber', 'pul biber', 'kekik']"
  },
  {
    "Title": "Testi Kebabı",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '3 adet patates', '2 adet domates', '2 adet sivri biber', '1 adet soğan', '3 diş sarımsak', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Eti ve sebzeleri büyük doğrayın.\nTereyağı ve salçayla karıştırın.\nBaharatları ekleyin.\nGüveç testisine veya kapaklı güvece doldurun.\nAğzını hamurla kapatın.\n180 derece fırında 2 saat pişirin.\nServis esnasında testiyi kırın.",
    "Image_Name": "testi-kebabi",
    "Cleaned_Ingredients": "['kuzu eti', 'patates', 'domates', 'sivri biber', 'soğan', 'sarımsak', 'tereyağı', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "Kağıt Kebabı",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '2 adet domates', '2 adet sivri biber', '2 adet patates', '1 adet soğan', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Eti ve sebzeleri doğrayın.\nSalça, tereyağı ve baharatlarla karıştırın.\nYağlı kağıtlara porsiyon porsiyon paylaştırın.\nKağıtları kapatıp tepsiye dizin.\n180 derece fırında 1.5 saat pişirin.\nKağıtları açarak servis yapın.",
    "Image_Name": "kagit-kebabi",
    "Cleaned_Ingredients": "['kuzu eti', 'domates', 'sivri biber', 'patates', 'soğan', 'tereyağı', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "Fırında Kuzu Tandır",
    "Ingredients": "['1.5 kilo kuzu kol', '3 adet patates', '2 adet soğan', '4 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 su bardağı sıcak su']",
    "Instructions": "Kuzu kolunu tuzlayıp baharatlayın.\nPatates ve soğanları büyük doğrayın.\nTepsiye sebzeleri dizin, eti üzerine koyun.\nSarımsakları etrafına yerleştirin.\nTereyağı parçalarını üzerine koyun.\nSıcak su ekleyin.\nFolyo ile kapatıp 160 derece fırında 3 saat pişirin.\nFolyoyu açıp 20 dakika kızartın.",
    "Image_Name": "firinda-kuzu-tandir",
    "Cleaned_Ingredients": "['kuzu kol', 'patates', 'soğan', 'sarımsak', 'tereyağı', 'tuz', 'karabiber', 'kekik', 'su']"
  },
  {
    "Title": "Fırında Köfte Patates",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '1 adet yumurta', '2 dilim bayat ekmek', '4 adet patates', '2 adet domates', '2 adet sivri biber', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Bayat ekmeği ıslatıp sıkın.\nKıyma, soğan, ekmek, yumurta ve baharatlarla yoğurun.\nKöfteleri şekillendirin.\nPatatesleri dilimleyip tepsiye dizin.\nKöfteleri aralarına yerleştirin.\nDomates, biber ve salçalı sosu hazırlayıp dökün.\nZeytinyağı gezdirin.\n200 derece fırında 40 dakika pişirin.",
    "Image_Name": "firinda-kofte-patates",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'yumurta', 'bayat ekmek', 'patates', 'domates', 'sivri biber', 'domates salçası', 'zeytinyağı', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Fırında Sebzeli Et",
    "Ingredients": "['500 gram kuşbaşı dana eti', '2 adet patlıcan', '2 adet kabak', '2 adet biber', '3 adet domates', '1 adet soğan', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Eti kavurun.\nSebzeleri büyük doğrayın.\nTepsiye sebzeleri dizin, eti üzerine koyun.\nSarımsak ve baharatları serpin.\nZeytinyağı gezdirin.\nAz su ekleyin.\n180 derece fırında 1 saat pişirin.",
    "Image_Name": "firinda-sebzeli-et",
    "Cleaned_Ingredients": "['dana eti', 'patlıcan', 'kabak', 'biber', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Fırında Tavuk Baget",
    "Ingredients": "['8 adet tavuk baget', '4 adet patates', '2 adet soğan', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 çay kaşığı pul biber']",
    "Instructions": "Bagetleri zeytinyağı, salça ve baharatlarla marine edin.\n1 saat buzdolabında bekletin.\nPatatesleri dilimleyip tepsiye dizin.\nSoğanları halkalar halinde ekleyin.\nBagetleri üzerine yerleştirin.\n200 derece fırında 45 dakika pişirin.",
    "Image_Name": "firinda-tavuk-baget",
    "Cleaned_Ingredients": "['tavuk baget', 'patates', 'soğan', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kekik', 'pul biber']"
  },
  {
    "Title": "Tepsi Kebabı",
    "Ingredients": "['500 gram kıyma', '3 adet domates', '3 adet sivri biber', '2 adet soğan', '3 adet patates', '1 yemek kaşığı biber salçası', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kıymayı baharatlar ve salçayla yoğurun.\nYağlanmış tepsiye ince tabaka halinde yayın.\nÜzerine domates, biber ve soğan dilimlerini dizin.\nPatates dilimlerini ekleyin.\nZeytinyağı gezdirin.\n200 derece fırında 45 dakika pişirin.",
    "Image_Name": "tepsi-kebabi",
    "Cleaned_Ingredients": "['kıyma', 'domates', 'sivri biber', 'soğan', 'patates', 'biber salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Hasan Paşa Köfte",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '1 adet yumurta', '2 dilim bayat ekmek', '3 adet patates', '2 yemek kaşığı tereyağı', '1 su bardağı beşamel sos', '50 gram kaşar peyniri', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Bayat ekmeği ıslatıp sıkın.\nKıyma, soğan, ekmek, yumurta ve baharatlarla yoğurun.\nKöfteleri yassı şekillendirin.\nOrtalarına çukur açın.\nPatatesleri haşlayıp püre yapın.\nKöfteleri tepsiye dizin, ortalarına püre koyun.\nBeşamel sos ve kaşar serpin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "hasan-pasa-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'yumurta', 'bayat ekmek', 'patates', 'tereyağı', 'beşamel sos', 'kaşar peyniri', 'tuz', 'karabiber']"
  },
  {
    "Title": "Etli Biber Dolması",
    "Ingredients": "['10 adet dolmalık biber', '300 gram kıyma', '1 su bardağı pirinç', '2 adet soğan', '2 adet domates', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Biberlerin içini çıkarın.\nKıyma, pirinç, soğan, maydanoz ve baharatlarla iç harç hazırlayın.\nSalçayı ekleyip karıştırın.\nBiberleri doldurun.\nTencereye dizin.\nDomates dilimlerini kapaklarına koyun.\nSu ekleyip kısık ateşte 45 dakika pişirin.",
    "Image_Name": "etli-biber-dolmasi",
    "Cleaned_Ingredients": "['dolmalık biber', 'kıyma', 'pirinç', 'soğan', 'domates', 'domates salçası', 'zeytinyağı', 'maydanoz', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Fırında Kıymalı Patlıcan Kebap",
    "Ingredients": "['4 adet patlıcan', '300 gram kıyma', '2 adet domates', '2 adet sivri biber', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Patlıcanları alacalı soyup dilimleyin.\nKıyma, soğan ve baharatlarla harç hazırlayın.\nSalçayı ekleyin.\nTepsiye patlıcan ve kıyma katları halinde dizin.\nDomates ve biber dilimlerini üzerine koyun.\nZeytinyağı gezdirin.\n180 derece fırında 40 dakika pişirin.",
    "Image_Name": "firinda-kiymali-patlican-kebap",
    "Cleaned_Ingredients": "['patlıcan', 'kıyma', 'domates', 'sivri biber', 'soğan', 'domates salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Glutensiz Kadınbudu Köfte (Glutensiz)",
    "Ingredients": "['300 gram kıyma', '0.5 su bardağı pirinç', '1 adet soğan', '2 adet yumurta', '0.5 su bardağı mısır unu', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı']",
    "Instructions": "Pirinci haşlayın.\nKıyma, soğan, maydanoz ve baharatlarla karıştırın.\n1 yumurtayı ekleyip yoğurun.\nOval şekil verin ve buzdolabında dinlendirin.\nKalan yumurtayı çırpın, köfteleri mısır ununa bulayıp yumurtaya batırın.\nKızgın yağda kızartın.",
    "Image_Name": "glutensiz-kadinbudu-kofte",
    "Cleaned_Ingredients": "['kıyma', 'pirinç', 'soğan', 'yumurta', 'mısır unu', 'maydanoz', 'tuz', 'karabiber', 'kızartma yağı']"
  },
  {
    "Title": "Glutensiz İzmir Köfte (Glutensiz)",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '2 diş sarımsak', '3 adet patates', '3 adet domates', '2 adet sivri biber', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Kıyma, soğan, sarımsak ve baharatlarla köfte harcı hazırlayın.\nKöfteleri şekillendirin.\nZeytinyağında hafif kızartın.\nPatatesleri dilimleyip kızartın.\nTepsiye köfte ve patatesleri dizin.\nDomates, biber ve salçalı sosu hazırlayıp dökün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "glutensiz-izmir-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'sarımsak', 'patates', 'domates', 'sivri biber', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Glutensiz Tekirdağ Köfte (Glutensiz)",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '1 su bardağı haşlanmış patates', '1 adet yumurta', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber']",
    "Instructions": "Haşlanmış patatesi ezin.\nKıyma, soğan, patates ve yumurtayı karıştırın.\nBaharatları ekleyip iyice yoğurun.\nBuzdolabında 1 saat dinlendirin.\nYassı köfteler yapıp ızgarada pişirin.",
    "Image_Name": "glutensiz-tekirdag-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'patates', 'yumurta', 'tuz', 'karabiber', 'kimyon', 'pul biber']"
  },
  {
    "Title": "Glutensiz Fırında Köfte (Glutensiz)",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '1 adet yumurta', '3 yemek kaşığı mısır unu', '4 adet patates', '2 adet domates', '2 adet sivri biber', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Kıyma, soğan, mısır unu, yumurta ve baharatlarla yoğurun.\nKöfteleri şekillendirin.\nPatatesleri dilimleyip tepsiye dizin.\nKöfteleri aralarına yerleştirin.\nDomates, biber ve salçalı sosu hazırlayıp dökün.\n200 derece fırında 40 dakika pişirin.",
    "Image_Name": "glutensiz-firinda-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'yumurta', 'mısır unu', 'patates', 'domates', 'sivri biber', 'domates salçası', 'zeytinyağı', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Süt Ürünsüz İskender (Süt Ürünü Yok)",
    "Ingredients": "['500 gram kuzu döner eti', '4 adet pide', '3 adet domates', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Pideleri dilimleyip tabağa dizin.\nDöner etini pidelerin üzerine yerleştirin.\nDomatesleri rendeleyin, salçayla kaynatıp sos yapın.\nSosu etin üzerine gezdirin.\nZeytinyağını pul biberle kızdırıp üzerine dökün.",
    "Image_Name": "sut-urunsuz-iskender",
    "Cleaned_Ingredients": "['kuzu döner eti', 'pide', 'domates', 'zeytinyağı', 'domates salçası', 'tuz', 'pul biber']"
  },
  {
    "Title": "Süt Ürünsüz Beyti Kebap (Süt Ürünü Yok)",
    "Ingredients": "['500 gram kıyma', '2 diş sarımsak', '1 yemek kaşığı biber salçası', '4 adet lavaş', '2 adet domates', '1 yemek kaşığı domates salçası', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kıyma, sarımsak, salça ve baharatlarla harç hazırlayın.\nŞişlere sarıp ızgarada pişirin.\nLavaşa sarın ve dilimleyin.\nDomates sosunu hazırlayın.\nTabağa dizin, sosu gezdirin.\nZeytinyağını pul biberle kızdırıp dökün.",
    "Image_Name": "sut-urunsuz-beyti-kebap",
    "Cleaned_Ingredients": "['kıyma', 'sarımsak', 'biber salçası', 'lavaş', 'domates', 'domates salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Süt Ürünsüz Orman Kebabı (Süt Ürünü Yok)",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '10 adet arpacık soğan', '3 adet patates', '2 adet havuç', '2 adet sivri biber', '2 adet domates', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kuzu etini zeytinyağında kavurun.\nArpacık soğanları ekleyin.\nSalçayı ilave edin.\nSebzeleri büyük doğrayıp tencereye alın.\nAz su ekleyin.\nKısık ateşte 1.5 saat pişirin.",
    "Image_Name": "sut-urunsuz-orman-kebabi",
    "Cleaned_Ingredients": "['kuzu eti', 'arpacık soğan', 'patates', 'havuç', 'sivri biber', 'domates', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "Süt Ürünsüz Saç Kavurma (Süt Ürünü Yok)",
    "Ingredients": "['500 gram kuşbaşı dana eti', '3 adet sivri biber', '3 adet domates', '2 adet soğan', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kekik']",
    "Instructions": "Sacı veya geniş tavayı kızdırın.\nZeytinyağında eti kavurun.\nSoğan ve sarımsakları ekleyin.\nBiberleri ilave edin.\nDomatesleri ekleyip pişirin.\nBaharatları serpin.\nSıcak servis yapın.",
    "Image_Name": "sut-urunsuz-sac-kavurma",
    "Cleaned_Ingredients": "['dana eti', 'sivri biber', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber', 'kekik']"
  },
  {
    "Title": "Vegan Sulu Köfte (Vegan)",
    "Ingredients": "['200 gram soya kıyma', '0.5 su bardağı pirinç', '1 adet soğan', '2 adet patates', '2 adet havuç', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı zeytinyağı', '6 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı nane']",
    "Instructions": "Soya kıymayı sıcak suda ıslatıp süzün.\nPirinç ve soğanla karıştırıp küçük köfteler yapın.\nPatates ve havuçları doğrayın.\nSıcak suya salçaları ekleyip kaynatın.\nSebzeleri ekleyin.\nKöfteleri tencereye bırakın.\nKısık ateşte 25 dakika pişirin.",
    "Image_Name": "vegan-sulu-kofte",
    "Cleaned_Ingredients": "['soya kıyma', 'pirinç', 'soğan', 'patates', 'havuç', 'domates salçası', 'biber salçası', 'zeytinyağı', 'su', 'tuz', 'karabiber', 'nane']"
  },
  {
    "Title": "Vegan Etli Güveç (Vegan)",
    "Ingredients": "['200 gram soya kuşbaşı', '2 adet patlıcan', '2 adet biber', '2 adet domates', '2 adet patates', '1 adet soğan', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Soya kuşbaşını sıcak suda ıslatıp süzün.\nZeytinyağında kavurun.\nSoğan ve sarımsağı ekleyin.\nSalçayı ilave edin.\nSebzeleri büyük doğrayıp güvece dizin.\nSoyayı üzerine koyun.\nBaharatları serpin.\n180 derece fırında 50 dakika pişirin.",
    "Image_Name": "vegan-etli-guvec",
    "Cleaned_Ingredients": "['soya kuşbaşı', 'patlıcan', 'biber', 'domates', 'patates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Tepsi Kebabı (Vegan)",
    "Ingredients": "['200 gram soya kıyma', '3 adet domates', '3 adet sivri biber', '2 adet soğan', '3 adet patates', '1 yemek kaşığı biber salçası', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Soya kıymayı sıcak suda ıslatıp süzün.\nBaharatlar ve salçayla yoğurun.\nYağlanmış tepsiye ince tabaka halinde yayın.\nÜzerine domates, biber ve soğan dilimlerini dizin.\nPatates dilimlerini ekleyin.\nZeytinyağı gezdirin.\n200 derece fırında 40 dakika pişirin.",
    "Image_Name": "vegan-tepsi-kebabi",
    "Cleaned_Ingredients": "['soya kıyma', 'domates', 'sivri biber', 'soğan', 'patates', 'biber salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Biber Dolması (Vegan)",
    "Ingredients": "['10 adet dolmalık biber', '1 su bardağı pirinç', '2 adet soğan', '2 adet domates', '1 demet maydanoz', '1 demet dereotu', '1 yemek kaşığı domates salçası', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Biberlerin içini çıkarın.\nPirinci yıkayın.\nSoğanı zeytinyağında kavurun.\nPirinci ekleyip karıştırın.\nDoğranmış domates, maydanoz ve dereotunu ilave edin.\nSalça ve baharatları ekleyin.\nBiberleri doldurun.\nTencereye dizip su ekleyin.\nKısık ateşte 45 dakika pişirin.",
    "Image_Name": "vegan-biber-dolmasi",
    "Cleaned_Ingredients": "['dolmalık biber', 'pirinç', 'soğan', 'domates', 'maydanoz', 'dereotu', 'domates salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Fırında Sebzeli Kebap (Vegan & Glutensiz)",
    "Ingredients": "['2 adet patlıcan', '2 adet kabak', '3 adet patates', '2 adet biber', '3 adet domates', '1 adet soğan', '4 diş sarımsak', '4 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Sebzeleri büyük doğrayın.\nTepsiye dizin.\nSarımsak, salça, zeytinyağı ve baharatlarla sos hazırlayın.\nSosu sebzelerin üzerine gezdirin.\nAz su ekleyin.\n180 derece fırında 50 dakika pişirin.",
    "Image_Name": "vegan-firinda-sebzeli-kebap",
    "Cleaned_Ingredients": "['patlıcan', 'kabak', 'patates', 'biber', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Vegan Kapuska (Vegan)",
    "Ingredients": "['500 gram beyaz lahana', '200 gram soya kıyma', '1 adet soğan', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Lahanayı ince ince doğrayın.\nSoya kıymayı sıcak suda ıslatıp süzün.\nZeytinyağında soğanı kavurun.\nSoya kıymayı ekleyin.\nSalçaları ilave edin.\nLahanayı ekleyip karıştırın.\nKısık ateşte 30 dakika pişirin.\nBaharatları ekleyin.",
    "Image_Name": "vegan-kapuska",
    "Cleaned_Ingredients": "['beyaz lahana', 'soya kıyma', 'soğan', 'domates salçası', 'biber salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Kuruyemişsiz Hasan Paşa Köfte (Kuruyemiş Alerjisi)",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '1 adet yumurta', '2 dilim bayat ekmek', '3 adet patates', '2 yemek kaşığı tereyağı', '1 su bardağı beşamel sos', '50 gram kaşar peyniri', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Bayat ekmeği ıslatıp sıkın.\nKıyma, soğan, ekmek, yumurta ve baharatlarla yoğurun.\nKöfteleri yassı şekillendirin.\nOrtalarına çukur açın.\nPatatesleri haşlayıp püre yapın.\nKöfteleri tepsiye dizin, ortalarına püre koyun.\nBeşamel sos ve kaşar serpin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "kuruyemissiz-hasan-pasa-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'yumurta', 'bayat ekmek', 'patates', 'tereyağı', 'beşamel sos', 'kaşar peyniri', 'tuz', 'karabiber']"
  },
  {
    "Title": "Glutensiz Sulu Köfte (Glutensiz)",
    "Ingredients": "['400 gram kıyma', '0.5 su bardağı pirinç', '1 adet soğan', '1 adet yumurta', '2 adet patates', '2 adet havuç', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '6 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı nane']",
    "Instructions": "Kıyma, pirinç, soğan ve yumurtayla köfte harcı hazırlayın.\nBaharatları ekleyip yoğurun.\nKüçük köfteler şekillendirin.\nPatates ve havuçları doğrayın.\nSıcak suya salçaları ekleyip kaynatın.\nSebzeleri atın.\nKöfteleri tencereye bırakın.\nKısık ateşte 30 dakika pişirin.",
    "Image_Name": "glutensiz-sulu-kofte",
    "Cleaned_Ingredients": "['kıyma', 'pirinç', 'soğan', 'yumurta', 'patates', 'havuç', 'domates salçası', 'biber salçası', 'su', 'tuz', 'karabiber', 'nane']"
  },
  {
    "Title": "Glutensiz Etli Güveç (Glutensiz)",
    "Ingredients": "['500 gram kuşbaşı dana eti', '2 adet patlıcan', '2 adet biber', '2 adet domates', '2 adet patates', '1 adet soğan', '3 diş sarımsak', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Eti zeytinyağında kavurun.\nSoğan ve sarımsağı ekleyin.\nSalçayı ilave edin.\nSebzeleri büyük doğrayıp güvece dizin.\nEti üzerine koyun.\nBaharatları serpin.\nAz su ekleyin.\n180 derece fırında 1 saat pişirin.",
    "Image_Name": "glutensiz-etli-guvec",
    "Cleaned_Ingredients": "['dana eti', 'patlıcan', 'biber', 'domates', 'patates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Süt Ürünsüz Fırında Kuzu Tandır (Süt Ürünü Yok)",
    "Ingredients": "['1.5 kilo kuzu kol', '3 adet patates', '2 adet soğan', '4 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 su bardağı sıcak su']",
    "Instructions": "Kuzu kolunu tuzlayıp baharatlayın.\nPatates ve soğanları büyük doğrayın.\nTepsiye sebzeleri dizin, eti üzerine koyun.\nSarımsakları etrafına yerleştirin.\nZeytinyağını gezdirin.\nSıcak su ekleyin.\nFolyo ile kapatıp 160 derece fırında 3 saat pişirin.\nFolyoyu açıp 20 dakika kızartın.",
    "Image_Name": "sut-urunsuz-firinda-kuzu-tandir",
    "Cleaned_Ingredients": "['kuzu kol', 'patates', 'soğan', 'sarımsak', 'zeytinyağı', 'tuz', 'karabiber', 'kekik', 'su']"
  },
  {
    "Title": "Süt Ürünsüz Çoban Kavurma (Süt Ürünü Yok)",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '2 adet sivri biber', '2 adet domates', '1 adet soğan', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kuzu etini zeytinyağında yüksek ateşte kavurun.\nSoğanı ekleyip soteleyin.\nBiberleri ilave edin.\nDoğranmış domatesleri ekleyin.\nBaharatları serpin.\nBirkaç dakika daha pişirip servis yapın.",
    "Image_Name": "sut-urunsuz-coban-kavurma",
    "Cleaned_Ingredients": "['kuzu eti', 'sivri biber', 'domates', 'soğan', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Glutensiz Kağıt Kebabı (Glutensiz)",
    "Ingredients": "['500 gram kuşbaşı kuzu eti', '2 adet domates', '2 adet sivri biber', '2 adet patates', '1 adet soğan', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Eti ve sebzeleri doğrayın.\nSalça, tereyağı ve baharatlarla karıştırın.\nYağlı kağıtlara porsiyon porsiyon paylaştırın.\nKağıtları kapatıp tepsiye dizin.\n180 derece fırında 1.5 saat pişirin.\nKağıtları açarak servis yapın.",
    "Image_Name": "glutensiz-kagit-kebabi",
    "Cleaned_Ingredients": "['kuzu eti', 'domates', 'sivri biber', 'patates', 'soğan', 'tereyağı', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Kağıt Kebabı (Vegan & Glutensiz)",
    "Ingredients": "['200 gram soya kuşbaşı', '2 adet patlıcan', '2 adet kabak', '2 adet domates', '2 adet sivri biber', '2 adet patates', '1 adet soğan', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Soya kuşbaşını sıcak suda ıslatıp süzün.\nSebzeleri büyük doğrayın.\nSalça, zeytinyağı ve baharatlarla karıştırın.\nYağlı kağıtlara porsiyon paylaştırın.\nKağıtları kapatıp tepsiye dizin.\n180 derece fırında 1 saat pişirin.\nKağıtları açarak servis yapın.",
    "Image_Name": "vegan-kagit-kebabi",
    "Cleaned_Ingredients": "['soya kuşbaşı', 'patlıcan', 'kabak', 'domates', 'sivri biber', 'patates', 'soğan', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "Glutensiz Tepsi Kebabı (Glutensiz)",
    "Ingredients": "['500 gram kıyma', '3 adet domates', '3 adet sivri biber', '2 adet soğan', '3 adet patates', '1 yemek kaşığı biber salçası', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kıymayı baharatlar ve salçayla yoğurun.\nYağlanmış tepsiye ince tabaka halinde yayın.\nÜzerine domates, biber ve soğan dilimlerini dizin.\nPatates dilimlerini ekleyin.\nZeytinyağı gezdirin.\n200 derece fırında 45 dakika pişirin.",
    "Image_Name": "glutensiz-tepsi-kebabi",
    "Cleaned_Ingredients": "['kıyma', 'domates', 'sivri biber', 'soğan', 'patates', 'biber salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Süt Ürünsüz Tavuk Şiş (Süt Ürünü Yok)",
    "Ingredients": "['600 gram tavuk göğsü', '2 adet sivri biber', '1 adet soğan', '3 yemek kaşığı zeytinyağı', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 çay kaşığı pul biber']",
    "Instructions": "Tavukları kuşbaşı doğrayın.\nZeytinyağı, limon suyu ve baharatlarla marine edin.\nBuzdolabında 2 saat bekletin.\nBiber ve soğanla şişlere dizin.\nIzgarada veya fırında pişirin.",
    "Image_Name": "sut-urunsuz-tavuk-sis",
    "Cleaned_Ingredients": "['tavuk göğsü', 'sivri biber', 'soğan', 'zeytinyağı', 'limon', 'tuz', 'karabiber', 'kekik', 'pul biber']"
  },
  {
    "Title": "Vegan Şiş Kebap (Vegan & Glutensiz)",
    "Ingredients": "['200 gram soya kuşbaşı', '2 adet sivri biber', '1 adet soğan', '1 adet kabak', '8 adet mantar', '3 yemek kaşığı zeytinyağı', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 çay kaşığı pul biber']",
    "Instructions": "Soya kuşbaşını sıcak suda ıslatıp süzün.\nZeytinyağı, limon suyu ve baharatlarla marine edin.\n1 saat bekletin.\nSebzeleri büyük doğrayın.\nSoya ve sebzeleri şişlere dizin.\nIzgarada veya fırında pişirin.",
    "Image_Name": "vegan-sis-kebap",
    "Cleaned_Ingredients": "['soya kuşbaşı', 'sivri biber', 'soğan', 'kabak', 'mantar', 'zeytinyağı', 'limon', 'tuz', 'karabiber', 'kekik', 'pul biber']"
  },
  {
    "Title": "Glutensiz Dalyan Köfte (Glutensiz)",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '1 demet maydanoz', '1 su bardağı haşlanmış patates', '1 adet yumurta', '1 yemek kaşığı biber salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Haşlanmış patatesi ezin.\nKıyma, soğan, maydanoz, patates ve yumurtayı karıştırın.\nSalça ve baharatları ekleyip yoğurun.\n1 saat buzdolabında dinlendirin.\nOval köfteler yapıp ızgarada pişirin.",
    "Image_Name": "glutensiz-dalyan-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'maydanoz', 'patates', 'yumurta', 'biber salçası', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Tavuk Sote",
    "Ingredients": "['600 gram tavuk but', '2 adet sivri biber', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kekik']",
    "Instructions": "Tavukları kuşbaşı doğrayın.\nTereyağında kavurun.\nSoğan ve sarımsakları ekleyin.\nBiberleri ilave edin.\nSalça ve doğranmış domatesleri ekleyin.\nBaharatları serpin.\nKısık ateşte 25 dakika pişirin.",
    "Image_Name": "tavuk-sote",
    "Cleaned_Ingredients": "['tavuk but', 'sivri biber', 'domates', 'soğan', 'sarımsak', 'tereyağı', 'domates salçası', 'tuz', 'karabiber', 'pul biber', 'kekik']"
  },
  {
    "Title": "Fırında Tavuk Pirzola",
    "Ingredients": "['8 adet tavuk pirzola', '3 adet patates', '2 adet soğan', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 çay kaşığı pul biber']",
    "Instructions": "Tavuk pirzolalarını zeytinyağı, salça ve baharatlarla marine edin.\n1 saat buzdolabında bekletin.\nPatatesleri dilimleyip tepsiye dizin.\nSoğan halkalarını ekleyin.\nPirzolları üzerine yerleştirin.\n200 derece fırında 45 dakika pişirin.",
    "Image_Name": "firinda-tavuk-pirzola",
    "Cleaned_Ingredients": "['tavuk pirzola', 'patates', 'soğan', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kekik', 'pul biber']"
  },
  {
    "Title": "Tavuk Döner",
    "Ingredients": "['1 kilo tavuk but', '2 su bardağı yoğurt', '2 adet soğan', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber', '4 adet lavaş']",
    "Instructions": "Tavukları ince dilimleyin.\nYoğurt, zeytinyağı ve baharatlarla marine edin.\nBuzdolabında en az 4 saat bekletin.\nGeniş tavada veya ızgarada yüksek ateşte pişirin.\nLavaş ile servis yapın.",
    "Image_Name": "tavuk-doner",
    "Cleaned_Ingredients": "['tavuk but', 'yoğurt', 'soğan', 'zeytinyağı', 'tuz', 'karabiber', 'kimyon', 'pul biber', 'lavaş']"
  },
  {
    "Title": "Kremalı Tavuk Makarna",
    "Ingredients": "['400 gram tavuk göğsü', '300 gram penne makarna', '1 su bardağı krema', '1 adet soğan', '3 diş sarımsak', '200 gram mantar', '2 yemek kaşığı tereyağı', '50 gram kaşar peyniri', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Makarnayı haşlayın.\nTavukları kuşbaşı doğrayıp tereyağında kavurun.\nSoğan ve sarımsakları ekleyin.\nMantarları ilave edin.\nKremayı dökün.\nHaşlanmış makarnayı ekleyin.\nKaşar rendeleyin.\nBaharatlarla tatlandırın.",
    "Image_Name": "kremali-tavuk-makarna",
    "Cleaned_Ingredients": "['tavuk göğsü', 'penne makarna', 'krema', 'soğan', 'sarımsak', 'mantar', 'tereyağı', 'kaşar peyniri', 'tuz', 'karabiber']"
  },
  {
    "Title": "Tavuk Tandır",
    "Ingredients": "['1 adet bütün tavuk', '4 adet patates', '2 adet soğan', '2 adet domates', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 çay kaşığı pul biber']",
    "Instructions": "Tavuğu zeytinyağı, salça ve baharatlarla ovun.\nPatatesleri büyük doğrayıp tepsiye dizin.\nSoğan ve domates dilimlerini ekleyin.\nTavuğu sebzelerin üzerine koyun.\nFolyo ile kapatıp 180 derece fırında 1.5 saat pişirin.\nFolyoyu açıp 20 dakika kızartın.",
    "Image_Name": "tavuk-tandir",
    "Cleaned_Ingredients": "['bütün tavuk', 'patates', 'soğan', 'domates', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kekik', 'pul biber']"
  },
  {
    "Title": "Tavuk Pane",
    "Ingredients": "['4 adet tavuk göğsü', '1 su bardağı un', '2 adet yumurta', '1.5 su bardağı galeta unu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı']",
    "Instructions": "Tavuk göğüslerini ince dilimleyin veya döverek inceltin.\nTuzlayıp biberleyin.\nUna bulayın.\nÇırpılmış yumurtaya batırın.\nGaleta ununa bulayın.\nKızgın yağda altın rengi olana kadar kızartın.\nKağıt havlu üzerinde süzün.",
    "Image_Name": "tavuk-pane",
    "Cleaned_Ingredients": "['tavuk göğsü', 'un', 'yumurta', 'galeta unu', 'tuz', 'karabiber', 'kızartma yağı']"
  },
  {
    "Title": "Fırında Tavuk Kanat",
    "Ingredients": "['1 kilo tavuk kanat', '3 yemek kaşığı zeytinyağı', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 diş sarımsak', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kekik']",
    "Instructions": "Kanatları zeytinyağı, salçalar, sarımsak ve baharatlarla marine edin.\n2 saat buzdolabında bekletin.\nTepsiye dizin.\n200 derece fırında 40 dakika pişirin.\nAra sıra çevirin.",
    "Image_Name": "firinda-tavuk-kanat",
    "Cleaned_Ingredients": "['tavuk kanat', 'zeytinyağı', 'domates salçası', 'biber salçası', 'sarımsak', 'tuz', 'karabiber', 'pul biber', 'kekik']"
  },
  {
    "Title": "Hindi Fırın",
    "Ingredients": "['1.5 kilo hindi but', '3 adet patates', '2 adet soğan', '3 yemek kaşığı zeytinyağı', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 çay kaşığı biberiye']",
    "Instructions": "Hindi butu zeytinyağı ve baharatlarla ovun.\nPatatesleri büyük doğrayıp tepsiye dizin.\nSoğan halkalarını ekleyin.\nHindiyi üzerine koyun.\nTereyağı parçalarını serpin.\nFolyo ile kapatıp 170 derece fırında 2 saat pişirin.\nFolyoyu açıp 20 dakika kızartın.",
    "Image_Name": "hindi-firin",
    "Cleaned_Ingredients": "['hindi but', 'patates', 'soğan', 'zeytinyağı', 'tereyağı', 'tuz', 'karabiber', 'kekik', 'biberiye']"
  },
  {
    "Title": "Tavuk Güveç",
    "Ingredients": "['600 gram tavuk but', '2 adet patlıcan', '2 adet biber', '2 adet domates', '2 adet patates', '1 adet soğan', '3 diş sarımsak', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Tavukları kuşbaşı doğrayın.\nSebzeleri büyük doğrayın.\nGüvece tavuk ve sebzeleri katlar halinde dizin.\nSalça, zeytinyağı ve baharatlarla sos hazırlayıp dökün.\nAz su ekleyin.\n180 derece fırında 1 saat pişirin.",
    "Image_Name": "tavuk-guvec",
    "Cleaned_Ingredients": "['tavuk but', 'patlıcan', 'biber', 'domates', 'patates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Hindi Sote",
    "Ingredients": "['500 gram hindi göğsü', '2 adet sivri biber', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Hindiyi kuşbaşı doğrayın.\nZeytinyağında kavurun.\nSoğan ve sarımsakları ekleyin.\nBiberleri ilave edin.\nSalça ve domatesleri ekleyin.\nBaharatları serpin.\nKısık ateşte 25 dakika pişirin.",
    "Image_Name": "hindi-sote",
    "Cleaned_Ingredients": "['hindi göğsü', 'sivri biber', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Hamsi Tava",
    "Ingredients": "['500 gram hamsi', '1 su bardağı mısır unu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı', '1 adet limon']",
    "Instructions": "Hamsileri temizleyip yıkayın.\nMısır unu, tuz ve karabiberi karıştırın.\nHamsileri una bulayın.\nKızgın yağda çıtır çıtır kızartın.\nKağıt havlu üzerinde süzün.\nLimon ile servis yapın.",
    "Image_Name": "hamsi-tava",
    "Cleaned_Ingredients": "['hamsi', 'mısır unu', 'tuz', 'karabiber', 'kızartma yağı', 'limon']"
  },
  {
    "Title": "Fırında Somon",
    "Ingredients": "['4 adet somon fileto', '1 adet limon', '3 yemek kaşığı zeytinyağı', '3 diş sarımsak', '1 demet dereotu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Somon filetolarını tepsiye dizin.\nZeytinyağı, limon suyu, sarımsak ve baharatlarla marine edin.\nDereotunu doğrayıp üzerine serpin.\n200 derece fırında 20 dakika pişirin.",
    "Image_Name": "firinda-somon",
    "Cleaned_Ingredients": "['somon fileto', 'limon', 'zeytinyağı', 'sarımsak', 'dereotu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Karides Güveç",
    "Ingredients": "['500 gram karides', '4 adet domates', '2 adet sivri biber', '3 diş sarımsak', '100 gram kaşar peyniri', '3 yemek kaşığı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Karidesleri temizleyin.\nDomatesleri rendeleyin.\nZeytinyağında sarımsakları kavurun.\nBiberleri ekleyin.\nDomates sosunu ilave edip kaynatın.\nKaridesleri ekleyin.\nGüveç kaplarına paylaştırın.\nKaşar rendeleyip üzerine serpin.\n200 derece fırında 15 dakika pişirin.",
    "Image_Name": "karides-guvec",
    "Cleaned_Ingredients": "['karides', 'domates', 'sivri biber', 'sarımsak', 'kaşar peyniri', 'zeytinyağı', 'maydanoz', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Tereyağlı Karides",
    "Ingredients": "['500 gram karides', '3 yemek kaşığı tereyağı', '4 diş sarımsak', '1 adet limon', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Karidesleri temizleyin.\nTereyağını eritin.\nSarımsakları kavurun.\nKaridesleri ekleyip 3-4 dakika soteleyin.\nLimon suyunu sıkın.\nMaydanoz ve baharatları serpin.\nSıcak servis yapın.",
    "Image_Name": "tereyagli-karides",
    "Cleaned_Ingredients": "['karides', 'tereyağı', 'sarımsak', 'limon', 'maydanoz', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Kalamar Tava",
    "Ingredients": "['500 gram kalamar', '1 su bardağı un', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı', '1 adet limon']",
    "Instructions": "Kalamarları temizleyip halka halka kesin.\nUn, tuz ve karabiberi karıştırın.\nKalamarları una bulayın.\nKızgın yağda 2-3 dakika kızartın.\nKağıt havlu üzerinde süzün.\nLimon ile servis yapın.",
    "Image_Name": "kalamar-tava",
    "Cleaned_Ingredients": "['kalamar', 'un', 'tuz', 'karabiber', 'kızartma yağı', 'limon']"
  },
  {
    "Title": "Fırında Mezgit",
    "Ingredients": "['4 adet mezgit fileto', '2 adet domates', '1 adet limon', '3 yemek kaşığı zeytinyağı', '2 diş sarımsak', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Mezgit filetolarını tepsiye dizin.\nDomates dilimlerini üzerine koyun.\nZeytinyağı, limon suyu, sarımsak ve baharatlarla sos hazırlayıp dökün.\nMaydanoz serpin.\n200 derece fırında 20 dakika pişirin.",
    "Image_Name": "firinda-mezgit",
    "Cleaned_Ingredients": "['mezgit fileto', 'domates', 'limon', 'zeytinyağı', 'sarımsak', 'maydanoz', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Balık Buğulama",
    "Ingredients": "['4 adet levrek fileto', '2 adet patates', '2 adet havuç', '1 adet soğan', '1 adet limon', '3 yemek kaşığı zeytinyağı', '1 demet dereotu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Sebzeleri dilimleyin.\nTencereye zeytinyağını koyun.\nSebzeleri dizin.\nBalık filetolarını üzerine yerleştirin.\nLimon suyu ve baharatları ekleyin.\nDereotunu serpin.\nAz su ekleyip kapağını kapatın.\nKısık ateşte 25 dakika pişirin.",
    "Image_Name": "balik-bugulama",
    "Cleaned_Ingredients": "['levrek fileto', 'patates', 'havuç', 'soğan', 'limon', 'zeytinyağı', 'dereotu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Midye Dolma",
    "Ingredients": "['2 kilo midye', '2 su bardağı pirinç', '3 adet soğan', '1 yemek kaşığı domates salçası', '0.5 su bardağı zeytinyağı', '3 yemek kaşığı çam fıstığı', '3 yemek kaşığı kuş üzümü', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı tarçın', '1 adet limon']",
    "Instructions": "Midyeleri temizleyin.\nSoğanları zeytinyağında kavurun.\nPirinci ekleyin.\nSalça, çam fıstığı ve kuş üzümünü ilave edin.\nBaharatları ekleyin.\nAz su ekleyip yarı pişirin.\nMidyelerin içine doldurun.\nTencereye dizin, su ekleyip kısık ateşte 20 dakika pişirin.\nLimonla servis yapın.",
    "Image_Name": "midye-dolma",
    "Cleaned_Ingredients": "['midye', 'pirinç', 'soğan', 'domates salçası', 'zeytinyağı', 'çam fıstığı', 'kuş üzümü', 'tuz', 'karabiber', 'tarçın', 'limon']"
  },
  {
    "Title": "Midye Tava",
    "Ingredients": "['500 gram midye eti', '1 su bardağı un', '1 su bardağı bira', '1 adet yumurta', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı', '1 adet limon']",
    "Instructions": "Un, bira ve yumurtayla akıcı bir bulamaç hazırlayın.\nTuz ve karabiberi ekleyin.\nMidye etlerini bulamaca batırın.\nKızgın yağda kızartın.\nKağıt havlu üzerinde süzün.\nLimonla servis yapın.",
    "Image_Name": "midye-tava",
    "Cleaned_Ingredients": "['midye eti', 'un', 'bira', 'yumurta', 'tuz', 'karabiber', 'kızartma yağı', 'limon']"
  },
  {
    "Title": "Levrek Izgara",
    "Ingredients": "['2 adet bütün levrek', '3 yemek kaşığı zeytinyağı', '1 adet limon', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Levrekleri temizleyin.\nZeytinyağı, limon suyu, tuz ve karabiberle marine edin.\n30 dakika bekletin.\nIzgarada her iki tarafını pişirin.\nMaydanoz ve limonla servis yapın.",
    "Image_Name": "levrek-izgara",
    "Cleaned_Ingredients": "['levrek', 'zeytinyağı', 'limon', 'maydanoz', 'tuz', 'karabiber']"
  },
  {
    "Title": "Somon Izgara",
    "Ingredients": "['4 adet somon fileto', '3 yemek kaşığı zeytinyağı', '1 adet limon', '2 diş sarımsak', '1 demet dereotu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Somon filetolarını zeytinyağı, limon, sarımsak ve baharatlarla marine edin.\n30 dakika bekletin.\nIzgarada veya tavada her iki tarafını pişirin.\nDereotu serperek servis yapın.",
    "Image_Name": "somon-izgara",
    "Cleaned_Ingredients": "['somon fileto', 'zeytinyağı', 'limon', 'sarımsak', 'dereotu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Glutensiz Tavuk Pane (Glutensiz)",
    "Ingredients": "['4 adet tavuk göğsü', '1 su bardağı mısır unu', '2 adet yumurta', '1.5 su bardağı mısır gevreği kırığı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı']",
    "Instructions": "Tavuk göğüslerini ince dilimleyin.\nTuzlayıp biberleyin.\nMısır ununa bulayın.\nÇırpılmış yumurtaya batırın.\nMısır gevreği kırığına bulayın.\nKızgın yağda kızartın.\nKağıt havlu üzerinde süzün.",
    "Image_Name": "glutensiz-tavuk-pane",
    "Cleaned_Ingredients": "['tavuk göğsü', 'mısır unu', 'yumurta', 'mısır gevreği kırığı', 'tuz', 'karabiber', 'kızartma yağı']"
  },
  {
    "Title": "Glutensiz Kalamar Tava (Glutensiz)",
    "Ingredients": "['500 gram kalamar', '1 su bardağı mısır unu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı', '1 adet limon']",
    "Instructions": "Kalamarları temizleyip halka halka kesin.\nMısır unu, tuz ve karabiberi karıştırın.\nKalamarları mısır ununa bulayın.\nKızgın yağda 2-3 dakika kızartın.\nKağıt havlu üzerinde süzün.\nLimon ile servis yapın.",
    "Image_Name": "glutensiz-kalamar-tava",
    "Cleaned_Ingredients": "['kalamar', 'mısır unu', 'tuz', 'karabiber', 'kızartma yağı', 'limon']"
  },
  {
    "Title": "Glutensiz Tavuk Sote (Glutensiz)",
    "Ingredients": "['600 gram tavuk but', '2 adet sivri biber', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kekik']",
    "Instructions": "Tavukları kuşbaşı doğrayın.\nTereyağında kavurun.\nSoğan ve sarımsakları ekleyin.\nBiberleri ilave edin.\nSalça ve domatesleri ekleyin.\nBaharatları serpin.\nKısık ateşte 25 dakika pişirin.",
    "Image_Name": "glutensiz-tavuk-sote",
    "Cleaned_Ingredients": "['tavuk but', 'sivri biber', 'domates', 'soğan', 'sarımsak', 'tereyağı', 'domates salçası', 'tuz', 'karabiber', 'pul biber', 'kekik']"
  },
  {
    "Title": "Süt Ürünsüz Tavuk Sote (Süt Ürünü Yok)",
    "Ingredients": "['600 gram tavuk but', '2 adet sivri biber', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kekik']",
    "Instructions": "Tavukları kuşbaşı doğrayın.\nZeytinyağında kavurun.\nSoğan ve sarımsakları ekleyin.\nBiberleri ilave edin.\nSalça ve domatesleri ekleyin.\nBaharatları serpin.\nKısık ateşte 25 dakika pişirin.",
    "Image_Name": "sut-urunsuz-tavuk-sote",
    "Cleaned_Ingredients": "['tavuk but', 'sivri biber', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'pul biber', 'kekik']"
  },
  {
    "Title": "Süt Ürünsüz Kremalı Tavuk (Süt Ürünü Yok)",
    "Ingredients": "['400 gram tavuk göğsü', '1 su bardağı hindistan cevizi sütü', '1 adet soğan', '3 diş sarımsak', '200 gram mantar', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı zerdeçal']",
    "Instructions": "Tavukları kuşbaşı doğrayıp zeytinyağında kavurun.\nSoğan ve sarımsakları ekleyin.\nMantarları ilave edin.\nHindistan cevizi sütünü dökün.\nBaharatları serpin.\nKısık ateşte 15 dakika pişirin.",
    "Image_Name": "sut-urunsuz-kremali-tavuk",
    "Cleaned_Ingredients": "['tavuk göğsü', 'hindistan cevizi sütü', 'soğan', 'sarımsak', 'mantar', 'zeytinyağı', 'tuz', 'karabiber', 'zerdeçal']"
  },
  {
    "Title": "Süt Ürünsüz Karides Sote (Süt Ürünü Yok)",
    "Ingredients": "['500 gram karides', '4 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 adet limon', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Karidesleri temizleyin.\nZeytinyağında sarımsakları kavurun.\nKaridesleri ekleyip 3-4 dakika soteleyin.\nLimon suyunu sıkın.\nMaydanoz ve baharatları serpin.\nSıcak servis yapın.",
    "Image_Name": "sut-urunsuz-karides-sote",
    "Cleaned_Ingredients": "['karides', 'sarımsak', 'zeytinyağı', 'limon', 'maydanoz', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Süt Ürünsüz Karides Güveç (Süt Ürünü Yok)",
    "Ingredients": "['500 gram karides', '4 adet domates', '2 adet sivri biber', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Karidesleri temizleyin.\nDomatesleri rendeleyin.\nZeytinyağında sarımsakları kavurun.\nBiberleri ekleyin.\nDomates sosunu ilave edip kaynatın.\nKaridesleri ekleyin.\nGüveç kaplarına paylaştırın.\n200 derece fırında 15 dakika pişirin.\nMaydanoz serpin.",
    "Image_Name": "sut-urunsuz-karides-guvec",
    "Cleaned_Ingredients": "['karides', 'domates', 'sivri biber', 'sarımsak', 'zeytinyağı', 'maydanoz', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Süt Ürünsüz Hindi Fırın (Süt Ürünü Yok)",
    "Ingredients": "['1.5 kilo hindi but', '3 adet patates', '2 adet soğan', '4 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 çay kaşığı biberiye']",
    "Instructions": "Hindi butu zeytinyağı ve baharatlarla ovun.\nPatatesleri büyük doğrayıp tepsiye dizin.\nSoğan halkalarını ekleyin.\nHindiyi üzerine koyun.\nFolyo ile kapatıp 170 derece fırında 2 saat pişirin.\nFolyoyu açıp 20 dakika kızartın.",
    "Image_Name": "sut-urunsuz-hindi-firin",
    "Cleaned_Ingredients": "['hindi but', 'patates', 'soğan', 'zeytinyağı', 'tuz', 'karabiber', 'kekik', 'biberiye']"
  },
  {
    "Title": "Glutensiz Midye Tava (Glutensiz)",
    "Ingredients": "['500 gram midye eti', '1 su bardağı mısır unu', '1 adet yumurta', '0.5 su bardağı soda', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı', '1 adet limon']",
    "Instructions": "Mısır unu, yumurta ve sodayla akıcı bir bulamaç hazırlayın.\nTuz ve karabiberi ekleyin.\nMidye etlerini bulamaca batırın.\nKızgın yağda kızartın.\nKağıt havlu üzerinde süzün.\nLimonla servis yapın.",
    "Image_Name": "glutensiz-midye-tava",
    "Cleaned_Ingredients": "['midye eti', 'mısır unu', 'yumurta', 'soda', 'tuz', 'karabiber', 'kızartma yağı', 'limon']"
  },
  {
    "Title": "Glutensiz Fırında Somon (Glutensiz)",
    "Ingredients": "['4 adet somon fileto', '1 adet limon', '3 yemek kaşığı zeytinyağı', '3 diş sarımsak', '1 demet dereotu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Somon filetolarını tepsiye dizin.\nZeytinyağı, limon suyu, sarımsak ve baharatlarla marine edin.\nDereotunu doğrayıp üzerine serpin.\n200 derece fırında 20 dakika pişirin.",
    "Image_Name": "glutensiz-firinda-somon",
    "Cleaned_Ingredients": "['somon fileto', 'limon', 'zeytinyağı', 'sarımsak', 'dereotu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Süt Ürünsüz Tavuk Döner (Süt Ürünü Yok)",
    "Ingredients": "['1 kilo tavuk but', '2 adet soğan', '4 yemek kaşığı zeytinyağı', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber', '4 adet lavaş']",
    "Instructions": "Tavukları ince dilimleyin.\nZeytinyağı, limon suyu ve baharatlarla marine edin.\nBuzdolabında en az 4 saat bekletin.\nGeniş tavada yüksek ateşte pişirin.\nLavaş ile servis yapın.",
    "Image_Name": "sut-urunsuz-tavuk-doner",
    "Cleaned_Ingredients": "['tavuk but', 'soğan', 'zeytinyağı', 'limon', 'tuz', 'karabiber', 'kimyon', 'pul biber', 'lavaş']"
  },
  {
    "Title": "Kuruyemişsiz Midye Dolma (Kuruyemiş Alerjisi)",
    "Ingredients": "['2 kilo midye', '2 su bardağı pirinç', '3 adet soğan', '1 yemek kaşığı domates salçası', '0.5 su bardağı zeytinyağı', '3 yemek kaşığı kuş üzümü', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı tarçın', '1 adet limon']",
    "Instructions": "Midyeleri temizleyin.\nSoğanları zeytinyağında kavurun.\nPirinci ekleyin.\nSalça ve kuş üzümünü ilave edin.\nBaharatları ekleyin.\nAz su ekleyip yarı pişirin.\nMidyelerin içine doldurun.\nTencereye dizin, su ekleyip 20 dakika pişirin.\nLimonla servis yapın.",
    "Image_Name": "kuruyemissiz-midye-dolma",
    "Cleaned_Ingredients": "['midye', 'pirinç', 'soğan', 'domates salçası', 'zeytinyağı', 'kuş üzümü', 'tuz', 'karabiber', 'tarçın', 'limon']"
  },
  {
    "Title": "Vegan Soya Tavuk Sote (Vegan)",
    "Ingredients": "['200 gram soya kuşbaşı', '2 adet sivri biber', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kekik']",
    "Instructions": "Soya kuşbaşını sıcak suda 15 dakika ıslatıp süzün.\nZeytinyağında kavurun.\nSoğan ve sarımsakları ekleyin.\nBiberleri ilave edin.\nSalça ve domatesleri ekleyin.\nBaharatları serpin.\nKısık ateşte 20 dakika pişirin.",
    "Image_Name": "vegan-soya-tavuk-sote",
    "Cleaned_Ingredients": "['soya kuşbaşı', 'sivri biber', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'pul biber', 'kekik']"
  },
  {
    "Title": "Vegan Mantarlı Kalamar (Vegan)",
    "Ingredients": "['400 gram istiridye mantarı', '1 su bardağı mısır unu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı', '1 adet limon']",
    "Instructions": "İstiridye mantarlarını şeritler halinde doğrayın.\nMısır unu, tuz ve karabiberi karıştırın.\nMantar şeritlerini una bulayın.\nKızgın yağda 2-3 dakika kızartın.\nKağıt havlu üzerinde süzün.\nLimon ile servis yapın.",
    "Image_Name": "vegan-mantarli-kalamar",
    "Cleaned_Ingredients": "['istiridye mantarı', 'mısır unu', 'tuz', 'karabiber', 'kızartma yağı', 'limon']"
  },
  {
    "Title": "Vegan Tofu Balık (Vegan & Glutensiz)",
    "Ingredients": "['400 gram sert tofu', '1 su bardağı mısır unu', '1 yaprak nori yosunu', '3 yemek kaşığı zeytinyağı', '1 adet limon', '1 çay kaşığı zerdeçal', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Tofuyu dilimleyin.\nNori yosununu küçük parçalara bölün.\nTofu dilimlerini nori ile sarın.\nMısır unu ve baharatlarla kaplama yapın.\nZeytinyağında kızartın.\nLimonla servis yapın.",
    "Image_Name": "vegan-tofu-balik",
    "Cleaned_Ingredients": "['tofu', 'mısır unu', 'nori yosunu', 'zeytinyağı', 'limon', 'zerdeçal', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Soya Tavuk Güveç (Vegan)",
    "Ingredients": "['200 gram soya kuşbaşı', '2 adet patlıcan', '2 adet biber', '2 adet domates', '2 adet patates', '1 adet soğan', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Soya kuşbaşını sıcak suda ıslatıp süzün.\nSebzeleri büyük doğrayın.\nGüvece soya ve sebzeleri katlar halinde dizin.\nSalça, zeytinyağı ve baharatlarla sos hazırlayıp dökün.\nAz su ekleyin.\n180 derece fırında 50 dakika pişirin.",
    "Image_Name": "vegan-soya-tavuk-guvec",
    "Cleaned_Ingredients": "['soya kuşbaşı', 'patlıcan', 'biber', 'domates', 'patates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Vegan Mantar Döner (Vegan)",
    "Ingredients": "['500 gram istiridye mantarı', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı soya sosu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber', '4 adet lavaş', '2 adet domates', '1 adet soğan']",
    "Instructions": "İstiridye mantarlarını şeritler halinde yırtın.\nZeytinyağı, soya sosu ve baharatlarla marine edin.\n30 dakika bekletin.\nGeniş tavada yüksek ateşte kavurun.\nDomates ve soğan doğrayın.\nLavaşa sararak servis yapın.",
    "Image_Name": "vegan-mantar-doner",
    "Cleaned_Ingredients": "['istiridye mantarı', 'zeytinyağı', 'soya sosu', 'tuz', 'karabiber', 'kimyon', 'pul biber', 'lavaş', 'domates', 'soğan']"
  },
  {
    "Title": "Vegan Karides Güveç (Vegan)",
    "Ingredients": "['300 gram istiridye mantarı', '4 adet domates', '2 adet sivri biber', '3 diş sarımsak', '3 yemek kaşığı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "İstiridye mantarlarını küçük parçalara ayırın.\nDomatesleri rendeleyin.\nZeytinyağında sarımsakları kavurun.\nBiberleri ekleyin.\nDomates sosunu ilave edip kaynatın.\nMantarları ekleyin.\nGüveç kaplarına paylaştırın.\n200 derece fırında 15 dakika pişirin.\nMaydanoz serpin.",
    "Image_Name": "vegan-karides-guvec",
    "Cleaned_Ingredients": "['istiridye mantarı', 'domates', 'sivri biber', 'sarımsak', 'zeytinyağı', 'maydanoz', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vejetaryen Balık Buğulama (Vejetaryen)",
    "Ingredients": "['4 adet kereviz dilimi', '2 adet patates', '2 adet havuç', '1 adet soğan', '1 adet limon', '3 yemek kaşığı zeytinyağı', '1 demet dereotu', '1 yaprak nori yosunu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Sebzeleri dilimleyin.\nTencereye zeytinyağını koyun.\nSebzeleri dizin.\nKereviz dilimlerini üzerine yerleştirin.\nNori yosununu küçük parçalayıp ekleyin.\nLimon suyu ve baharatları ekleyin.\nDereotunu serpin.\nAz su ekleyip kapağını kapatın.\nKısık ateşte 30 dakika pişirin.",
    "Image_Name": "vejetaryen-balik-bugulama",
    "Cleaned_Ingredients": "['kereviz', 'patates', 'havuç', 'soğan', 'limon', 'zeytinyağı', 'dereotu', 'nori yosunu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Glutensiz Tavuk Güveç (Glutensiz)",
    "Ingredients": "['600 gram tavuk but', '2 adet patlıcan', '2 adet biber', '2 adet domates', '2 adet patates', '1 adet soğan', '3 diş sarımsak', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Tavukları kuşbaşı doğrayın.\nSebzeleri büyük doğrayın.\nGüvece tavuk ve sebzeleri katlar halinde dizin.\nSalça, zeytinyağı ve baharatlarla sos hazırlayıp dökün.\nAz su ekleyin.\n180 derece fırında 1 saat pişirin.",
    "Image_Name": "glutensiz-tavuk-guvec",
    "Cleaned_Ingredients": "['tavuk but', 'patlıcan', 'biber', 'domates', 'patates', 'soğan', 'sarımsak', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Glutensiz Hamsi Tava (Glutensiz)",
    "Ingredients": "['500 gram hamsi', '1 su bardağı mısır unu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'kızartma yağı', '1 adet limon']",
    "Instructions": "Hamsileri temizleyip yıkayın.\nMısır unu, tuz ve karabiberi karıştırın.\nHamsileri mısır ununa bulayın.\nKızgın yağda çıtır çıtır kızartın.\nKağıt havlu üzerinde süzün.\nLimon ile servis yapın.",
    "Image_Name": "glutensiz-hamsi-tava",
    "Cleaned_Ingredients": "['hamsi', 'mısır unu', 'tuz', 'karabiber', 'kızartma yağı', 'limon']"
  },
  {
    "Title": "Fırında Palamut",
    "Ingredients": "['4 adet palamut dilimi', '2 adet domates', '2 adet sivri biber', '1 adet soğan', '3 yemek kaşığı zeytinyağı', '1 adet limon', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Palamut dilimlerini tepsiye dizin.\nDomates, biber ve soğan dilimlerini üzerine koyun.\nZeytinyağı, limon suyu ve baharatlarla sos hazırlayıp dökün.\nMaydanoz serpin.\n200 derece fırında 25 dakika pişirin.",
    "Image_Name": "firinda-palamut",
    "Cleaned_Ingredients": "['palamut', 'domates', 'sivri biber', 'soğan', 'zeytinyağı', 'limon', 'maydanoz', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Balık Köfte",
    "Ingredients": "['400 gram balık fileto', '2 adet patates', '1 adet soğan', '1 adet yumurta', '1 demet maydanoz', '0.5 su bardağı galeta unu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', 'kızartma yağı']",
    "Instructions": "Balık filetoyu haşlayıp didikleyin.\nPatatesleri haşlayıp ezin.\nBalık, patates, soğan, maydanoz ve yumurtayı karıştırın.\nBaharatları ekleyip yoğurun.\nKöfteler şekillendirin.\nGaleta ununa bulayın.\nKızgın yağda kızartın.",
    "Image_Name": "balik-kofte",
    "Cleaned_Ingredients": "['balık fileto', 'patates', 'soğan', 'yumurta', 'maydanoz', 'galeta unu', 'tuz', 'karabiber', 'kimyon', 'kızartma yağı']"
  },
  {
    "Title": "Tavuklu Pilav",
    "Ingredients": "['400 gram tavuk göğsü', '2 su bardağı pirinç', '1 adet soğan', '2 yemek kaşığı tereyağı', '3.5 su bardağı tavuk suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Tavuğu haşlayıp didikleyin.\nSuyu ayırın.\nTereyağında soğanı kavurun.\nYıkanmış pirinci ekleyip kavurun.\nTavuk suyunu ilave edin.\nBaharatları ekleyin.\nKısık ateşte pilav pişirin.\nDidiklenmiş tavuğu ekleyip karıştırın.",
    "Image_Name": "tavuklu-pilav",
    "Cleaned_Ingredients": "['tavuk göğsü', 'pirinç', 'soğan', 'tereyağı', 'tavuk suyu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Fırında Tavuk Sarma",
    "Ingredients": "['4 adet tavuk göğsü', '100 gram kaşar peyniri', '8 dilim pastırma', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Tavuk göğüslerini döverek inceltin.\nTuzlayıp biberleyin.\nÜzerine kaşar peyniri koyun.\nRulo şeklinde sarın.\nPastırma ile dışını sarın.\nKürdan ile sabitleyin.\nTepsiye dizin, zeytinyağı gezdirin.\n200 derece fırında 30 dakika pişirin.",
    "Image_Name": "firinda-tavuk-sarma",
    "Cleaned_Ingredients": "['tavuk göğsü', 'kaşar peyniri', 'pastırma', 'zeytinyağı', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Glutensiz Balık Köfte (Glutensiz)",
    "Ingredients": "['400 gram balık fileto', '2 adet patates', '1 adet soğan', '1 adet yumurta', '1 demet maydanoz', '0.5 su bardağı mısır unu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', 'kızartma yağı']",
    "Instructions": "Balık filetoyu haşlayıp didikleyin.\nPatatesleri haşlayıp ezin.\nBalık, patates, soğan, maydanoz ve yumurtayı karıştırın.\nBaharatları ekleyip yoğurun.\nKöfteler şekillendirin.\nMısır ununa bulayın.\nKızgın yağda kızartın.",
    "Image_Name": "glutensiz-balik-kofte",
    "Cleaned_Ingredients": "['balık fileto', 'patates', 'soğan', 'yumurta', 'maydanoz', 'mısır unu', 'tuz', 'karabiber', 'kimyon', 'kızartma yağı']"
  },
  {
    "Title": "Vegan Mantarlı Tandır (Vegan)",
    "Ingredients": "['500 gram istiridye mantarı', '3 adet patates', '2 adet soğan', '2 adet domates', '4 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 yemek kaşığı soya sosu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "İstiridye mantarlarını büyük parçalar halinde yırtın.\nZeytinyağı, soya sosu ve baharatlarla marine edin.\nPatatesleri büyük doğrayıp tepsiye dizin.\nSoğan ve domates dilimlerini ekleyin.\nMantarları üzerine koyun.\nSalçalı sosu gezdirin.\nFolyo ile kapatıp 180 derece fırında 1 saat pişirin.\nFolyoyu açıp 15 dakika kızartın.",
    "Image_Name": "vegan-mantarli-tandir",
    "Cleaned_Ingredients": "['istiridye mantarı', 'patates', 'soğan', 'domates', 'zeytinyağı', 'domates salçası', 'soya sosu', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Süt Ürünsüz Tavuk Tandır (Süt Ürünü Yok)",
    "Ingredients": "['1 adet bütün tavuk', '4 adet patates', '2 adet soğan', '2 adet domates', '4 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik', '1 çay kaşığı pul biber']",
    "Instructions": "Tavuğu zeytinyağı, salça ve baharatlarla ovun.\nPatatesleri büyük doğrayıp tepsiye dizin.\nSoğan ve domates dilimlerini ekleyin.\nTavuğu sebzelerin üzerine koyun.\nFolyo ile kapatıp 180 derece fırında 1.5 saat pişirin.\nFolyoyu açıp 20 dakika kızartın.",
    "Image_Name": "sut-urunsuz-tavuk-tandir",
    "Cleaned_Ingredients": "['bütün tavuk', 'patates', 'soğan', 'domates', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'kekik', 'pul biber']"
  },
  {
    "Title": "Vegan Fırında Tofu Somon (Vegan & Glutensiz)",
    "Ingredients": "['400 gram sert tofu', '2 yaprak nori yosunu', '3 yemek kaşığı zeytinyağı', '1 adet limon', '2 diş sarımsak', '1 demet dereotu', '1 çay kaşığı zerdeçal', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Tofuyu dikdörtgen dilimler halinde kesin.\nNori yosununu şeritler halinde kesip tofu dilimlerinin altına yerleştirin.\nZeytinyağı, limon suyu, sarımsak, zerdeçal ve baharatlarla marine edin.\n30 dakika bekletin.\nTepsiye dizin.\nDereotu serpin.\n200 derece fırında 20 dakika pişirin.",
    "Image_Name": "vegan-firinda-tofu-somon",
    "Cleaned_Ingredients": "['tofu', 'nori yosunu', 'zeytinyağı', 'limon', 'sarımsak', 'dereotu', 'zerdeçal', 'tuz', 'karabiber']"
  },
  {
    "Title": "Peynirli Poğaça",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '0.5 su bardağı süt', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '200 gram beyaz peynir', '1 çay kaşığı tuz', '1 çay kaşığı şeker', 'çörek otu']",
    "Instructions": "Un, maya, süt, zeytinyağı, yumurta, tuz ve şekeri yoğurun.\n30 dakika mayalandırın.\nPeyniri ufalayın.\nHamurdan bezeler koparıp içine peynir koyun.\nYuvarlayıp tepsiye dizin.\nÜzerine yumurta sarısı sürün.\nÇörek otu serpin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "peynirli-pogaca",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'süt', 'zeytinyağı', 'yumurta', 'beyaz peynir', 'tuz', 'şeker', 'çörek otu']"
  },
  {
    "Title": "Patatesli Poğaça",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '0.5 su bardağı süt', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '3 adet patates', '1 adet soğan', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'çörek otu']",
    "Instructions": "Un, maya, süt, zeytinyağı, yumurta ve tuzla hamur yoğurun.\n30 dakika mayalandırın.\nPatatesleri haşlayıp ezin.\nSoğan ve maydanozu doğrayıp ekleyin.\nBaharatları ilave edin.\nHamurdan bezeler koparıp iç harç koyun.\nTepsiye dizin, yumurta sarısı ve çörek otu serpin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "patatesli-pogaca",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'süt', 'zeytinyağı', 'yumurta', 'patates', 'soğan', 'maydanoz', 'tuz', 'karabiber', 'çörek otu']"
  },
  {
    "Title": "Açma",
    "Ingredients": "['4 su bardağı un', '1 paket yaş maya', '1 su bardağı süt', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '2 yemek kaşığı toz şeker', '1 çay kaşığı tuz']",
    "Instructions": "Un, maya, süt, zeytinyağı, yumurta, şeker ve tuzla hamur yoğurun.\n1 saat mayalandırın.\nHamuru bezeler ayırın.\nHer bezeyi yuvarlayıp uzatın.\nRulo şeklinde sarın.\nTepsiye dizin.\nÜzerine yumurta sarısı sürün.\n180 derece fırında 20 dakika pişirin.",
    "Image_Name": "acma",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'süt', 'zeytinyağı', 'yumurta', 'toz şeker', 'tuz']"
  },
  {
    "Title": "Simit",
    "Ingredients": "['4 su bardağı un', '1 paket yaş maya', '1 su bardağı ılık su', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker', '3 yemek kaşığı pekmez', 'susam']",
    "Instructions": "Un, maya, su, zeytinyağı, tuz ve şekeri yoğurun.\n1 saat mayalandırın.\nHamuru bezeler ayırın.\nHer bezeyi uzun fitil yapın.\nHalka şeklinde birleştirin.\nPekmezli suya batırın.\nSusama bulayın.\n220 derece fırında 20 dakika pişirin.",
    "Image_Name": "simit",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'su', 'zeytinyağı', 'tuz', 'şeker', 'pekmez', 'susam']"
  },
  {
    "Title": "Su Böreği",
    "Ingredients": "['6 adet yufka', '300 gram beyaz peynir', '3 adet yumurta', '1 su bardağı süt', '0.5 su bardağı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz']",
    "Instructions": "Yumurta, süt ve zeytinyağını çırpın.\nBüyük bir tencerede su kaynatın.\nYufkaları teker teker kaynar suda 1 dakika haşlayın.\nTepsiye yufka sererek aralarına peynir ve maydanoz serpin.\nHer kata sıvı karışımdan gezdirin.\nÜst yufkaya bol sıvı sürün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "su-boregi",
    "Cleaned_Ingredients": "['yufka', 'beyaz peynir', 'yumurta', 'süt', 'zeytinyağı', 'maydanoz', 'tuz']"
  },
  {
    "Title": "Sigara Böreği",
    "Ingredients": "['10 adet yufka', '300 gram beyaz peynir', '1 demet maydanoz', '1 adet yumurta', '1 çay kaşığı tuz', 'kızartma yağı']",
    "Instructions": "Peyniri ufalayıp maydanozla karıştırın.\nYufkaları üçgen şeklinde kesin.\nGeniş kenarına peynirli harç koyun.\nSıkıca rulo şeklinde sarın.\nUçlarını yumurtayla yapıştırın.\nKızgın yağda altın rengi olana kadar kızartın.",
    "Image_Name": "sigara-boregi",
    "Cleaned_Ingredients": "['yufka', 'beyaz peynir', 'maydanoz', 'yumurta', 'tuz', 'kızartma yağı']"
  },
  {
    "Title": "Kol Böreği",
    "Ingredients": "['4 adet yufka', '250 gram kıyma', '2 adet soğan', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kıymayı soğanla kavurun.\nBaharatları ekleyin.\nYufkaları zeytinyağıyla yağlayın.\nÜzerine kıymalı harç serpin.\nRulo şeklinde sarın.\nHalkalar yaparak tepsiye dizin.\nÜzerine yumurta sarısı sürün.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "kol-boregi",
    "Cleaned_Ingredients": "['yufka', 'kıyma', 'soğan', 'zeytinyağı', 'yumurta', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Ispanaklı Börek",
    "Ingredients": "['6 adet yufka', '500 gram ıspanak', '200 gram beyaz peynir', '2 adet yumurta', '0.5 su bardağı süt', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz']",
    "Instructions": "Ispanakları yıkayıp doğrayın.\nPeyniri ufalayıp ıspanakla karıştırın.\nYumurta, süt ve zeytinyağını çırpın.\nYufkaları tepsiye sererken aralarına sıvı sürün.\nHer 2 yufkada bir ıspanaklı harç serpin.\nÜst yufkayı serdikten sonra kalan sıvıyı gezdirin.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "ispanakli-borek",
    "Cleaned_Ingredients": "['yufka', 'ıspanak', 'beyaz peynir', 'yumurta', 'süt', 'zeytinyağı', 'tuz']"
  },
  {
    "Title": "Kıymalı Pide",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '300 gram kıyma', '2 adet domates', '2 adet sivri biber', '1 adet soğan', '1 yemek kaşığı biber salçası', '1 çay kaşığı pul biber']",
    "Instructions": "Un, maya, tuz ve suyla hamur yoğurun.\n30 dakika mayalandırın.\nKıymayı soğan, domates, biber ve salçayla karıştırın.\nBaharatları ekleyin.\nHamuru kayık şeklinde açın.\nÜzerine harcı yayın.\nKenarlarını kıvırın.\n250 derece fırında 12 dakika pişirin.",
    "Image_Name": "kiymali-pide",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'tuz', 'su', 'kıyma', 'domates', 'sivri biber', 'soğan', 'biber salçası', 'pul biber']"
  },
  {
    "Title": "Kuşbaşılı Pide",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '300 gram kuşbaşı dana eti', '2 adet domates', '2 adet sivri biber', '1 adet soğan', '1 yemek kaşığı tereyağı', '1 çay kaşığı karabiber']",
    "Instructions": "Un, maya, tuz ve suyla hamur yoğurun.\n30 dakika mayalandırın.\nEti soğanla kavurun.\nDomates, biber ve baharatları ekleyin.\nHamuru kayık şeklinde açın.\nÜzerine harcı yayın.\n250 derece fırında 15 dakika pişirin.\nÜzerine tereyağı gezdirin.",
    "Image_Name": "kusbasili-pide",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'tuz', 'su', 'dana eti', 'domates', 'sivri biber', 'soğan', 'tereyağı', 'karabiber']"
  },
  {
    "Title": "Kaşarlı Pide",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '300 gram kaşar peyniri', '2 adet yumurta', '1 yemek kaşığı tereyağı']",
    "Instructions": "Un, maya, tuz ve suyla hamur yoğurun.\n30 dakika mayalandırın.\nKaşarı rendeleyin.\nHamuru kayık şeklinde açın.\nÜzerine kaşar serpin.\nKenarlarını kıvırın.\n250 derece fırında 12 dakika pişirin.\nFırından çıkınca yumurta kırıp tereyağı gezdirin.",
    "Image_Name": "kasarli-pide",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'tuz', 'su', 'kaşar peyniri', 'yumurta', 'tereyağı']"
  },
  {
    "Title": "Gözleme",
    "Ingredients": "['3 su bardağı un', '1 su bardağı ılık su', '1 çay kaşığı tuz', '200 gram beyaz peynir', '500 gram ıspanak', '2 yemek kaşığı tereyağı']",
    "Instructions": "Un, su ve tuzla yumuşak hamur yoğurun.\n20 dakika dinlendirin.\nIspanakları doğrayıp peynirle karıştırın.\nHamuru bezeler ayırıp ince açın.\nOrtasına harç koyup kapatın.\nSac veya tavada tereyağıyla iki tarafını pişirin.",
    "Image_Name": "gozleme",
    "Cleaned_Ingredients": "['un', 'su', 'tuz', 'beyaz peynir', 'ıspanak', 'tereyağı']"
  },
  {
    "Title": "Kıymalı Mantı",
    "Ingredients": "['3 su bardağı un', '2 adet yumurta', '1 çay kaşığı tuz', '0.5 su bardağı su', '250 gram kıyma', '1 adet soğan', '2 su bardağı yoğurt', '3 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber', '1 çay kaşığı nane']",
    "Instructions": "Un, yumurta, tuz ve suyla hamur yoğurun.\n30 dakika dinlendirin.\nKıyma ve soğanı karıştırarak iç harç yapın.\nHamuru ince açıp kareler kesin.\nHer karenin ortasına harç koyup kapatın.\nKaynayan tuzlu suda 15 dakika haşlayın.\nSarımsaklı yoğurdu hazırlayın.\nTereyağında pul biberi kızdırın.\nÜzerine yoğurt ve sos gezdirin.",
    "Image_Name": "kiymali-manti",
    "Cleaned_Ingredients": "['un', 'yumurta', 'tuz', 'su', 'kıyma', 'soğan', 'yoğurt', 'sarımsak', 'tereyağı', 'pul biber', 'nane']"
  },
  {
    "Title": "Tepsi Böreği",
    "Ingredients": "['5 adet yufka', '200 gram beyaz peynir', '200 gram kıyma', '1 adet soğan', '3 adet yumurta', '0.5 su bardağı süt', '0.5 su bardağı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kıymayı soğanla kavurup baharatlayın.\nPeyniri ufalayıp maydanozla karıştırın.\nYumurta, süt ve zeytinyağını çırpın.\nYufkaları tepsiye sererken sıvı gezdirin.\nAralarına kıymalı ve peynirli harçları katlar halinde serpin.\nÜst yufkaya bol sıvı sürün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "tepsi-boregi",
    "Cleaned_Ingredients": "['yufka', 'beyaz peynir', 'kıyma', 'soğan', 'yumurta', 'süt', 'zeytinyağı', 'maydanoz', 'tuz', 'karabiber']"
  },
  {
    "Title": "Glutensiz Peynirli Poğaça (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 paket yaş maya', '0.5 su bardağı yulaf sütü', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '200 gram beyaz peynir', '1 çay kaşığı tuz', '1 çay kaşığı şeker', 'çörek otu']",
    "Instructions": "Glutensiz un, mısır unu, maya, yulaf sütü, zeytinyağı, yumurta, tuz ve şekeri yoğurun.\n40 dakika mayalandırın.\nPeyniri ufalayın.\nHamurdan bezeler koparıp içine peynir koyun.\nTepsiye dizin, yumurta sarısı ve çörek otu serpin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "glutensiz-peynirli-pogaca",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'yaş maya', 'yulaf sütü', 'zeytinyağı', 'yumurta', 'beyaz peynir', 'tuz', 'şeker', 'çörek otu']"
  },
  {
    "Title": "Glutensiz Patatesli Poğaça (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 paket yaş maya', '0.5 su bardağı yulaf sütü', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '3 adet patates', '1 adet soğan', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', 'çörek otu']",
    "Instructions": "Glutensiz un, mısır unu, maya, yulaf sütü, zeytinyağı, yumurta ve tuzla hamur yoğurun.\n40 dakika mayalandırın.\nPatatesleri haşlayıp ezin.\nSoğan ve maydanoz ekleyip baharatlayın.\nBezeler koparıp iç harç koyun.\nTepsiye dizin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "glutensiz-patatesli-pogaca",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'yaş maya', 'yulaf sütü', 'zeytinyağı', 'yumurta', 'patates', 'soğan', 'maydanoz', 'tuz', 'karabiber', 'çörek otu']"
  },
  {
    "Title": "Vegan Patatesli Poğaça (Vegan)",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '0.5 su bardağı yulaf sütü', '0.5 su bardağı zeytinyağı', '3 adet patates', '1 adet soğan', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı şeker', 'çörek otu']",
    "Instructions": "Un, maya, yulaf sütü, zeytinyağı, tuz ve şekeri yoğurun.\n30 dakika mayalandırın.\nPatatesleri haşlayıp ezin.\nSoğan ve maydanozu doğrayıp ekleyin.\nBaharatları ilave edin.\nBezeler koparıp iç harç koyun.\nTepsiye dizin, çörek otu serpin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "vegan-patatesli-pogaca",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'yulaf sütü', 'zeytinyağı', 'patates', 'soğan', 'maydanoz', 'tuz', 'karabiber', 'şeker', 'çörek otu']"
  },
  {
    "Title": "Vegan Sigara Böreği (Vegan)",
    "Ingredients": "['10 adet yufka', '2 adet patates', '1 adet soğan', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', 'kızartma yağı']",
    "Instructions": "Patatesleri haşlayıp ezin.\nSoğan ve maydanozu doğrayıp karıştırın.\nBaharatları ekleyin.\nYufkaları üçgen kesin.\nGeniş kenarına patatesli harç koyun.\nRulo sarın.\nKızgın yağda kızartın.",
    "Image_Name": "vegan-sigara-boregi",
    "Cleaned_Ingredients": "['yufka', 'patates', 'soğan', 'maydanoz', 'tuz', 'karabiber', 'pul biber', 'kızartma yağı']"
  },
  {
    "Title": "Glutensiz Sigara Böreği (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '0.5 su bardağı mısır nişastası', '2 adet yumurta', '1 su bardağı su', '200 gram beyaz peynir', '1 demet maydanoz', '1 çay kaşığı tuz', 'kızartma yağı']",
    "Instructions": "Glutensiz un, nişasta, 1 yumurta, su ve tuzla akışkan hamur hazırlayın.\nTavada krep gibi ince pişirin.\nPeyniri ufalayıp maydanozla karıştırın.\nKreplerin üzerine peynirli harç koyun.\nSıkıca rulo sarın.\nKızgın yağda kızartın.",
    "Image_Name": "glutensiz-sigara-boregi",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır nişastası', 'yumurta', 'su', 'beyaz peynir', 'maydanoz', 'tuz', 'kızartma yağı']"
  },
  {
    "Title": "Glutensiz Ispanaklı Börek (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '0.5 su bardağı mısır nişastası', '3 adet yumurta', '1 su bardağı su', '500 gram ıspanak', '200 gram beyaz peynir', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz']",
    "Instructions": "Glutensiz un, nişasta, 1 yumurta, su ve tuzla akışkan hamur hazırlayın.\nTavada krep gibi ince pişirin.\nIspanakları doğrayıp peynirle karıştırın.\nTepsiye krepleri sererken aralarına harç serpin.\nKalan yumurta ve zeytinyağını çırpıp gezdirin.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "glutensiz-ispanakli-borek",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır nişastası', 'yumurta', 'su', 'ıspanak', 'beyaz peynir', 'zeytinyağı', 'tuz']"
  },
  {
    "Title": "Süt Ürünsüz Kol Böreği (Süt Ürünü Yok)",
    "Ingredients": "['4 adet yufka', '250 gram kıyma', '2 adet soğan', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kıymayı soğanla kavurup baharatlayın.\nYufkaları zeytinyağıyla yağlayın.\nÜzerine kıymalı harç serpin.\nRulo şeklinde sarın.\nHalkalar yaparak tepsiye dizin.\nÜzerine yumurta sarısı sürün.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "sut-urunsuz-kol-boregi",
    "Cleaned_Ingredients": "['yufka', 'kıyma', 'soğan', 'zeytinyağı', 'yumurta', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Kol Böreği (Vegan)",
    "Ingredients": "['4 adet yufka', '1 su bardağı kırmızı mercimek', '2 adet soğan', '1 yemek kaşığı domates salçası', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Mercimeği haşlayın.\nSoğanı zeytinyağında kavurun.\nHaşlanmış mercimeği ve salçayı ekleyin.\nBaharatları ilave edin.\nYufkaları zeytinyağıyla yağlayıp harç serpin.\nRulo sarıp halkalar yaparak tepsiye dizin.\nÜzerine zeytinyağı gezdirin.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "vegan-kol-boregi",
    "Cleaned_Ingredients": "['yufka', 'kırmızı mercimek', 'soğan', 'domates salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Glutensiz Kıymalı Pide (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '300 gram kıyma', '2 adet domates', '2 adet sivri biber', '1 adet soğan', '1 yemek kaşığı biber salçası', '1 çay kaşığı pul biber']",
    "Instructions": "Glutensiz un, mısır unu, maya, tuz ve suyla hamur yoğurun.\n40 dakika mayalandırın.\nKıymayı soğan, domates, biber ve salçayla karıştırın.\nHamuru kayık şeklinde açın.\nÜzerine harcı yayın.\n250 derece fırında 15 dakika pişirin.",
    "Image_Name": "glutensiz-kiymali-pide",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'yaş maya', 'tuz', 'su', 'kıyma', 'domates', 'sivri biber', 'soğan', 'biber salçası', 'pul biber']"
  },
  {
    "Title": "Vegan Lahmacun (Vegan)",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '200 gram soya kıyma', '2 adet soğan', '2 adet domates', '1 demet maydanoz', '2 adet sivri biber', '1 yemek kaşığı biber salçası', '1 çay kaşığı pul biber']",
    "Instructions": "Un, maya, tuz ve suyu yoğurun.\n30 dakika mayalandırın.\nSoya kıymayı sıcak suda ıslatıp süzün.\nSoğan, domates, biber ve maydanozla karıştırın.\nSalça ve baharatları ekleyin.\nHamuru ince açın.\nÜzerine harcı yayın.\n250 derece fırında 8-10 dakika pişirin.",
    "Image_Name": "vegan-lahmacun",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'tuz', 'su', 'soya kıyma', 'soğan', 'domates', 'maydanoz', 'sivri biber', 'biber salçası', 'pul biber']"
  },
  {
    "Title": "Glutensiz Vegan Lahmacun (Glutensiz & Vegan)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '200 gram soya kıyma', '2 adet soğan', '2 adet domates', '1 demet maydanoz', '2 adet sivri biber', '1 yemek kaşığı biber salçası', '1 çay kaşığı pul biber']",
    "Instructions": "Glutensiz un, mısır unu, maya, tuz ve suyla hamur yoğurun.\n40 dakika mayalandırın.\nSoya kıymayı sıcak suda ıslatıp süzün.\nSoğan, domates, biber ve maydanozla karıştırın.\nSalça ve baharatları ekleyin.\nHamuru ince açın, harcı yayın.\n250 derece fırında 10 dakika pişirin.",
    "Image_Name": "glutensiz-vegan-lahmacun",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'yaş maya', 'tuz', 'su', 'soya kıyma', 'soğan', 'domates', 'maydanoz', 'sivri biber', 'biber salçası', 'pul biber']"
  },
  {
    "Title": "Vegan Mantı (Vegan)",
    "Ingredients": "['3 su bardağı un', '1 çay kaşığı tuz', '0.5 su bardağı su', '3 adet patates', '1 adet soğan', '1 su bardağı soya yoğurdu', '2 diş sarımsak', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı pul biber', '1 çay kaşığı nane']",
    "Instructions": "Un, tuz ve suyla hamur yoğurun.\n30 dakika dinlendirin.\nPatatesleri haşlayıp ezin, soğanla karıştırın.\nHamuru ince açıp kareler kesin.\nOrtasına patatesli harç koyup kapatın.\nKaynayan suda 15 dakika haşlayın.\nSarımsaklı soya yoğurdunu hazırlayın.\nZeytinyağında pul biberi kızdırın.\nÜzerine yoğurt ve sos gezdirin.",
    "Image_Name": "vegan-manti",
    "Cleaned_Ingredients": "['un', 'tuz', 'su', 'patates', 'soğan', 'soya yoğurdu', 'sarımsak', 'zeytinyağı', 'pul biber', 'nane']"
  },
  {
    "Title": "Glutensiz Mantı (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '2 adet yumurta', '1 çay kaşığı tuz', '0.5 su bardağı su', '200 gram kıyma', '1 adet soğan', '2 su bardağı yoğurt', '3 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber', '1 çay kaşığı nane']",
    "Instructions": "Glutensiz un, mısır unu, yumurta, tuz ve suyla hamur yoğurun.\n30 dakika dinlendirin.\nKıyma ve soğanla iç harç hazırlayın.\nHamuru açıp kareler kesin.\nHarç koyup kapatın.\nKaynayan suda haşlayın.\nSarımsaklı yoğurt ve tereyağlı sos hazırlayın.\nÜzerine gezdirin.",
    "Image_Name": "glutensiz-manti",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'yumurta', 'tuz', 'su', 'kıyma', 'soğan', 'yoğurt', 'sarımsak', 'tereyağı', 'pul biber', 'nane']"
  },
  {
    "Title": "Glutensiz Simit (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 paket yaş maya', '1 su bardağı ılık su', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker', '3 yemek kaşığı pekmez', 'susam']",
    "Instructions": "Glutensiz un, mısır unu, maya, su, zeytinyağı, tuz ve şekeri yoğurun.\n1 saat mayalandırın.\nBezeler ayırıp fitil yapın.\nHalka birleştirin.\nPekmezli suya batırın.\nSusama bulayın.\n220 derece fırında 20 dakika pişirin.",
    "Image_Name": "glutensiz-simit",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'yaş maya', 'su', 'zeytinyağı', 'tuz', 'şeker', 'pekmez', 'susam']"
  },
  {
    "Title": "Vegan Simit (Vegan)",
    "Ingredients": "['4 su bardağı un', '1 paket yaş maya', '1 su bardağı ılık su', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker', '3 yemek kaşığı pekmez', 'susam']",
    "Instructions": "Un, maya, su, zeytinyağı, tuz ve şekeri yoğurun.\n1 saat mayalandırın.\nBezeler ayırıp fitil yapın.\nHalka birleştirin.\nPekmezli suya batırın.\nSusama bulayın.\n220 derece fırında 20 dakika pişirin.",
    "Image_Name": "vegan-simit",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'su', 'zeytinyağı', 'tuz', 'şeker', 'pekmez', 'susam']"
  },
  {
    "Title": "Süt Ürünsüz Gözleme (Süt Ürünü Yok)",
    "Ingredients": "['3 su bardağı un', '1 su bardağı ılık su', '1 çay kaşığı tuz', '3 adet patates', '1 adet soğan', '1 demet maydanoz', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı karabiber']",
    "Instructions": "Un, su ve tuzla hamur yoğurun.\n20 dakika dinlendirin.\nPatatesleri haşlayıp ezin.\nSoğan ve maydanoz ekleyip baharatlayın.\nHamuru ince açın.\nOrtasına harç koyup kapatın.\nTavada zeytinyağıyla iki tarafını pişirin.",
    "Image_Name": "sut-urunsuz-gozleme",
    "Cleaned_Ingredients": "['un', 'su', 'tuz', 'patates', 'soğan', 'maydanoz', 'zeytinyağı', 'karabiber']"
  },
  {
    "Title": "Vegan Gözleme (Vegan)",
    "Ingredients": "['3 su bardağı un', '1 su bardağı ılık su', '1 çay kaşığı tuz', '500 gram ıspanak', '1 adet soğan', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı pul biber']",
    "Instructions": "Un, su ve tuzla hamur yoğurun.\n20 dakika dinlendirin.\nIspanakları doğrayıp soğanla karıştırın.\nBaharatları ekleyin.\nHamuru ince açın.\nOrtasına harç koyup kapatın.\nTavada zeytinyağıyla iki tarafını pişirin.",
    "Image_Name": "vegan-gozleme",
    "Cleaned_Ingredients": "['un', 'su', 'tuz', 'ıspanak', 'soğan', 'zeytinyağı', 'pul biber']"
  },
  {
    "Title": "Glutensiz Gözleme (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 su bardağı ılık su', '1 çay kaşığı tuz', '200 gram beyaz peynir', '500 gram ıspanak', '2 yemek kaşığı zeytinyağı']",
    "Instructions": "Glutensiz un, mısır unu, su ve tuzla hamur yoğurun.\n20 dakika dinlendirin.\nIspanakları doğrayıp peynirle karıştırın.\nHamuru ince açın.\nOrtasına harç koyup kapatın.\nTavada zeytinyağıyla iki tarafını pişirin.",
    "Image_Name": "glutensiz-gozleme",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'su', 'tuz', 'beyaz peynir', 'ıspanak', 'zeytinyağı']"
  },
  {
    "Title": "Vegan Su Böreği (Vegan)",
    "Ingredients": "['6 adet yufka', '3 adet patates', '1 adet soğan', '1 demet maydanoz', '0.5 su bardağı yulaf sütü', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Yulaf sütü ve zeytinyağını karıştırın.\nBüyük tencerede su kaynatın.\nYufkaları teker teker 1 dakika haşlayın.\nPatatesleri haşlayıp ezin.\nSoğan ve maydanoz ekleyip baharatlayın.\nTepsiye yufka sererek aralarına patatesli harç serpin.\nHer kata sıvı gezdirin.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "vegan-su-boregi",
    "Cleaned_Ingredients": "['yufka', 'patates', 'soğan', 'maydanoz', 'yulaf sütü', 'zeytinyağı', 'tuz', 'karabiber']"
  },
  {
    "Title": "Glutensiz Su Böreği (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '0.5 su bardağı mısır nişastası', '3 adet yumurta', '1 su bardağı su', '200 gram beyaz peynir', '1 demet maydanoz', '0.5 su bardağı süt', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz']",
    "Instructions": "Glutensiz un, nişasta, 1 yumurta, su ve tuzla hamur hazırlayın.\nTavada krep gibi ince pişirin.\nPeyniri ufalayıp maydanozla karıştırın.\nKalan yumurta, süt ve zeytinyağını çırpın.\nTepsiye krepleri sererken aralarına peynirli harç ve sıvı gezdirin.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "glutensiz-su-boregi",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır nişastası', 'yumurta', 'su', 'beyaz peynir', 'maydanoz', 'süt', 'zeytinyağı', 'tuz']"
  },
  {
    "Title": "Glutensiz Açma (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 paket yaş maya', '0.5 su bardağı yulaf sütü', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '2 yemek kaşığı toz şeker', '1 çay kaşığı tuz']",
    "Instructions": "Glutensiz un, mısır unu, maya, yulaf sütü, zeytinyağı, yumurta, şeker ve tuzla hamur yoğurun.\n1 saat mayalandırın.\nBezeler ayırıp yuvarlayın ve uzatın.\nRulo sarın.\nTepsiye dizin, yumurta sarısı sürün.\n180 derece fırında 20 dakika pişirin.",
    "Image_Name": "glutensiz-acma",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'yaş maya', 'yulaf sütü', 'zeytinyağı', 'yumurta', 'toz şeker', 'tuz']"
  },
  {
    "Title": "Vegan Açma (Vegan)",
    "Ingredients": "['4 su bardağı un', '1 paket yaş maya', '0.5 su bardağı yulaf sütü', '0.5 su bardağı zeytinyağı', '2 yemek kaşığı toz şeker', '1 çay kaşığı tuz']",
    "Instructions": "Un, maya, yulaf sütü, zeytinyağı, şeker ve tuzla hamur yoğurun.\n1 saat mayalandırın.\nBezeler ayırıp yuvarlayın ve uzatın.\nRulo sarın.\nTepsiye dizin.\nÜzerine yulaf sütü sürün.\n180 derece fırında 20 dakika pişirin.",
    "Image_Name": "vegan-acma",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'yulaf sütü', 'zeytinyağı', 'toz şeker', 'tuz']"
  },
  {
    "Title": "Vegan Tepsi Böreği (Vegan)",
    "Ingredients": "['5 adet yufka', '1 su bardağı kırmızı mercimek', '2 adet soğan', '1 yemek kaşığı domates salçası', '0.5 su bardağı yulaf sütü', '0.5 su bardağı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Mercimeği haşlayın.\nSoğanı kavurup salça ve mercimek ekleyin.\nBaharatları ve maydanozu ilave edin.\nYulaf sütü ve zeytinyağını karıştırın.\nYufkaları tepsiye sererken sıvı gezdirin.\nAralarına mercimekli harç serpin.\nÜst yufkaya bol sıvı sürün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "vegan-tepsi-boregi",
    "Cleaned_Ingredients": "['yufka', 'kırmızı mercimek', 'soğan', 'domates salçası', 'yulaf sütü', 'zeytinyağı', 'maydanoz', 'tuz', 'karabiber']"
  },
  {
    "Title": "Süt Ürünsüz Kaşarlı Pide (Süt Ürünü Yok)",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '200 gram vegan kaşar', '2 adet yumurta', '2 yemek kaşığı zeytinyağı']",
    "Instructions": "Un, maya, tuz ve suyla hamur yoğurun.\n30 dakika mayalandırın.\nVegan kaşarı rendeleyin.\nHamuru kayık şeklinde açın.\nÜzerine vegan kaşar serpin.\nKenarlarını kıvırın.\n250 derece fırında 12 dakika pişirin.\nFırından çıkınca yumurta kırıp zeytinyağı gezdirin.",
    "Image_Name": "sut-urunsuz-kasarli-pide",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'tuz', 'su', 'vegan kaşar', 'yumurta', 'zeytinyağı']"
  },
  {
    "Title": "Glutensiz Kaşarlı Pide (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '300 gram kaşar peyniri', '2 adet yumurta', '1 yemek kaşığı tereyağı']",
    "Instructions": "Glutensiz un, mısır unu, maya, tuz ve suyla hamur yoğurun.\n40 dakika mayalandırın.\nKaşarı rendeleyin.\nHamuru kayık şeklinde açın.\nÜzerine kaşar serpin.\n250 derece fırında 12 dakika pişirin.\nYumurta kırıp tereyağı gezdirin.",
    "Image_Name": "glutensiz-kasarli-pide",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'yaş maya', 'tuz', 'su', 'kaşar peyniri', 'yumurta', 'tereyağı']"
  },
  {
    "Title": "Glutensiz Vegan Mantı (Glutensiz & Vegan)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 çay kaşığı tuz', '0.5 su bardağı su', '3 adet patates', '1 adet soğan', '1 su bardağı soya yoğurdu', '2 diş sarımsak', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı pul biber', '1 çay kaşığı nane']",
    "Instructions": "Glutensiz un, mısır unu, tuz ve suyla hamur yoğurun.\n30 dakika dinlendirin.\nPatatesleri haşlayıp ezin, soğanla karıştırın.\nHamuru açıp kareler kesin.\nOrtasına patatesli harç koyup kapatın.\nKaynayan suda haşlayın.\nSarımsaklı soya yoğurdunu hazırlayın.\nZeytinyağında pul biberi kızdırın.\nÜzerine yoğurt ve sos gezdirin.",
    "Image_Name": "glutensiz-vegan-manti",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'tuz', 'su', 'patates', 'soğan', 'soya yoğurdu', 'sarımsak', 'zeytinyağı', 'pul biber', 'nane']"
  },
  {
    "Title": "Glutensiz Kol Böreği (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '0.5 su bardağı mısır nişastası', '3 adet yumurta', '1 su bardağı su', '250 gram kıyma', '2 adet soğan', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Glutensiz un, nişasta, 1 yumurta, su ve tuzla hamur hazırlayın.\nTavada krep gibi ince pişirin.\nKıymayı soğanla kavurup baharatlayın.\nKreplere kıymalı harç koyup rulo sarın.\nHalkalar yaparak tepsiye dizin.\nKalan yumurta ve zeytinyağını çırpıp gezdirin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "glutensiz-kol-boregi",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır nişastası', 'yumurta', 'su', 'kıyma', 'soğan', 'zeytinyağı', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Pide (Vegan)",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '200 gram soya kıyma', '2 adet domates', '2 adet sivri biber', '1 adet soğan', '1 yemek kaşığı biber salçası', '1 çay kaşığı pul biber']",
    "Instructions": "Un, maya, tuz ve suyla hamur yoğurun.\n30 dakika mayalandırın.\nSoya kıymayı ıslatıp süzün.\nSoğan, domates, biber ve salçayla karıştırın.\nBaharatları ekleyin.\nHamuru kayık şeklinde açın.\nÜzerine harcı yayın.\n250 derece fırında 12 dakika pişirin.",
    "Image_Name": "vegan-pide",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'tuz', 'su', 'soya kıyma', 'domates', 'sivri biber', 'soğan', 'biber salçası', 'pul biber']"
  },
  {
    "Title": "Çiğ Börek",
    "Ingredients": "['3 su bardağı un', '1 adet yumurta', '0.5 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı sirke', '250 gram kıyma', '2 adet soğan', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', 'kızartma yağı']",
    "Instructions": "Un, yumurta, su, tuz ve sirkeyle hamur yoğurun.\n30 dakika dinlendirin.\nKıymayı çiğ soğanla karıştırıp baharatlayın.\nHamuru ince açın.\nYarım ay şeklinde kesin.\nBir yarısına kıymalı harç koyun.\nDiğer yarıyla kapatıp kenarlarını çatalla bastırın.\nKızgın yağda kızartın.",
    "Image_Name": "cig-borek",
    "Cleaned_Ingredients": "['un', 'yumurta', 'su', 'tuz', 'sirke', 'kıyma', 'soğan', 'karabiber', 'pul biber', 'kızartma yağı']"
  },
  {
    "Title": "Zeytinli Poğaça",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '0.5 su bardağı süt', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '1 su bardağı yeşil zeytin', '1 çay kaşığı tuz', '1 çay kaşığı şeker', 'çörek otu']",
    "Instructions": "Un, maya, süt, zeytinyağı, yumurta, tuz ve şekeri yoğurun.\n30 dakika mayalandırın.\nZeytinleri çekirdeklerini çıkarıp doğrayın.\nHamurdan bezeler koparıp içine zeytin koyun.\nTepsiye dizin.\nÜzerine yumurta sarısı ve çörek otu serpin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "zeytinli-pogaca",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'süt', 'zeytinyağı', 'yumurta', 'yeşil zeytin', 'tuz', 'şeker', 'çörek otu']"
  },
  {
    "Title": "Peynirli Gözleme",
    "Ingredients": "['3 su bardağı un', '1 su bardağı ılık su', '1 çay kaşığı tuz', '300 gram beyaz peynir', '1 demet maydanoz', '2 yemek kaşığı tereyağı']",
    "Instructions": "Un, su ve tuzla yumuşak hamur yoğurun.\n20 dakika dinlendirin.\nPeyniri ufalayıp maydanozla karıştırın.\nHamuru bezeler ayırıp ince açın.\nOrtasına peynirli harç koyup kapatın.\nSac veya tavada tereyağıyla iki tarafını pişirin.",
    "Image_Name": "peynirli-gozleme",
    "Cleaned_Ingredients": "['un', 'su', 'tuz', 'beyaz peynir', 'maydanoz', 'tereyağı']"
  },
  {
    "Title": "Karadeniz Pidesi",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '300 gram kıyma', '3 adet soğan', '2 yemek kaşığı tereyağı', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Un, maya, tuz ve suyla hamur yoğurun.\n30 dakika mayalandırın.\nKıymayı çiğ soğanla karıştırıp baharatlayın.\nHamuru yuvarlak açın.\nÜzerine harcı yayın.\nKenarlarını içe kıvırarak kapatın.\n250 derece fırında 15 dakika pişirin.\nÜzerine tereyağı gezdirin.",
    "Image_Name": "karadeniz-pidesi",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'tuz', 'su', 'kıyma', 'soğan', 'tereyağı', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Glutensiz Çiğ Börek (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '1 su bardağı mısır unu', '1 adet yumurta', '0.5 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı sirke', '250 gram kıyma', '2 adet soğan', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', 'kızartma yağı']",
    "Instructions": "Glutensiz un, mısır unu, yumurta, su, tuz ve sirkeyle hamur yoğurun.\n30 dakika dinlendirin.\nKıymayı çiğ soğanla karıştırıp baharatlayın.\nHamuru ince açın.\nYarım ay şeklinde kesin.\nKıymalı harç koyup kapatın.\nKenarlarını çatalla bastırın.\nKızgın yağda kızartın.",
    "Image_Name": "glutensiz-cig-borek",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır unu', 'yumurta', 'su', 'tuz', 'sirke', 'kıyma', 'soğan', 'karabiber', 'pul biber', 'kızartma yağı']"
  },
  {
    "Title": "Vegan Zeytinli Poğaça (Vegan)",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '0.5 su bardağı yulaf sütü', '0.5 su bardağı zeytinyağı', '1 su bardağı yeşil zeytin', '1 çay kaşığı tuz', '1 çay kaşığı şeker', 'çörek otu']",
    "Instructions": "Un, maya, yulaf sütü, zeytinyağı, tuz ve şekeri yoğurun.\n30 dakika mayalandırın.\nZeytinleri çekirdeklerini çıkarıp doğrayın.\nHamurdan bezeler koparıp içine zeytin koyun.\nTepsiye dizin, çörek otu serpin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "vegan-zeytinli-pogaca",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'yulaf sütü', 'zeytinyağı', 'yeşil zeytin', 'tuz', 'şeker', 'çörek otu']"
  },
  {
    "Title": "Glutensiz Tepsi Böreği (Glutensiz)",
    "Ingredients": "['2 su bardağı glutensiz un karışımı', '0.5 su bardağı mısır nişastası', '3 adet yumurta', '1 su bardağı su', '200 gram beyaz peynir', '200 gram kıyma', '1 adet soğan', '0.5 su bardağı süt', '0.5 su bardağı zeytinyağı', '1 demet maydanoz', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Glutensiz un, nişasta, 1 yumurta, su ve tuzla hamur hazırlayın.\nTavada krep gibi ince pişirin.\nKıymayı soğanla kavurup baharatlayın.\nPeyniri ufalayıp maydanozla karıştırın.\nKalan yumurta, süt ve zeytinyağını çırpın.\nTepsiye krepleri sererken aralarına harçlar ve sıvı gezdirin.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "glutensiz-tepsi-boregi",
    "Cleaned_Ingredients": "['glutensiz un karışımı', 'mısır nişastası', 'yumurta', 'su', 'beyaz peynir', 'kıyma', 'soğan', 'süt', 'zeytinyağı', 'maydanoz', 'tuz', 'karabiber']"
  },
  {
    "Title": "Süt Ürünsüz Peynirli Poğaça (Süt Ürünü Yok)",
    "Ingredients": "['3 su bardağı un', '1 paket yaş maya', '0.5 su bardağı yulaf sütü', '0.5 su bardağı zeytinyağı', '1 adet yumurta', '200 gram vegan beyaz peynir', '1 çay kaşığı tuz', '1 çay kaşığı şeker', 'çörek otu']",
    "Instructions": "Un, maya, yulaf sütü, zeytinyağı, yumurta, tuz ve şekeri yoğurun.\n30 dakika mayalandırın.\nVegan peyniri ufalayın.\nHamurdan bezeler koparıp içine peynir koyun.\nTepsiye dizin.\nÜzerine yumurta sarısı ve çörek otu serpin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "sut-urunsuz-peynirli-pogaca",
    "Cleaned_Ingredients": "['un', 'yaş maya', 'yulaf sütü', 'zeytinyağı', 'yumurta', 'vegan beyaz peynir', 'tuz', 'şeker', 'çörek otu']"
  },
  {
    "Title": "Tereyağlı Pirinç Pilavı",
    "Ingredients": "['2 su bardağı pirinç', '3 su bardağı tavuk suyu', '2 yemek kaşığı tereyağı', '0.5 su bardağı şehriye', '1 çay kaşığı tuz']",
    "Instructions": "Pirinci yıkayıp süzün.\nTereyağında şehriyeyi kavurun.\nPirinci ekleyip kavurun.\nTavuk suyunu ve tuzu ilave edin.\nKaynayınca kısık ateşe alın.\n15 dakika pişirip ocaktan alın.\n10 dakika demlendirin.",
    "Image_Name": "tereyagli-pirinc-pilavi",
    "Cleaned_Ingredients": "['pirinç', 'tavuk suyu', 'tereyağı', 'şehriye', 'tuz']"
  },
  {
    "Title": "Bulgur Pilavı",
    "Ingredients": "['2 su bardağı bulgur', '1 adet soğan', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı tereyağı', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Soğanı tereyağında kavurun.\nSalçaları ekleyip karıştırın.\nBulguru ilave edip kavurun.\nSıcak suyu ve tuzu ekleyin.\nKaynayınca kısık ateşe alın.\n15 dakika pişirip ocaktan alın.\n10 dakika demlendirin.",
    "Image_Name": "bulgur-pilavi",
    "Cleaned_Ingredients": "['bulgur', 'soğan', 'domates salçası', 'biber salçası', 'tereyağı', 'su', 'tuz', 'karabiber']"
  },
  {
    "Title": "Firik Pilavı",
    "Ingredients": "['2 su bardağı firik', '1 adet soğan', '2 yemek kaşığı tereyağı', '3 su bardağı tavuk suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Firiği yıkayıp süzün.\nSoğanı tereyağında kavurun.\nFiriği ekleyip kavurun.\nTavuk suyunu ve tuzu ilave edin.\nKaynayınca kısık ateşe alın.\n20 dakika pişirin.\n10 dakika demlendirin.",
    "Image_Name": "firik-pilavi",
    "Cleaned_Ingredients": "['firik', 'soğan', 'tereyağı', 'tavuk suyu', 'tuz', 'karabiber']"
  },
  {
    "Title": "İç Pilav",
    "Ingredients": "['2 su bardağı pirinç', '200 gram tavuk ciğeri', '1 adet soğan', '3 yemek kaşığı tereyağı', '2 yemek kaşığı çam fıstığı', '2 yemek kaşığı kuş üzümü', '3 su bardağı tavuk suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı tarçın', '1 demet dereotu']",
    "Instructions": "Pirinci yıkayıp süzün.\nCiğerleri küçük doğrayın.\nTereyağında soğanı kavurun.\nCiğerleri ekleyin.\nÇam fıstığı ve kuş üzümünü ilave edin.\nPirinci ekleyip kavurun.\nTavuk suyunu ve baharatları ekleyin.\nKısık ateşte 15 dakika pişirin.\nDereotu serperek demlendirin.",
    "Image_Name": "ic-pilav",
    "Cleaned_Ingredients": "['pirinç', 'tavuk ciğeri', 'soğan', 'tereyağı', 'çam fıstığı', 'kuş üzümü', 'tavuk suyu', 'tuz', 'karabiber', 'tarçın', 'dereotu']"
  },
  {
    "Title": "Nohutlu Pirinç Pilavı",
    "Ingredients": "['2 su bardağı pirinç', '1 su bardağı haşlanmış nohut', '2 yemek kaşığı tereyağı', '3 su bardağı tavuk suyu', '1 çay kaşığı tuz']",
    "Instructions": "Pirinci yıkayıp süzün.\nTereyağında pirinci kavurun.\nTavuk suyunu ve tuzu ekleyin.\nHaşlanmış nohudu ilave edin.\nKaynayınca kısık ateşe alın.\n15 dakika pişirip demlendirin.",
    "Image_Name": "nohutlu-pirinc-pilavi",
    "Cleaned_Ingredients": "['pirinç', 'nohut', 'tereyağı', 'tavuk suyu', 'tuz']"
  },
  {
    "Title": "Domatesli Bulgur Pilavı",
    "Ingredients": "['2 su bardağı bulgur', '3 adet domates', '1 adet soğan', '2 adet sivri biber', '2 yemek kaşığı tereyağı', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Soğanı tereyağında kavurun.\nBiberleri ekleyin.\nDoğranmış domatesleri ilave edin.\nBulguru ekleyip kavurun.\nSıcak su ve tuzu ilave edin.\nKısık ateşte 15 dakika pişirin.\nDemlendirin.",
    "Image_Name": "domatesli-bulgur-pilavi",
    "Cleaned_Ingredients": "['bulgur', 'domates', 'soğan', 'sivri biber', 'tereyağı', 'su', 'tuz', 'pul biber']"
  },
  {
    "Title": "Meyhane Pilavı",
    "Ingredients": "['2 su bardağı pirinç', '1 adet soğan', '2 adet domates', '2 adet sivri biber', '2 yemek kaşığı tereyağı', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Pirinci yıkayıp süzün.\nSoğanı tereyağında kavurun.\nBiberleri ve domatesleri ekleyin.\nPirinci ilave edip kavurun.\nSıcak su ve baharatları ekleyin.\nKısık ateşte 15 dakika pişirin.\nDemlendirin.",
    "Image_Name": "meyhane-pilavi",
    "Cleaned_Ingredients": "['pirinç', 'soğan', 'domates', 'sivri biber', 'tereyağı', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Maklube",
    "Ingredients": "['2 su bardağı pirinç', '300 gram kuşbaşı kuzu eti', '2 adet patlıcan', '2 adet patates', '1 adet soğan', '3 yemek kaşığı zeytinyağı', '3 su bardağı et suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı yenibahar', '2 yemek kaşığı çam fıstığı']",
    "Instructions": "Patlıcan ve patatesleri dilimleyip kızartın.\nEti kavurun.\nTencereye eti dizin.\nÜzerine patlıcan ve patates yerleştirin.\nYıkanmış pirinci ekleyin.\nEt suyu ve baharatları dökün.\nKısık ateşte 20 dakika pişirin.\nDemlendirip tabağa ters çevirin.\nÇam fıstığı serpin.",
    "Image_Name": "maklube",
    "Cleaned_Ingredients": "['pirinç', 'kuzu eti', 'patlıcan', 'patates', 'soğan', 'zeytinyağı', 'et suyu', 'tuz', 'karabiber', 'yenibahar', 'çam fıstığı']"
  },
  {
    "Title": "Etli Nohut",
    "Ingredients": "['2 su bardağı nohut', '250 gram kuşbaşı dana eti', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '5 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Nohudu bir gece ıslatın.\nEti tereyağında kavurun.\nSoğanı ekleyin.\nSalçayı ilave edin.\nNohudu ve sıcak suyu ekleyin.\nKısık ateşte 1 saat pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "etli-nohut-yemegi",
    "Cleaned_Ingredients": "['nohut', 'dana eti', 'soğan', 'domates salçası', 'tereyağı', 'su', 'tuz', 'karabiber']"
  },
  {
    "Title": "Etli Kuru Fasulye",
    "Ingredients": "['2 su bardağı kuru fasulye', '200 gram kuşbaşı dana eti', '1 adet soğan', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı tereyağı', '6 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Fasulyeleri bir gece ıslatın.\nEti tereyağında kavurun.\nSoğanı ekleyin.\nSalçaları ilave edin.\nFasulyeleri ve sıcak suyu ekleyin.\nKısık ateşte 1.5 saat pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "etli-kuru-fasulye-tencere",
    "Cleaned_Ingredients": "['kuru fasulye', 'dana eti', 'soğan', 'domates salçası', 'biber salçası', 'tereyağı', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Barbunya Pilaki",
    "Ingredients": "['2 su bardağı barbunya', '2 adet havuç', '2 adet patates', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Barbunya fasulyelerini bir gece ıslatın.\nHaşlayın.\nSoğanı zeytinyağında kavurun.\nHavuç ve patatesleri doğrayıp ekleyin.\nDomatesleri ve sarımsağı ilave edin.\nHaşlanmış barbunya'yı ekleyin.\nTuz ve şekeri ilave edip kısık ateşte 30 dakika pişirin.\nSoğuk veya ılık servis yapın.",
    "Image_Name": "barbunya-pilaki",
    "Cleaned_Ingredients": "['barbunya', 'havuç', 'patates', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Fava",
    "Ingredients": "['2 su bardağı kuru bakla', '1 adet soğan', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker', '1 demet dereotu', '1 adet limon']",
    "Instructions": "Kuru baklaları bir gece ıslatın.\nKabuklarını soyun.\nSoğanı zeytinyağında kavurun.\nBaklaları ekleyip su ilave edin.\nTuz ve şekeri ekleyin.\nYumuşayana kadar pişirin.\nBlenderdan geçirin.\nDereotu ve limonla süsleyip soğuk servis yapın.",
    "Image_Name": "fava",
    "Cleaned_Ingredients": "['kuru bakla', 'soğan', 'zeytinyağı', 'tuz', 'şeker', 'dereotu', 'limon']"
  },
  {
    "Title": "Fellah Köftesi",
    "Ingredients": "['2 su bardağı ince bulgur', '1 su bardağı un', '2 adet yeşil soğan', '1 demet maydanoz', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 yemek kaşığı nar ekşisi', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber']",
    "Instructions": "Bulguru sıcak suyla ıslatın.\n15 dakika bekletin.\nUnu ekleyip yoğurun.\nMinik köfteler şekillendirin.\nKaynayan suda 5 dakika haşlayın.\nSüzüp soğutun.\nYeşil soğan ve maydanozu doğrayın.\nZeytinyağı, salça, nar ekşisi ve baharatlarla sos yapıp köftelere karıştırın.",
    "Image_Name": "fellah-koftesi",
    "Cleaned_Ingredients": "['ince bulgur', 'un', 'yeşil soğan', 'maydanoz', 'zeytinyağı', 'domates salçası', 'nar ekşisi', 'tuz', 'kimyon', 'pul biber']"
  },
  {
    "Title": "Nohut Köftesi",
    "Ingredients": "['2 su bardağı nohut', '1 adet soğan', '2 diş sarımsak', '1 demet maydanoz', '2 yemek kaşığı un', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 çay kaşığı karabiber', 'kızartma yağı']",
    "Instructions": "Nohudu bir gece ıslatın.\nSüzüp blendere alın.\nSoğan, sarımsak ve maydanozu ekleyin.\nUn ve baharatları ilave edin.\nHamur kıvamına gelene kadar çekin.\nKöfteler şekillendirin.\nKızgın yağda kızartın.",
    "Image_Name": "nohut-koftesi",
    "Cleaned_Ingredients": "['nohut', 'soğan', 'sarımsak', 'maydanoz', 'un', 'tuz', 'kimyon', 'karabiber', 'kızartma yağı']"
  },
  {
    "Title": "Yeşil Mercimek Yemeği",
    "Ingredients": "['2 su bardağı yeşil mercimek', '1 adet soğan', '1 adet havuç', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '5 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Mercimeği yıkayın.\nSoğanı zeytinyağında kavurun.\nHavucu doğrayıp ekleyin.\nSalçayı ilave edin.\nMercimeği ve sıcak suyu ekleyin.\nKısık ateşte 35 dakika pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "yesil-mercimek-yemegi",
    "Cleaned_Ingredients": "['yeşil mercimek', 'soğan', 'havuç', 'domates salçası', 'zeytinyağı', 'su', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Börülce Salatası",
    "Ingredients": "['2 su bardağı kuru börülce', '2 adet domates', '1 adet soğan', '1 demet maydanoz', '3 yemek kaşığı zeytinyağı', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı sumak']",
    "Instructions": "Börülceyi bir gece ıslatıp haşlayın.\nSüzüp soğutun.\nDomates ve soğanı doğrayın.\nMaydanozu kıyın.\nHepsini karıştırın.\nLimon suyu ve zeytinyağını ekleyin.\nSumak ve tuz serpin.",
    "Image_Name": "borulce-salatasi",
    "Cleaned_Ingredients": "['börülce', 'domates', 'soğan', 'maydanoz', 'zeytinyağı', 'limon', 'tuz', 'sumak']"
  },
  {
    "Title": "Kuru Bamya",
    "Ingredients": "['200 gram kuru bamya', '200 gram kuşbaşı dana eti', '1 adet soğan', '2 adet domates', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '4 su bardağı sıcak su', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kuru bamyaları ılık suda 1 saat ıslatın.\nEti tereyağında kavurun.\nSoğanı ekleyin.\nSalça ve domatesleri ilave edin.\nBamyaları ekleyin.\nSıcak su ve limon suyunu ilave edin.\nKısık ateşte 45 dakika pişirin.",
    "Image_Name": "kuru-bamya",
    "Cleaned_Ingredients": "['kuru bamya', 'dana eti', 'soğan', 'domates', 'domates salçası', 'tereyağı', 'su', 'limon', 'tuz', 'karabiber']"
  },
  {
    "Title": "Sade Pirinç Pilavı",
    "Ingredients": "['2 su bardağı pirinç', '3 su bardağı sıcak su', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz']",
    "Instructions": "Pirinci yıkayıp süzün.\nTereyağında pirinci kavurun.\nSıcak suyu ve tuzu ekleyin.\nKaynayınca kısık ateşe alın.\n15 dakika pişirin.\nOcaktan alıp 10 dakika demlendirin.",
    "Image_Name": "sade-pirinc-pilavi",
    "Cleaned_Ingredients": "['pirinç', 'su', 'tereyağı', 'tuz']"
  },
  {
    "Title": "Mercimek Köftesi",
    "Ingredients": "['2 su bardağı kırmızı mercimek', '1.5 su bardağı ince bulgur', '3 adet yeşil soğan', '1 demet maydanoz', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber', '1 adet limon']",
    "Instructions": "Mercimeği haşlayın.\nÜzerine bulguru ekleyip kapağını kapatın.\n15 dakika demlendirin.\nSalçaları ve zeytinyağını ekleyip yoğurun.\nYeşil soğan ve maydanozu doğrayıp katın.\nBaharatları ve limon suyunu ekleyin.\nKöfte şekli verip servis yapın.",
    "Image_Name": "mercimek-koftesi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'ince bulgur', 'yeşil soğan', 'maydanoz', 'domates salçası', 'biber salçası', 'zeytinyağı', 'tuz', 'kimyon', 'pul biber', 'limon']"
  },
  {
    "Title": "Vegan Pirinç Pilavı (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı pirinç', '3 su bardağı sebze suyu', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz']",
    "Instructions": "Pirinci yıkayıp süzün.\nZeytinyağında pirinci kavurun.\nSebze suyunu ve tuzu ekleyin.\nKaynayınca kısık ateşe alın.\n15 dakika pişirin.\nOcaktan alıp 10 dakika demlendirin.",
    "Image_Name": "vegan-pirinc-pilavi",
    "Cleaned_Ingredients": "['pirinç', 'sebze suyu', 'zeytinyağı', 'tuz']"
  },
  {
    "Title": "Süt Ürünsüz Şehriyeli Pilav (Süt Ürünü Yok)",
    "Ingredients": "['2 su bardağı pirinç', '3 su bardağı tavuk suyu', '2 yemek kaşığı zeytinyağı', '0.5 su bardağı şehriye', '1 çay kaşığı tuz']",
    "Instructions": "Pirinci yıkayıp süzün.\nZeytinyağında şehriyeyi kavurun.\nPirinci ekleyip kavurun.\nTavuk suyunu ve tuzu ilave edin.\nKaynayınca kısık ateşe alın.\n15 dakika pişirip demlendirin.",
    "Image_Name": "sut-urunsuz-sehriyeli-pilav",
    "Cleaned_Ingredients": "['pirinç', 'tavuk suyu', 'zeytinyağı', 'şehriye', 'tuz']"
  },
  {
    "Title": "Glutensiz Pirinç Pilavı (Glutensiz)",
    "Ingredients": "['2 su bardağı pirinç', '3 su bardağı tavuk suyu', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz']",
    "Instructions": "Pirinci yıkayıp süzün.\nTereyağında pirinci kavurun.\nTavuk suyunu ve tuzu ekleyin.\nKaynayınca kısık ateşe alın.\n15 dakika pişirin.\nDemlendirin.",
    "Image_Name": "glutensiz-pirinc-pilavi",
    "Cleaned_Ingredients": "['pirinç', 'tavuk suyu', 'tereyağı', 'tuz']"
  },
  {
    "Title": "Glutensiz Kinoa Pilavı (Glutensiz & Vegan)",
    "Ingredients": "['2 su bardağı kinoa', '3 su bardağı sebze suyu', '2 yemek kaşığı zeytinyağı', '1 adet soğan', '1 adet havuç', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı zerdeçal']",
    "Instructions": "Kinoayı yıkayıp süzün.\nSoğanı zeytinyağında kavurun.\nHavucu doğrayıp ekleyin.\nKinoayı ilave edip kavurun.\nSebze suyu ve baharatları ekleyin.\nKaynayınca kısık ateşte 15 dakika pişirin.\nDemlendirin.",
    "Image_Name": "glutensiz-kinoa-pilavi",
    "Cleaned_Ingredients": "['kinoa', 'sebze suyu', 'zeytinyağı', 'soğan', 'havuç', 'tuz', 'karabiber', 'zerdeçal']"
  },
  {
    "Title": "Glutensiz Karabuğday Pilavı (Glutensiz)",
    "Ingredients": "['2 su bardağı karabuğday', '3 su bardağı sebze suyu', '2 yemek kaşığı tereyağı', '1 adet soğan', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Karabuğdayı yıkayıp süzün.\nSoğanı tereyağında kavurun.\nKarabuğdayı ekleyip kavurun.\nSebze suyunu ve baharatları ekleyin.\nKaynayınca kısık ateşte 15 dakika pişirin.\nDemlendirin.",
    "Image_Name": "glutensiz-karabugday-pilavi",
    "Cleaned_Ingredients": "['karabuğday', 'sebze suyu', 'tereyağı', 'soğan', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Bulgur Pilavı (Vegan)",
    "Ingredients": "['2 su bardağı bulgur', '1 adet soğan', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı zeytinyağı', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Soğanı zeytinyağında kavurun.\nSalçaları ekleyip karıştırın.\nBulguru ilave edip kavurun.\nSıcak suyu ve tuzu ekleyin.\nKaynayınca kısık ateşe alın.\n15 dakika pişirip demlendirin.",
    "Image_Name": "vegan-bulgur-pilavi",
    "Cleaned_Ingredients": "['bulgur', 'soğan', 'domates salçası', 'biber salçası', 'zeytinyağı', 'su', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Domatesli Bulgur Pilavı (Vegan)",
    "Ingredients": "['2 su bardağı bulgur', '3 adet domates', '1 adet soğan', '2 adet sivri biber', '2 yemek kaşığı zeytinyağı', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı pul biber']",
    "Instructions": "Soğanı zeytinyağında kavurun.\nBiberleri ekleyin.\nDoğranmış domatesleri ilave edin.\nBulguru ekleyip kavurun.\nSıcak su ve tuzu ekleyin.\nKısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "vegan-domatesli-bulgur-pilavi",
    "Cleaned_Ingredients": "['bulgur', 'domates', 'soğan', 'sivri biber', 'zeytinyağı', 'su', 'tuz', 'pul biber']"
  },
  {
    "Title": "Süt Ürünsüz Nohutlu Pilav (Süt Ürünü Yok)",
    "Ingredients": "['2 su bardağı pirinç', '1 su bardağı haşlanmış nohut', '2 yemek kaşığı zeytinyağı', '3 su bardağı tavuk suyu', '1 çay kaşığı tuz']",
    "Instructions": "Pirinci yıkayıp süzün.\nZeytinyağında pirinci kavurun.\nTavuk suyunu ve tuzu ekleyin.\nHaşlanmış nohudu ilave edin.\nKaynayınca kısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "sut-urunsuz-nohutlu-pilav",
    "Cleaned_Ingredients": "['pirinç', 'nohut', 'zeytinyağı', 'tavuk suyu', 'tuz']"
  },
  {
    "Title": "Vegan Nohut Yemeği (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı nohut', '2 adet soğan', '2 adet domates', '1 yemek kaşığı domates salçası', '3 yemek kaşığı zeytinyağı', '5 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Nohudu bir gece ıslatın.\nSoğanları zeytinyağında kavurun.\nDoğranmış domatesleri ve salçayı ekleyin.\nNohudu ve sıcak suyu ilave edin.\nKısık ateşte 1 saat pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "vegan-nohut-pilaki",
    "Cleaned_Ingredients": "['nohut', 'soğan', 'domates', 'domates salçası', 'zeytinyağı', 'su', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Vegan Kuru Fasulye (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı kuru fasulye', '2 adet soğan', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '3 yemek kaşığı zeytinyağı', '6 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Fasulyeleri bir gece ıslatın.\nSoğanları zeytinyağında kavurun.\nSalçaları ilave edin.\nFasulyeleri ve sıcak suyu ekleyin.\nKısık ateşte 1.5 saat pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "vegan-kuru-fasulye-tencere",
    "Cleaned_Ingredients": "['kuru fasulye', 'soğan', 'domates salçası', 'biber salçası', 'zeytinyağı', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Barbunya Pilaki (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı barbunya', '2 adet havuç', '2 adet patates', '2 adet domates', '1 adet soğan', '3 diş sarımsak', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker']",
    "Instructions": "Barbunya fasulyelerini bir gece ıslatıp haşlayın.\nSoğanı zeytinyağında kavurun.\nHavuç ve patatesleri doğrayıp ekleyin.\nDomatesleri ve sarımsağı ilave edin.\nBarbunya'yı ekleyin.\nTuz ve şekeri ilave edip 30 dakika pişirin.\nSoğuk servis yapın.",
    "Image_Name": "vegan-barbunya-pilaki",
    "Cleaned_Ingredients": "['barbunya', 'havuç', 'patates', 'domates', 'soğan', 'sarımsak', 'zeytinyağı', 'tuz', 'şeker']"
  },
  {
    "Title": "Glutensiz Fellah Köftesi (Glutensiz & Vegan)",
    "Ingredients": "['2 su bardağı karabuğday', '2 adet yeşil soğan', '1 demet maydanoz', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 yemek kaşığı nar ekşisi', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber']",
    "Instructions": "Karabuğdayı haşlayın.\nSüzüp soğutun.\nYoğurup minik köfteler şekillendirin.\nKaynayan suda 5 dakika haşlayın.\nSüzüp soğutun.\nYeşil soğan ve maydanozu doğrayın.\nZeytinyağı, salça, nar ekşisi ve baharatlarla sos yapıp köftelere karıştırın.",
    "Image_Name": "glutensiz-fellah-koftesi",
    "Cleaned_Ingredients": "['karabuğday', 'yeşil soğan', 'maydanoz', 'zeytinyağı', 'domates salçası', 'nar ekşisi', 'tuz', 'kimyon', 'pul biber']"
  },
  {
    "Title": "Glutensiz Nohut Köftesi (Glutensiz & Vegan)",
    "Ingredients": "['2 su bardağı nohut', '1 adet soğan', '2 diş sarımsak', '1 demet maydanoz', '3 yemek kaşığı mısır unu', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 çay kaşığı karabiber', 'kızartma yağı']",
    "Instructions": "Nohudu bir gece ıslatın.\nSüzüp blendere alın.\nSoğan, sarımsak ve maydanozu ekleyin.\nMısır unu ve baharatları ilave edin.\nKöfteler şekillendirin.\nKızgın yağda kızartın.",
    "Image_Name": "glutensiz-nohut-koftesi",
    "Cleaned_Ingredients": "['nohut', 'soğan', 'sarımsak', 'maydanoz', 'mısır unu', 'tuz', 'kimyon', 'karabiber', 'kızartma yağı']"
  },
  {
    "Title": "Vegan Fava (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı kuru bakla', '1 adet soğan', '0.5 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker', '1 demet dereotu', '1 adet limon']",
    "Instructions": "Kuru baklaları bir gece ıslatın.\nKabuklarını soyun.\nSoğanı zeytinyağında kavurun.\nBaklaları ekleyip su ilave edin.\nTuz ve şekeri ekleyin.\nYumuşayana kadar pişirin.\nBlenderdan geçirin.\nDereotu ve limonla süsleyip soğuk servis yapın.",
    "Image_Name": "vegan-fava",
    "Cleaned_Ingredients": "['kuru bakla', 'soğan', 'zeytinyağı', 'tuz', 'şeker', 'dereotu', 'limon']"
  },
  {
    "Title": "Vegan Yeşil Mercimek (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı yeşil mercimek', '1 adet soğan', '1 adet havuç', '1 yemek kaşığı domates salçası', '3 yemek kaşığı zeytinyağı', '5 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Mercimeği yıkayın.\nSoğanı zeytinyağında kavurun.\nHavucu doğrayıp ekleyin.\nSalçayı ilave edin.\nMercimeği ve sıcak suyu ekleyin.\nKısık ateşte 35 dakika pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "vegan-yesil-mercimek",
    "Cleaned_Ingredients": "['yeşil mercimek', 'soğan', 'havuç', 'domates salçası', 'zeytinyağı', 'su', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Vegan Kuru Bamya (Vegan & Glutensiz)",
    "Ingredients": "['200 gram kuru bamya', '2 adet domates', '1 adet soğan', '1 yemek kaşığı domates salçası', '3 yemek kaşığı zeytinyağı', '4 su bardağı sıcak su', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kuru bamyaları ılık suda 1 saat ıslatın.\nSoğanı zeytinyağında kavurun.\nSalça ve domatesleri ilave edin.\nBamyaları ekleyin.\nSıcak su ve limon suyunu ilave edin.\nKısık ateşte 45 dakika pişirin.",
    "Image_Name": "vegan-kuru-bamya",
    "Cleaned_Ingredients": "['kuru bamya', 'domates', 'soğan', 'domates salçası', 'zeytinyağı', 'su', 'limon', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Maklube (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı pirinç', '1 su bardağı nohut', '2 adet patlıcan', '2 adet patates', '1 adet soğan', '4 yemek kaşığı zeytinyağı', '3 su bardağı sebze suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı yenibahar']",
    "Instructions": "Nohudu bir gece ıslatıp haşlayın.\nPatlıcan ve patatesleri dilimleyip kızartın.\nSoğanı zeytinyağında kavurun.\nTencereye nohudu dizin.\nPatlıcan ve patates yerleştirin.\nYıkanmış pirinci ekleyin.\nSebze suyu ve baharatları dökün.\nKısık ateşte 20 dakika pişirip demlendirin.\nTabağa ters çevirin.",
    "Image_Name": "vegan-maklube",
    "Cleaned_Ingredients": "['pirinç', 'nohut', 'patlıcan', 'patates', 'soğan', 'zeytinyağı', 'sebze suyu', 'tuz', 'karabiber', 'yenibahar']"
  },
  {
    "Title": "Süt Ürünsüz Meyhane Pilavı (Süt Ürünü Yok)",
    "Ingredients": "['2 su bardağı pirinç', '1 adet soğan', '2 adet domates', '2 adet sivri biber', '2 yemek kaşığı zeytinyağı', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Pirinci yıkayıp süzün.\nSoğanı zeytinyağında kavurun.\nBiberleri ve domatesleri ekleyin.\nPirinci ilave edip kavurun.\nSıcak su ve baharatları ekleyin.\nKısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "sut-urunsuz-meyhane-pilavi",
    "Cleaned_Ingredients": "['pirinç', 'soğan', 'domates', 'sivri biber', 'zeytinyağı', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Glutensiz Mercimek Köftesi (Glutensiz & Vegan)",
    "Ingredients": "['2 su bardağı kırmızı mercimek', '1.5 su bardağı karabuğday', '3 adet yeşil soğan', '1 demet maydanoz', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber', '1 adet limon']",
    "Instructions": "Mercimeği haşlayın.\nKarabuğdayı ayrı haşlayın.\nMercimeğin üzerine karabuğdayı ekleyip yoğurun.\nSalçaları ve zeytinyağını ekleyin.\nYeşil soğan ve maydanozu doğrayıp katın.\nBaharatları ve limon suyunu ekleyin.\nKöfte şekli verip servis yapın.",
    "Image_Name": "glutensiz-mercimek-koftesi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'karabuğday', 'yeşil soğan', 'maydanoz', 'domates salçası', 'biber salçası', 'zeytinyağı', 'tuz', 'kimyon', 'pul biber', 'limon']"
  },
  {
    "Title": "Vegan Firik Pilavı (Vegan)",
    "Ingredients": "['2 su bardağı firik', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '3 su bardağı sebze suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Firiği yıkayıp süzün.\nSoğanı zeytinyağında kavurun.\nFiriği ekleyip kavurun.\nSebze suyunu ve baharatları ekleyin.\nKaynayınca kısık ateşte 20 dakika pişirin.\nDemlendirin.",
    "Image_Name": "vegan-firik-pilavi",
    "Cleaned_Ingredients": "['firik', 'soğan', 'zeytinyağı', 'sebze suyu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Kuruyemişsiz İç Pilav (Kuruyemiş Alerjisi)",
    "Ingredients": "['2 su bardağı pirinç', '200 gram tavuk ciğeri', '1 adet soğan', '3 yemek kaşığı tereyağı', '2 yemek kaşığı kuş üzümü', '3 su bardağı tavuk suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı tarçın', '1 demet dereotu']",
    "Instructions": "Pirinci yıkayıp süzün.\nCiğerleri küçük doğrayın.\nTereyağında soğanı kavurun.\nCiğerleri ekleyin.\nKuş üzümünü ilave edin.\nPirinci ekleyip kavurun.\nTavuk suyunu ve baharatları ekleyin.\nKısık ateşte 15 dakika pişirin.\nDereotu serperek demlendirin.",
    "Image_Name": "kuruyemissiz-ic-pilav",
    "Cleaned_Ingredients": "['pirinç', 'tavuk ciğeri', 'soğan', 'tereyağı', 'kuş üzümü', 'tavuk suyu', 'tuz', 'karabiber', 'tarçın', 'dereotu']"
  },
  {
    "Title": "Süt Ürünsüz Firik Pilavı (Süt Ürünü Yok)",
    "Ingredients": "['2 su bardağı firik', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '3 su bardağı tavuk suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Firiği yıkayıp süzün.\nSoğanı zeytinyağında kavurun.\nFiriği ekleyip kavurun.\nTavuk suyunu ve baharatları ekleyin.\nKaynayınca kısık ateşte 20 dakika pişirin.\nDemlendirin.",
    "Image_Name": "sut-urunsuz-firik-pilavi",
    "Cleaned_Ingredients": "['firik', 'soğan', 'zeytinyağı', 'tavuk suyu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Glutensiz Vegan Kinoa Tabbule (Glutensiz & Vegan)",
    "Ingredients": "['1 su bardağı kinoa', '3 adet domates', '2 adet salatalık', '4 adet yeşil soğan', '2 demet maydanoz', '1 demet nane', '3 yemek kaşığı zeytinyağı', '2 adet limon', '1 çay kaşığı tuz']",
    "Instructions": "Kinoayı haşlayıp soğutun.\nDomates, salatalık ve yeşil soğanı küçük doğrayın.\nMaydanoz ve naneyi ince kıyın.\nHepsini karıştırın.\nZeytinyağı ve limon suyunu ekleyin.\nTuzlayıp soğuk servis yapın.",
    "Image_Name": "glutensiz-kinoa-tabbule",
    "Cleaned_Ingredients": "['kinoa', 'domates', 'salatalık', 'yeşil soğan', 'maydanoz', 'nane', 'zeytinyağı', 'limon', 'tuz']"
  },
  {
    "Title": "Patlıcanlı Pilav",
    "Ingredients": "['2 su bardağı pirinç', '2 adet patlıcan', '1 adet soğan', '2 yemek kaşığı tereyağı', '3 su bardağı sıcak su', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Patlıcanları küp küp doğrayıp kızartın.\nSoğanı tereyağında kavurun.\nSalçayı ekleyin.\nPirinci ilave edip kavurun.\nSıcak suyu ve tuzu ekleyin.\nKızartılmış patlıcanları üzerine dizin.\nKısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "patlicanli-pilav",
    "Cleaned_Ingredients": "['pirinç', 'patlıcan', 'soğan', 'tereyağı', 'su', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "Etli Bezelye",
    "Ingredients": "['500 gram bezelye', '200 gram kuşbaşı dana eti', '1 adet soğan', '2 adet domates', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '2 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı şeker']",
    "Instructions": "Eti tereyağında kavurun.\nSoğanı ekleyin.\nSalça ve domatesleri ilave edin.\nBezelyeleri ekleyin.\nSıcak su, tuz ve şekeri ilave edin.\nKısık ateşte 30 dakika pişirin.",
    "Image_Name": "etli-bezelye",
    "Cleaned_Ingredients": "['bezelye', 'dana eti', 'soğan', 'domates', 'tereyağı', 'domates salçası', 'su', 'tuz', 'karabiber', 'şeker']"
  },
  {
    "Title": "Nohutlu Bulgur Pilavı",
    "Ingredients": "['2 su bardağı bulgur', '1 su bardağı haşlanmış nohut', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Soğanı tereyağında kavurun.\nSalçayı ekleyin.\nBulguru ilave edip kavurun.\nSıcak su ve tuzu ekleyin.\nHaşlanmış nohudu ilave edin.\nKısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "nohutlu-bulgur-pilavi",
    "Cleaned_Ingredients": "['bulgur', 'nohut', 'soğan', 'domates salçası', 'tereyağı', 'su', 'tuz', 'karabiber']"
  },
  {
    "Title": "Kıymalı Bulgur Pilavı",
    "Ingredients": "['2 su bardağı bulgur', '200 gram kıyma', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kıymayı tereyağında kavurun.\nSoğanı ekleyin.\nSalçayı ilave edin.\nBulguru ekleyip kavurun.\nSıcak su ve baharatları ekleyin.\nKısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "kiymali-bulgur-pilavi",
    "Cleaned_Ingredients": "['bulgur', 'kıyma', 'soğan', 'domates salçası', 'tereyağı', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Patlıcanlı Pilav (Vegan)",
    "Ingredients": "['2 su bardağı pirinç', '2 adet patlıcan', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '3 su bardağı sebze suyu', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Patlıcanları küp küp doğrayıp zeytinyağında kızartın.\nSoğanı zeytinyağında kavurun.\nSalçayı ekleyin.\nPirinci ilave edip kavurun.\nSebze suyunu ve tuzu ekleyin.\nPatlıcanları üzerine dizin.\nKısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "vegan-patlicanli-pilav",
    "Cleaned_Ingredients": "['pirinç', 'patlıcan', 'soğan', 'zeytinyağı', 'sebze suyu', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Bezelye Yemeği (Vegan & Glutensiz)",
    "Ingredients": "['500 gram bezelye', '1 adet soğan', '2 adet domates', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '2 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı şeker']",
    "Instructions": "Soğanı zeytinyağında kavurun.\nSalça ve domatesleri ilave edin.\nBezelyeleri ekleyin.\nSıcak su, tuz ve şekeri ilave edin.\nKısık ateşte 30 dakika pişirin.",
    "Image_Name": "vegan-bezelye-yemegi",
    "Cleaned_Ingredients": "['bezelye', 'soğan', 'domates', 'zeytinyağı', 'domates salçası', 'su', 'tuz', 'karabiber', 'şeker']"
  },
  {
    "Title": "Glutensiz Nohutlu Kinoa Pilavı (Glutensiz & Vegan)",
    "Ingredients": "['2 su bardağı kinoa', '1 su bardağı haşlanmış nohut', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '3 su bardağı sebze suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon']",
    "Instructions": "Kinoayı yıkayıp süzün.\nSoğanı zeytinyağında kavurun.\nKinoayı ekleyip kavurun.\nSebze suyunu ve baharatları ekleyin.\nHaşlanmış nohudu ilave edin.\nKısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "glutensiz-nohutlu-kinoa-pilavi",
    "Cleaned_Ingredients": "['kinoa', 'nohut', 'soğan', 'zeytinyağı', 'sebze suyu', 'tuz', 'karabiber', 'kimyon']"
  },
  {
    "Title": "Süt Ürünsüz Bulgur Pilavı (Süt Ürünü Yok)",
    "Ingredients": "['2 su bardağı bulgur', '1 adet soğan', '1 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '2 yemek kaşığı zeytinyağı', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Soğanı zeytinyağında kavurun.\nSalçaları ekleyip karıştırın.\nBulguru ilave edip kavurun.\nSıcak suyu ve tuzu ekleyin.\nKaynayınca kısık ateşe alın.\n15 dakika pişirip demlendirin.",
    "Image_Name": "sut-urunsuz-bulgur-pilavi",
    "Cleaned_Ingredients": "['bulgur', 'soğan', 'domates salçası', 'biber salçası', 'zeytinyağı', 'su', 'tuz', 'karabiber']"
  },
  {
    "Title": "Muhallebi",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '5 yemek kaşığı nişasta', '1 paket vanilya']",
    "Instructions": "Sütün bir kısmını ayırıp nişastayı eritin.\nKalan sütü ve şekeri tencereye alıp kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nSürekli karıştırarak koyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.\nBuzdolabında 2 saat bekletin.",
    "Image_Name": "muhallebi",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'nişasta', 'vanilya']"
  },
  {
    "Title": "Kazandibi",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '5 yemek kaşığı nişasta', '2 yemek kaşığı pirinç unu', '1 paket vanilya', '2 yemek kaşığı tereyağı']",
    "Instructions": "Sütün bir kısmıyla nişasta ve pirinç ununu eritin.\nKalan sütü ve şekeri kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ilave edin.\nTereyağı sürülmüş tepsiye dökün.\nAltını ocakta veya fırında kızartın.\nSoğutup rulo yaparak servis edin.",
    "Image_Name": "kazandibi",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'nişasta', 'pirinç unu', 'vanilya', 'tereyağı']"
  },
  {
    "Title": "Keşkül",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '4 yemek kaşığı nişasta', '100 gram çekilmiş badem', '1 paket vanilya', '2 yemek kaşığı hindistan cevizi']",
    "Instructions": "Bademi blenderdan geçirin.\nSütün bir kısmıyla nişastayı eritin.\nKalan sütü, şekeri ve bademi kaynatın.\nNişastalı karışımı ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırın.\nHindistan cevizi serperek buzdolabında soğutun.",
    "Image_Name": "keskul",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'nişasta', 'badem', 'vanilya', 'hindistan cevizi']"
  },
  {
    "Title": "Güllaç",
    "Ingredients": "['10 adet güllaç yaprağı', '1 litre süt', '1.5 su bardağı toz şeker', '1 yemek kaşığı gül suyu', '100 gram ceviz', '1 adet nar']",
    "Instructions": "Sütü ve şekeri kaynatıp soğutun.\nGül suyunu ekleyin.\nGüllaç yapraklarını sütle ıslatarak tepsiye dizin.\nAralarına ceviz serpin.\nTüm yaprakları dizdikten sonra kalan sütü dökün.\nBuzdolabında 2 saat bekletin.\nNar taneleriyle süsleyip servis yapın.",
    "Image_Name": "gullac",
    "Cleaned_Ingredients": "['güllaç yaprağı', 'süt', 'toz şeker', 'gül suyu', 'ceviz', 'nar']"
  },
  {
    "Title": "Supangle",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '4 yemek kaşığı nişasta', '4 yemek kaşığı kakao', '50 gram bitter çikolata', '1 paket vanilya']",
    "Instructions": "Sütün bir kısmıyla nişasta ve kakaoyu eritin.\nKalan sütü ve şekeri kaynatın.\nKakaolu karışımı yavaşça ekleyin.\nSürekli karıştırarak pişirin.\nÇikolatayı ilave edip eritin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "supangle",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'nişasta', 'kakao', 'bitter çikolata', 'vanilya']"
  },
  {
    "Title": "Tavuk Göğsü Tatlısı",
    "Ingredients": "['200 gram tavuk göğsü', '1 litre süt', '1.5 su bardağı toz şeker', '5 yemek kaşığı nişasta', '2 yemek kaşığı pirinç unu', '1 paket vanilya']",
    "Instructions": "Tavuk göğsünü haşlayıp liflerine ayırın.\nÇok ince didikleyin.\nSütün bir kısmıyla nişasta ve pirinç ununu eritin.\nKalan sütü ve şekeri kaynatın.\nDidiklenmiş tavuğu ekleyin.\nNişastalı karışımı yavaşça ilave edin.\nKoyulaşana kadar pişirin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "tavuk-gogsu-tatlisi",
    "Cleaned_Ingredients": "['tavuk göğsü', 'süt', 'toz şeker', 'nişasta', 'pirinç unu', 'vanilya']"
  },
  {
    "Title": "Trileçe",
    "Ingredients": "['4 adet yumurta', '1 su bardağı toz şeker', '1 su bardağı un', '1 su bardağı süt', '1 kutu yoğunlaştırılmış süt', '1 su bardağı krema', '3 yemek kaşığı toz şeker']",
    "Instructions": "Yumurta ve şekeri çırpın.\nUnu ekleyip karıştırın.\nYağlanmış tepsiye dökün.\n180 derece fırında 25 dakika pişirin.\nSüt ve yoğunlaştırılmış sütü karıştırıp kekin üzerine dökün.\nBuzdolabında 4 saat bekletin.\nKremayı şekerle çırpıp üzerine yayın.\nDilimleyip servis yapın.",
    "Image_Name": "trilece",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'un', 'süt', 'yoğunlaştırılmış süt', 'krema', 'toz şeker']"
  },
  {
    "Title": "Profiterol",
    "Ingredients": "['1 su bardağı su', '100 gram tereyağı', '1 su bardağı un', '4 adet yumurta', '1 litre süt', '1 su bardağı toz şeker', '4 yemek kaşığı nişasta', '4 yemek kaşığı kakao', '1 paket vanilya']",
    "Instructions": "Su ve tereyağını kaynatın.\nUnu ekleyip karıştırarak pişirin.\nSoğutup yumurtaları teker teker ekleyin.\nTepsiye kaşıkla bezeler bırakın.\n200 derece fırında 25 dakika pişirin.\nSüt, şeker, nişasta ve kakaodan sos yapın.\nŞuların içini vanilya pudingiyle doldurun.\nÇikolata sosunu üzerine dökün.",
    "Image_Name": "profiterol",
    "Cleaned_Ingredients": "['su', 'tereyağı', 'un', 'yumurta', 'süt', 'toz şeker', 'nişasta', 'kakao', 'vanilya']"
  },
  {
    "Title": "Dondurma",
    "Ingredients": "['0.5 litre süt', '1 su bardağı krema', '0.5 su bardağı toz şeker', '2 yemek kaşığı salep', '1 paket vanilya']",
    "Instructions": "Süt, krema ve şekeri kaynatın.\nSalebi az sütte eritip ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ilave edin.\nSoğutun.\nDondurma makinesinde çekin veya derin dondurucuda her 30 dakikada bir karıştırarak dondurun.",
    "Image_Name": "dondurma",
    "Cleaned_Ingredients": "['süt', 'krema', 'toz şeker', 'salep', 'vanilya']"
  },
  {
    "Title": "Magnolya Tatlısı",
    "Ingredients": "['1 litre süt', '0.5 su bardağı toz şeker', '4 yemek kaşığı nişasta', '1 paket vanilya', '200 gram bisküvi', '1 adet muz', '1 su bardağı çilek']",
    "Instructions": "Süt, şeker ve nişastayla muhallebi yapın.\nVanilyayı ekleyin.\nServis kabının tabanına bisküvi dizin.\nÜzerine muhallebi dökün.\nDilimlenmiş muz ve çilek yerleştirin.\nTekrar muhallebi dökün.\nBuzdolabında 3 saat soğutun.",
    "Image_Name": "magnolya-tatlisi",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'nişasta', 'vanilya', 'bisküvi', 'muz', 'çilek']"
  },
  {
    "Title": "Panna Cotta",
    "Ingredients": "['2 su bardağı krema', '0.5 su bardağı süt', '0.5 su bardağı toz şeker', '1 paket vanilya', '10 gram jelatin']",
    "Instructions": "Jelatini soğuk suda ıslatın.\nKrema, süt ve şekeri kaynatın.\nIslatılmış jelatini ekleyip eritin.\nVanilyayı ilave edin.\nKalıplara dökün.\nBuzdolabında 4 saat bekletin.\nKalıptan çıkarıp servis yapın.",
    "Image_Name": "panna-cotta",
    "Cleaned_Ingredients": "['krema', 'süt', 'toz şeker', 'vanilya', 'jelatin']"
  },
  {
    "Title": "Sütlü İrmik Tatlısı",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '0.5 su bardağı irmik', '2 yemek kaşığı tereyağı', '1 paket vanilya', '2 yemek kaşığı hindistan cevizi']",
    "Instructions": "Sütü kaynatın.\nİrmiği yavaş yavaş ekleyerek karıştırın.\nŞekeri ilave edin.\nKoyulaşana kadar pişirin.\nTereyağı ve vanilyayı ekleyin.\nKaselere paylaştırın.\nHindistan cevizi serperek soğutun.",
    "Image_Name": "sutlu-irmik-tatlisi",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'irmik', 'tereyağı', 'vanilya', 'hindistan cevizi']"
  },
  {
    "Title": "Sakızlı Muhallebi",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '5 yemek kaşığı nişasta', '1 çay kaşığı damla sakızı', '1 paket vanilya']",
    "Instructions": "Damla sakızını toz şekerle dövün.\nSütün bir kısmıyla nişastayı eritin.\nKalan sütü ve şekeri kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nDövülmüş sakızı ilave edin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "sakizli-muhallebi",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'nişasta', 'damla sakızı', 'vanilya']"
  },
  {
    "Title": "Fırında Sütlaç",
    "Ingredients": "['1 litre süt', '1 çay bardağı pirinç', '1 su bardağı toz şeker', '2 yemek kaşığı nişasta', '1 paket vanilya', '1 adet yumurta sarısı']",
    "Instructions": "Pirinçleri yıkayıp haşlayın.\nSütü ekleyip kaynatın.\nŞekeri ilave edin.\nNişastayı az sütte eritip ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırın.\nYumurta sarısı sürüp fırında üzerini kızartın.",
    "Image_Name": "firinda-sutlac",
    "Cleaned_Ingredients": "['süt', 'pirinç', 'toz şeker', 'nişasta', 'vanilya', 'yumurta sarısı']"
  },
  {
    "Title": "Vegan Muhallebi (Vegan & Glutensiz)",
    "Ingredients": "['1 litre yulaf sütü', '1 su bardağı toz şeker', '5 yemek kaşığı mısır nişastası', '1 paket vanilya']",
    "Instructions": "Yulaf sütünün bir kısmını ayırıp nişastayı eritin.\nKalan yulaf sütünü ve şekeri tencereye alıp kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nSürekli karıştırarak koyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "vegan-muhallebi",
    "Cleaned_Ingredients": "['yulaf sütü', 'toz şeker', 'mısır nişastası', 'vanilya']"
  },
  {
    "Title": "Vegan Kazandibi (Vegan)",
    "Ingredients": "['1 litre badem sütü', '1 su bardağı toz şeker', '5 yemek kaşığı mısır nişastası', '2 yemek kaşığı pirinç unu', '1 paket vanilya', '2 yemek kaşığı margarin']",
    "Instructions": "Badem sütünün bir kısmıyla nişasta ve pirinç ununu eritin.\nKalan badem sütünü ve şekeri kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ilave edin.\nMargarin sürülmüş tepsiye dökün.\nAltını ocakta kızartın.\nSoğutup rulo yaparak servis edin.",
    "Image_Name": "vegan-kazandibi",
    "Cleaned_Ingredients": "['badem sütü', 'toz şeker', 'mısır nişastası', 'pirinç unu', 'vanilya', 'margarin']"
  },
  {
    "Title": "Vegan Keşkül (Vegan & Glutensiz)",
    "Ingredients": "['1 litre yulaf sütü', '1 su bardağı toz şeker', '4 yemek kaşığı mısır nişastası', '100 gram çekilmiş badem', '1 paket vanilya', '2 yemek kaşığı hindistan cevizi']",
    "Instructions": "Bademi blenderdan geçirin.\nYulaf sütünün bir kısmıyla nişastayı eritin.\nKalan yulaf sütünü, şekeri ve bademi kaynatın.\nNişastalı karışımı ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp hindistan cevizi serpin.\nSoğutun.",
    "Image_Name": "vegan-keskul",
    "Cleaned_Ingredients": "['yulaf sütü', 'toz şeker', 'mısır nişastası', 'badem', 'vanilya', 'hindistan cevizi']"
  },
  {
    "Title": "Laktozsuz Güllaç (Süt Ürünü Yok)",
    "Ingredients": "['10 adet güllaç yaprağı', '1 litre badem sütü', '1.5 su bardağı toz şeker', '1 yemek kaşığı gül suyu', '100 gram ceviz', '1 adet nar']",
    "Instructions": "Badem sütünü ve şekeri kaynatıp soğutun.\nGül suyunu ekleyin.\nGüllaç yapraklarını sütle ıslatarak tepsiye dizin.\nAralarına ceviz serpin.\nKalan sütü dökün.\nBuzdolabında 2 saat bekletin.\nNar taneleriyle süsleyin.",
    "Image_Name": "laktozsuz-gullac",
    "Cleaned_Ingredients": "['güllaç yaprağı', 'badem sütü', 'toz şeker', 'gül suyu', 'ceviz', 'nar']"
  },
  {
    "Title": "Vegan Supangle (Vegan & Glutensiz)",
    "Ingredients": "['1 litre yulaf sütü', '1 su bardağı toz şeker', '4 yemek kaşığı mısır nişastası', '4 yemek kaşığı kakao', '50 gram vegan bitter çikolata', '1 paket vanilya']",
    "Instructions": "Yulaf sütünün bir kısmıyla nişasta ve kakaoyu eritin.\nKalan yulaf sütünü ve şekeri kaynatın.\nKakaolu karışımı yavaşça ekleyin.\nSürekli karıştırarak pişirin.\nVegan çikolatayı ilave edip eritin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "vegan-supangle",
    "Cleaned_Ingredients": "['yulaf sütü', 'toz şeker', 'mısır nişastası', 'kakao', 'vegan bitter çikolata', 'vanilya']"
  },
  {
    "Title": "Vejetaryen Yalancı Tavuk Göğsü (Vejetaryen & Glutensiz)",
    "Ingredients": "['1 litre süt', '1.5 su bardağı toz şeker', '5 yemek kaşığı mısır nişastası', '2 yemek kaşığı pirinç unu', '2 yemek kaşığı hindistan cevizi', '1 paket vanilya']",
    "Instructions": "Sütün bir kısmıyla nişasta ve pirinç ununu eritin.\nKalan sütü ve şekeri kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nHindistan cevizini ilave edin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "vejetaryen-yalanci-tavuk-gogsu",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'mısır nişastası', 'pirinç unu', 'hindistan cevizi', 'vanilya']"
  },
  {
    "Title": "Vegan Yalancı Tavuk Göğsü (Vegan & Glutensiz)",
    "Ingredients": "['1 litre yulaf sütü', '1.5 su bardağı toz şeker', '5 yemek kaşığı mısır nişastası', '2 yemek kaşığı pirinç unu', '2 yemek kaşığı hindistan cevizi', '1 paket vanilya']",
    "Instructions": "Yulaf sütünün bir kısmıyla nişasta ve pirinç ununu eritin.\nKalan yulaf sütünü ve şekeri kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nHindistan cevizini ilave edin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "vegan-yalanci-tavuk-gogsu",
    "Cleaned_Ingredients": "['yulaf sütü', 'toz şeker', 'mısır nişastası', 'pirinç unu', 'hindistan cevizi', 'vanilya']"
  },
  {
    "Title": "Süt Ürünsüz Trileçe (Süt Ürünü Yok)",
    "Ingredients": "['4 adet yumurta', '1 su bardağı toz şeker', '1 su bardağı un', '1 su bardağı yulaf sütü', '1 su bardağı hindistan cevizi sütü', '3 yemek kaşığı toz şeker']",
    "Instructions": "Yumurta ve şekeri çırpın.\nUnu ekleyip karıştırın.\nYağlanmış tepsiye dökün.\n180 derece fırında 25 dakika pişirin.\nYulaf sütü ve hindistan cevizi sütünü karıştırıp kekin üzerine dökün.\nBuzdolabında 4 saat bekletin.\nDilimleyip servis yapın.",
    "Image_Name": "sut-urunsuz-trilece",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'un', 'yulaf sütü', 'hindistan cevizi sütü', 'toz şeker']"
  },
  {
    "Title": "Vegan Dondurma (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı hindistan cevizi sütü', '1 su bardağı hindistan cevizi krema', '0.5 su bardağı toz şeker', '1 paket vanilya', '2 yemek kaşığı mısır nişastası']",
    "Instructions": "Hindistan cevizi sütü, krema ve şekeri kaynatın.\nNişastayı az sıvıda eritip ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ilave edin.\nSoğutun.\nDerin dondurucuda her 30 dakikada bir karıştırarak dondurun.",
    "Image_Name": "vegan-dondurma",
    "Cleaned_Ingredients": "['hindistan cevizi sütü', 'hindistan cevizi krema', 'toz şeker', 'vanilya', 'mısır nişastası']"
  },
  {
    "Title": "Vegan Magnolya (Vegan)",
    "Ingredients": "['1 litre yulaf sütü', '0.5 su bardağı toz şeker', '4 yemek kaşığı mısır nişastası', '1 paket vanilya', '200 gram vegan bisküvi', '1 adet muz', '1 su bardağı çilek']",
    "Instructions": "Yulaf sütü, şeker ve nişastayla muhallebi yapın.\nVanilyayı ekleyin.\nServis kabının tabanına vegan bisküvi dizin.\nÜzerine muhallebi dökün.\nDilimlenmiş muz ve çilek yerleştirin.\nTekrar muhallebi dökün.\nBuzdolabında 3 saat soğutun.",
    "Image_Name": "vegan-magnolya",
    "Cleaned_Ingredients": "['yulaf sütü', 'toz şeker', 'mısır nişastası', 'vanilya', 'vegan bisküvi', 'muz', 'çilek']"
  },
  {
    "Title": "Glutensiz Muhallebi (Glutensiz)",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '5 yemek kaşığı mısır nişastası', '1 paket vanilya']",
    "Instructions": "Sütün bir kısmını ayırıp mısır nişastasını eritin.\nKalan sütü ve şekeri kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "glutensiz-muhallebi",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'mısır nişastası', 'vanilya']"
  },
  {
    "Title": "Glutensiz Supangle (Glutensiz)",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '4 yemek kaşığı mısır nişastası', '4 yemek kaşığı kakao', '50 gram bitter çikolata', '1 paket vanilya']",
    "Instructions": "Sütün bir kısmıyla mısır nişastası ve kakaoyu eritin.\nKalan sütü ve şekeri kaynatın.\nKakaolu karışımı yavaşça ekleyin.\nÇikolatayı ilave edip eritin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "glutensiz-supangle",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'mısır nişastası', 'kakao', 'bitter çikolata', 'vanilya']"
  },
  {
    "Title": "Kuruyemişsiz Güllaç (Kuruyemiş Alerjisi)",
    "Ingredients": "['10 adet güllaç yaprağı', '1 litre süt', '1.5 su bardağı toz şeker', '1 yemek kaşığı gül suyu', '1 adet nar']",
    "Instructions": "Sütü ve şekeri kaynatıp soğutun.\nGül suyunu ekleyin.\nGüllaç yapraklarını sütle ıslatarak tepsiye dizin.\nKalan sütü dökün.\nBuzdolabında 2 saat bekletin.\nNar taneleriyle süsleyip servis yapın.",
    "Image_Name": "kuruyemissiz-gullac",
    "Cleaned_Ingredients": "['güllaç yaprağı', 'süt', 'toz şeker', 'gül suyu', 'nar']"
  },
  {
    "Title": "Kuruyemişsiz Keşkül (Kuruyemiş Alerjisi)",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '5 yemek kaşığı nişasta', '2 yemek kaşığı pirinç unu', '1 paket vanilya']",
    "Instructions": "Sütün bir kısmıyla nişasta ve pirinç ununu eritin.\nKalan sütü ve şekeri kaynatın.\nNişastalı karışımı ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "kuruyemissiz-keskul",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'nişasta', 'pirinç unu', 'vanilya']"
  },
  {
    "Title": "Süt Ürünsüz Sakızlı Muhallebi (Süt Ürünü Yok)",
    "Ingredients": "['1 litre badem sütü', '1 su bardağı toz şeker', '5 yemek kaşığı mısır nişastası', '1 çay kaşığı damla sakızı', '1 paket vanilya']",
    "Instructions": "Damla sakızını toz şekerle dövün.\nBadem sütünün bir kısmıyla nişastayı eritin.\nKalan badem sütünü ve şekeri kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nDövülmüş sakızı ilave edin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "sut-urunsuz-sakizli-muhallebi",
    "Cleaned_Ingredients": "['badem sütü', 'toz şeker', 'mısır nişastası', 'damla sakızı', 'vanilya']"
  },
  {
    "Title": "Vegan Güllaç (Vegan)",
    "Ingredients": "['10 adet güllaç yaprağı', '1 litre yulaf sütü', '1.5 su bardağı toz şeker', '1 yemek kaşığı gül suyu', '1 adet nar']",
    "Instructions": "Yulaf sütünü ve şekeri kaynatıp soğutun.\nGül suyunu ekleyin.\nGüllaç yapraklarını sütle ıslatarak tepsiye dizin.\nKalan sütü dökün.\nBuzdolabında 2 saat bekletin.\nNar taneleriyle süsleyin.",
    "Image_Name": "vegan-gullac",
    "Cleaned_Ingredients": "['güllaç yaprağı', 'yulaf sütü', 'toz şeker', 'gül suyu', 'nar']"
  },
  {
    "Title": "Süt Ürünsüz Fırında Sütlaç (Süt Ürünü Yok)",
    "Ingredients": "['1 litre badem sütü', '1 çay bardağı pirinç', '1 su bardağı toz şeker', '2 yemek kaşığı mısır nişastası', '1 paket vanilya']",
    "Instructions": "Pirinçleri yıkayıp haşlayın.\nBadem sütünü ekleyip kaynatın.\nŞekeri ilave edin.\nNişastayı az badem sütünde eritip ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırın.\nFırında üzerini kızartın.",
    "Image_Name": "sut-urunsuz-firinda-sutlac",
    "Cleaned_Ingredients": "['badem sütü', 'pirinç', 'toz şeker', 'mısır nişastası', 'vanilya']"
  },
  {
    "Title": "Vegan Profiterol (Vegan)",
    "Ingredients": "['1 su bardağı su', '100 gram margarin', '1 su bardağı un', '1 litre yulaf sütü', '1 su bardağı toz şeker', '4 yemek kaşığı mısır nişastası', '4 yemek kaşığı kakao', '50 gram vegan bitter çikolata', '1 paket vanilya']",
    "Instructions": "Su ve margarini kaynatın.\nUnu ekleyip karıştırarak pişirin.\nSoğutun.\nTepsiye kaşıkla bezeler bırakın.\n200 derece fırında 25 dakika pişirin.\nYulaf sütü, şeker, nişasta ve kakaodan vegan sos yapın.\nÇikolatayı ekleyin.\nŞuları vanilya pudingiyle doldurup sos dökün.",
    "Image_Name": "vegan-profiterol",
    "Cleaned_Ingredients": "['su', 'margarin', 'un', 'yulaf sütü', 'toz şeker', 'mısır nişastası', 'kakao', 'vegan bitter çikolata', 'vanilya']"
  },
  {
    "Title": "Süt Ürünsüz Dondurma (Süt Ürünü Yok & Glutensiz)",
    "Ingredients": "['2 su bardağı hindistan cevizi sütü', '1 su bardağı hindistan cevizi krema', '0.5 su bardağı toz şeker', '2 yemek kaşığı salep', '1 paket vanilya']",
    "Instructions": "Hindistan cevizi sütü, krema ve şekeri kaynatın.\nSalebi az sıvıda eritip ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ilave edin.\nSoğutun.\nDerin dondurucuda her 30 dakikada karıştırarak dondurun.",
    "Image_Name": "sut-urunsuz-dondurma",
    "Cleaned_Ingredients": "['hindistan cevizi sütü', 'hindistan cevizi krema', 'toz şeker', 'salep', 'vanilya']"
  },
  {
    "Title": "Glutensiz Kazandibi (Glutensiz)",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '5 yemek kaşığı mısır nişastası', '2 yemek kaşığı pirinç unu', '1 paket vanilya', '2 yemek kaşığı tereyağı']",
    "Instructions": "Sütün bir kısmıyla mısır nişastası ve pirinç ununu eritin.\nKalan sütü ve şekeri kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ilave edin.\nTereyağı sürülmüş tepsiye dökün.\nAltını ocakta kızartın.\nSoğutup rulo yaparak servis edin.",
    "Image_Name": "glutensiz-kazandibi",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'mısır nişastası', 'pirinç unu', 'vanilya', 'tereyağı']"
  },
  {
    "Title": "Glutensiz Trileçe (Glutensiz)",
    "Ingredients": "['4 adet yumurta', '1 su bardağı toz şeker', '1 su bardağı mısır unu', '1 su bardağı süt', '1 kutu yoğunlaştırılmış süt', '1 su bardağı krema', '3 yemek kaşığı toz şeker']",
    "Instructions": "Yumurta ve şekeri çırpın.\nMısır ununu ekleyip karıştırın.\nTepsiye dökün.\n180 derece fırında 25 dakika pişirin.\nSüt ve yoğunlaştırılmış sütü karıştırıp kekin üzerine dökün.\nBuzdolabında 4 saat bekletin.\nKremayı şekerle çırpıp üzerine yayın.",
    "Image_Name": "glutensiz-trilece",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'mısır unu', 'süt', 'yoğunlaştırılmış süt', 'krema', 'toz şeker']"
  },
  {
    "Title": "Vegan Sütlaç (Vegan & Glutensiz)",
    "Ingredients": "['1 litre yulaf sütü', '1 çay bardağı pirinç', '1 su bardağı toz şeker', '2 yemek kaşığı mısır nişastası', '1 paket vanilya']",
    "Instructions": "Pirinçleri yıkayıp haşlayın.\nYulaf sütünü ekleyip kaynatın.\nŞekeri ilave edin.\nNişastayı az yulaf sütünde eritip ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırıp soğutun.",
    "Image_Name": "vegan-sutlac-tatli",
    "Cleaned_Ingredients": "['yulaf sütü', 'pirinç', 'toz şeker', 'mısır nişastası', 'vanilya']"
  },
  {
    "Title": "Vegan Panna Cotta (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı hindistan cevizi krema', '0.5 su bardağı hindistan cevizi sütü', '0.5 su bardağı toz şeker', '1 paket vanilya', '2 yemek kaşığı agar agar']",
    "Instructions": "Hindistan cevizi krema, sütü ve şekeri kaynatın.\nAgar agarı ekleyip 2 dakika kaynatın.\nVanilyayı ilave edin.\nKalıplara dökün.\nBuzdolabında 3 saat bekletin.\nKalıptan çıkarıp servis yapın.",
    "Image_Name": "vegan-panna-cotta",
    "Cleaned_Ingredients": "['hindistan cevizi krema', 'hindistan cevizi sütü', 'toz şeker', 'vanilya', 'agar agar']"
  },
  {
    "Title": "Süt Ürünsüz Magnolya (Süt Ürünü Yok)",
    "Ingredients": "['1 litre badem sütü', '0.5 su bardağı toz şeker', '4 yemek kaşığı mısır nişastası', '1 paket vanilya', '200 gram bisküvi', '1 adet muz', '1 su bardağı çilek']",
    "Instructions": "Badem sütü, şeker ve nişastayla muhallebi yapın.\nVanilyayı ekleyin.\nServis kabının tabanına bisküvi dizin.\nÜzerine muhallebi dökün.\nMuz ve çilek yerleştirin.\nTekrar muhallebi dökün.\nBuzdolabında 3 saat soğutun.",
    "Image_Name": "sut-urunsuz-magnolya",
    "Cleaned_Ingredients": "['badem sütü', 'toz şeker', 'mısır nişastası', 'vanilya', 'bisküvi', 'muz', 'çilek']"
  },
  {
    "Title": "Glutensiz Sütlü İrmik Tatlısı (Glutensiz)",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '0.5 su bardağı mısır unu', '2 yemek kaşığı tereyağı', '1 paket vanilya', '2 yemek kaşığı hindistan cevizi']",
    "Instructions": "Sütü kaynatın.\nMısır ununu yavaş yavaş ekleyerek karıştırın.\nŞekeri ilave edin.\nKoyulaşana kadar pişirin.\nTereyağı ve vanilyayı ekleyin.\nKaselere paylaştırın.\nHindistan cevizi serperek soğutun.",
    "Image_Name": "glutensiz-sutlu-irmik-tatlisi",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'mısır unu', 'tereyağı', 'vanilya', 'hindistan cevizi']"
  },
  {
    "Title": "Vegan Çikolatalı Mus (Vegan & Glutensiz)",
    "Ingredients": "['1 su bardağı hindistan cevizi krema', '150 gram vegan bitter çikolata', '2 yemek kaşığı toz şeker', '1 paket vanilya']",
    "Instructions": "Hindistan cevizi kremayı ısıtın.\nVegan çikolatayı kırıp ekleyin.\nŞekeri ilave edin.\nKarıştırarak eritin.\nVanilyayı ekleyin.\nKaselere paylaştırıp buzdolabında 3 saat soğutun.",
    "Image_Name": "vegan-cikolatali-mus",
    "Cleaned_Ingredients": "['hindistan cevizi krema', 'vegan bitter çikolata', 'toz şeker', 'vanilya']"
  },
  {
    "Title": "Glutensiz Fırında Sütlaç (Glutensiz)",
    "Ingredients": "['1 litre süt', '1 çay bardağı pirinç', '1 su bardağı toz şeker', '2 yemek kaşığı mısır nişastası', '1 paket vanilya', '1 adet yumurta sarısı']",
    "Instructions": "Pirinçleri yıkayıp haşlayın.\nSütü ekleyip kaynatın.\nŞekeri ilave edin.\nMısır nişastasını az sütte eritip ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırın.\nYumurta sarısı sürüp fırında üzerini kızartın.",
    "Image_Name": "glutensiz-firinda-sutlac",
    "Cleaned_Ingredients": "['süt', 'pirinç', 'toz şeker', 'mısır nişastası', 'vanilya', 'yumurta sarısı']"
  },
  {
    "Title": "Vegan Meyveli Dondurma (Vegan & Glutensiz)",
    "Ingredients": "['3 adet olgun muz', '1 su bardağı çilek', '2 yemek kaşığı toz şeker', '1 paket vanilya']",
    "Instructions": "Muzları dilimleyip derin dondurucuda dondurun.\nDonmuş muzları blendere alın.\nÇilekleri ekleyin.\nŞeker ve vanilyayı ilave edin.\nPürüzsüz olana kadar çekin.\nHemen servis yapın veya dondurucu poşette saklayın.",
    "Image_Name": "vegan-meyveli-dondurma",
    "Cleaned_Ingredients": "['muz', 'çilek', 'toz şeker', 'vanilya']"
  },
  {
    "Title": "Süt Ürünsüz Profiterol (Süt Ürünü Yok)",
    "Ingredients": "['1 su bardağı su', '100 gram margarin', '1 su bardağı un', '4 adet yumurta', '1 litre badem sütü', '1 su bardağı toz şeker', '4 yemek kaşığı mısır nişastası', '4 yemek kaşığı kakao', '1 paket vanilya']",
    "Instructions": "Su ve margarini kaynatın.\nUnu ekleyip karıştırarak pişirin.\nSoğutup yumurtaları teker teker ekleyin.\nTepsiye bezeler bırakın.\n200 derece fırında 25 dakika pişirin.\nBadem sütü, şeker, nişasta ve kakaodan sos yapın.\nŞuların içini vanilya kremayla doldurup sos dökün.",
    "Image_Name": "sut-urunsuz-profiterol",
    "Cleaned_Ingredients": "['su', 'margarin', 'un', 'yumurta', 'badem sütü', 'toz şeker', 'mısır nişastası', 'kakao', 'vanilya']"
  },
  {
    "Title": "Aşure",
    "Ingredients": "['1 su bardağı aşurelik buğday', '0.5 su bardağı nohut', '0.5 su bardağı kuru fasulye', '2 su bardağı toz şeker', '1 yemek kaşığı nişasta', '100 gram ceviz', '100 gram kuru kayısı', '50 gram kuru üzüm', '1 adet nar', '2 litre su']",
    "Instructions": "Buğdayı bir gece ıslatın.\nNohut ve fasulyeyi ayrı ayrı haşlayın.\nBuğdayı yumuşayana kadar pişirin.\nHaşlanmış baklagilleri ekleyin.\nŞekeri ilave edin.\nNişastayı az suda eritip ekleyin.\nKuru meyveleri ilave edip 10 dakika pişirin.\nKaselere paylaştırıp ceviz ve nar ile süsleyin.",
    "Image_Name": "asure",
    "Cleaned_Ingredients": "['aşurelik buğday', 'nohut', 'kuru fasulye', 'toz şeker', 'nişasta', 'ceviz', 'kuru kayısı', 'kuru üzüm', 'nar', 'su']"
  },
  {
    "Title": "Çikolatalı Sufle",
    "Ingredients": "['200 gram bitter çikolata', '100 gram tereyağı', '3 adet yumurta', '0.5 su bardağı toz şeker', '2 yemek kaşığı un']",
    "Instructions": "Çikolata ve tereyağını benmari usulü eritin.\nYumurta ve şekeri çırpın.\nÇikolatalı karışımı ekleyin.\nUnu ilave edip karıştırın.\nYağlanmış ramakinlere dökün.\n200 derece fırında 12 dakika pişirin.\nHemen servis yapın.",
    "Image_Name": "cikolatali-sufle",
    "Cleaned_Ingredients": "['bitter çikolata', 'tereyağı', 'yumurta', 'toz şeker', 'un']"
  },
  {
    "Title": "Keskül-i Fükaralı",
    "Ingredients": "['1 litre süt', '1 su bardağı toz şeker', '5 yemek kaşığı nişasta', '1 paket vanilya', '2 yemek kaşığı pirinç unu', '100 gram ceviz', '50 gram antep fıstığı']",
    "Instructions": "Sütün bir kısmıyla nişasta ve pirinç ununu eritin.\nKalan sütü ve şekeri kaynatın.\nNişastalı karışımı yavaşça ekleyin.\nKoyulaşana kadar pişirin.\nVanilyayı ekleyin.\nKaselere paylaştırın.\nCeviz ve antep fıstığı ile süsleyip soğutun.",
    "Image_Name": "keskul-i-fukarali",
    "Cleaned_Ingredients": "['süt', 'toz şeker', 'nişasta', 'vanilya', 'pirinç unu', 'ceviz', 'antep fıstığı']"
  },
  {
    "Title": "Çilekli Dondurma",
    "Ingredients": "['0.5 litre süt', '1 su bardağı krema', '0.5 su bardağı toz şeker', '2 su bardağı çilek', '1 yemek kaşığı limon suyu']",
    "Instructions": "Çilekleri blenderdan geçirin.\nSüt, krema ve şekeri kaynatın.\nÇilek püresini ekleyin.\nLimon suyunu ilave edin.\nSoğutun.\nDerin dondurucuda her 30 dakikada bir karıştırarak dondurun.",
    "Image_Name": "cilekli-dondurma",
    "Cleaned_Ingredients": "['süt', 'krema', 'toz şeker', 'çilek', 'limon suyu']"
  },
  {
    "Title": "Vegan Aşure (Vegan)",
    "Ingredients": "['1 su bardağı aşurelik buğday', '0.5 su bardağı nohut', '0.5 su bardağı kuru fasulye', '2 su bardağı toz şeker', '1 yemek kaşığı nişasta', '100 gram kuru kayısı', '50 gram kuru üzüm', '1 adet nar', '2 litre su']",
    "Instructions": "Buğdayı bir gece ıslatın.\nNohut ve fasulyeyi ayrı ayrı haşlayın.\nBuğdayı yumuşayana kadar pişirin.\nHaşlanmış baklagilleri ekleyin.\nŞekeri ilave edin.\nNişastayı az suda eritip ekleyin.\nKuru meyveleri ilave edip 10 dakika pişirin.\nKaselere paylaştırıp nar ile süsleyin.",
    "Image_Name": "vegan-asure",
    "Cleaned_Ingredients": "['aşurelik buğday', 'nohut', 'kuru fasulye', 'toz şeker', 'nişasta', 'kuru kayısı', 'kuru üzüm', 'nar', 'su']"
  },
  {
    "Title": "Vegan Çikolatalı Sufle (Vegan & Glutensiz)",
    "Ingredients": "['200 gram vegan bitter çikolata', '100 gram margarin', '3 yemek kaşığı mısır nişastası', '0.5 su bardağı toz şeker', '3 yemek kaşığı yulaf sütü']",
    "Instructions": "Çikolata ve margarini benmari usulü eritin.\nYulaf sütü, şeker ve nişastayı çırpın.\nÇikolatalı karışımı ekleyin.\nYağlanmış ramakinlere dökün.\n200 derece fırında 12 dakika pişirin.\nHemen servis yapın.",
    "Image_Name": "vegan-cikolatali-sufle",
    "Cleaned_Ingredients": "['vegan bitter çikolata', 'margarin', 'mısır nişastası', 'toz şeker', 'yulaf sütü']"
  },
  {
    "Title": "Süt Ürünsüz Çilekli Dondurma (Süt Ürünü Yok & Glutensiz)",
    "Ingredients": "['2 su bardağı hindistan cevizi sütü', '1 su bardağı hindistan cevizi krema', '0.5 su bardağı toz şeker', '2 su bardağı çilek', '1 yemek kaşığı limon suyu']",
    "Instructions": "Çilekleri blenderdan geçirin.\nHindistan cevizi sütü, krema ve şekeri kaynatın.\nÇilek püresini ekleyin.\nLimon suyunu ilave edin.\nSoğutun.\nDerin dondurucuda her 30 dakikada karıştırarak dondurun.",
    "Image_Name": "sut-urunsuz-cilekli-dondurma",
    "Cleaned_Ingredients": "['hindistan cevizi sütü', 'hindistan cevizi krema', 'toz şeker', 'çilek', 'limon suyu']"
  },
  {
    "Title": "Antep Baklavası",
    "Ingredients": "['500 gram baklava yufkası', '250 gram tereyağı', '300 gram antep fıstığı', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Yufkaları tepsiye sererek aralarına eritilmiş tereyağı sürün.\nHer 3-4 yufkada bir antep fıstığı serpin.\nTüm yufkaları dizdikten sonra dilimleyin.\nKalan tereyağını üzerine gezdirin.\n180 derece fırında 40 dakika pişirin.\nŞeker, su ve limon suyundan şerbet yapın.\nSıcak baklavanın üzerine soğuk şerbeti dökün.",
    "Image_Name": "antep-baklavasi",
    "Cleaned_Ingredients": "['baklava yufkası', 'tereyağı', 'antep fıstığı', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Kadayıf",
    "Ingredients": "['500 gram tel kadayıf', '200 gram tereyağı', '250 gram ceviz', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tel kadayıfı ikiye bölün.\nYarısını tepsiye yayın.\nEritilmiş tereyağının yarısını gezdirin.\nCevizi üzerine serpin.\nKalan kadayıfı üzerine kapatın.\nKalan tereyağını dökün.\n180 derece fırında 35 dakika pişirin.\nŞerbeti hazırlayıp sıcak kadayıfa dökün.",
    "Image_Name": "kadayif",
    "Cleaned_Ingredients": "['tel kadayıf', 'tereyağı', 'ceviz', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Şekerpare",
    "Ingredients": "['2 su bardağı un', '100 gram tereyağı', '1 adet yumurta', '0.5 su bardağı irmik', '0.5 çay kaşığı kabartma tozu', '2 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tereyağını eritip unla karıştırın.\nYumurta, irmik ve kabartma tozunu ekleyin.\nHamuru yoğurup ceviz büyüklüğünde toplar yapın.\nTepsiye dizin.\n180 derece fırında 20 dakika pişirin.\nŞeker ve sudan şerbet yapıp limon suyu ekleyin.\nSıcak şekerpareye soğuk şerbet dökün.",
    "Image_Name": "sekerpare",
    "Cleaned_Ingredients": "['un', 'tereyağı', 'yumurta', 'irmik', 'kabartma tozu', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Revani",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '1 su bardağı irmik', '1 su bardağı un', '0.5 su bardağı yoğurt', '1 paket kabartma tozu', '2.5 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Yumurta ve şekeri çırpın.\nYoğurdu ekleyin.\nİrmik, un ve kabartma tozunu ilave edin.\nYağlanmış tepsiye dökün.\n180 derece fırında 30 dakika pişirin.\nŞerbeti hazırlayın.\nSıcak revaniye soğuk şerbet dökün.\nDilimleyip servis yapın.",
    "Image_Name": "revani",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'irmik', 'un', 'yoğurt', 'kabartma tozu', 'su', 'limon suyu']"
  },
  {
    "Title": "Tulumba Tatlısı",
    "Ingredients": "['1 su bardağı su', '100 gram tereyağı', '1.5 su bardağı un', '4 adet yumurta', '1 çay kaşığı tuz', '2.5 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu', 'kızartma yağı']",
    "Instructions": "Su ve tereyağını kaynatın.\nUnu ekleyip karıştırarak pişirin.\nSoğutun.\nYumurtaları teker teker ekleyin.\nHamuru yıldız uçlu sıkma torbasına doldurun.\nKızgın yağda kızartın.\nŞerbeti hazırlayıp soğuk şerbete sıcak tulumbaları batırın.",
    "Image_Name": "tulumba-tatlisi",
    "Cleaned_Ingredients": "['su', 'tereyağı', 'un', 'yumurta', 'tuz', 'toz şeker', 'limon suyu', 'kızartma yağı']"
  },
  {
    "Title": "Lokma Tatlısı",
    "Ingredients": "['2 su bardağı un', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu', 'kızartma yağı']",
    "Instructions": "Un, maya, tuz, şeker ve ılık suyu yoğurun.\n30 dakika mayalanmaya bırakın.\nIslak elle parçalar koparıp kızgın yağda kızartın.\nŞerbeti hazırlayın.\nKızartılan lokmaları şerbete batırın.\nServis tabağına alın.",
    "Image_Name": "lokma-tatlisi",
    "Cleaned_Ingredients": "['un', 'instant maya', 'tuz', 'toz şeker', 'su', 'limon suyu', 'kızartma yağı']"
  },
  {
    "Title": "Künefe",
    "Ingredients": "['500 gram tel kadayıf', '200 gram tereyağı', '250 gram künefe peyniri', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu', '2 yemek kaşığı antep fıstığı']",
    "Instructions": "Tel kadayıfı ince kıyın.\nEritilmiş tereyağıyla karıştırın.\nYarısını künefe kalıbına yayın.\nPeyniri üzerine dizin.\nKalan kadayıfı kapatın.\nKısık ateşte iki tarafını kızartın.\nŞerbeti hazırlayıp dökün.\nAntep fıstığı serpin.",
    "Image_Name": "kunefe",
    "Cleaned_Ingredients": "['tel kadayıf', 'tereyağı', 'künefe peyniri', 'toz şeker', 'su', 'limon suyu', 'antep fıstığı']"
  },
  {
    "Title": "Kalburabastı",
    "Ingredients": "['2 su bardağı un', '100 gram tereyağı', '0.5 su bardağı irmik', '1 adet yumurta', '0.5 çay kaşığı kabartma tozu', '50 gram ceviz', '2 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tereyağını eritip un ve irmikle karıştırın.\nYumurta ve kabartma tozunu ekleyin.\nHamuru yoğurun.\nParçalar koparıp rende üzerinde şekil verin.\nİçine ceviz koyun.\nTepsiye dizin.\n180 derece fırında 25 dakika pişirin.\nŞerbet dökün.",
    "Image_Name": "kalburabasti",
    "Cleaned_Ingredients": "['un', 'tereyağı', 'irmik', 'yumurta', 'kabartma tozu', 'ceviz', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Ekmek Kadayıfı",
    "Ingredients": "['6 dilim bayat ekmek', '200 gram tereyağı', '2.5 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu', '1 su bardağı kaymak']",
    "Instructions": "Ekmeklerin kabuklarını soyun.\nTereyağında iki tarafını kızartın.\nŞeker ve sudan şerbet yapın.\nLimon suyunu ekleyin.\nKızartılmış ekmekleri şerbete batırın.\nTabağa alıp üzerine kaymak koyarak servis yapın.",
    "Image_Name": "ekmek-kadayifi",
    "Cleaned_Ingredients": "['bayat ekmek', 'tereyağı', 'toz şeker', 'su', 'limon suyu', 'kaymak']"
  },
  {
    "Title": "Irmik Helvası",
    "Ingredients": "['2 su bardağı irmik', '100 gram tereyağı', '0.5 su bardağı çam fıstığı', '2 su bardağı süt', '1.5 su bardağı toz şeker']",
    "Instructions": "Tereyağında çam fıstıklarını kavurun.\nİrmiği ekleyip kızarana kadar kavurun.\nSütü ve şekeri ayrı tencerede kaynatın.\nSıcak sütlü karışımı irmiğe yavaşça ekleyin.\nKapağını kapatıp 5 dakika pişirin.\nKarıştırıp kaselere paylaştırın.",
    "Image_Name": "irmik-helvasi",
    "Cleaned_Ingredients": "['irmik', 'tereyağı', 'çam fıstığı', 'süt', 'toz şeker']"
  },
  {
    "Title": "Un Helvası",
    "Ingredients": "['2 su bardağı un', '100 gram tereyağı', '0.5 su bardağı çam fıstığı', '2 su bardağı su', '1.5 su bardağı toz şeker']",
    "Instructions": "Tereyağında çam fıstıklarını kavurun.\nUnu ekleyip kızarana kadar kavurun.\nSuyu ve şekeri ayrı tencerede kaynatın.\nSıcak şerbet karışımını helva hamuruna yavaşça ekleyin.\nKapağını kapatıp kısık ateşte 5 dakika pişirin.\nKaselere paylaştırıp servis yapın.",
    "Image_Name": "un-helvasi",
    "Cleaned_Ingredients": "['un', 'tereyağı', 'çam fıstığı', 'su', 'toz şeker']"
  },
  {
    "Title": "Islak Kek",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '1 su bardağı süt', '0.5 su bardağı sıvı yağ', '2 su bardağı un', '3 yemek kaşığı kakao', '1 paket kabartma tozu', '1 paket vanilya', '1 su bardağı toz şeker', '1 su bardağı su', '2 yemek kaşığı kakao']",
    "Instructions": "Yumurta ve şekeri çırpın.\nSüt ve sıvı yağı ekleyin.\nUn, kakao, kabartma tozu ve vanilyayı ilave edin.\nYağlanmış tepsiye dökün.\n180 derece fırında 30 dakika pişirin.\nSos için şeker, su ve kakaoyu kaynatın.\nSıcak kekin üzerine sosu dökün.",
    "Image_Name": "islak-kek",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'süt', 'sıvı yağ', 'un', 'kakao', 'kabartma tozu', 'vanilya', 'su']"
  },
  {
    "Title": "Havuçlu Tarçınlı Kek",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '0.5 su bardağı sıvı yağ', '2 su bardağı un', '1 paket kabartma tozu', '2 adet havuç', '1 çay kaşığı tarçın', '1 paket vanilya']",
    "Instructions": "Yumurta ve şekeri çırpın.\nSıvı yağı ekleyin.\nUn, kabartma tozu, tarçın ve vanilyayı ilave edin.\nHavuçları rendeleyin ve hamura karıştırın.\nYağlanmış kalıba dökün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "havuclu-tarcinli-kek",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'sıvı yağ', 'un', 'kabartma tozu', 'havuç', 'tarçın', 'vanilya']"
  },
  {
    "Title": "Un Kurabiyesi",
    "Ingredients": "['250 gram tereyağı', '1 su bardağı pudra şekeri', '3.5 su bardağı un', '1 paket vanilya']",
    "Instructions": "Tereyağını oda sıcaklığında yumuşatın.\nPudra şekerini ekleyip çırpın.\nVanilyayı ilave edin.\nUnu azar azar ekleyip yoğurun.\nŞekil verin ve tepsiye dizin.\n170 derece fırında 15 dakika pişirin.\nSoğuyunca pudra şekeri serpin.",
    "Image_Name": "un-kurabiyesi",
    "Cleaned_Ingredients": "['tereyağı', 'pudra şekeri', 'un', 'vanilya']"
  },
  {
    "Title": "Mozaik Pasta",
    "Ingredients": "['200 gram bisküvi', '100 gram tereyağı', '3 yemek kaşığı kakao', '0.5 su bardağı süt', '0.5 su bardağı toz şeker', '1 paket vanilya']",
    "Instructions": "Bisküvileri kırın.\nTereyağını eritin.\nSüt, şeker ve kakaoyu karıştırıp kaynatın.\nTereyağını ekleyin.\nVanilyayı ilave edin.\nKırık bisküvileri karışıma ekleyin.\nStreç filme sararak rulo yapın.\nBuzdolabında 3 saat bekletin.\nDilimleyip servis yapın.",
    "Image_Name": "mozaik-pasta",
    "Cleaned_Ingredients": "['bisküvi', 'tereyağı', 'kakao', 'süt', 'toz şeker', 'vanilya']"
  },
  {
    "Title": "Limonlu Kek",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '0.5 su bardağı sıvı yağ', '0.5 su bardağı süt', '2 su bardağı un', '1 paket kabartma tozu', '1 adet limon kabuğu rendesi', '2 yemek kaşığı limon suyu']",
    "Instructions": "Yumurta ve şekeri çırpın.\nSıvı yağ ve sütü ekleyin.\nUn, kabartma tozu, limon kabuğu rendesi ve limon suyunu ilave edin.\nYağlanmış kalıba dökün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "limonlu-kek",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'sıvı yağ', 'süt', 'un', 'kabartma tozu', 'limon kabuğu', 'limon suyu']"
  },
  {
    "Title": "Kuruyemişsiz Sade Baklava (Kuruyemiş Alerjisi)",
    "Ingredients": "['500 gram baklava yufkası', '250 gram tereyağı', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Yufkaları tepsiye sererek aralarına eritilmiş tereyağı sürün.\nTüm yufkaları dizdikten sonra dilimleyin.\nKalan tereyağını üzerine gezdirin.\n180 derece fırında 40 dakika pişirin.\nŞerbeti hazırlayıp sıcak baklavanın üzerine soğuk şerbet dökün.",
    "Image_Name": "kuruyemissiz-sade-baklava",
    "Cleaned_Ingredients": "['baklava yufkası', 'tereyağı', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Kuruyemişsiz Kadayıf (Kuruyemiş Alerjisi)",
    "Ingredients": "['500 gram tel kadayıf', '200 gram tereyağı', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tel kadayıfı tepsiye yayın.\nEritilmiş tereyağını gezdirin.\n180 derece fırında 35 dakika pişirin.\nŞerbeti hazırlayıp sıcak kadayıfa soğuk şerbet dökün.",
    "Image_Name": "kuruyemissiz-kadayif",
    "Cleaned_Ingredients": "['tel kadayıf', 'tereyağı', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Kuruyemişsiz Künefe (Kuruyemiş Alerjisi)",
    "Ingredients": "['500 gram tel kadayıf', '200 gram tereyağı', '250 gram künefe peyniri', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tel kadayıfı ince kıyın.\nEritilmiş tereyağıyla karıştırın.\nYarısını kalıba yayın.\nPeyniri dizin.\nKalan kadayıfı kapatın.\nKısık ateşte iki tarafını kızartın.\nŞerbeti hazırlayıp dökün.",
    "Image_Name": "kuruyemissiz-kunefe",
    "Cleaned_Ingredients": "['tel kadayıf', 'tereyağı', 'künefe peyniri', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Kuruyemişsiz Şekerpare (Kuruyemiş Alerjisi)",
    "Ingredients": "['2 su bardağı un', '100 gram tereyağı', '1 adet yumurta', '0.5 su bardağı irmik', '0.5 çay kaşığı kabartma tozu', '2 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tereyağını eritip unla karıştırın.\nYumurta, irmik ve kabartma tozunu ekleyin.\nHamuru yoğurup toplar yapın.\nTepsiye dizin.\n180 derece fırında 20 dakika pişirin.\nŞerbeti hazırlayıp dökün.",
    "Image_Name": "kuruyemissiz-sekerpare",
    "Cleaned_Ingredients": "['un', 'tereyağı', 'yumurta', 'irmik', 'kabartma tozu', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Kuruyemişsiz Kalburabastı (Kuruyemiş Alerjisi)",
    "Ingredients": "['2 su bardağı un', '100 gram tereyağı', '0.5 su bardağı irmik', '1 adet yumurta', '0.5 çay kaşığı kabartma tozu', '2 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tereyağını eritip un ve irmikle karıştırın.\nYumurta ve kabartma tozunu ekleyin.\nHamuru yoğurun.\nParçalar koparıp rende üzerinde şekil verin.\nTepsiye dizin.\n180 derece fırında 25 dakika pişirin.\nŞerbet dökün.",
    "Image_Name": "kuruyemissiz-kalburabasti",
    "Cleaned_Ingredients": "['un', 'tereyağı', 'irmik', 'yumurta', 'kabartma tozu', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Kuruyemişsiz İrmik Helvası (Kuruyemiş Alerjisi)",
    "Ingredients": "['2 su bardağı irmik', '100 gram tereyağı', '2 su bardağı süt', '1.5 su bardağı toz şeker']",
    "Instructions": "Tereyağında irmiği kızarana kadar kavurun.\nSütü ve şekeri ayrı tencerede kaynatın.\nSıcak sütlü karışımı irmiğe yavaşça ekleyin.\nKapağını kapatıp 5 dakika pişirin.\nKarıştırıp kaselere paylaştırın.",
    "Image_Name": "kuruyemissiz-irmik-helvasi",
    "Cleaned_Ingredients": "['irmik', 'tereyağı', 'süt', 'toz şeker']"
  },
  {
    "Title": "Glutensiz Şekerpare (Glutensiz)",
    "Ingredients": "['1 su bardağı mısır unu', '1 su bardağı badem unu', '100 gram tereyağı', '1 adet yumurta', '0.5 çay kaşığı kabartma tozu', '2 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tereyağını eritip mısır unu ve badem unuyla karıştırın.\nYumurta ve kabartma tozunu ekleyin.\nHamuru yoğurup toplar yapın.\nTepsiye dizin.\n180 derece fırında 20 dakika pişirin.\nŞerbeti hazırlayıp dökün.",
    "Image_Name": "glutensiz-sekerpare",
    "Cleaned_Ingredients": "['mısır unu', 'badem unu', 'tereyağı', 'yumurta', 'kabartma tozu', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Glutensiz Revani (Glutensiz)",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '1 su bardağı mısır unu', '0.5 su bardağı yoğurt', '1 paket kabartma tozu', '2.5 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Yumurta ve şekeri çırpın.\nYoğurdu ekleyin.\nMısır unu ve kabartma tozunu ilave edin.\nYağlanmış tepsiye dökün.\n180 derece fırında 30 dakika pişirin.\nŞerbeti hazırlayın.\nSıcak revaniye soğuk şerbet dökün.",
    "Image_Name": "glutensiz-revani",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'mısır unu', 'yoğurt', 'kabartma tozu', 'su', 'limon suyu']"
  },
  {
    "Title": "Glutensiz Islak Kek (Glutensiz)",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '1 su bardağı süt', '0.5 su bardağı sıvı yağ', '1.5 su bardağı mısır unu', '0.5 su bardağı pirinç unu', '3 yemek kaşığı kakao', '1 paket kabartma tozu', '1 paket vanilya', '1 su bardağı toz şeker', '1 su bardağı su', '2 yemek kaşığı kakao']",
    "Instructions": "Yumurta ve şekeri çırpın.\nSüt ve sıvı yağı ekleyin.\nMısır unu, pirinç unu, kakao, kabartma tozu ve vanilyayı ilave edin.\nYağlanmış tepsiye dökün.\n180 derece fırında 30 dakika pişirin.\nSos için şeker, su ve kakaoyu kaynatın.\nSıcak kekin üzerine dökün.",
    "Image_Name": "glutensiz-islak-kek",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'süt', 'sıvı yağ', 'mısır unu', 'pirinç unu', 'kakao', 'kabartma tozu', 'vanilya', 'su']"
  },
  {
    "Title": "Glutensiz Havuçlu Kek (Glutensiz)",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '0.5 su bardağı sıvı yağ', '1 su bardağı badem unu', '1 su bardağı mısır unu', '1 paket kabartma tozu', '2 adet havuç', '1 çay kaşığı tarçın', '1 paket vanilya']",
    "Instructions": "Yumurta ve şekeri çırpın.\nSıvı yağı ekleyin.\nBadem unu, mısır unu, kabartma tozu, tarçın ve vanilyayı ilave edin.\nHavuçları rendeleyin ve hamura karıştırın.\nYağlanmış kalıba dökün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "glutensiz-havuclu-kek",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'sıvı yağ', 'badem unu', 'mısır unu', 'kabartma tozu', 'havuç', 'tarçın', 'vanilya']"
  },
  {
    "Title": "Vegan Revani (Vegan)",
    "Ingredients": "['1 su bardağı irmik', '1 su bardağı un', '0.5 su bardağı toz şeker', '0.5 su bardağı sıvı yağ', '1 su bardağı portakal suyu', '1 paket kabartma tozu', '2.5 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "İrmik, un, şeker, sıvı yağ, portakal suyu ve kabartma tozunu karıştırın.\nYağlanmış tepsiye dökün.\n180 derece fırında 30 dakika pişirin.\nŞerbeti hazırlayın.\nSıcak revaniye soğuk şerbet dökün.",
    "Image_Name": "vegan-revani",
    "Cleaned_Ingredients": "['irmik', 'un', 'toz şeker', 'sıvı yağ', 'portakal suyu', 'kabartma tozu', 'su', 'limon suyu']"
  },
  {
    "Title": "Vegan Islak Kek (Vegan)",
    "Ingredients": "['1 su bardağı toz şeker', '1 su bardağı yulaf sütü', '0.5 su bardağı sıvı yağ', '2 su bardağı un', '3 yemek kaşığı kakao', '1 paket kabartma tozu', '1 paket vanilya', '1 yemek kaşığı sirke', '1 su bardağı toz şeker', '1 su bardağı su', '2 yemek kaşığı kakao']",
    "Instructions": "Şeker, yulaf sütü ve sıvı yağı karıştırın.\nUn, kakao, kabartma tozu ve vanilyayı ekleyin.\nSirkeyi ilave edin.\nYağlanmış tepsiye dökün.\n180 derece fırında 30 dakika pişirin.\nSos için şeker, su ve kakaoyu kaynatıp kekin üzerine dökün.",
    "Image_Name": "vegan-islak-kek",
    "Cleaned_Ingredients": "['toz şeker', 'yulaf sütü', 'sıvı yağ', 'un', 'kakao', 'kabartma tozu', 'vanilya', 'sirke', 'su']"
  },
  {
    "Title": "Vegan Lokma (Vegan)",
    "Ingredients": "['2 su bardağı un', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu', 'kızartma yağı']",
    "Instructions": "Un, maya, tuz, şeker ve ılık suyu yoğurun.\n30 dakika mayalanmaya bırakın.\nIslak elle parçalar koparıp kızgın yağda kızartın.\nŞerbeti hazırlayın.\nKızartılan lokmaları şerbete batırın.",
    "Image_Name": "vegan-lokma",
    "Cleaned_Ingredients": "['un', 'instant maya', 'tuz', 'toz şeker', 'su', 'limon suyu', 'kızartma yağı']"
  },
  {
    "Title": "Vegan Un Helvası (Vegan)",
    "Ingredients": "['2 su bardağı un', '100 gram margarin', '2 su bardağı su', '1.5 su bardağı toz şeker']",
    "Instructions": "Margarinde unu kızarana kadar kavurun.\nSuyu ve şekeri ayrı tencerede kaynatın.\nSıcak şerbet karışımını helva hamuruna yavaşça ekleyin.\nKapağını kapatıp kısık ateşte 5 dakika pişirin.\nKaselere paylaştırıp servis yapın.",
    "Image_Name": "vegan-un-helvasi",
    "Cleaned_Ingredients": "['un', 'margarin', 'su', 'toz şeker']"
  },
  {
    "Title": "Vegan Limonlu Kek (Vegan)",
    "Ingredients": "['1 su bardağı toz şeker', '0.5 su bardağı sıvı yağ', '1 su bardağı yulaf sütü', '2 su bardağı un', '1 paket kabartma tozu', '1 adet limon kabuğu rendesi', '2 yemek kaşığı limon suyu', '1 yemek kaşığı sirke']",
    "Instructions": "Şeker ve sıvı yağı karıştırın.\nYulaf sütünü ekleyin.\nUn, kabartma tozu ve limon kabuğu rendesini ilave edin.\nLimon suyu ve sirkeyi ekleyin.\nYağlanmış kalıba dökün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "vegan-limonlu-kek",
    "Cleaned_Ingredients": "['toz şeker', 'sıvı yağ', 'yulaf sütü', 'un', 'kabartma tozu', 'limon kabuğu', 'limon suyu', 'sirke']"
  },
  {
    "Title": "Vegan Un Kurabiyesi (Vegan)",
    "Ingredients": "['250 gram margarin', '1 su bardağı pudra şekeri', '3.5 su bardağı un', '1 paket vanilya']",
    "Instructions": "Margarini oda sıcaklığında yumuşatın.\nPudra şekerini ekleyip çırpın.\nVanilyayı ilave edin.\nUnu azar azar ekleyip yoğurun.\nŞekil verin ve tepsiye dizin.\n170 derece fırında 15 dakika pişirin.\nSoğuyunca pudra şekeri serpin.",
    "Image_Name": "vegan-un-kurabiyesi",
    "Cleaned_Ingredients": "['margarin', 'pudra şekeri', 'un', 'vanilya']"
  },
  {
    "Title": "Vegan Mozaik Pasta (Vegan)",
    "Ingredients": "['200 gram vegan bisküvi', '100 gram margarin', '3 yemek kaşığı kakao', '0.5 su bardağı yulaf sütü', '0.5 su bardağı toz şeker', '1 paket vanilya']",
    "Instructions": "Vegan bisküvileri kırın.\nMargarini eritin.\nYulaf sütü, şeker ve kakaoyu karıştırıp kaynatın.\nMargarini ekleyin.\nVanilyayı ilave edin.\nKırık bisküvileri karışıma ekleyin.\nStreç filme sararak rulo yapın.\nBuzdolabında 3 saat bekletin.",
    "Image_Name": "vegan-mozaik-pasta",
    "Cleaned_Ingredients": "['vegan bisküvi', 'margarin', 'kakao', 'yulaf sütü', 'toz şeker', 'vanilya']"
  },
  {
    "Title": "Süt Ürünsüz Baklava (Süt Ürünü Yok)",
    "Ingredients": "['500 gram baklava yufkası', '250 gram margarin', '300 gram ceviz', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Yufkaları tepsiye sererek aralarına eritilmiş margarin sürün.\nHer 3-4 yufkada bir ceviz serpin.\nTüm yufkaları dizdikten sonra dilimleyin.\nKalan margarini üzerine gezdirin.\n180 derece fırında 40 dakika pişirin.\nŞerbeti hazırlayıp sıcak baklavanın üzerine soğuk şerbet dökün.",
    "Image_Name": "sut-urunsuz-baklava",
    "Cleaned_Ingredients": "['baklava yufkası', 'margarin', 'ceviz', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Süt Ürünsüz Kadayıf (Süt Ürünü Yok)",
    "Ingredients": "['500 gram tel kadayıf', '200 gram margarin', '250 gram ceviz', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tel kadayıfı ikiye bölün.\nYarısını tepsiye yayın.\nEritilmiş margarinin yarısını gezdirin.\nCevizi serpin.\nKalan kadayıfı kapatın.\nKalan margarini dökün.\n180 derece fırında 35 dakika pişirin.\nŞerbeti hazırlayıp sıcak kadayıfa dökün.",
    "Image_Name": "sut-urunsuz-kadayif",
    "Cleaned_Ingredients": "['tel kadayıf', 'margarin', 'ceviz', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Süt Ürünsüz Şekerpare (Süt Ürünü Yok)",
    "Ingredients": "['2 su bardağı un', '100 gram margarin', '1 adet yumurta', '0.5 su bardağı irmik', '0.5 çay kaşığı kabartma tozu', '2 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Margarini eritip unla karıştırın.\nYumurta, irmik ve kabartma tozunu ekleyin.\nHamuru yoğurup toplar yapın.\nTepsiye dizin.\n180 derece fırında 20 dakika pişirin.\nŞerbeti hazırlayıp dökün.",
    "Image_Name": "sut-urunsuz-sekerpare",
    "Cleaned_Ingredients": "['un', 'margarin', 'yumurta', 'irmik', 'kabartma tozu', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Süt Ürünsüz Islak Kek (Süt Ürünü Yok)",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '1 su bardağı yulaf sütü', '0.5 su bardağı sıvı yağ', '2 su bardağı un', '3 yemek kaşığı kakao', '1 paket kabartma tozu', '1 paket vanilya', '1 su bardağı toz şeker', '1 su bardağı su', '2 yemek kaşığı kakao']",
    "Instructions": "Yumurta ve şekeri çırpın.\nYulaf sütü ve sıvı yağı ekleyin.\nUn, kakao, kabartma tozu ve vanilyayı ilave edin.\nYağlanmış tepsiye dökün.\n180 derece fırında 30 dakika pişirin.\nSos için şeker, su ve kakaoyu kaynatıp kekin üzerine dökün.",
    "Image_Name": "sut-urunsuz-islak-kek",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'yulaf sütü', 'sıvı yağ', 'un', 'kakao', 'kabartma tozu', 'vanilya', 'su']"
  },
  {
    "Title": "Süt Ürünsüz İrmik Helvası (Süt Ürünü Yok)",
    "Ingredients": "['2 su bardağı irmik', '100 gram margarin', '2 su bardağı yulaf sütü', '1.5 su bardağı toz şeker']",
    "Instructions": "Margarinde irmiği kızarana kadar kavurun.\nYulaf sütünü ve şekeri ayrı tencerede kaynatın.\nSıcak sütlü karışımı irmiğe yavaşça ekleyin.\nKapağını kapatıp 5 dakika pişirin.\nKarıştırıp kaselere paylaştırın.",
    "Image_Name": "sut-urunsuz-irmik-helvasi",
    "Cleaned_Ingredients": "['irmik', 'margarin', 'yulaf sütü', 'toz şeker']"
  },
  {
    "Title": "Glutensiz Vegan Revani (Glutensiz & Vegan)",
    "Ingredients": "['1 su bardağı mısır unu', '0.5 su bardağı toz şeker', '0.5 su bardağı sıvı yağ', '1 su bardağı portakal suyu', '1 paket kabartma tozu', '2.5 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Mısır unu, şeker, sıvı yağ, portakal suyu ve kabartma tozunu karıştırın.\nYağlanmış tepsiye dökün.\n180 derece fırında 30 dakika pişirin.\nŞerbeti hazırlayın.\nSıcak revaniye soğuk şerbet dökün.",
    "Image_Name": "glutensiz-vegan-revani",
    "Cleaned_Ingredients": "['mısır unu', 'toz şeker', 'sıvı yağ', 'portakal suyu', 'kabartma tozu', 'su', 'limon suyu']"
  },
  {
    "Title": "Glutensiz Vegan Islak Kek (Glutensiz & Vegan)",
    "Ingredients": "['1 su bardağı toz şeker', '1 su bardağı yulaf sütü', '0.5 su bardağı sıvı yağ', '1 su bardağı mısır unu', '0.5 su bardağı pirinç unu', '3 yemek kaşığı kakao', '1 paket kabartma tozu', '1 paket vanilya', '1 yemek kaşığı sirke', '1 su bardağı toz şeker', '1 su bardağı su', '2 yemek kaşığı kakao']",
    "Instructions": "Şeker, yulaf sütü ve sıvı yağı karıştırın.\nMısır unu, pirinç unu, kakao, kabartma tozu ve vanilyayı ekleyin.\nSirkeyi ilave edin.\nYağlanmış tepsiye dökün.\n180 derece fırında 30 dakika pişirin.\nSos için şeker, su ve kakaoyu kaynatıp dökün.",
    "Image_Name": "glutensiz-vegan-islak-kek",
    "Cleaned_Ingredients": "['toz şeker', 'yulaf sütü', 'sıvı yağ', 'mısır unu', 'pirinç unu', 'kakao', 'kabartma tozu', 'vanilya', 'sirke', 'su']"
  },
  {
    "Title": "Glutensiz Un Kurabiyesi (Glutensiz)",
    "Ingredients": "['250 gram tereyağı', '1 su bardağı pudra şekeri', '2 su bardağı mısır unu', '1 su bardağı pirinç unu', '1 paket vanilya']",
    "Instructions": "Tereyağını oda sıcaklığında yumuşatın.\nPudra şekerini ekleyip çırpın.\nVanilyayı ilave edin.\nMısır unu ve pirinç ununu azar azar ekleyip yoğurun.\nŞekil verin ve tepsiye dizin.\n170 derece fırında 15 dakika pişirin.\nSoğuyunca pudra şekeri serpin.",
    "Image_Name": "glutensiz-un-kurabiyesi",
    "Cleaned_Ingredients": "['tereyağı', 'pudra şekeri', 'mısır unu', 'pirinç unu', 'vanilya']"
  },
  {
    "Title": "Vegan Havuçlu Kek (Vegan)",
    "Ingredients": "['1 su bardağı toz şeker', '0.5 su bardağı sıvı yağ', '0.5 su bardağı yulaf sütü', '2 su bardağı un', '1 paket kabartma tozu', '2 adet havuç', '1 çay kaşığı tarçın', '1 paket vanilya', '1 yemek kaşığı sirke']",
    "Instructions": "Şeker ve sıvı yağı karıştırın.\nYulaf sütünü ekleyin.\nUn, kabartma tozu, tarçın ve vanilyayı ilave edin.\nSirkeyi ekleyin.\nHavuçları rendeleyin ve hamura karıştırın.\nYağlanmış kalıba dökün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "vegan-havuclu-kek",
    "Cleaned_Ingredients": "['toz şeker', 'sıvı yağ', 'yulaf sütü', 'un', 'kabartma tozu', 'havuç', 'tarçın', 'vanilya', 'sirke']"
  },
  {
    "Title": "Sobiyet",
    "Ingredients": "['500 gram baklava yufkası', '200 gram tereyağı', '200 gram antep fıstığı', '1 litre süt', '0.5 su bardağı toz şeker', '3 yemek kaşığı nişasta', '1 paket vanilya', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Süt, şeker ve nişastayla muhallebi yapıp soğutun.\nYufkaları üçgen şeklinde kesin.\nAralarına tereyağı sürün.\nMuhallebi ve antep fıstığı koyarak sarın.\nTepsiye dizin.\n180 derece fırında 30 dakika pişirin.\nŞerbeti hazırlayıp dökün.",
    "Image_Name": "sobiyet",
    "Cleaned_Ingredients": "['baklava yufkası', 'tereyağı', 'antep fıstığı', 'süt', 'toz şeker', 'nişasta', 'vanilya', 'su', 'limon suyu']"
  },
  {
    "Title": "Cevizli Kek",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '0.5 su bardağı sıvı yağ', '0.5 su bardağı süt', '2 su bardağı un', '1 paket kabartma tozu', '100 gram ceviz', '1 çay kaşığı tarçın', '1 paket vanilya']",
    "Instructions": "Yumurta ve şekeri çırpın.\nSıvı yağ ve sütü ekleyin.\nUn, kabartma tozu, tarçın ve vanilyayı ilave edin.\nCevizleri kırıp hamura karıştırın.\nYağlanmış kalıba dökün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "cevizli-kek",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'sıvı yağ', 'süt', 'un', 'kabartma tozu', 'ceviz', 'tarçın', 'vanilya']"
  },
  {
    "Title": "Kabak Tatlısı",
    "Ingredients": "['1 kg kabak', '2 su bardağı toz şeker', '100 gram ceviz', '2 yemek kaşığı tahin']",
    "Instructions": "Kabağı dilimleyin.\nŞekeri kabakların üzerine serpin.\nBir gece bekletin.\nKısık ateşte kendi suyuyla pişirin.\nTabağa alıp ceviz ve tahin ile servis yapın.",
    "Image_Name": "kabak-tatlisi",
    "Cleaned_Ingredients": "['kabak', 'toz şeker', 'ceviz', 'tahin']"
  },
  {
    "Title": "Kemalpaşa Tatlısı",
    "Ingredients": "['250 gram taze kaşar peyniri', '2 su bardağı un', '1 adet yumurta', '1 çay kaşığı kabartma tozu', '2.5 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu', 'kızartma yağı']",
    "Instructions": "Peyniri rendeleyin.\nUn, yumurta ve kabartma tozuyla yoğurun.\nKüçük toplar yapın.\nKızgın yağda kızartın.\nŞeker ve sudan şerbet yapıp limon suyu ekleyin.\nKızartılmış topları sıcak şerbete atın.\n15 dakika şerbeti emmeye bırakın.",
    "Image_Name": "kemalpasa-tatlisi",
    "Cleaned_Ingredients": "['taze kaşar peyniri', 'un', 'yumurta', 'kabartma tozu', 'toz şeker', 'su', 'limon suyu', 'kızartma yağı']"
  },
  {
    "Title": "Kuruyemişsiz Ekmek Kadayıfı (Kuruyemiş Alerjisi)",
    "Ingredients": "['6 dilim bayat ekmek', '200 gram tereyağı', '2.5 su bardağı toz şeker', '2 su bardağı su', '1 yemek kaşığı limon suyu', '1 su bardağı kaymak']",
    "Instructions": "Ekmeklerin kabuklarını soyun.\nTereyağında iki tarafını kızartın.\nŞerbet yapıp kızartılmış ekmekleri batırın.\nTabağa alıp üzerine kaymak koyarak servis yapın.",
    "Image_Name": "kuruyemissiz-ekmek-kadayifi",
    "Cleaned_Ingredients": "['bayat ekmek', 'tereyağı', 'toz şeker', 'su', 'limon suyu', 'kaymak']"
  },
  {
    "Title": "Glutensiz Limonlu Kek (Glutensiz)",
    "Ingredients": "['3 adet yumurta', '1 su bardağı toz şeker', '0.5 su bardağı sıvı yağ', '0.5 su bardağı süt', '1 su bardağı mısır unu', '1 su bardağı pirinç unu', '1 paket kabartma tozu', '1 adet limon kabuğu rendesi', '2 yemek kaşığı limon suyu']",
    "Instructions": "Yumurta ve şekeri çırpın.\nSıvı yağ ve sütü ekleyin.\nMısır unu, pirinç unu, kabartma tozu, limon kabuğu rendesi ve limon suyunu ilave edin.\nYağlanmış kalıba dökün.\n180 derece fırında 35 dakika pişirin.",
    "Image_Name": "glutensiz-limonlu-kek",
    "Cleaned_Ingredients": "['yumurta', 'toz şeker', 'sıvı yağ', 'süt', 'mısır unu', 'pirinç unu', 'kabartma tozu', 'limon kabuğu', 'limon suyu']"
  },
  {
    "Title": "Süt Ürünsüz Künefe (Süt Ürünü Yok)",
    "Ingredients": "['500 gram tel kadayıf', '200 gram margarin', '250 gram tuzsuz lor', '2 su bardağı toz şeker', '1.5 su bardağı su', '1 yemek kaşığı limon suyu']",
    "Instructions": "Tel kadayıfı ince kıyın.\nEritilmiş margarinle karıştırın.\nYarısını kalıba yayın.\nTuzsuz loru dizin.\nKalan kadayıfı kapatın.\nKısık ateşte iki tarafını kızartın.\nŞerbeti hazırlayıp dökün.",
    "Image_Name": "sut-urunsuz-kunefe",
    "Cleaned_Ingredients": "['tel kadayıf', 'margarin', 'tuzsuz lor', 'toz şeker', 'su', 'limon suyu']"
  },
  {
    "Title": "Vegan Kabak Tatlısı (Vegan & Glutensiz)",
    "Ingredients": "['1 kg kabak', '2 su bardağı toz şeker', '2 yemek kaşığı tahin']",
    "Instructions": "Kabağı dilimleyin.\nŞekeri kabakların üzerine serpin.\nBir gece bekletin.\nKısık ateşte kendi suyuyla pişirin.\nTabağa alıp tahin gezdirerek servis yapın.",
    "Image_Name": "vegan-kabak-tatlisi",
    "Cleaned_Ingredients": "['kabak', 'toz şeker', 'tahin']"
  },
  {
    "Title": "Kokoreç",
    "Ingredients": "['500 gram kuzu bağırsak', '3 adet sivri biber', '2 adet domates', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon', '1 çay kaşığı kekik', '2 adet ekmek arası']",
    "Instructions": "Bağırsakları iyice yıkayıp şişe sarın.\nKömür ateşinde veya fırında çevirerek pişirin.\nPişen kokoreçi ince ince kıyın.\nBiberleri ve domatesleri doğrayıp karıştırın.\nBaharatları ekleyin.\nEkmek arasına koyup servis yapın.",
    "Image_Name": "kokorec",
    "Cleaned_Ingredients": "['kuzu bağırsak', 'sivri biber', 'domates', 'tuz', 'pul biber', 'kimyon', 'kekik', 'ekmek']"
  },
  {
    "Title": "Sokak Midye Dolma",
    "Ingredients": "['30 adet midye', '1 su bardağı pirinç', '2 adet soğan', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı dolmalık fıstık', '1 çay kaşığı tarçın', '1 çay kaşığı karabiber', '1 çay kaşığı tuz']",
    "Instructions": "Midyeleri fırçalayıp temizleyin.\nSoğanı yemeklik doğrayıp zeytinyağında kavurun.\nPirinci, fıstığı ve baharatları ekleyin.\nKavurun.\nMidyelerin içine harcı doldurun.\nTencereye sıkıca dizin.\nÜzerini geçecek kadar su ekleyin.\nKısık ateşte 30 dakika pişirin.",
    "Image_Name": "sokak-midye-dolma",
    "Cleaned_Ingredients": "['midye', 'pirinç', 'soğan', 'zeytinyağı', 'dolmalık fıstık', 'tarçın', 'karabiber', 'tuz']"
  },
  {
    "Title": "Islak Hamburger",
    "Ingredients": "['4 adet hamburger ekmeği', '300 gram dana kıyma', '1 adet soğan', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '2 yemek kaşığı tereyağı', '2 yemek kaşığı domates salçası', '1 diş sarımsak', '1 su bardağı su']",
    "Instructions": "Kıymayı soğan, tuz ve karabiberle yoğurun.\nKöfteler yapıp pişirin.\nEkmeklerin arasına koyun.\nTereyağı, salça, sarımsak ve suyla sos yapın.\nHamburgerleri buharlı tencereye dizin.\nSosu üzerlerine gezdirin.\n10 dakika buharda bekletin.",
    "Image_Name": "islak-hamburger",
    "Cleaned_Ingredients": "['hamburger ekmeği', 'dana kıyma', 'soğan', 'tuz', 'karabiber', 'tereyağı', 'domates salçası', 'sarımsak', 'su']"
  },
  {
    "Title": "Tantuni",
    "Ingredients": "['500 gram dana eti', '2 adet soğan', '3 adet domates', '3 adet sivri biber', '2 yemek kaşığı sıvı yağ', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '4 adet lavaş']",
    "Instructions": "Eti ince ince doğrayın.\nSıvı yağda yüksek ateşte kavurun.\nSoğanları ince doğrayıp ekleyin.\nBiberleri ve domatesleri ilave edin.\nBaharatları ekleyin.\nLavaşın içine sararak servis yapın.",
    "Image_Name": "tantuni",
    "Cleaned_Ingredients": "['dana eti', 'soğan', 'domates', 'sivri biber', 'sıvı yağ', 'tuz', 'karabiber', 'pul biber', 'lavaş']"
  },
  {
    "Title": "Kumpir",
    "Ingredients": "['4 adet büyük patates', '100 gram tereyağı', '100 gram kaşar peyniri', '4 yemek kaşığı mısır', '4 yemek kaşığı bezelye', '100 gram sosis', '4 yemek kaşığı turşu', '2 yemek kaşığı mayonez', '1 çay kaşığı tuz']",
    "Instructions": "Patatesleri yıkayıp fırında pişirin.\nOrtalarını kesin.\nİçlerini kaşıkla çıkarıp tereyağı ve kaşar ile ezin.\nGeri doldurun.\nÜzerine mısır, bezelye, sosis, turşu ve mayonez ekleyin.",
    "Image_Name": "kumpir",
    "Cleaned_Ingredients": "['patates', 'tereyağı', 'kaşar peyniri', 'mısır', 'bezelye', 'sosis', 'turşu', 'mayonez', 'tuz']"
  },
  {
    "Title": "Döner Dürüm",
    "Ingredients": "['500 gram kuzu eti', '1 adet soğan', '2 adet domates', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', '1 çay kaşığı pul biber', '4 adet lavaş', '2 adet yeşil biber']",
    "Instructions": "Kuzu etini ince ince dilimleyin.\nBaharatlarla marine edin.\nDöner şişine veya tavaya alıp pişirin.\nLavaşın üzerine eti koyun.\nDomates, soğan ve biber ekleyin.\nSararak servis yapın.",
    "Image_Name": "doner-durum",
    "Cleaned_Ingredients": "['kuzu eti', 'soğan', 'domates', 'tuz', 'karabiber', 'kimyon', 'pul biber', 'lavaş', 'yeşil biber']"
  },
  {
    "Title": "Balık Ekmek",
    "Ingredients": "['4 adet uskumru fileto', '2 yemek kaşığı un', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '3 yemek kaşığı zeytinyağı', '4 adet ekmek arası', '1 adet soğan', '2 adet domates', '1 adet marul']",
    "Instructions": "Balıkları un, tuz ve karabiberle harmanlayın.\nZeytinyağında kızartın.\nEkmekleri ikiye kesin.\nMarul, domates ve soğan dilimleyin.\nBalıkları ekmek arasına koyun.\nSebzeleri ekleyin.",
    "Image_Name": "balik-ekmek",
    "Cleaned_Ingredients": "['uskumru fileto', 'un', 'tuz', 'karabiber', 'zeytinyağı', 'ekmek', 'soğan', 'domates', 'marul']"
  },
  {
    "Title": "Kahvaltı Menemen",
    "Ingredients": "['4 adet yumurta', '3 adet domates', '2 adet sivri biber', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Soğanı zeytinyağında kavurun.\nBiberleri doğrayıp ekleyin.\nDomatesleri rendeleyin ve ilave edin.\nBaharatları ekleyin.\nDomatesler suyunu salıp pişince yumurtaları kırın.\nYavaşça karıştırarak kıvamına gelene kadar pişirin.",
    "Image_Name": "kahvalti-menemen",
    "Cleaned_Ingredients": "['yumurta', 'domates', 'sivri biber', 'soğan', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Kuymak",
    "Ingredients": "['3 yemek kaşığı tereyağı', '3 yemek kaşığı mısır unu', '200 gram Trabzon peyniri', '1 su bardağı su', '1 çay kaşığı tuz']",
    "Instructions": "Tereyağını tencerede eritin.\nMısır ununu ekleyip kavurun.\nSuyu azar azar ekleyerek karıştırın.\nPeyniri ilave edin.\nUzayıp çekilene kadar karıştırarak pişirin.\nSıcak servis yapın.",
    "Image_Name": "kuymak",
    "Cleaned_Ingredients": "['tereyağı', 'mısır unu', 'Trabzon peyniri', 'su', 'tuz']"
  },
  {
    "Title": "Pişi",
    "Ingredients": "['3 su bardağı un', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '0.5 su bardağı yoğurt', 'kızartma yağı']",
    "Instructions": "Un, maya, tuz, şeker, su ve yoğurdu yoğurun.\n30 dakika mayalandırın.\nParçalar koparıp yuvarlak açın.\nKızgın yağda kızartın.\nKağıt havluyla yağını alın.",
    "Image_Name": "pisi",
    "Cleaned_Ingredients": "['un', 'instant maya', 'tuz', 'toz şeker', 'su', 'yoğurt', 'kızartma yağı']"
  },
  {
    "Title": "Sucuklu Yumurta",
    "Ingredients": "['200 gram sucuk', '4 adet yumurta', '1 yemek kaşığı tereyağı', '1 çay kaşığı pul biber']",
    "Instructions": "Sucuğu dilimleyin.\nTereyağında sucukları kızartın.\nYumurtaları kırıp üzerine ekleyin.\nPul biber serpin.\nYumurtalar pişene kadar bekleyin.",
    "Image_Name": "sucuklu-yumurta",
    "Cleaned_Ingredients": "['sucuk', 'yumurta', 'tereyağı', 'pul biber']"
  },
  {
    "Title": "Poşe Yumurtalı Çılbır",
    "Ingredients": "['4 adet yumurta', '1 su bardağı yoğurt', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber', '1 yemek kaşığı sirke', '1 çay kaşığı tuz']",
    "Instructions": "Suyu kaynatıp sirke ekleyin.\nYumurtaları teker teker poşe yapın.\nYoğurdu sarımsakla karıştırıp tabağa yayın.\nPoşe yumurtaları üzerine koyun.\nTereyağını kızdırıp pul biber ekleyin.\nYumurtaların üzerine gezdirin.",
    "Image_Name": "pose-yumurtali-cilbir",
    "Cleaned_Ingredients": "['yumurta', 'yoğurt', 'tereyağı', 'pul biber', 'sirke', 'tuz']"
  },
  {
    "Title": "Sokak Simidi",
    "Ingredients": "['4 su bardağı un', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '0.5 su bardağı pekmez', '2 su bardağı susam']",
    "Instructions": "Un, maya, tuz, şeker ve ılık suyu yoğurun.\n30 dakika mayalandırın.\nParçalara bölüp uzun fitiller yapın.\nHalka şekli verin.\nPekmezli suya batırın.\nSusama bulayın.\n220 derece fırında 20 dakika pişirin.",
    "Image_Name": "sokak-simidi",
    "Cleaned_Ingredients": "['un', 'instant maya', 'tuz', 'toz şeker', 'su', 'pekmez', 'susam']"
  },
  {
    "Title": "Vegan Kokoreç (Vegan)",
    "Ingredients": "['500 gram istiridye mantarı', '3 adet sivri biber', '2 adet domates', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon', '1 çay kaşığı kekik', '2 adet ekmek arası']",
    "Instructions": "Mantarları ince ince kıyın.\nZeytinyağında yüksek ateşte kavurun.\nBiberleri ve domatesleri doğrayıp ekleyin.\nBaharatları ilave edin.\nKarıştırarak pişirin.\nEkmek arasına koyup servis yapın.",
    "Image_Name": "vegan-kokorec",
    "Cleaned_Ingredients": "['istiridye mantarı', 'sivri biber', 'domates', 'zeytinyağı', 'tuz', 'pul biber', 'kimyon', 'kekik', 'ekmek']"
  },
  {
    "Title": "Vegan Midye Dolma (Vegan)",
    "Ingredients": "['8 adet patlıcan', '1 su bardağı pirinç', '2 adet soğan', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tarçın', '1 çay kaşığı karabiber', '1 çay kaşığı tuz', '1 yemek kaşığı domates salçası']",
    "Instructions": "Patlıcanları boyuna yarın.\nİçlerini oyun.\nSoğanı zeytinyağında kavurun.\nPirinci, salçayı ve baharatları ekleyin.\nHarcı patlıcanlara doldurun.\nTencereye dizin.\nÜzerini geçecek kadar su ekleyin.\nKısık ateşte 35 dakika pişirin.",
    "Image_Name": "vegan-midye-dolma",
    "Cleaned_Ingredients": "['patlıcan', 'pirinç', 'soğan', 'zeytinyağı', 'tarçın', 'karabiber', 'tuz', 'domates salçası']"
  },
  {
    "Title": "Vegan Tantuni (Vegan)",
    "Ingredients": "['300 gram soya kıyma', '2 adet soğan', '3 adet domates', '3 adet sivri biber', '2 yemek kaşığı sıvı yağ', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '4 adet lavaş']",
    "Instructions": "Soya kıymayı sıcak suda ıslatıp süzün.\nSıvı yağda yüksek ateşte kavurun.\nSoğanları ince doğrayıp ekleyin.\nBiberleri ve domatesleri ilave edin.\nBaharatları ekleyin.\nLavaşın içine sararak servis yapın.",
    "Image_Name": "vegan-tantuni",
    "Cleaned_Ingredients": "['soya kıyma', 'soğan', 'domates', 'sivri biber', 'sıvı yağ', 'tuz', 'karabiber', 'pul biber', 'lavaş']"
  },
  {
    "Title": "Vegan Kumpir (Vegan & Glutensiz)",
    "Ingredients": "['4 adet büyük patates', '3 yemek kaşığı zeytinyağı', '4 yemek kaşığı mısır', '4 yemek kaşığı bezelye', '4 yemek kaşığı turşu', '2 yemek kaşığı domates salçası', '1 çay kaşığı tuz']",
    "Instructions": "Patatesleri yıkayıp fırında pişirin.\nOrtalarını kesin.\nİçlerini kaşıkla çıkarıp zeytinyağı ile ezin.\nGeri doldurun.\nÜzerine mısır, bezelye, turşu ve salça ekleyin.",
    "Image_Name": "vegan-kumpir",
    "Cleaned_Ingredients": "['patates', 'zeytinyağı', 'mısır', 'bezelye', 'turşu', 'domates salçası', 'tuz']"
  },
  {
    "Title": "Tofulu Vegan Menemen (Vegan & Glutensiz)",
    "Ingredients": "['200 gram tofu', '3 adet domates', '2 adet sivri biber', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı zerdeçal', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Soğanı zeytinyağında kavurun.\nBiberleri doğrayıp ekleyin.\nDomatesleri rendeleyin ve ilave edin.\nBaharatları ekleyin.\nTofuyu ufalayıp ekleyin.\nZerdeçal ilave edin.\nKarıştırarak 5 dakika pişirin.",
    "Image_Name": "tofulu-vegan-menemen",
    "Cleaned_Ingredients": "['tofu', 'domates', 'sivri biber', 'soğan', 'zeytinyağı', 'zerdeçal', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Vegan Kuymak (Vegan & Glutensiz)",
    "Ingredients": "['3 yemek kaşığı margarin', '3 yemek kaşığı mısır unu', '200 gram vegan kaşar', '1 su bardağı yulaf sütü', '1 çay kaşığı tuz']",
    "Instructions": "Margarini tencerede eritin.\nMısır ununu ekleyip kavurun.\nYulaf sütünü azar azar ekleyerek karıştırın.\nVegan kaşarı ilave edin.\nUzayıp çekilene kadar karıştırarak pişirin.\nSıcak servis yapın.",
    "Image_Name": "vegan-kuymak",
    "Cleaned_Ingredients": "['margarin', 'mısır unu', 'vegan kaşar', 'yulaf sütü', 'tuz']"
  },
  {
    "Title": "Glutensiz Pişi (Glutensiz)",
    "Ingredients": "['2 su bardağı mısır unu', '1 su bardağı pirinç unu', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '0.5 su bardağı yoğurt', 'kızartma yağı']",
    "Instructions": "Mısır unu, pirinç unu, maya, tuz, şeker, su ve yoğurdu yoğurun.\n30 dakika mayalandırın.\nParçalar koparıp yuvarlak şekil verin.\nKızgın yağda kızartın.\nKağıt havluyla yağını alın.",
    "Image_Name": "glutensiz-pisi",
    "Cleaned_Ingredients": "['mısır unu', 'pirinç unu', 'instant maya', 'tuz', 'toz şeker', 'su', 'yoğurt', 'kızartma yağı']"
  },
  {
    "Title": "Glutensiz Islak Hamburger (Glutensiz)",
    "Ingredients": "['4 adet glutensiz hamburger ekmeği', '300 gram dana kıyma', '1 adet soğan', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '2 yemek kaşığı tereyağı', '2 yemek kaşığı domates salçası', '1 diş sarımsak', '1 su bardağı su']",
    "Instructions": "Kıymayı soğan, tuz ve karabiberle yoğurun.\nKöfteler yapıp pişirin.\nGlutensiz ekmeklerin arasına koyun.\nTereyağı, salça, sarımsak ve suyla sos yapın.\nHamburgerleri buharlı tencereye dizin.\nSosu gezdirip 10 dakika buharda bekletin.",
    "Image_Name": "glutensiz-islak-hamburger",
    "Cleaned_Ingredients": "['glutensiz hamburger ekmeği', 'dana kıyma', 'soğan', 'tuz', 'karabiber', 'tereyağı', 'domates salçası', 'sarımsak', 'su']"
  },
  {
    "Title": "Süt Ürünsüz Kumpir (Süt Ürünü Yok)",
    "Ingredients": "['4 adet büyük patates', '3 yemek kaşığı zeytinyağı', '4 yemek kaşığı mısır', '4 yemek kaşığı bezelye', '100 gram sosis', '4 yemek kaşığı turşu', '1 çay kaşığı tuz']",
    "Instructions": "Patatesleri yıkayıp fırında pişirin.\nOrtalarını kesin.\nİçlerini kaşıkla çıkarıp zeytinyağı ile ezin.\nGeri doldurun.\nÜzerine mısır, bezelye, sosis ve turşu ekleyin.",
    "Image_Name": "sut-urunsuz-kumpir",
    "Cleaned_Ingredients": "['patates', 'zeytinyağı', 'mısır', 'bezelye', 'sosis', 'turşu', 'tuz']"
  },
  {
    "Title": "Süt Ürünsüz Kuymak (Süt Ürünü Yok & Glutensiz)",
    "Ingredients": "['3 yemek kaşığı margarin', '3 yemek kaşığı mısır unu', '200 gram vegan kaşar', '1 su bardağı yulaf sütü', '1 çay kaşığı tuz']",
    "Instructions": "Margarini tencerede eritin.\nMısır ununu ekleyip kavurun.\nYulaf sütünü azar azar ekleyerek karıştırın.\nVegan kaşarı ilave edin.\nUzayıp çekilene kadar karıştırarak pişirin.\nSıcak servis yapın.",
    "Image_Name": "sut-urunsuz-kuymak",
    "Cleaned_Ingredients": "['margarin', 'mısır unu', 'vegan kaşar', 'yulaf sütü', 'tuz']"
  },
  {
    "Title": "Süt Ürünsüz Çılbır (Süt Ürünü Yok)",
    "Ingredients": "['4 adet yumurta', '1 su bardağı soya yoğurt', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı pul biber', '1 yemek kaşığı sirke', '1 çay kaşığı tuz']",
    "Instructions": "Suyu kaynatıp sirke ekleyin.\nYumurtaları teker teker poşe yapın.\nSoya yoğurdu tabağa yayın.\nPoşe yumurtaları üzerine koyun.\nZeytinyağını kızdırıp pul biber ekleyin.\nYumurtaların üzerine gezdirin.",
    "Image_Name": "sut-urunsuz-cilbir",
    "Cleaned_Ingredients": "['yumurta', 'soya yoğurt', 'zeytinyağı', 'pul biber', 'sirke', 'tuz']"
  },
  {
    "Title": "Vejetaryen Menemen (Vejetaryen)",
    "Ingredients": "['4 adet yumurta', '3 adet domates', '2 adet sivri biber', '1 adet soğan', '100 gram lor peyniri', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Soğanı zeytinyağında kavurun.\nBiberleri doğrayıp ekleyin.\nDomatesleri rendeleyin ve ilave edin.\nBaharatları ekleyin.\nYumurtaları kırıp karıştırın.\nLor peynirini ufalayıp üzerine serpin.",
    "Image_Name": "vejetaryen-menemen",
    "Cleaned_Ingredients": "['yumurta', 'domates', 'sivri biber', 'soğan', 'lor peyniri', 'zeytinyağı', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Pişi (Vegan)",
    "Ingredients": "['3 su bardağı un', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '2 yemek kaşığı sıvı yağ', 'kızartma yağı']",
    "Instructions": "Un, maya, tuz, şeker, su ve sıvı yağı yoğurun.\n30 dakika mayalandırın.\nParçalar koparıp yuvarlak açın.\nKızgın yağda kızartın.\nKağıt havluyla yağını alın.",
    "Image_Name": "vegan-pisi",
    "Cleaned_Ingredients": "['un', 'instant maya', 'tuz', 'toz şeker', 'su', 'sıvı yağ', 'kızartma yağı']"
  },
  {
    "Title": "Vegan Susamlı Simit (Vegan)",
    "Ingredients": "['4 su bardağı un', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '2 yemek kaşığı sıvı yağ', '0.5 su bardağı pekmez', '2 su bardağı susam']",
    "Instructions": "Un, maya, tuz, şeker, su ve sıvı yağı yoğurun.\n30 dakika mayalandırın.\nParçalara bölüp uzun fitiller yapın.\nHalka şekli verin.\nPekmezli suya batırın.\nSusama bulayın.\n220 derece fırında 20 dakika pişirin.",
    "Image_Name": "vegan-susamli-simit",
    "Cleaned_Ingredients": "['un', 'instant maya', 'tuz', 'toz şeker', 'su', 'sıvı yağ', 'pekmez', 'susam']"
  },
  {
    "Title": "Glutensiz Susamlı Simit (Glutensiz)",
    "Ingredients": "['2 su bardağı mısır unu', '2 su bardağı pirinç unu', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '2 yemek kaşığı sıvı yağ', '0.5 su bardağı pekmez', '2 su bardağı susam']",
    "Instructions": "Mısır unu, pirinç unu, maya, tuz, şeker, su ve sıvı yağı yoğurun.\n30 dakika mayalandırın.\nParçalara bölüp halka şekli verin.\nPekmezli suya batırıp susama bulayın.\n220 derece fırında 20 dakika pişirin.",
    "Image_Name": "glutensiz-susamli-simit",
    "Cleaned_Ingredients": "['mısır unu', 'pirinç unu', 'instant maya', 'tuz', 'toz şeker', 'su', 'sıvı yağ', 'pekmez', 'susam']"
  },
  {
    "Title": "Vegan Islak Hamburger (Vegan)",
    "Ingredients": "['4 adet hamburger ekmeği', '200 gram soya kıyma', '1 adet soğan', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '2 yemek kaşığı zeytinyağı', '2 yemek kaşığı domates salçası', '1 diş sarımsak', '1 su bardağı su']",
    "Instructions": "Soya kıymayı ıslatıp süzün.\nSoğan, tuz ve karabiberle yoğurun.\nKöfteler yapıp zeytinyağında pişirin.\nEkmeklerin arasına koyun.\nZeytinyağı, salça, sarımsak ve suyla sos yapın.\nHamburgerleri buharlı tencereye dizin.\nSosu gezdirip 10 dakika bekletin.",
    "Image_Name": "vegan-islak-hamburger",
    "Cleaned_Ingredients": "['hamburger ekmeği', 'soya kıyma', 'soğan', 'tuz', 'karabiber', 'zeytinyağı', 'domates salçası', 'sarımsak', 'su']"
  },
  {
    "Title": "Süt Ürünsüz Sucuklu Yumurta (Süt Ürünü Yok)",
    "Ingredients": "['200 gram sucuk', '4 adet yumurta', '1 yemek kaşığı zeytinyağı', '1 çay kaşığı pul biber']",
    "Instructions": "Sucuğu dilimleyin.\nZeytinyağında sucukları kızartın.\nYumurtaları kırıp üzerine ekleyin.\nPul biber serpin.\nYumurtalar pişene kadar bekleyin.",
    "Image_Name": "sut-urunsuz-sucuklu-yumurta",
    "Cleaned_Ingredients": "['sucuk', 'yumurta', 'zeytinyağı', 'pul biber']"
  },
  {
    "Title": "Adana Dürüm",
    "Ingredients": "['500 gram dana kıyma', '1 adet soğan', '2 adet sivri biber', '2 adet domates', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', '4 adet lavaş']",
    "Instructions": "Kıymayı soğan ve baharatlarla yoğurun.\nŞişlere sarın.\nKömür ateşinde pişirin.\nLavaş üzerine koyun.\nDomates ve biber ekleyin.\nSararak servis yapın.",
    "Image_Name": "adana-durum",
    "Cleaned_Ingredients": "['dana kıyma', 'soğan', 'sivri biber', 'domates', 'tuz', 'pul biber', 'karabiber', 'kimyon', 'lavaş']"
  },
  {
    "Title": "Çiğ Köfte Dürüm",
    "Ingredients": "['300 gram çiğ köftelik bulgur', '2 yemek kaşığı biber salçası', '1 yemek kaşığı domates salçası', '1 adet soğan', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon', '4 adet lavaş', '1 adet marul', '1 adet limon']",
    "Instructions": "Bulguru sıcak suyla ıslatın.\nSalçaları ve baharatları ekleyip yoğurun.\nSoğanı rendeleyin ve ilave edin.\nİyice yoğurup köfte kıvamına getirin.\nLavaşa yayın.\nMarul ve limon sıkarak sarın.",
    "Image_Name": "cig-kofte-durum",
    "Cleaned_Ingredients": "['çiğ köftelik bulgur', 'biber salçası', 'domates salçası', 'soğan', 'tuz', 'pul biber', 'kimyon', 'lavaş', 'marul', 'limon']"
  },
  {
    "Title": "Dürüm Döner",
    "Ingredients": "['500 gram tavuk göğsü', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kekik', '4 adet lavaş', '2 adet domates', '1 adet soğan']",
    "Instructions": "Tavuk göğsünü ince dilimleyin.\nBaharatlar ve zeytinyağıyla marine edin.\nTavada veya ızgarada pişirin.\nLavaşa koyun.\nDomates ve soğan ekleyin.\nSararak servis yapın.",
    "Image_Name": "durum-doner",
    "Cleaned_Ingredients": "['tavuk göğsü', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber', 'kekik', 'lavaş', 'domates', 'soğan']"
  },
  {
    "Title": "Kaşarlı Tost",
    "Ingredients": "['8 dilim tost ekmeği', '200 gram kaşar peyniri', '2 yemek kaşığı tereyağı']",
    "Instructions": "Tost ekmeklerinin arasına kaşar peyniri koyun.\nTereyağı ile tost makinesinde veya tavada kızartın.\nPeynir eriyene kadar pişirin.\nSıcak servis yapın.",
    "Image_Name": "kasarli-tost",
    "Cleaned_Ingredients": "['tost ekmeği', 'kaşar peyniri', 'tereyağı']"
  },
  {
    "Title": "Sokak Usulü Acılı Ezme",
    "Ingredients": "['4 adet domates', '2 adet sivri biber', '1 adet soğan', '1 demet maydanoz', '2 yemek kaşığı nar ekşisi', '1 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı sumak']",
    "Instructions": "Domatesleri ince ince doğrayın.\nBiberleri ve soğanı ince kıyın.\nMaydanozu doğrayın.\nTüm malzemeleri karıştırın.\nNar ekşisi, zeytinyağı ve baharatları ekleyin.\nSoğuk servis yapın.",
    "Image_Name": "sokak-usulu-acili-ezme",
    "Cleaned_Ingredients": "['domates', 'sivri biber', 'soğan', 'maydanoz', 'nar ekşisi', 'zeytinyağı', 'tuz', 'pul biber', 'sumak']"
  },
  {
    "Title": "Sahanda Yumurta",
    "Ingredients": "['4 adet yumurta', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Tereyağını sahanda eritin.\nYumurtaları kırıp sahana bırakın.\nTuz ve karabiber serpin.\nBeyazı pişip sarısı akışkan kalana kadar pişirin.\nSıcak servis yapın.",
    "Image_Name": "sahanda-yumurta",
    "Cleaned_Ingredients": "['yumurta', 'tereyağı', 'tuz', 'karabiber']"
  },
  {
    "Title": "Peynirli Pide",
    "Ingredients": "['3 su bardağı un', '1 paket instant maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '2 yemek kaşığı zeytinyağı', '300 gram beyaz peynir', '1 adet yumurta']",
    "Instructions": "Un, maya, tuz, su ve zeytinyağını yoğurun.\n30 dakika mayalandırın.\nHamuru kayık şeklinde açın.\nPeyniri ufalayıp üzerine yayın.\nKenarlarını kıvırın.\n220 derece fırında 15 dakika pişirin.\nÜzerine yumurta kırıp 2 dakika daha pişirin.",
    "Image_Name": "peynirli-pide",
    "Cleaned_Ingredients": "['un', 'instant maya', 'tuz', 'su', 'zeytinyağı', 'beyaz peynir', 'yumurta']"
  },
  {
    "Title": "Boyoz",
    "Ingredients": "['3 su bardağı un', '1 çay kaşığı tuz', '0.5 su bardağı sıvı yağ', '1 su bardağı ılık su', '1 adet yumurta sarısı']",
    "Instructions": "Un, tuz ve ılık suyu yoğurun.\n1 saat dinlendirin.\nHamuru parçalara bölün.\nHer parçayı ince açıp sıvı yağ sürün.\nKatlayıp tekrar açın.\nTepsiye dizin.\nÜzerine yumurta sarısı sürün.\n200 derece fırında 20 dakika pişirin.",
    "Image_Name": "boyoz",
    "Cleaned_Ingredients": "['un', 'tuz', 'sıvı yağ', 'su', 'yumurta sarısı']"
  },
  {
    "Title": "Vegan Döner Dürüm (Vegan)",
    "Ingredients": "['500 gram istiridye mantarı', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kekik', '4 adet lavaş', '2 adet domates', '1 adet soğan']",
    "Instructions": "İstiridye mantarlarını şerit şerit doğrayın.\nBaharatlar ve zeytinyağıyla marine edin.\nTavada yüksek ateşte pişirin.\nLavaşa koyun.\nDomates ve soğan ekleyin.\nSararak servis yapın.",
    "Image_Name": "vegan-doner-durum",
    "Cleaned_Ingredients": "['istiridye mantarı', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber', 'kekik', 'lavaş', 'domates', 'soğan']"
  },
  {
    "Title": "Glutensiz Tantuni (Glutensiz)",
    "Ingredients": "['500 gram dana eti', '2 adet soğan', '3 adet domates', '3 adet sivri biber', '2 yemek kaşığı sıvı yağ', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '4 adet mısır tortilla']",
    "Instructions": "Eti ince ince doğrayın.\nSıvı yağda yüksek ateşte kavurun.\nSoğanları ince doğrayıp ekleyin.\nBiberleri ve domatesleri ilave edin.\nBaharatları ekleyin.\nMısır tortillaya sararak servis yapın.",
    "Image_Name": "glutensiz-tantuni",
    "Cleaned_Ingredients": "['dana eti', 'soğan', 'domates', 'sivri biber', 'sıvı yağ', 'tuz', 'karabiber', 'pul biber', 'mısır tortilla']"
  },
  {
    "Title": "Süt Ürünsüz Kaşarlı Tost (Süt Ürünü Yok)",
    "Ingredients": "['8 dilim tost ekmeği', '200 gram vegan kaşar', '2 yemek kaşığı zeytinyağı']",
    "Instructions": "Tost ekmeklerinin arasına vegan kaşar koyun.\nZeytinyağı ile tost makinesinde veya tavada kızartın.\nVegan kaşar eriyene kadar pişirin.\nSıcak servis yapın.",
    "Image_Name": "sut-urunsuz-kasarli-tost",
    "Cleaned_Ingredients": "['tost ekmeği', 'vegan kaşar', 'zeytinyağı']"
  },
  {
    "Title": "Vegan Boyoz (Vegan)",
    "Ingredients": "['3 su bardağı un', '1 çay kaşığı tuz', '0.5 su bardağı sıvı yağ', '1 su bardağı ılık su']",
    "Instructions": "Un, tuz ve ılık suyu yoğurun.\n1 saat dinlendirin.\nHamuru parçalara bölün.\nHer parçayı ince açıp sıvı yağ sürün.\nKatlayıp tekrar açın.\nTepsiye dizin.\n200 derece fırında 20 dakika pişirin.",
    "Image_Name": "vegan-boyoz",
    "Cleaned_Ingredients": "['un', 'tuz', 'sıvı yağ', 'su']"
  },
  {
    "Title": "Vegan Peynirli Pide (Vegan)",
    "Ingredients": "['3 su bardağı un', '1 paket instant maya', '1 çay kaşığı tuz', '1 su bardağı ılık su', '2 yemek kaşığı zeytinyağı', '300 gram tofu', '1 çay kaşığı zerdeçal']",
    "Instructions": "Un, maya, tuz, su ve zeytinyağını yoğurun.\n30 dakika mayalandırın.\nHamuru kayık şeklinde açın.\nTofuyu ufalayıp zerdeçalle karıştırın.\nÜzerine yayın.\nKenarlarını kıvırın.\n220 derece fırında 15 dakika pişirin.",
    "Image_Name": "vegan-peynirli-pide",
    "Cleaned_Ingredients": "['un', 'instant maya', 'tuz', 'su', 'zeytinyağı', 'tofu', 'zerdeçal']"
  },
  {
    "Title": "Glutensiz Vegan Pişi (Glutensiz & Vegan)",
    "Ingredients": "['2 su bardağı mısır unu', '1 su bardağı pirinç unu', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '2 yemek kaşığı sıvı yağ', 'kızartma yağı']",
    "Instructions": "Mısır unu, pirinç unu, maya, tuz, şeker, su ve sıvı yağı yoğurun.\n30 dakika mayalandırın.\nParçalar koparıp yuvarlak şekil verin.\nKızgın yağda kızartın.\nKağıt havluyla yağını alın.",
    "Image_Name": "glutensiz-vegan-pisi",
    "Cleaned_Ingredients": "['mısır unu', 'pirinç unu', 'instant maya', 'tuz', 'toz şeker', 'su', 'sıvı yağ', 'kızartma yağı']"
  },
  {
    "Title": "Süt Ürünsüz Sahanda Yumurta (Süt Ürünü Yok)",
    "Ingredients": "['4 adet yumurta', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Zeytinyağını sahanda kızdırın.\nYumurtaları kırıp sahana bırakın.\nTuz ve karabiber serpin.\nBeyazı pişip sarısı akışkan kalana kadar pişirin.\nSıcak servis yapın.",
    "Image_Name": "sut-urunsuz-sahanda-yumurta",
    "Cleaned_Ingredients": "['yumurta', 'zeytinyağı', 'tuz', 'karabiber']"
  },
  {
    "Title": "Vegan Adana Dürüm (Vegan)",
    "Ingredients": "['300 gram soya kıyma', '1 adet soğan', '2 adet sivri biber', '2 adet domates', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', '4 adet lavaş']",
    "Instructions": "Soya kıymayı ıslatıp süzün.\nSoğan ve baharatlarla yoğurun.\nŞişlere veya mangal teline sarın.\nIzgarada veya tavada pişirin.\nLavaşa koyun.\nDomates ve biber ekleyip sarın.",
    "Image_Name": "vegan-adana-durum",
    "Cleaned_Ingredients": "['soya kıyma', 'soğan', 'sivri biber', 'domates', 'tuz', 'pul biber', 'karabiber', 'kimyon', 'lavaş']"
  },
  {
    "Title": "Glutensiz Çiğ Köfte Dürüm (Glutensiz & Vegan)",
    "Ingredients": "['300 gram karabuğday', '2 yemek kaşığı biber salçası', '1 yemek kaşığı domates salçası', '1 adet soğan', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon', '4 adet marul yaprağı', '1 adet limon']",
    "Instructions": "Karabuğdayı sıcak suyla ıslatın.\nSalçaları ve baharatları ekleyip yoğurun.\nSoğanı rendeleyin ve ilave edin.\nİyice yoğurup köfte kıvamına getirin.\nMarul yapraklarına yayın.\nLimon sıkarak sarın.",
    "Image_Name": "glutensiz-cig-kofte-durum",
    "Cleaned_Ingredients": "['karabuğday', 'biber salçası', 'domates salçası', 'soğan', 'tuz', 'pul biber', 'kimyon', 'marul', 'limon']"
  },
  {
    "Title": "Süt Ürünsüz Pişi (Süt Ürünü Yok)",
    "Ingredients": "['3 su bardağı un', '1 paket instant maya', '1 çay kaşığı tuz', '1 çay kaşığı toz şeker', '1 su bardağı ılık su', '2 yemek kaşığı sıvı yağ', 'kızartma yağı']",
    "Instructions": "Un, maya, tuz, şeker, su ve sıvı yağı yoğurun.\n30 dakika mayalandırın.\nParçalar koparıp yuvarlak açın.\nKızgın yağda kızartın.\nKağıt havluyla yağını alın.",
    "Image_Name": "sut-urunsuz-pisi",
    "Cleaned_Ingredients": "['un', 'instant maya', 'tuz', 'toz şeker', 'su', 'sıvı yağ', 'kızartma yağı']"
  },
  {
    "Title": "Vejetaryen Kumpir (Vejetaryen)",
    "Ingredients": "['4 adet büyük patates', '100 gram tereyağı', '100 gram kaşar peyniri', '4 yemek kaşığı mısır', '4 yemek kaşığı bezelye', '4 yemek kaşığı turşu', '100 gram lor peyniri', '1 çay kaşığı tuz']",
    "Instructions": "Patatesleri yıkayıp fırında pişirin.\nOrtalarını kesin.\nİçlerini kaşıkla çıkarıp tereyağı ve kaşar ile ezin.\nGeri doldurun.\nÜzerine mısır, bezelye, turşu ve lor peyniri ekleyin.",
    "Image_Name": "vejetaryen-kumpir",
    "Cleaned_Ingredients": "['patates', 'tereyağı', 'kaşar peyniri', 'mısır', 'bezelye', 'turşu', 'lor peyniri', 'tuz']"
  },
  {
    "Title": "Glutensiz Balık Ekmek (Glutensiz)",
    "Ingredients": "['4 adet uskumru fileto', '3 yemek kaşığı mısır unu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '3 yemek kaşığı zeytinyağı', '4 adet glutensiz ekmek', '1 adet soğan', '2 adet domates', '1 adet marul']",
    "Instructions": "Balıkları mısır unu, tuz ve karabiberle harmanlayın.\nZeytinyağında kızartın.\nGlutensiz ekmekleri ikiye kesin.\nMarul, domates ve soğan dilimleyin.\nBalıkları ekmek arasına koyun.\nSebzeleri ekleyin.",
    "Image_Name": "glutensiz-balik-ekmek",
    "Cleaned_Ingredients": "['uskumru fileto', 'mısır unu', 'tuz', 'karabiber', 'zeytinyağı', 'glutensiz ekmek', 'soğan', 'domates', 'marul']"
  },
  {
    "Title": "Perde Pilavı",
    "Ingredients": "['2 su bardağı pirinç', '300 gram tavuk göğsü', '2 yemek kaşığı tereyağı', '1 adet soğan', '50 gram badem', '50 gram kuru üzüm', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '3 su bardağı tavuk suyu', '4 adet yufka', '1 adet yumurta']",
    "Instructions": "Tavuğu haşlayıp didikleyin.\nSoğanı tereyağında kavurun.\nBademi ve kuru üzümü ekleyin.\nPirinci ilave edip kavurun.\nTavuk suyunu ekleyip pişirin.\nDidiklenmiş tavuğu karıştırın.\nYufkaları kaseye sererek pilavı doldurun.\nÜstünü kapatıp yumurta sürün.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "perde-pilavi",
    "Cleaned_Ingredients": "['pirinç', 'tavuk göğsü', 'tereyağı', 'soğan', 'badem', 'kuru üzüm', 'tuz', 'karabiber', 'tavuk suyu', 'yufka', 'yumurta']"
  },
  {
    "Title": "Analıkızlı Çorbası",
    "Ingredients": "['1 su bardağı kırmızı mercimek', '0.5 su bardağı bulgur', '1 adet soğan', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı nane', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '6 su bardağı su']",
    "Instructions": "Mercimeği yıkayıp tencereye alın.\nSuyu ekleyip kaynatın.\nSoğanı tereyağında kavurun.\nSalçayı ekleyin.\nKavurma ve bulguru mercimeğe ilave edin.\n20 dakika pişirin.\nNane ve baharatları ekleyin.",
    "Image_Name": "analikizli-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'bulgur', 'soğan', 'tereyağı', 'domates salçası', 'nane', 'tuz', 'karabiber', 'su']"
  },
  {
    "Title": "Höşmerim",
    "Ingredients": "['250 gram taze lor peyniri', '3 yemek kaşığı tereyağı', '3 yemek kaşığı toz şeker', '2 yemek kaşığı un']",
    "Instructions": "Tereyağını tavada eritin.\nUnu ekleyip hafifçe kavurun.\nLor peynirini ilave edin.\nŞekeri ekleyin.\nKarıştırarak peynir eriyene ve karışım koyulaşana kadar pişirin.\nSıcak servis yapın.",
    "Image_Name": "hosmerim",
    "Cleaned_Ingredients": "['lor peyniri', 'tereyağı', 'toz şeker', 'un']"
  },
  {
    "Title": "Sütlü Nuriye",
    "Ingredients": "['500 gram baklava yufkası', '200 gram tereyağı', '200 gram ceviz', '1 litre süt', '1 su bardağı toz şeker', '1 paket vanilya']",
    "Instructions": "Yufkaları tepsiye sererek aralarına tereyağı ve ceviz serpin.\nDilimleyip 180 derece fırında 30 dakika pişirin.\nSütü ve şekeri kaynatıp vanilyayı ekleyin.\nSıcak tatlının üzerine sıcak sütü dökün.\nBuzdolabında 3 saat soğutun.",
    "Image_Name": "sutlu-nuriye",
    "Cleaned_Ingredients": "['baklava yufkası', 'tereyağı', 'ceviz', 'süt', 'toz şeker', 'vanilya']"
  },
  {
    "Title": "Maraş Tarhanası Çorbası",
    "Ingredients": "['100 gram Maraş tarhanası', '1 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı nane', '1 çay kaşığı pul biber', '1 çay kaşığı tuz', '5 su bardağı su']",
    "Instructions": "Tarhana parçalarını suda ıslatın.\nTereyağında salçayı kavurun.\nIslatılmış tarhanayı ve suyunu ekleyin.\nKaynayana kadar karıştırarak pişirin.\nNane, pul biber ve tuzu ilave edin.\n15 dakika kısık ateşte pişirin.",
    "Image_Name": "maras-tarhanasi-corbasi",
    "Cleaned_Ingredients": "['Maraş tarhanası', 'tereyağı', 'domates salçası', 'nane', 'pul biber', 'tuz', 'su']"
  },
  {
    "Title": "Çeçil Peynirli Börek",
    "Ingredients": "['4 adet yufka', '200 gram çeçil peyniri', '2 yemek kaşığı tereyağı', '1 su bardağı süt', '2 adet yumurta', '1 çay kaşığı tuz']",
    "Instructions": "Süt, yumurta ve tuzu çırpın.\nYufkaları sütlü karışıma batırın.\nÇeçil peynirini rulo şeklinde sarın.\nTepsiye dizin.\nEritilmiş tereyağını gezdirin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "cecil-peynirli-borek",
    "Cleaned_Ingredients": "['yufka', 'çeçil peyniri', 'tereyağı', 'süt', 'yumurta', 'tuz']"
  },
  {
    "Title": "Kayseri Mantısı",
    "Ingredients": "['2 su bardağı un', '1 adet yumurta', '0.5 su bardağı su', '1 çay kaşığı tuz', '200 gram dana kıyma', '1 adet soğan', '1 su bardağı yoğurt', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber', '1 çay kaşığı nane']",
    "Instructions": "Un, yumurta, su ve tuzla hamur yoğurun.\nDinlendirin.\nKıyma ve soğanla iç harç hazırlayın.\nHamuru ince açıp küçük kareler kesin.\nİç harcı koyup kapatın.\nKaynayan suda haşlayın.\nYoğurt ve tereyağlı sos ile servis yapın.",
    "Image_Name": "kayseri-mantisi",
    "Cleaned_Ingredients": "['un', 'yumurta', 'su', 'tuz', 'dana kıyma', 'soğan', 'yoğurt', 'tereyağı', 'pul biber', 'nane']"
  },
  {
    "Title": "Bici Bici",
    "Ingredients": "['1 su bardağı nişasta', '4 su bardağı su', '1 su bardağı toz şeker', '1 yemek kaşığı gül suyu', 'buz']",
    "Instructions": "Nişasta ve suyu karıştırıp kaynatın.\nKoyulaşana kadar pişirin.\nGeniş bir tepsiye dökün.\nSoğuyunca küp küp kesin.\nŞeker ve suyla şerbet yapın.\nGül suyunu ekleyin.\nBuz üzerine nişasta küplerini koyup şerbet dökün.",
    "Image_Name": "bici-bici",
    "Cleaned_Ingredients": "['nişasta', 'su', 'toz şeker', 'gül suyu', 'buz']"
  },
  {
    "Title": "Keledoş",
    "Ingredients": "['500 gram taze fasulye', '3 adet patates', '2 adet domates', '1 adet soğan', '3 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '2 su bardağı su']",
    "Instructions": "Fasulyeleri doğrayın.\nPatatesleri küp kesin.\nSoğanı tereyağında kavurun.\nSalçayı ekleyin.\nFasulye ve patatesleri ilave edin.\nDomatesleri rendeleyin ve ekleyin.\nSuyu ilave edip kısık ateşte 30 dakika pişirin.",
    "Image_Name": "keledos",
    "Cleaned_Ingredients": "['taze fasulye', 'patates', 'domates', 'soğan', 'tereyağı', 'domates salçası', 'tuz', 'karabiber', 'su']"
  },
  {
    "Title": "Arabaşı Çorbası",
    "Ingredients": "['1 adet tavuk but', '2 yemek kaşığı un', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '6 su bardağı su']",
    "Instructions": "Tavuğu haşlayıp didikleyin.\nSuyunu saklayın.\nTereyağında unu kavurun.\nSalçayı ekleyin.\nTavuk suyunu azar azar ilave edin.\nDidiklenmiş tavuğu ekleyin.\nKısık ateşte 15 dakika pişirin.",
    "Image_Name": "arabasi-corbasi",
    "Cleaned_Ingredients": "['tavuk but', 'un', 'tereyağı', 'domates salçası', 'tuz', 'karabiber', 'su']"
  },
  {
    "Title": "Çırpma",
    "Ingredients": "['4 adet yumurta', '2 su bardağı yoğurt', '1 su bardağı un', '2 yemek kaşığı tereyağı', '1 çay kaşığı nane', '1 çay kaşığı pul biber', '1 çay kaşığı tuz', '3 su bardağı su']",
    "Instructions": "Yumurta, yoğurt ve unu çırpın.\nSuyu ekleyip karıştırın.\nTencereye alıp sürekli karıştırarak kaynatın.\nKoyulaşana kadar pişirin.\nTereyağını eritip nane ve pul biber ekleyin.\nÜzerine gezdirerek servis yapın.",
    "Image_Name": "cirpma",
    "Cleaned_Ingredients": "['yumurta', 'yoğurt', 'un', 'tereyağı', 'nane', 'pul biber', 'tuz', 'su']"
  },
  {
    "Title": "Gülüzar Çorbası",
    "Ingredients": "['1 su bardağı kırmızı mercimek', '1 su bardağı bulgur', '1 adet soğan', '2 yemek kaşığı tereyağı', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '1 çay kaşığı nane', '1 çay kaşığı tuz', '6 su bardağı su']",
    "Instructions": "Mercimeği yıkayıp suda haşlayın.\nSoğanı tereyağında kavurun.\nSalçaları ekleyin.\nKavurmayı mercimeğe ilave edin.\nBulguru ekleyin.\n20 dakika daha pişirin.\nNane ve tuzu ilave edin.",
    "Image_Name": "guluzar-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'bulgur', 'soğan', 'tereyağı', 'domates salçası', 'biber salçası', 'nane', 'tuz', 'su']"
  },
  {
    "Title": "Tirit",
    "Ingredients": "['4 adet bayat pide', '500 gram kuzu eti', '2 su bardağı yoğurt', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber', '1 çay kaşığı tuz', '3 su bardağı et suyu']",
    "Instructions": "Kuzu etini haşlayın.\nPideleri küçük parçalara bölün.\nEt suyunu ısıtın.\nPide parçalarını tabağa dizin.\nÜzerine et suyu dökün.\nEtleri yerleştirin.\nYoğurt gezdirin.\nTereyağını kızdırıp pul biberle üzerine dökün.",
    "Image_Name": "tirit",
    "Cleaned_Ingredients": "['bayat pide', 'kuzu eti', 'yoğurt', 'tereyağı', 'pul biber', 'tuz', 'et suyu']"
  },
  {
    "Title": "Gendime Pilavı",
    "Ingredients": "['2 su bardağı gendime', '1 adet soğan', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '3 su bardağı sıcak su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Gendimeyi yıkayıp ıslatın.\nSoğanı tereyağında kavurun.\nSalçayı ekleyin.\nGendimeyi ilave edip kavurun.\nSıcak suyu ve tuzu ekleyin.\nKısık ateşte 20 dakika pişirip demlendirin.",
    "Image_Name": "gendime-pilavi",
    "Cleaned_Ingredients": "['gendime', 'soğan', 'tereyağı', 'domates salçası', 'su', 'tuz', 'karabiber']"
  },
  {
    "Title": "Hıngel",
    "Ingredients": "['2 su bardağı un', '1 adet yumurta', '0.5 su bardağı su', '1 çay kaşığı tuz', '200 gram dana kıyma', '1 adet soğan', '1 su bardağı yoğurt', '2 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber']",
    "Instructions": "Un, yumurta, su ve tuzla hamur yoğurun.\nDinlendirin.\nKıyma ve soğanla iç harç yapın.\nHamuru açıp kareler kesin.\nİçini doldurup üçgen kapatın.\nKaynayan suda haşlayın.\nSarımsaklı yoğurt ve tereyağlı sos ile servis yapın.",
    "Image_Name": "hingel",
    "Cleaned_Ingredients": "['un', 'yumurta', 'su', 'tuz', 'dana kıyma', 'soğan', 'yoğurt', 'sarımsak', 'tereyağı', 'pul biber']"
  },
  {
    "Title": "Kaygana",
    "Ingredients": "['4 adet yumurta', '2 yemek kaşığı un', '0.5 su bardağı süt', '1 çay kaşığı tuz', '2 yemek kaşığı tereyağı']",
    "Instructions": "Yumurta, un, süt ve tuzu çırpın.\nTereyağını tavada eritin.\nKarışımı dökün.\nAltı kızarınca çevirin.\nİki tarafı da kızarana kadar pişirin.\nSıcak servis yapın.",
    "Image_Name": "kaygana",
    "Cleaned_Ingredients": "['yumurta', 'un', 'süt', 'tuz', 'tereyağı']"
  },
  {
    "Title": "Kirde",
    "Ingredients": "['2 su bardağı un', '1 adet yumurta', '1 çay kaşığı tuz', '0.5 su bardağı su', '200 gram dana kıyma', '1 adet soğan', '2 yemek kaşığı tereyağı', '1 su bardağı yoğurt', '1 çay kaşığı nane']",
    "Instructions": "Un, yumurta, tuz ve suyla hamur yoğurun.\nKıyma ve soğanla iç harç yapın.\nHamuru ince açın.\nŞeritler kesip iç harcı yerleştirin.\nKapatıp kaynayan suda haşlayın.\nYoğurt ve tereyağlı sos ile servis yapın.",
    "Image_Name": "kirde",
    "Cleaned_Ingredients": "['un', 'yumurta', 'tuz', 'su', 'dana kıyma', 'soğan', 'tereyağı', 'yoğurt', 'nane']"
  },
  {
    "Title": "Mumbar Dolması",
    "Ingredients": "['500 gram kuzu bağırsak', '1 su bardağı pirinç', '200 gram dana kıyma', '1 adet soğan', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon']",
    "Instructions": "Bağırsakları iyice temizleyin.\nPirinç, kıyma, soğan, salça ve baharatları karıştırın.\nHarcı bağırsaklara doldurun.\nUçlarını bağlayın.\nKaynayan suda 45 dakika haşlayın.\nDilimleyip servis yapın.",
    "Image_Name": "mumbar-dolmasi",
    "Cleaned_Ingredients": "['kuzu bağırsak', 'pirinç', 'dana kıyma', 'soğan', 'domates salçası', 'tuz', 'karabiber', 'pul biber', 'kimyon']"
  },
  {
    "Title": "Yağlama",
    "Ingredients": "['4 adet yufka', '200 gram taze kaşar peyniri', '2 yemek kaşığı tereyağı', '1 su bardağı süt', '2 adet yumurta', '1 çay kaşığı tuz']",
    "Instructions": "Yufkaları süt ve yumurta karışımına batırın.\nTepsiye sererek aralarına peynir serpin.\nTereyağını eritip üzerine gezdirin.\n180 derece fırında 25 dakika pişirin.\nÜzeri kızarana kadar bekleyin.",
    "Image_Name": "yaglama",
    "Cleaned_Ingredients": "['yufka', 'taze kaşar peyniri', 'tereyağı', 'süt', 'yumurta', 'tuz']"
  },
  {
    "Title": "Lobik",
    "Ingredients": "['2 su bardağı taze barbunya', '2 adet patates', '1 adet soğan', '2 adet domates', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '2 su bardağı su']",
    "Instructions": "Soğanı tereyağında kavurun.\nSalçayı ekleyin.\nBarbunya ve patatesleri ilave edin.\nDomatesleri rendeleyin ve ekleyin.\nSuyu ilave edin.\nKısık ateşte 35 dakika pişirin.",
    "Image_Name": "lobik",
    "Cleaned_Ingredients": "['taze barbunya', 'patates', 'soğan', 'domates', 'tereyağı', 'domates salçası', 'tuz', 'karabiber', 'su']"
  },
  {
    "Title": "Düğürcük Çorbası",
    "Ingredients": "['200 gram dana kıyma', '0.5 su bardağı pirinç', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı tereyağı', '1 çay kaşığı nane', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '6 su bardağı su']",
    "Instructions": "Kıymayı pirinç, tuz ve karabiberle yoğurun.\nKüçük köfteler yapın.\nSoğanı tereyağında kavurup salçayı ekleyin.\nSuyu ilave edip kaynatın.\nKöfteleri tek tek bırakın.\n20 dakika pişirin.\nNane serpin.",
    "Image_Name": "dugurcuk-corbasi",
    "Cleaned_Ingredients": "['dana kıyma', 'pirinç', 'soğan', 'domates salçası', 'tereyağı', 'nane', 'tuz', 'karabiber', 'su']"
  },
  {
    "Title": "Çullama",
    "Ingredients": "['1 adet tavuk but', '2 su bardağı yoğurt', '2 yemek kaşığı tereyağı', '2 adet yufka', '1 çay kaşığı pul biber', '1 çay kaşığı tuz', '2 su bardağı tavuk suyu']",
    "Instructions": "Tavuğu haşlayıp didikleyin.\nYufkaları parçalayın.\nTabağa yufka parçaları dizin.\nÜzerine tavuk suyu dökün.\nDidiklenmiş tavuk yerleştirin.\nYoğurt gezdirin.\nTereyağını kızdırıp pul biberle üzerine dökün.",
    "Image_Name": "cullama",
    "Cleaned_Ingredients": "['tavuk but', 'yoğurt', 'tereyağı', 'yufka', 'pul biber', 'tuz', 'tavuk suyu']"
  },
  {
    "Title": "Ekşili Pilav",
    "Ingredients": "['2 su bardağı pirinç', '300 gram kuzu eti', '1 adet soğan', '2 yemek kaşığı tereyağı', '2 yemek kaşığı nar ekşisi', '3 su bardağı et suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kuzu etini kavurun.\nSoğanı ekleyin.\nPirinci ilave edip kavurun.\nEt suyunu ve nar ekşisini ekleyin.\nTuzu ilave edin.\nKısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "eksili-pilav",
    "Cleaned_Ingredients": "['pirinç', 'kuzu eti', 'soğan', 'tereyağı', 'nar ekşisi', 'et suyu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Katıklı Ekmek",
    "Ingredients": "['3 su bardağı mısır unu', '1 su bardağı ılık su', '1 çay kaşığı tuz', '200 gram lor peyniri', '100 gram karalahana', '2 yemek kaşığı tereyağı']",
    "Instructions": "Mısır unu, su ve tuzu yoğurun.\nKaralahanaları doğrayıp haşlayın.\nLor peyniri ve karalahanayla iç harç yapın.\nHamuru açıp içine harç koyun.\nKapatıp sacda veya tavada pişirin.\nTereyağı sürüp servis yapın.",
    "Image_Name": "katikli-ekmek",
    "Cleaned_Ingredients": "['mısır unu', 'su', 'tuz', 'lor peyniri', 'karalahana', 'tereyağı']"
  },
  {
    "Title": "Vegan Perde Pilavı (Vegan)",
    "Ingredients": "['2 su bardağı pirinç', '200 gram istiridye mantarı', '2 yemek kaşığı zeytinyağı', '1 adet soğan', '50 gram kuru üzüm', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '3 su bardağı sebze suyu', '4 adet yufka']",
    "Instructions": "Mantarları doğrayıp zeytinyağında kavurun.\nSoğanı ekleyin.\nKuru üzümü ilave edin.\nPirinci ekleyip kavurun.\nSebze suyunu ekleyip pişirin.\nYufkaları kaseye sererek pilavı doldurun.\nÜstünü kapatıp 180 derece fırında 25 dakika pişirin.",
    "Image_Name": "vegan-perde-pilavi",
    "Cleaned_Ingredients": "['pirinç', 'istiridye mantarı', 'zeytinyağı', 'soğan', 'kuru üzüm', 'tuz', 'karabiber', 'sebze suyu', 'yufka']"
  },
  {
    "Title": "Glutensiz Analıkızlı Çorbası (Glutensiz & Vegan)",
    "Ingredients": "['1 su bardağı kırmızı mercimek', '0.5 su bardağı pirinç', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı nane', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '6 su bardağı su']",
    "Instructions": "Mercimeği yıkayıp tencereye alın.\nSuyu ekleyip kaynatın.\nSoğanı zeytinyağında kavurun.\nSalçayı ekleyin.\nKavurma ve pirinci mercimeğe ilave edin.\n20 dakika pişirin.\nNane ve baharatları ekleyin.",
    "Image_Name": "glutensiz-analikizli-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'pirinç', 'soğan', 'zeytinyağı', 'domates salçası', 'nane', 'tuz', 'karabiber', 'su']"
  },
  {
    "Title": "Süt Ürünsüz Sütlü Nuriye (Süt Ürünü Yok)",
    "Ingredients": "['500 gram baklava yufkası', '200 gram margarin', '200 gram ceviz', '1 litre yulaf sütü', '1 su bardağı toz şeker', '1 paket vanilya']",
    "Instructions": "Yufkaları tepsiye sererek aralarına margarin ve ceviz serpin.\nDilimleyip 180 derece fırında 30 dakika pişirin.\nYulaf sütünü ve şekeri kaynatıp vanilyayı ekleyin.\nSıcak tatlının üzerine sıcak sütü dökün.\nBuzdolabında 3 saat soğutun.",
    "Image_Name": "sut-urunsuz-sutlu-nuriye",
    "Cleaned_Ingredients": "['baklava yufkası', 'margarin', 'ceviz', 'yulaf sütü', 'toz şeker', 'vanilya']"
  },
  {
    "Title": "Vegan Keledoş (Vegan & Glutensiz)",
    "Ingredients": "['500 gram taze fasulye', '3 adet patates', '2 adet domates', '1 adet soğan', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '2 su bardağı su']",
    "Instructions": "Fasulyeleri doğrayın.\nPatatesleri küp kesin.\nSoğanı zeytinyağında kavurun.\nSalçayı ekleyin.\nFasulye ve patatesleri ilave edin.\nDomatesleri rendeleyin ve ekleyin.\nSuyu ilave edip kısık ateşte 30 dakika pişirin.",
    "Image_Name": "vegan-keledos",
    "Cleaned_Ingredients": "['taze fasulye', 'patates', 'domates', 'soğan', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'su']"
  },
  {
    "Title": "Süt Ürünsüz Höşmerim (Süt Ürünü Yok)",
    "Ingredients": "['250 gram tofu', '3 yemek kaşığı margarin', '3 yemek kaşığı toz şeker', '2 yemek kaşığı un']",
    "Instructions": "Margarini tavada eritin.\nUnu ekleyip hafifçe kavurun.\nTofuyu ufalayıp ilave edin.\nŞekeri ekleyin.\nKarıştırarak koyulaşana kadar pişirin.\nSıcak servis yapın.",
    "Image_Name": "sut-urunsuz-hosmerim",
    "Cleaned_Ingredients": "['tofu', 'margarin', 'toz şeker', 'un']"
  },
  {
    "Title": "Glutensiz Kayseri Mantısı (Glutensiz)",
    "Ingredients": "['1 su bardağı mısır unu', '1 su bardağı pirinç unu', '1 adet yumurta', '0.5 su bardağı su', '1 çay kaşığı tuz', '200 gram dana kıyma', '1 adet soğan', '1 su bardağı yoğurt', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber', '1 çay kaşığı nane']",
    "Instructions": "Mısır unu, pirinç unu, yumurta, su ve tuzla hamur yoğurun.\nDinlendirin.\nKıyma ve soğanla iç harç yapın.\nHamuru açıp küçük kareler kesin.\nDoldurup kapatın.\nKaynayan suda haşlayın.\nYoğurt ve tereyağlı sos ile servis yapın.",
    "Image_Name": "glutensiz-kayseri-mantisi",
    "Cleaned_Ingredients": "['mısır unu', 'pirinç unu', 'yumurta', 'su', 'tuz', 'dana kıyma', 'soğan', 'yoğurt', 'tereyağı', 'pul biber', 'nane']"
  },
  {
    "Title": "Vegan Lobik (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı taze barbunya', '2 adet patates', '1 adet soğan', '2 adet domates', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '2 su bardağı su']",
    "Instructions": "Soğanı zeytinyağında kavurun.\nSalçayı ekleyin.\nBarbunya ve patatesleri ilave edin.\nDomatesleri rendeleyin ve ekleyin.\nSuyu ilave edin.\nKısık ateşte 35 dakika pişirin.",
    "Image_Name": "vegan-lobik",
    "Cleaned_Ingredients": "['taze barbunya', 'patates', 'soğan', 'domates', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'su']"
  },
  {
    "Title": "Süt Ürünsüz Çırpma (Süt Ürünü Yok)",
    "Ingredients": "['4 adet yumurta', '2 su bardağı soya yoğurt', '1 su bardağı un', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı nane', '1 çay kaşığı pul biber', '1 çay kaşığı tuz', '3 su bardağı su']",
    "Instructions": "Yumurta, soya yoğurt ve unu çırpın.\nSuyu ekleyip karıştırın.\nTencereye alıp sürekli karıştırarak kaynatın.\nKoyulaşana kadar pişirin.\nZeytinyağını kızdırıp nane ve pul biber ekleyin.\nÜzerine gezdirerek servis yapın.",
    "Image_Name": "sut-urunsuz-cirpma",
    "Cleaned_Ingredients": "['yumurta', 'soya yoğurt', 'un', 'zeytinyağı', 'nane', 'pul biber', 'tuz', 'su']"
  },
  {
    "Title": "Vegan Gendime Pilavı (Vegan)",
    "Ingredients": "['2 su bardağı gendime', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '3 su bardağı sebze suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Gendimeyi yıkayıp ıslatın.\nSoğanı zeytinyağında kavurun.\nSalçayı ekleyin.\nGendimeyi ilave edip kavurun.\nSebze suyunu ve tuzu ekleyin.\nKısık ateşte 20 dakika pişirip demlendirin.",
    "Image_Name": "vegan-gendime-pilavi",
    "Cleaned_Ingredients": "['gendime', 'soğan', 'zeytinyağı', 'domates salçası', 'sebze suyu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Süt Ürünsüz Kaygana (Süt Ürünü Yok)",
    "Ingredients": "['4 adet yumurta', '2 yemek kaşığı un', '0.5 su bardağı yulaf sütü', '1 çay kaşığı tuz', '2 yemek kaşığı zeytinyağı']",
    "Instructions": "Yumurta, un, yulaf sütü ve tuzu çırpın.\nZeytinyağını tavada kızdırın.\nKarışımı dökün.\nAltı kızarınca çevirin.\nİki tarafı da kızarana kadar pişirin.\nSıcak servis yapın.",
    "Image_Name": "sut-urunsuz-kaygana",
    "Cleaned_Ingredients": "['yumurta', 'un', 'yulaf sütü', 'tuz', 'zeytinyağı']"
  },
  {
    "Title": "Vegan Ekşili Pilav (Vegan & Glutensiz)",
    "Ingredients": "['2 su bardağı pirinç', '200 gram istiridye mantarı', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '2 yemek kaşığı nar ekşisi', '3 su bardağı sebze suyu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Mantarları doğrayıp zeytinyağında kavurun.\nSoğanı ekleyin.\nPirinci ilave edip kavurun.\nSebze suyunu ve nar ekşisini ekleyin.\nTuzu ilave edin.\nKısık ateşte 15 dakika pişirip demlendirin.",
    "Image_Name": "vegan-eksili-pilav",
    "Cleaned_Ingredients": "['pirinç', 'istiridye mantarı', 'soğan', 'zeytinyağı', 'nar ekşisi', 'sebze suyu', 'tuz', 'karabiber']"
  },
  {
    "Title": "Kuruyemişsiz Sütlü Nuriye (Kuruyemiş Alerjisi)",
    "Ingredients": "['500 gram baklava yufkası', '200 gram tereyağı', '1 litre süt', '1 su bardağı toz şeker', '1 paket vanilya']",
    "Instructions": "Yufkaları tepsiye sererek aralarına tereyağı sürün.\nDilimleyip 180 derece fırında 30 dakika pişirin.\nSütü ve şekeri kaynatıp vanilyayı ekleyin.\nSıcak tatlının üzerine sıcak sütü dökün.\nBuzdolabında 3 saat soğutun.",
    "Image_Name": "kuruyemissiz-sutlu-nuriye",
    "Cleaned_Ingredients": "['baklava yufkası', 'tereyağı', 'süt', 'toz şeker', 'vanilya']"
  },
  {
    "Title": "Glutensiz Bici Bici (Glutensiz & Vegan)",
    "Ingredients": "['1 su bardağı mısır nişastası', '4 su bardağı su', '1 su bardağı toz şeker', '1 yemek kaşığı gül suyu', 'buz']",
    "Instructions": "Mısır nişastası ve suyu karıştırıp kaynatın.\nKoyulaşana kadar pişirin.\nGeniş tepsiye dökün.\nSoğuyunca küp küp kesin.\nŞeker ve suyla şerbet yapın.\nGül suyunu ekleyin.\nBuz üzerine nişasta küplerini koyup şerbet dökün.",
    "Image_Name": "glutensiz-bici-bici",
    "Cleaned_Ingredients": "['mısır nişastası', 'su', 'toz şeker', 'gül suyu', 'buz']"
  },
  {
    "Title": "Vegan Katıklı Ekmek (Vegan & Glutensiz)",
    "Ingredients": "['3 su bardağı mısır unu', '1 su bardağı ılık su', '1 çay kaşığı tuz', '200 gram ıspanak', '1 adet soğan', '2 yemek kaşığı zeytinyağı']",
    "Instructions": "Mısır unu, su ve tuzu yoğurun.\nIspanakları doğrayıp zeytinyağında soğanla kavurun.\nHamuru açıp içine ıspanaklı harcı koyun.\nKapatıp sacda veya tavada pişirin.",
    "Image_Name": "vegan-katikli-ekmek",
    "Cleaned_Ingredients": "['mısır unu', 'su', 'tuz', 'ıspanak', 'soğan', 'zeytinyağı']"
  },
  {
    "Title": "Süt Ürünsüz Tirit (Süt Ürünü Yok)",
    "Ingredients": "['4 adet bayat pide', '500 gram kuzu eti', '2 su bardağı soya yoğurt', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı pul biber', '1 çay kaşığı tuz', '3 su bardağı et suyu']",
    "Instructions": "Kuzu etini haşlayın.\nPideleri küçük parçalara bölün.\nEt suyunu ısıtın.\nPide parçalarını tabağa dizin.\nÜzerine et suyu dökün.\nEtleri yerleştirin.\nSoya yoğurt gezdirin.\nZeytinyağını kızdırıp pul biberle dökün.",
    "Image_Name": "sut-urunsuz-tirit",
    "Cleaned_Ingredients": "['bayat pide', 'kuzu eti', 'soya yoğurt', 'zeytinyağı', 'pul biber', 'tuz', 'et suyu']"
  },
  {
    "Title": "Vegan Arabaşı Çorbası (Vegan)",
    "Ingredients": "['200 gram istiridye mantarı', '2 yemek kaşığı un', '2 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '6 su bardağı sebze suyu']",
    "Instructions": "Mantarları doğrayıp haşlayın.\nZeytinyağında unu kavurun.\nSalçayı ekleyin.\nSebze suyunu azar azar ilave edin.\nHaşlanmış mantarları ekleyin.\nKısık ateşte 15 dakika pişirin.",
    "Image_Name": "vegan-arabasi-corbasi",
    "Cleaned_Ingredients": "['istiridye mantarı', 'un', 'zeytinyağı', 'domates salçası', 'tuz', 'karabiber', 'sebze suyu']"
  },
  {
    "Title": "Süt Ürünsüz Gülüzar Çorbası (Süt Ürünü Yok)",
    "Ingredients": "['1 su bardağı kırmızı mercimek', '1 su bardağı bulgur', '1 adet soğan', '2 yemek kaşığı zeytinyağı', '2 yemek kaşığı domates salçası', '1 yemek kaşığı biber salçası', '1 çay kaşığı nane', '1 çay kaşığı tuz', '6 su bardağı su']",
    "Instructions": "Mercimeği yıkayıp suda haşlayın.\nSoğanı zeytinyağında kavurun.\nSalçaları ekleyin.\nKavurmayı mercimeğe ilave edin.\nBulguru ekleyin.\n20 dakika daha pişirin.\nNane ve tuzu ilave edin.",
    "Image_Name": "sut-urunsuz-guluzar-corbasi",
    "Cleaned_Ingredients": "['kırmızı mercimek', 'bulgur', 'soğan', 'zeytinyağı', 'domates salçası', 'biber salçası', 'nane', 'tuz', 'su']"
  },
  {
    "Title": "Vegan Düğürcük Çorbası (Vegan)",
    "Ingredients": "['200 gram soya kıyma', '0.5 su bardağı pirinç', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı nane', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '6 su bardağı sebze suyu']",
    "Instructions": "Soya kıymayı ıslatıp süzün.\nPirinç, tuz ve karabiberle yoğurun.\nKüçük köfteler yapın.\nSoğanı zeytinyağında kavurup salçayı ekleyin.\nSebze suyunu ilave edip kaynatın.\nKöfteleri tek tek bırakın.\n20 dakika pişirin.\nNane serpin.",
    "Image_Name": "vegan-dugurcuk-corbasi",
    "Cleaned_Ingredients": "['soya kıyma', 'pirinç', 'soğan', 'domates salçası', 'zeytinyağı', 'nane', 'tuz', 'karabiber', 'sebze suyu']"
  },
  {
    "Title": "Sırın",
    "Ingredients": "['2 su bardağı un', '1 su bardağı su', '1 çay kaşığı tuz', '200 gram lor peyniri', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber']",
    "Instructions": "Un, su ve tuzla yumuşak hamur yoğurun.\nHamuru ince açın.\nKaynayan suda haşlayın.\nTabağa alıp lor peyniri serpin.\nTereyağını kızdırıp pul biberle üzerine dökün.",
    "Image_Name": "sirin",
    "Cleaned_Ingredients": "['un', 'su', 'tuz', 'lor peyniri', 'tereyağı', 'pul biber']"
  },
  {
    "Title": "Ayran Aşı Çorbası",
    "Ingredients": "['2 su bardağı yoğurt', '1 su bardağı un', '1 adet yumurta', '0.5 su bardağı pirinç', '1 yemek kaşığı nane', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '5 su bardağı su']",
    "Instructions": "Yoğurt, un ve yumurtayı çırpın.\nSuyu azar azar ekleyin.\nTencereye alıp sürekli karıştırarak kaynatın.\nPirinci ekleyin.\n20 dakika pişirin.\nTereyağını eritip nane ile kızdırın.\nÜzerine gezdirin.",
    "Image_Name": "ayran-asi-corbasi",
    "Cleaned_Ingredients": "['yoğurt', 'un', 'yumurta', 'pirinç', 'nane', 'tereyağı', 'tuz', 'su']"
  },
  {
    "Title": "Glutensiz Hıngel (Glutensiz)",
    "Ingredients": "['1 su bardağı mısır unu', '1 su bardağı pirinç unu', '1 adet yumurta', '0.5 su bardağı su', '1 çay kaşığı tuz', '200 gram dana kıyma', '1 adet soğan', '1 su bardağı yoğurt', '2 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber']",
    "Instructions": "Mısır unu, pirinç unu, yumurta, su ve tuzla hamur yoğurun.\nDinlendirin.\nKıyma ve soğanla iç harç yapın.\nHamuru açıp kareler kesin.\nİçini doldurup üçgen kapatın.\nKaynayan suda haşlayın.\nSarımsaklı yoğurt ve tereyağlı sos ile servis yapın.",
    "Image_Name": "glutensiz-hingel",
    "Cleaned_Ingredients": "['mısır unu', 'pirinç unu', 'yumurta', 'su', 'tuz', 'dana kıyma', 'soğan', 'yoğurt', 'sarımsak', 'tereyağı', 'pul biber']"
  },
  {
    "Title": "Vegan Çullama (Vegan)",
    "Ingredients": "['300 gram istiridye mantarı', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '4 adet lavaş', '2 su bardağı sebze suyu', '2 yemek kaşığı margarin', '1 çay kaşığı pul biber']",
    "Instructions": "Mantarları doğrayıp zeytinyağında kavurun.\nLavaşları parçalayın.\nTabağa lavaş parçaları dizin.\nÜzerine sebze suyu dökün.\nKavurulmuş mantarları yerleştirin.\nMargarini kızdırıp pul biberle üzerine dökün.",
    "Image_Name": "vegan-cullama",
    "Cleaned_Ingredients": "['istiridye mantarı', 'zeytinyağı', 'tuz', 'karabiber', 'lavaş', 'sebze suyu', 'margarin', 'pul biber']"
  },
  {
    "Title": "Süt Ürünsüz Çeçil Peynirli Börek (Süt Ürünü Yok)",
    "Ingredients": "['4 adet yufka', '200 gram vegan kaşar', '2 yemek kaşığı margarin', '1 su bardağı yulaf sütü', '2 adet yumurta', '1 çay kaşığı tuz']",
    "Instructions": "Yulaf sütü, yumurta ve tuzu çırpın.\nYufkaları sütlü karışıma batırın.\nVegan kaşarı rulo şeklinde sarın.\nTepsiye dizin.\nEritilmiş margarini gezdirin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "sut-urunsuz-cecil-peynirli-borek",
    "Cleaned_Ingredients": "['yufka', 'vegan kaşar', 'margarin', 'yulaf sütü', 'yumurta', 'tuz']"
  },
  {
    "Title": "Vegan Mumbar Dolması (Vegan)",
    "Ingredients": "['4 adet kabak', '1 su bardağı pirinç', '1 adet soğan', '1 yemek kaşığı domates salçası', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon', '2 su bardağı sebze suyu']",
    "Instructions": "Kabakları oyun.\nPirinç, soğan, salça, zeytinyağı ve baharatları karıştırın.\nHarcı kabaklara doldurun.\nTencereye dizin.\nSebze suyunu ekleyin.\nKısık ateşte 35 dakika pişirin.",
    "Image_Name": "vegan-mumbar-dolmasi",
    "Cleaned_Ingredients": "['kabak', 'pirinç', 'soğan', 'domates salçası', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber', 'kimyon', 'sebze suyu']"
  },
  {
    "Title": "Glutensiz Maraş Tarhanası Çorbası (Glutensiz)",
    "Ingredients": "['100 gram glutensiz tarhana', '1 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı nane', '1 çay kaşığı pul biber', '1 çay kaşığı tuz', '5 su bardağı su']",
    "Instructions": "Glutensiz tarhana parçalarını suda ıslatın.\nTereyağında salçayı kavurun.\nIslatılmış tarhanayı ve suyunu ekleyin.\nKaynayana kadar karıştırarak pişirin.\nNane, pul biber ve tuzu ilave edin.\n15 dakika kısık ateşte pişirin.",
    "Image_Name": "glutensiz-maras-tarhanasi",
    "Cleaned_Ingredients": "['glutensiz tarhana', 'tereyağı', 'domates salçası', 'nane', 'pul biber', 'tuz', 'su']"
  },
  {
    "Title": "Süt Ürünsüz Yağlama (Süt Ürünü Yok)",
    "Ingredients": "['4 adet yufka', '200 gram vegan kaşar', '2 yemek kaşığı margarin', '1 su bardağı yulaf sütü', '2 adet yumurta', '1 çay kaşığı tuz']",
    "Instructions": "Yulaf sütü ve yumurtayı karıştırın.\nYufkaları karışıma batırın.\nTepsiye sererek aralarına vegan kaşar serpin.\nMargarini eritip üzerine gezdirin.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "sut-urunsuz-yaglama",
    "Cleaned_Ingredients": "['yufka', 'vegan kaşar', 'margarin', 'yulaf sütü', 'yumurta', 'tuz']"
  },
  {
    "Title": "Patates Köftesi",
    "Ingredients": "['4 adet patates', '1 adet yumurta', '2 yemek kaşığı un', '1 adet soğan', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '2 yemek kaşığı sıvı yağ', 'Kızartmak için sıvı yağ']",
    "Instructions": "Patatesleri haşlayıp kabuklarını soyun ve ezerek püre haline getirin.\nSoğanı rendeleyip suyunu sıkın.\nPatates püresine yumurta, un, soğan, tuz, karabiber ve pul biberi ekleyip yoğurun.\nCeviz büyüklüğünde köfteler şekillendirin.\nKızgın yağda her iki tarafını kızartın.\nKağıt havlu üzerinde fazla yağı alın ve sıcak servis yapın.",
    "Image_Name": "patates-koftesi",
    "Cleaned_Ingredients": "['patates', 'yumurta', 'un', 'soğan', 'tuz', 'karabiber', 'pul biber', 'sıvı yağ', 'sıvı yağ']"
  },
  {
    "Title": "Sodalı Köfte",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '2 dilim bayat ekmek', '1 çay kaşığı karbonat', '1 yumurta', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '2 yemek kaşığı sıvı yağ', 'Kızartmak için sıvı yağ']",
    "Instructions": "Soğanı rendeleyip suyunu sıkın.\nBayat ekmeği ıslatıp suyunu sıkın.\nKıymaya soğan, ekmek, karbonat, yumurta ve baharatları ekleyip iyice yoğurun.\nBuzdolabında 30 dakika dinlendirin.\nKöfteleri şekillendirip kızgın yağda kızartın.\nSıcak servis yapın.",
    "Image_Name": "sodali-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'bayat ekmek', 'karbonat', 'yumurta', 'tuz', 'karabiber', 'pul biber', 'sıvı yağ', 'sıvı yağ']"
  },
  {
    "Title": "Mantarlı Tavuk",
    "Ingredients": "['500 gram tavuk göğsü', '300 gram kültür mantarı', '2 adet soğan', '2 adet domates', '2 adet sivri biber', '3 yemek kaşığı sıvı yağ', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Tavukları kuşbaşı doğrayın.\nMantarları dilimleyin, soğan ve biberleri doğrayın.\nTavada yağı kızdırıp tavukları kavurun.\nSoğan ve biberleri ekleyip soteleyin.\nMantarları ve salçayı ilave edin.\nDomatesleri ekleyip kısık ateşte 15 dakika pişirin.\nBaharatlarla tatlandırıp servis yapın.",
    "Image_Name": "mantarli-tavuk",
    "Cleaned_Ingredients": "['tavuk göğsü', 'kültür mantarı', 'soğan', 'domates', 'sivri biber', 'sıvı yağ', 'domates salçası', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Mantar Sote",
    "Ingredients": "['1 paket kültür mantarı', '1 adet orta boy soğan', '3 yemek kaşığı sıvı yağ', '1/2 yemek kaşığı tereyağı', '1 adet büyük boy domates', '2 adet yeşil biber', '1 adet kapya biber', '2 diş sarımsak', '1 yemek kaşığı salça', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1/2 çay kaşığı karabiber', '1 tutam kıyılmış maydanoz']",
    "Instructions": "Tencereye tereyağı ve sıvı yağı ekleyin. Soğanı yemeklik doğrayıp kavurun.\nYeşil biber ve kapya biberi ekleyip kavurmaya devam edin.\nMantarları iri doğrayıp ekleyin. 2 dakika dokunmayın, sonra karıştırın.\nTuz, pul biber ve karabiberi ekleyin.\nSalçayı ilave edip karıştırın. Gerekirse 1/2 su bardağı sıcak su ekleyin.\nKüp küp domatesi ekleyin. Kısık ateşte 10 dakika pişirin.\nMaydanoz serperek servis edin.",
    "Image_Name": "mantar-sote",
    "Cleaned_Ingredients": "['kültür mantarı', 'soğan', 'sıvı yağ', 'tereyağı', 'domates', 'yeşil biber', 'kapya biber', 'sarımsak', 'salça', 'tuz', 'pul biber', 'karabiber', 'kıyılmış maydanoz']"
  },
  {
    "Title": "Ispanaklı Fırın Patates",
    "Ingredients": "['6 adet patates', '250 gram ıspanak', '1 adet soğan', '2 diş sarımsak', '100 gram rendelenmiş kaşar peyniri', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Patatesleri soyup dilimleyin ve haşlayın.\nIspanağı yıkayıp soteleyin, soğan ve sarımsak ekleyin.\nFırın kabına patates dilimlerini dizin.\nÜzerine ıspanaklı harç ve kaşar peyniri ekleyin.\nZeytinyağı ve baharatlarla tatlandırın.\n180 derece fırında 25 dakika pişirin.",
    "Image_Name": "ispanakli-firin-patates",
    "Cleaned_Ingredients": "['patates', 'ıspanak', 'soğan', 'sarımsak', 'rendelenmiş kaşar peyniri', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Fırında Soslu Karnabahar",
    "Ingredients": "['1 adet orta boy karnabahar', '3 adet yumurta', '1/2 su bardağı süt', '4 yemek kaşığı un', '1 çay kaşığı tuz', '1/2 paket kabartma tozu', '1/2 çay bardağı sıvı yağ', '1 adet rendelenmiş havuç', '1/2 adet kıyılmış maydanoz', '1 su bardağı rendelenmiş kaşar peyniri', '6 yemek kaşığı süzme yoğurt', '1 çay kaşığı toz kırmızı biber', '4 yemek kaşığı sıvı yağ']",
    "Instructions": "Karnabaharı çiçek çiçek ayırıp haşlayın ve parçalayın.\nGeniş bir kaba alıp yumurta, süt, un, tuz, kabartma tozu, sıvı yağ, havuç ve maydanozu ekleyip karıştırın.\nYağlı fırın kabına harcı yerleştirin.\nÜzerini toz kırmızı biberle karıştırdığınız kaşar peyniri ile kaplayın.\n190 derece fırında 25 dakika üzeri kızarana kadar pişirin.\nDilimleyip üzerine yoğurt ve kızdırılmış yağ gezdirerek servis edin.",
    "Image_Name": "firinda-soslu-karnabahar",
    "Cleaned_Ingredients": "['karnabahar', 'yumurta', 'süt', 'un', 'tuz', 'kabartma tozu', 'sıvı yağ', 'rendelenmiş havuç', 'kıyılmış maydanoz', 'rendelenmiş kaşar peyniri', 'süzme yoğurt', 'toz kırmızı biber', 'sıvı yağ']"
  },
  {
    "Title": "Patates Oturtma",
    "Ingredients": "['4 adet büyük boy patates', '500 gram orta yağlı kıyma', '1 adet büyük boy soğan', '1 diş sarımsak', '1 yemek kaşığı tereyağı', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı domates salçası', '1.5 su bardağı domates konservesi', '4 adet sivri biber', '1 çay kaşığı tuz', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon', '1/2 çay kaşığı karabiber', '250 gram rendelenmiş kaşar peyniri']",
    "Instructions": "Patatesleri soyup ince yuvarlak dilimleyin. Fırın tepsisine yayıp zeytinyağı ve tuzla 180 derecede 15 dakika ön pişirin.\nTavada tereyağı ve zeytinyağı ile kıymayı kavurun. Soğan ve sarımsak ekleyin.\nSalça, domates ve sivri biberi ekleyip kavurun. Baharatları ilave edin.\nBorcamı yağlayıp patateslerin yarısını tabana dizin.\nÜzerine kıymalı harcı yayın. Kalan patatesleri dizin.\nKaşar peynirini serpin. 180 derece fırında 10 dakika, ardından ızgara ile 7-8 dakika daha pişirin.\n10-15 dakika dinlendirip servis yapın.",
    "Image_Name": "patates-oturtma",
    "Cleaned_Ingredients": "['patates', 'orta yağlı kıyma', 'soğan', 'sarımsak', 'tereyağı', 'zeytinyağı', 'domates salçası', 'domates konservesi', 'sivri biber', 'tuz', 'pul biber', 'kimyon', 'karabiber', 'rendelenmiş kaşar peyniri']"
  },
  {
    "Title": "Patates Yatağında Soslu Köfte",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '1 yumurta', '2 dilim ekmek içi', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '4 adet patates', '2 adet domates', '1 yemek kaşığı salça', '2 yemek kaşığı sıvı yağ', '1 su bardağı sıcak su']",
    "Instructions": "Kıyma, rendelenmiş soğan, yumurta, ıslatılmış ekmek ve baharatlarla köfte harcı hazırlayın.\nKöfteleri şekillendirin.\nPatatesleri dilimleyip fırın kabına dizin.\nÜzerine köfteleri yerleştirin.\nSalça, domates ve su ile sos hazırlayıp üzerine gezdirin.\n180 derece fırında 40 dakika pişirin.",
    "Image_Name": "patates-yataginda-soslu-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'yumurta', 'ekmek içi', 'tuz', 'karabiber', 'patates', 'domates', 'salça', 'sıvı yağ', 'sıcak su']"
  },
  {
    "Title": "Mantarlı Tavuk Sote",
    "Ingredients": "['500 gram tavuk but eti', '400 gram mantar', '1 adet soğan', '1 adet yeşil biber', '1 adet domates', '1 adet kırmızı biber', '3 yemek kaşığı zeytinyağı', '1 tatlı kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kimyon', '1 çay kaşığı kekik', '1 tatlı kaşığı kırmızı toz biber']",
    "Instructions": "Tavaya yağı alıp tavuk etlerini ekleyin. Suyunu salıp çekene kadar pişirin.\nSoğan ve biberleri doğrayıp ekleyin. 2-3 dakika kavurun.\nMantarları ekleyip 2-3 dakika pişirin.\nDomates, baharat ve tuzu ekleyin. Suyunu çekene kadar pişirin.\nSıcak servis yapın.",
    "Image_Name": "mantarli-tavuk-sote",
    "Cleaned_Ingredients": "['tavuk but eti', 'mantar', 'soğan', 'yeşil biber', 'domates', 'kırmızı biber', 'zeytinyağı', 'tuz', 'karabiber', 'kimyon', 'kekik', 'kırmızı toz biber']"
  },
  {
    "Title": "Kaşarlı Tas Kebabı",
    "Ingredients": "['500 gram kuşbaşı dana eti', '3 adet patates', '2 adet soğan', '2 adet domates', '2 adet sivri biber', '150 gram rendelenmiş kaşar peyniri', '2 yemek kaşığı tereyağı', '1 yemek kaşığı domates salçası', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Eti tereyağında kavurun.\nSoğanları ekleyin. Salçayı ilave edin.\nSu ekleyip 30 dakika pişirin.\nPatatesleri ekleyin. Domates ve biberleri ilave edin.\n20 dakika daha pişirin.\nServis tabağına alıp üzerine kaşar peyniri serpin. Fırında veya mikrodalgada eritip servis yapın.",
    "Image_Name": "kasarli-tas-kebabi",
    "Cleaned_Ingredients": "['kuşbaşı dana eti', 'patates', 'soğan', 'domates', 'sivri biber', 'rendelenmiş kaşar peyniri', 'tereyağı', 'domates salçası', 'tuz', 'karabiber']"
  },
  {
    "Title": "Sebzeli Misket Köfte",
    "Ingredients": "['400 gram kıyma', '1 adet soğan', '1 adet havuç', '1 adet patates', '1 adet kabak', '1 yumurta', '2 yemek kaşığı un', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '2 yemek kaşığı sıvı yağ', '1 yemek kaşığı salça', '1 su bardağı sıcak su']",
    "Instructions": "Sebzeleri rendeleyip suyunu sıkın.\nKıyma, soğan, sebzeler, yumurta, un ve baharatları karıştırıp yoğurun.\nCeviz büyüklüğünde köfteler yapın.\nTavada yağda köfteleri kavurun.\nSalça ve su ekleyip 15 dakika pişirin.",
    "Image_Name": "sebzeli-misket-kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'havuç', 'patates', 'kabak', 'yumurta', 'un', 'tuz', 'karabiber', 'sıvı yağ', 'salça', 'sıcak su']"
  },
  {
    "Title": "Tavuklu Patates Karnıyarık",
    "Ingredients": "['4 adet patates', '400 gram tavuk göğsü', '2 adet soğan', '2 adet domates', '2 adet sivri biber', '3 yemek kaşığı zeytinyağı', '1 yemek kaşığı salça', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Patatesleri ortadan ikiye bölüp içlerini oyun.\nTavuk ve soğanı kavurup salça, domates ve biber ekleyin.\nPatateslerin içine harcı doldurun.\nÜzerine domates dilimi koyun.\n180 derece fırında 45 dakika pişirin.",
    "Image_Name": "tavuklu-patates-karniyarik",
    "Cleaned_Ingredients": "['patates', 'tavuk göğsü', 'soğan', 'domates', 'sivri biber', 'zeytinyağı', 'salça', 'tuz', 'karabiber']"
  },
  {
    "Title": "Tavuk Kanat",
    "Ingredients": "['1 kg tavuk kanadı', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon', '1 diş sarımsak']",
    "Instructions": "Tavuk kanatlarını yıkayıp kurulayın.\nZeytinyağı, baharatlar ve ezilmiş sarımsakla marine edin. 1 saat bekletin.\nFırın tepsisine dizin.\n200 derece fırında 40-45 dakika pişirin. Ara ara çevirip üzeri kızarsın.",
    "Image_Name": "tavuk-kanat",
    "Cleaned_Ingredients": "['tavuk kanadı', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber', 'kimyon', 'sarımsak']"
  },
  {
    "Title": "Patatesli Bezelyeli Tavuk",
    "Ingredients": "['500 gram tavuk butu', '3 adet patates', '1 su bardağı bezelye', '2 adet soğan', '2 adet domates', '2 yemek kaşığı sıvı yağ', '1 yemek kaşığı salça', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Tavukları kuşbaşı doğrayıp yağda kavurun.\nSoğanı ekleyip soteleyin. Salçayı ilave edin.\nPatatesleri küp doğrayıp ekleyin. Su ekleyip 20 dakika pişirin.\nBezelye ve domatesleri ekleyin. 10 dakika daha pişirin.\nBaharatlarla tatlandırıp servis yapın.",
    "Image_Name": "patatesli-bezelyeli-tavuk",
    "Cleaned_Ingredients": "['tavuk butu', 'patates', 'bezelye', 'soğan', 'domates', 'sıvı yağ', 'salça', 'tuz', 'karabiber']"
  },
  {
    "Title": "Patatesli Tavuk Göğsü",
    "Ingredients": "['400 gram tavuk göğsü', '4 adet patates', '2 adet soğan', '2 adet domates', '2 yemek kaşığı sıvı yağ', '1 yemek kaşığı salça', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Tavuk göğsünü kuşbaşı doğrayın.\nPatatesleri dilimleyin.\nTavada tavuk ve soğanı kavurun.\nSalça, patates ve domates ekleyin. Su ilave edip kısık ateşte 30 dakika pişirin.\nBaharatlarla tatlandırın.",
    "Image_Name": "patatesli-tavuk-gogsu",
    "Cleaned_Ingredients": "['tavuk göğsü', 'patates', 'soğan', 'domates', 'sıvı yağ', 'salça', 'tuz', 'karabiber']"
  },
  {
    "Title": "Karnabahar Shots",
    "Ingredients": "['1 adet karnabahar', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon']",
    "Instructions": "Karnabaharı küçük çiçeklere ayırın.\nZeytinyağı ve baharatlarla karıştırın.\nFırın tepsisine dizin.\n200 derece fırında 20-25 dakika kızartın.\nSıcak veya ılık atıştırmalık olarak servis yapın.",
    "Image_Name": "karnabahar-shots",
    "Cleaned_Ingredients": "['karnabahar', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber', 'kimyon']"
  },
  {
    "Title": "Belen Tava",
    "Ingredients": "['500 gram kıyma', '4 adet patlıcan', '4 adet patates', '2 adet domates', '2 adet biber', '2 adet soğan', '3 yemek kaşığı sıvı yağ', '1 yemek kaşığı salça', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Patlıcan ve patatesleri alacalı soyup kızartın veya fırında pişirin.\nKıymayı soğanla kavurun. Salça ve baharatları ekleyin.\nFırın kabına patlıcan ve patatesleri dizin.\nÜzerine kıymalı harç, domates ve biber ekleyin.\n180 derece fırında 30 dakika pişirin.",
    "Image_Name": "belen-tava",
    "Cleaned_Ingredients": "['kıyma', 'patlıcan', 'patates', 'domates', 'biber', 'soğan', 'sıvı yağ', 'salça', 'tuz', 'karabiber']"
  },
  {
    "Title": "Patatesli Sulu Köfte",
    "Ingredients": "['300 gram kıyma', '1/2 su bardağı ince bulgur', '1 adet soğan', '1 yumurta', '3 adet patates', '2 adet domates', '1 yemek kaşığı salça', '4 su bardağı su', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Kıyma, bulgur, rendelenmiş soğan ve yumurtayı yoğurup köfteler yapın.\nTencerede salçayı kavurun. Su, domates ve patatesleri ekleyin.\nKöfteleri ekleyip kaynatın. Kısık ateşte 25 dakika pişirin.\nBaharatlarla tatlandırıp servis yapın.",
    "Image_Name": "patatesli-sulu-kofte",
    "Cleaned_Ingredients": "['kıyma', 'ince bulgur', 'soğan', 'yumurta', 'patates', 'domates', 'salça', 'su', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Sultan Kebabı",
    "Ingredients": "['750 gram kemiksiz tavuk eti', '5 adet yufka', '1 adet soğan', '2 adet yeşil biber', '1 adet kırmızı biber', '3 yemek kaşığı sıvı yağ', '1 su bardağı tavuk suyu', '1 kase yoğurt', '2 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı pul biber', '1 çay kaşığı kırmızı biber', 'tuz', 'karabiber']",
    "Instructions": "Tavukları küçük doğrayıp haşlayın.\nSoğanı yağda kavurun. Biberleri ekleyip kavurun.\nTavukları süzüp tavaya ekleyin. Tuz ve baharatları ilave edin. Soğumaya bırakın.\nYufkayı 8 parçaya bölün. İç harcı koyup sigara böreği gibi sarın.\nYağlı kağıt serili tepsiye dizin. 180 derece fırında kızartın.\nIlık tavuk suyuna 3-4 dakika batırıp çıkarın.\n2-3 parmak kalınlığında kesip yoğurt, sarımsak ve kızdırılmış tereyağı ile servis yapın.",
    "Image_Name": "sultan-kebabi",
    "Cleaned_Ingredients": "['kemiksiz tavuk eti', 'yufka', 'soğan', 'yeşil biber', 'kırmızı biber', 'sıvı yağ', 'tavuk suyu', 'kase yoğurt', 'sarımsak', 'tereyağı', 'pul biber', 'kırmızı biber', 'tuz', 'karabiber']"
  },
  {
    "Title": "Kuru Patlıcan Dolması",
    "Ingredients": "['20 adet kuru patlıcan', '1.5 su bardağı pirinç', '250 gram kıyma', '2 adet soğan', '2 adet domates', '1 demet maydanoz', '1 yemek kaşığı salça', '1 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '4 su bardağı sıcak su']",
    "Instructions": "Kuru patlıcanları sıcak suda 15 dakika bekletip yumuşatın.\nPirinci yıkayın. Kıyma, soğan, domates, maydanoz, salça ve baharatlarla iç harç hazırlayın.\nPatlıcanların içini açıp harçla doldurun.\nTencereye dizin. Zeytinyağı ve sıcak su ekleyin.\nKısık ateşte 45 dakika pişirin.",
    "Image_Name": "kuru-patlican-dolmasi",
    "Cleaned_Ingredients": "['kuru patlıcan', 'pirinç', 'kıyma', 'soğan', 'domates', 'demet maydanoz', 'salça', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber', 'sıcak su']"
  },
  {
    "Title": "Mantar Soslu Tavuk",
    "Ingredients": "['500 gram tavuk göğsü', '300 gram kültür mantarı', '1 kase krema', '2 diş sarımsak', '2 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı kekik']",
    "Instructions": "Tavukları kuşbaşı doğrayıp tereyağında kavurun.\nMantarları dilimleyip ekleyin. 5 dakika pişirin.\nKrema, ezilmiş sarımsak ve baharatları ekleyin.\nKısık ateşte 5 dakika daha pişirip servis yapın.",
    "Image_Name": "mantar-soslu-tavuk",
    "Cleaned_Ingredients": "['tavuk göğsü', 'kültür mantarı', 'kase krema', 'sarımsak', 'tereyağı', 'tuz', 'karabiber', 'kekik']"
  },
  {
    "Title": "Fırın Karnabahar",
    "Ingredients": "['1 adet karnabahar', '3 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon']",
    "Instructions": "Karnabaharı çiçek çiçek ayırın.\nZeytinyağı ve baharatlarla karıştırın.\nFırın tepsisine yayın.\n200 derece fırında 25-30 dakika pişirin. Ara ara karıştırın.",
    "Image_Name": "firin-karnabahar",
    "Cleaned_Ingredients": "['karnabahar', 'zeytinyağı', 'tuz', 'karabiber', 'pul biber', 'kimyon']"
  },
  {
    "Title": "Soğan Dolması",
    "Ingredients": "['6 adet büyük soğan', '1 su bardağı pirinç', '250 gram kıyma', '2 adet domates', '1 demet maydanoz', '1 yemek kaşığı salça', '2 yemek kaşığı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '3 su bardağı sıcak su']",
    "Instructions": "Soğanları haşlayıp içlerini oyun.\nPirinci yıkayın. Kıyma, domates, maydanoz, salça ve baharatlarla iç harç hazırlayın.\nSoğanların içine harç doldurun.\nTencereye dizin. Zeytinyağı ve su ekleyin.\nKısık ateşte 40 dakika pişirin.",
    "Image_Name": "sogan-dolmasi",
    "Cleaned_Ingredients": "['büyük soğan', 'pirinç', 'kıyma', 'domates', 'demet maydanoz', 'salça', 'zeytinyağı', 'tuz', 'karabiber', 'sıcak su']"
  },
  {
    "Title": "Tavuk Köftesi",
    "Ingredients": "['500 gram tavuk kıyması', '1 adet soğan', '1 yumurta', '2 yemek kaşığı galeta unu', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '2 yemek kaşığı sıvı yağ']",
    "Instructions": "Tavuk kıymasına rendelenmiş soğan, yumurta, galeta unu ve baharatları ekleyip yoğurun.\nCeviz büyüklüğünde köfteler şekillendirin.\nTavada veya ızgarada pişirin.\nSıcak servis yapın.",
    "Image_Name": "tavuk-koftesi",
    "Cleaned_Ingredients": "['tavuk kıyması', 'soğan', 'yumurta', 'galeta unu', 'tuz', 'karabiber', 'pul biber', 'sıvı yağ']"
  },
  {
    "Title": "Zeytinyağlı Patlıcan Yemeği",
    "Ingredients": "['4 adet patlıcan', '2 adet soğan', '3 adet domates', '2 adet sivri biber', '1 su bardağı zeytinyağı', '1 çay kaşığı tuz', '1 çay kaşığı şeker', '1 adet limon']",
    "Instructions": "Patlıcanları alacalı soyup küp doğrayın. Tuzlu suda bekletin.\nSoğanları zeytinyağında kavurun.\nPatlıcan ve biberleri ekleyin.\nDomatesleri ekleyip kısık ateşte 30 dakika pişirin.\nLimon suyu, tuz ve şekerle tatlandırın. Soğuk servis yapın.",
    "Image_Name": "zeytinyagli-patlican-yemegi",
    "Cleaned_Ingredients": "['patlıcan', 'soğan', 'domates', 'sivri biber', 'zeytinyağı', 'tuz', 'şeker', 'limon']"
  },
  {
    "Title": "Köfte",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '2 dilim ekmek içi', '1 yumurta', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '1 çay kaşığı kimyon']",
    "Instructions": "Soğanı rendeleyip suyunu sıkın.\nEkmek içini ıslatıp suyunu sıkın.\nKıymaya soğan, ekmek, yumurta ve baharatları ekleyip yoğurun.\nBuzdolabında 1 saat dinlendirin.\nKöfteleri şekillendirip ızgarada veya tavada pişirin.",
    "Image_Name": "kofte",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'ekmek içi', 'yumurta', 'tuz', 'karabiber', 'pul biber', 'kimyon']"
  },
  {
    "Title": "Zeytinyağlı Kuru Dolma",
    "Ingredients": "['20 adet kuru biber veya kuru patlıcan', '1.5 su bardağı pirinç', '3 adet soğan', '2 adet domates', '1 demet dereotu', '1 demet nane', '1 su bardağı zeytinyağı', '1 adet limon', '1 çay kaşığı tuz', '1 çay kaşığı şeker', '4 su bardağı sıcak su']",
    "Instructions": "Kuru dolmalıkları sıcak suda yumuşatın.\nPirinci yıkayın. Soğan, domates, dereotu, nane ve baharatlarla iç harç hazırlayın.\nDolmalıkları harçla doldurun.\nTencereye dizin. Zeytinyağı, limon suyu ve sıcak su ekleyin.\nKısık ateşte 45 dakika pişirin. Soğuk servis yapın.",
    "Image_Name": "zeytinyagli-kuru-dolma",
    "Cleaned_Ingredients": "['kuru biber veya kuru patlıcan', 'pirinç', 'soğan', 'domates', 'demet dereotu', 'demet nane', 'zeytinyağı', 'limon', 'tuz', 'şeker', 'sıcak su']"
  },
  {
    "Title": "Soslu Tavuk",
    "Ingredients": "['500 gram tavuk butu', '2 adet domates', '2 adet sivri biber', '1 adet soğan', '2 yemek kaşığı salça', '3 yemek kaşığı sıvı yağ', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 su bardağı sıcak su']",
    "Instructions": "Tavukları kuşbaşı doğrayıp yağda kavurun.\nSoğanı ekleyip soteleyin. Salçayı ilave edin.\nDomates ve biberleri doğrayıp ekleyin.\nSu ekleyip kısık ateşte 25 dakika pişirin.\nBaharatlarla tatlandırıp servis yapın.",
    "Image_Name": "soslu-tavuk",
    "Cleaned_Ingredients": "['tavuk butu', 'domates', 'sivri biber', 'soğan', 'salça', 'sıvı yağ', 'tuz', 'karabiber', 'sıcak su']"
  },
  {
    "Title": "Mantar Kavurması",
    "Ingredients": "['500 gram kültür mantarı', '2 adet soğan', '3 yemek kaşığı tereyağı', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber']",
    "Instructions": "Mantarları dilimleyin. Yıkamayın, nemli bezle silin.\nTavada tereyağını eritin. Soğanı kavurun.\nMantarları ekleyin. Yüksek ateşte 5-7 dakika kavurun.\nTuz ve baharatları ekleyip servis yapın.",
    "Image_Name": "mantar-kavurmasi",
    "Cleaned_Ingredients": "['kültür mantarı', 'soğan', 'tereyağı', 'tuz', 'karabiber', 'pul biber']"
  },
  {
    "Title": "Bayat Pide Kebabı",
    "Ingredients": "['4 adet bayat pide', '300 gram kıyma', '2 adet soğan', '2 adet domates', '2 adet biber', '2 yemek kaşığı sıvı yağ', '1 yemek kaşığı salça', '1 çay kaşığı tuz', '1 çay kaşığı karabiber']",
    "Instructions": "Kıymayı soğanla kavurun. Salça, domates ve biber ekleyin.\nBaharatlarla tatlandırın.\nBayat pideleri ısıtıp üzerine kıymalı harç koyun.\nFırında veya tavada ısıtıp servis yapın.",
    "Image_Name": "bayat-pide-kebabi",
    "Cleaned_Ingredients": "['bayat pide', 'kıyma', 'soğan', 'domates', 'biber', 'sıvı yağ', 'salça', 'tuz', 'karabiber']"
  },
  {
    "Title": "Taco",
    "Ingredients": "['8 adet taco ekmeği', '400 gram kıyma', '1 paket taco baharatı', '1 adet soğan', '2 adet domates', '1 kase marul', '1 kase rendelenmiş kaşar', '1 kase salsa sos', '1 kase ekşi krema']",
    "Instructions": "Kıymayı soğanla kavurun. Taco baharatını ekleyin.\nTaco ekmeklerini ısıtın.\nHer taco ekmeğine kıyma, doğranmış domates, marul, kaşar, salsa ve ekşi krema ekleyin.\nKatlayıp servis yapın.",
    "Image_Name": "taco",
    "Cleaned_Ingredients": "['taco ekmeği', 'kıyma', 'taco baharatı', 'soğan', 'domates', 'kase marul', 'kase rendelenmiş kaşar', 'kase salsa sos', 'kase ekşi krema']"
  },
  {
    "Title": "Ödemiş Köftesi",
    "Ingredients": "['500 gram kıyma', '1 adet soğan', '2 dilim ekmek içi', '1 yumurta', '1 çay kaşığı karbonat', '1 çay kaşığı tuz', '1 çay kaşığı karabiber', '1 çay kaşığı pul biber', '2 yemek kaşığı sıvı yağ']",
    "Instructions": "Soğanı rendeleyip suyunu sıkın.\nEkmek içini ıslatıp suyunu sıkın.\nKıymaya soğan, ekmek, yumurta, karbonat ve baharatları ekleyip yoğurun.\nİzmir usulü yassı köfteler şekillendirin.\nTavada veya ızgarada pişirin. Patates kızartması ile servis yapın.",
    "Image_Name": "odemis-koftesi",
    "Cleaned_Ingredients": "['kıyma', 'soğan', 'ekmek içi', 'yumurta', 'karbonat', 'tuz', 'karabiber', 'pul biber', 'sıvı yağ']"
  }
]
````

## File: backend/data/recipes.ts
````typescript
import { Recipe } from '../types';
````

## File: backend/evaluation/__init__.py
````python

````

## File: backend/evaluation/baselines.py
````python
logger = logging.getLogger(__name__)
⋮----
def _parse_ingredient_list(raw: str) -> List[str]
⋮----
parsed = ast.literal_eval(raw)
⋮----
parsed = json.loads(raw)
⋮----
def _jaccard(a: Set[str], b: Set[str]) -> float
⋮----
class JaccardRecommender
⋮----
def __init__(self)
⋮----
def _ensure_loaded(self) -> None
⋮----
recipes = recipe_service.get_all_recipes(limit=recipe_service.get_total_count())
⋮----
def recommend(self, query_ingredients: List[str], top_k: int = 10) -> List[str]
⋮----
query_set = {ing.strip().lower() for ing in query_ingredients}
scored = [
⋮----
jaccard_recommender = JaccardRecommender()
````

## File: backend/evaluation/dataset.py
````python
logger = logging.getLogger(__name__)
⋮----
QuerySet = List[Tuple[List[str], Set[str]]]
⋮----
def _parse_ingredient_list(raw: str) -> List[str]
⋮----
parsed = ast.literal_eval(raw)
⋮----
parsed = json.loads(raw)
⋮----
all_recipes = recipe_service.get_all_recipes(limit=recipe_service.get_total_count())
⋮----
rng = random.Random(seed)
shuffled = list(all_recipes)
⋮----
n_test = max(1, int(len(shuffled) * holdout_ratio))
test_recipes = shuffled[:n_test]
⋮----
queries: QuerySet = []
skipped = 0
⋮----
ingredients = _parse_ingredient_list(recipe.Cleaned_Ingredients)
⋮----
n_sample = min(rng.randint(sample_min, sample_max), len(ingredients))
sampled = rng.sample(ingredients, n_sample)
⋮----
async def fetch_interaction_queries(min_interactions: int = 3) -> QuerySet
⋮----
"""
    Leave-one-out evaluation using real user interactions.
    For each user with >= min_interactions like/cook events (with context_ingredients),
    hold out the most recent one; query = context_ingredients, ground-truth = recipe.
    """
⋮----
result = await conn.execute(
users = [row[0] for row in result.fetchall()]
⋮----
row = result.fetchone()
⋮----
query_ingredients = json.loads(ctx_json)
````

## File: backend/evaluation/metrics.py
````python
def precision_at_k(recommended: List[str], relevant: Set[str], k: int) -> float
⋮----
hits = sum(1 for r in recommended[:k] if r in relevant)
⋮----
def hit_rate_at_k(recommended: List[str], relevant: Set[str], k: int) -> float
⋮----
def ndcg_at_k(recommended: List[str], relevant: Set[str], k: int) -> float
⋮----
dcg = sum(
⋮----
n_ideal = min(len(relevant), k)
idcg = sum(1.0 / math.log2(i + 2) for i in range(n_ideal))
⋮----
def coverage(all_recommendations: List[List[str]], catalog_size: int) -> float
⋮----
unique = {item for recs in all_recommendations for item in recs}
⋮----
total = sum(item_popularity.values()) or 1
scores: List[float] = []
⋮----
pop = item_popularity.get(item, 1)
````

## File: backend/evaluation/reporter.py
````python
today = date.today().isoformat()
lines: List[str] = [f"
⋮----
sep = ["---"] + ["---:"] * (len(headers) - 1)
rows = [headers, sep]
⋮----
row = [system_name]
````

## File: backend/evaluation/runner.py
````python
logger = logging.getLogger(__name__)
⋮----
System = Callable[[List[str], int], List[str]]
⋮----
max_k = max(k_values)
results: Dict[str, Dict[str, float]] = {}
⋮----
all_recs: List[List[str]] = []
p_acc: Dict[int, List[float]] = {k: [] for k in k_values}
hr_acc: Dict[int, List[float]] = {k: [] for k in k_values}
ndcg_acc: Dict[int, List[float]] = {k: [] for k in k_values}
⋮----
recommended = recommend_fn(query_ingredients, max_k)
⋮----
recommended = []
⋮----
n = len(queries)
sys_metrics: Dict[str, float] = {}
````

## File: backend/scripts/build_faiss_index.py
````python
def main()
⋮----
recipes = recipe_service.recipes
⋮----
embeddings = embedding_service.encode_recipes_batch(recipes, batch_size=32)
````

## File: backend/scripts/build_tfidf_index.py
````python
def main()
⋮----
recipes = recipe_service.recipes
````

## File: backend/scripts/copy_variant_images.py
````python
ROOT = Path(__file__).resolve().parent.parent.parent
RECIPES_JSON = ROOT / "backend" / "data" / "recipes.json"
IMG_DIR = ROOT / "public" / "images" / "recipies"
⋮----
PREFIXES = [
⋮----
def main()
⋮----
data = json.loads(RECIPES_JSON.read_text(encoding="utf-8"))
existing = {f.name for f in IMG_DIR.iterdir() if f.suffix == ".jpg"}
⋮----
copied = 0
base_missing = []
⋮----
img_name = recipe.get("Image_Name", "")
⋮----
target = f"{img_name}.jpg"
⋮----
base = f"{img_name[len(prefix):]}.jpg"
````

## File: backend/scripts/download_manual_images.py
````python
ROOT = Path(__file__).resolve().parent.parent.parent
IMG_DIR = ROOT / "public" / "images" / "recipies"
⋮----
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; recipe-image-downloader/1.0)"}
⋮----
MANUAL_URLS: dict = {
⋮----
def download(url: str, dest: Path) -> bool
⋮----
req = urllib.request.Request(url, headers=HEADERS)
⋮----
data = r.read()
⋮----
def main()
⋮----
existing = {f.stem for f in IMG_DIR.iterdir() if f.suffix in (".jpg", ".jpeg")}
downloaded = 0
skipped = 0
⋮----
dest = IMG_DIR / f"{img_name}.jpg"
⋮----
size_kb = dest.stat().st_size // 1024
````

## File: backend/scripts/download_models.py
````python
def main()
````

## File: backend/scripts/evaluate_recommendations.py
````python
async def _fetch_db_data(min_interactions: int)
⋮----
interaction_queries = await fetch_interaction_queries(min_interactions)
⋮----
item_popularity: dict = {}
⋮----
result = await conn.execute(
item_popularity = {row[0]: int(row[1]) for row in result.fetchall()}
⋮----
def main() -> None
⋮----
parser = argparse.ArgumentParser(
⋮----
args = parser.parse_args()
⋮----
k_values = sorted(args.k) if args.k else [5, 10]
⋮----
catalog_size = recipe_service.get_total_count()
⋮----
loaded = faiss_service.load_index()
⋮----
synthetic_queries = build_synthetic_queries(
⋮----
systems = {
⋮----
synthetic_results = run_evaluation(
⋮----
interaction_results = None
⋮----
interaction_results = run_evaluation(
⋮----
# --- 6. Generate report ---
⋮----
report = generate_markdown_report(
⋮----
out_path = Path(args.output)
````

## File: backend/scripts/seed_users.py
````python
PASSWORD = "Test123456"
⋮----
FAKE_USERS = [
⋮----
async def insert_user(conn, user: dict) -> None
⋮----
dietary_json = json.dumps(user["dietary"], ensure_ascii=False)
⋮----
async def insert_fridge(conn, user: dict) -> None
⋮----
async def insert_interactions(conn, user: dict) -> None
⋮----
base_date = datetime.utcnow() - timedelta(days=30)
⋮----
created_at = base_date + timedelta(days=i * 2, hours=i)
⋮----
async def insert_consumption(conn, user: dict) -> None
⋮----
base_date = datetime.utcnow() - timedelta(days=20)
⋮----
consumed_at = base_date + timedelta(days=i * 3)
⋮----
async def seed_db() -> None
⋮----
async def signup_supabase(email: str, password: str, client: httpx.AsyncClient) -> str
⋮----
resp = await client.post(
⋮----
data = resp.json()
⋮----
body = resp.json()
msg = body.get("msg") or body.get("message") or body.get("error_description") or str(body)
⋮----
async def seed_supabase() -> None
⋮----
needs_confirm: list[str] = []
errors: list[str] = []
⋮----
result = await signup_supabase(user["email"], PASSWORD, client)
⋮----
async def main() -> None
````

## File: backend/scripts/set_supabase_password.py
````python
TARGET_EMAIL = "aysebelenpisdil@gmail.com"
NEW_PASSWORD  = "523103"
⋮----
SUPABASE_URL      = os.environ.get("SUPABASE_URL", "").rstrip("/")
SERVICE_ROLE_KEY  = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
⋮----
list_url = f"{SUPABASE_URL}/auth/v1/admin/users?email={TARGET_EMAIL}"
req = urllib.request.Request(
⋮----
data = json.loads(r.read())
⋮----
users = data.get("users", [])
user = next((u for u in users if u.get("email") == TARGET_EMAIL), None)
⋮----
# --- 2b. Yeni kullanıcı oluştur -----------------------------------------
create_url = f"{SUPABASE_URL}/auth/v1/admin/users"
payload = json.dumps({
⋮----
created = json.loads(r.read())
⋮----
user_id = created["id"]
⋮----
user_id = user["id"]
⋮----
# --- 3. Şifreyi güncelle ----------------------------------------------------
⋮----
update_url = f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}"
payload = json.dumps({"password": NEW_PASSWORD, "email_confirm": True}).encode()
⋮----
result = json.loads(r.read())
````

## File: backend/tests/__init__.py
````python

````

## File: backend/tests/test_evaluation_metrics.py
````python
def test_precision_at_k_basic()
⋮----
recs = ["A", "B", "C", "D", "E"]
relevant = {"B", "D"}
⋮----
def test_precision_at_k_all_relevant()
⋮----
recs = ["A", "B"]
relevant = {"A", "B"}
⋮----
def test_precision_at_k_no_relevant()
⋮----
recs = ["A", "B", "C"]
relevant = {"X", "Y"}
⋮----
def test_precision_at_k_zero_k()
⋮----
def test_precision_at_k_k_larger_than_list()
⋮----
relevant = {"A"}
⋮----
def test_hit_rate_hit()
⋮----
def test_hit_rate_miss()
⋮----
relevant = {"X"}
⋮----
def test_hit_rate_relevant_outside_k()
⋮----
recs = ["A", "C", "D", "B", "E"]
relevant = {"B"}
⋮----
def test_ndcg_perfect_ranking()
⋮----
def test_ndcg_relevant_at_position_2()
⋮----
recs = ["X", "A", "Y"]
⋮----
expected = (1 / math.log2(3)) / (1 / math.log2(2))
⋮----
def test_ndcg_no_relevant_in_top_k()
⋮----
def test_ndcg_empty_relevant()
⋮----
def test_coverage_basic()
⋮----
all_recs = [["A", "B", "C"], ["D", "E", "F"], ["A", "G", "H"]]
⋮----
def test_coverage_full()
⋮----
all_recs = [["A", "B"], ["C", "D"]]
⋮----
def test_coverage_zero_catalog()
⋮----
def test_coverage_empty_recs()
⋮----
def test_novelty_uniform_popularity()
⋮----
popularity = {"A": 5, "B": 5, "C": 5}
all_recs = [["A", "B"], ["C"]]
total = 15
expected = -math.log2(5 / total)
⋮----
def test_novelty_less_popular_is_more_novel()
⋮----
popularity = {"popular": 100, "niche": 1}
score_popular = novelty([["popular"]], popularity)
score_niche = novelty([["niche"]], popularity)
⋮----
def test_novelty_unknown_item_gets_pop1()
⋮----
popularity = {"A": 10}
total = 10
expected_a = -math.log2(10 / total)
expected_u = -math.log2(1 / total)
expected = (expected_a + expected_u) / 2
⋮----
def test_novelty_empty()
````

## File: backend/tests/test_fridge.py
````python
async def test_fridge_requires_auth(client)
⋮----
r = await client.get("/api/fridge/ingredients")
⋮----
async def test_fridge_save_requires_auth(client)
⋮----
r = await client.post("/api/fridge/ingredients", json={"ingredients": ["domates"]})
⋮----
async def test_fridge_get_initially_empty(auth_client)
⋮----
async def test_fridge_save_and_retrieve(auth_client)
⋮----
ingredients = ["domates", "biber", "soğan"]
⋮----
r = await client.post("/api/fridge/ingredients", json={"ingredients": ingredients})
⋮----
data = r.json()
⋮----
saved = r.json()["ingredients"]
⋮----
async def test_fridge_full_overwrite(auth_client)
⋮----
async def test_fridge_empty_save(auth_client)
⋮----
async def test_fridge_strips_blank_ingredients(auth_client)
⋮----
r = await client.post("/api/fridge/ingredients", json={"ingredients": ["domates", "", "  "]})
````

## File: backend/tests/test_recipes.py
````python
async def test_get_recipes(client)
⋮----
r = await client.get("/api/recipes/")
⋮----
data = r.json()
⋮----
async def test_recommend_needs_ingredients(client)
⋮----
r = await client.post(
⋮----
async def test_recommend_with_ingredients(client)
````

## File: backend/tests/test_shopping_list.py
````python
async def test_shopping_list_get_requires_auth(client)
⋮----
r = await client.get("/api/shopping-list/items")
⋮----
async def test_shopping_list_post_requires_auth(client)
⋮----
r = await client.post("/api/shopping-list/items", json={"items": []})
⋮----
async def test_shopping_list_initially_accessible(auth_client)
⋮----
async def test_shopping_list_save_and_retrieve(auth_client)
⋮----
items = [
⋮----
r = await client.post("/api/shopping-list/items", json={"items": items})
⋮----
data = r.json()
⋮----
saved = r.json()["items"]
names = {i["name"] for i in saved}
⋮----
async def test_shopping_list_full_overwrite(auth_client)
⋮----
saved_names = {i["name"] for i in r.json()["items"]}
⋮----
async def test_shopping_list_purchased_flag_persisted(auth_client)
⋮----
item = next(i for i in r.json()["items"] if i["name"] == "seker")
⋮----
async def test_shopping_list_from_recipes_persisted(auth_client)
⋮----
recipes = ["Hünkar Beğendi", "İmam Bayıldı"]
⋮----
item = next(i for i in r.json()["items"] if i["name"] == "patlican2")
⋮----
async def test_shopping_list_empty_save_clears(auth_client)
⋮----
async def test_shopping_list_blank_name_ignored(auth_client)
⋮----
names = {i["name"] for i in r.json()["items"]}
⋮----
async def test_shopping_list_item_name_normalized_lowercase(auth_client)
⋮----
"""item_name is stored lowercase regardless of input case."""
⋮----
names = [i["name"] for i in r.json()["items"]]
````

## File: backend/tests/test_survey.py
````python
async def test_survey_requires_auth(client)
⋮----
r = await client.post(
⋮----
async def test_survey_stats_requires_auth(client)
⋮----
r = await client.get("/api/feedback/survey/stats")
⋮----
async def test_submit_survey_success(auth_client)
⋮----
data = r.json()
⋮----
async def test_submit_survey_minimal(auth_client)
⋮----
async def test_submit_survey_invalid_rating_zero(auth_client)
⋮----
async def test_submit_survey_invalid_rating_six(auth_client)
⋮----
async def test_submit_survey_invalid_intent(auth_client)
⋮----
async def test_submit_survey_comment_too_long(auth_client)
⋮----
async def test_get_survey_stats(auth_client)
⋮----
payloads = [
⋮----
r = await client.post("/api/feedback/survey", json=p)
````

## File: backend/tests/test_tfidf_service.py
````python
class DummyRecipe
⋮----
def __init__(self, title, cleaned)
⋮----
CORPUS = [
⋮----
@pytest.fixture
def built_service(tmp_path)
⋮----
svc = TFIDFService(
⋮----
@pytest.fixture
def loaded_service(tmp_path)
⋮----
svc2 = TFIDFService(
⋮----
def test_clean_ingredients_strips_brackets()
⋮----
raw = "['domates', 'soğan', 'tuz']"
result = _clean_ingredients_text(raw)
⋮----
def test_build_matrix_shape(built_service)
⋮----
def test_build_vocab_nonempty(built_service)
⋮----
def test_is_loaded_after_build(built_service)
⋮----
def test_roundtrip_shape(loaded_service)
⋮----
def test_roundtrip_vocab(loaded_service, built_service)
⋮----
def test_is_loaded_after_load(loaded_service)
⋮----
def test_load_returns_false_missing_files(tmp_path)
⋮----
def test_domates_query_top_result(built_service)
⋮----
def test_mercimek_query_top_result(built_service)
⋮----
def test_scores_descending(built_service)
⋮----
def test_unknown_ingredient_returns_empty(built_service)
⋮----
def test_k_limits_results(built_service)
⋮----
def test_scores_nonnegative(built_service)
⋮----
def test_rrf_merge_two_lists()
⋮----
result = RAGPipeline._rrf_fuse([[0, 1, 2], [1, 0, 3]], top_k=4, rrf_k=60)
⋮----
def test_rrf_dedup()
⋮----
result = RAGPipeline._rrf_fuse([[0, 1, 2], [0, 2, 1]], top_k=10, rrf_k=60)
⋮----
def test_rrf_top_k_limits(built_service)
⋮----
result = RAGPipeline._rrf_fuse([[0, 1, 2], [2, 1, 0]], top_k=2, rrf_k=60)
````

## File: backend/tests/test_user_preferences.py
````python
async def test_preferences_requires_auth(client)
⋮----
r = await client.get("/api/user/preferences")
⋮----
async def test_save_preferences_requires_auth(client)
⋮----
r = await client.post("/api/user/preferences", json={"dietary": {}, "excluded": []})
⋮----
async def test_preferences_default_empty(auth_client)
⋮----
data = r.json()
⋮----
async def test_save_and_retrieve_preferences(auth_client)
⋮----
payload = {
r = await client.post("/api/user/preferences", json=payload)
⋮----
async def test_preferences_overwrite(auth_client)
````

## File: backend/.env.example
````
# Gerekli (asla gerçek değerleri commit etmeyin)
GEMINI_API_KEY=your_gemini_api_key
SESSION_SECRET=rastgele-guvenli-bir-string

# Magic Link E-posta (SMTP)
# SMTP_ENABLED=true yaparak e-posta gönderimini etkinleştirin
SMTP_ENABLED=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# Gmail için: "Uygulama şifresi" (App Password) kullanın; normal şifre çalışmaz.
# https://myaccount.google.com/apppasswords

FRONTEND_URL=http://localhost:3000
````

## File: backend/.gitignore
````
__pycache__/
*.pyc
*.pyo
.env
venv/
.venv/
*.log
.DS_Store
*.db
*.db-wal
*.db-shm
.pytest_cache/
````

## File: backend/.python-version
````
3.11
````

## File: backend/pytest.ini
````ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_functions = test_*
````

## File: src/components/RecipeSurvey.tsx
````typescript
import React, { useState } from 'react';
import { submitSurvey } from '../utils/api';
⋮----
interface RecipeSurveyProps {
    contextIngredients: string[];
    recipeTitles: string[];
    onComplete: () => void;
}
⋮----
const handleSubmit = async () =>
⋮----
onMouseLeave=
````

## File: src/constants/ingredientData.ts
````typescript
export interface IngredientMetadata {
  emoji: string;
  category: string;
  label: string;
}
⋮----
export function getIngredientDetails(name: string): IngredientMetadata
⋮----
export function groupIngredientsByCategory(ingredientNames: string[]): Record<string, string[]>
⋮----
export function sortCategories(categories: string[]): string[]
````

## File: src/data/calorieData.json
````json
{
  "tuz": 0,
  "soğan": 16,
  "karabiber": 3,
  "zeytinyağı": 120,
  "su": 0,
  "pul biber": 4,
  "tereyağı": 108,
  "toz şeker": 60,
  "domates": 18,
  "domates salçası": 30,
  "yumurta": 78,
  "un": 180,
  "patates": 77,
  "sarımsak": 5,
  "sivri biber": 10,
  "limon": 12,
  "maydanoz": 5,
  "vanilya": 5,
  "pirinç": 180,
  "süt": 60,
  "kimyon": 4,
  "mısır unu": 120,
  "biber salçası": 25,
  "kıyma": 200,
  "nane": 2,
  "yulaf sütü": 48,
  "limon suyu": 8,
  "kekik": 3,
  "kızartma yağı": 180,
  "mısır nişastası": 60,
  "yoğurt": 60,
  "patlıcan": 20,
  "yaş maya": 10,
  "şeker": 60,
  "havuç": 16,
  "sıvı yağ": 120,
  "kabartma tozu": 2,
  "yufka": 120,
  "dereotu": 3,
  "margarin": 108,
  "beyaz peynir": 80,
  "pirinç unu": 140,
  "dana eti": 250,
  "kuzu eti": 280,
  "kırmızı mercimek": 170,
  "nişasta": 60,
  "nohut": 180,
  "ceviz": 130,
  "glutensiz un karışımı": 170,
  "lavaş": 120,
  "nar ekşisi": 20,
  "sebze suyu": 10,
  "kakao": 40,
  "instant maya": 10,
  "irmik": 130,
  "tavuk suyu": 15,
  "kabak": 14,
  "kaşar peyniri": 110,
  "sirke": 3,
  "tarçın": 3,
  "tavuk göğsü": 165,
  "biber": 10,
  "bulgur": 170,
  "dana kıyma": 200,
  "istiridye mantarı": 15,
  "soya kıyma": 80,
  "zerdeçal": 3,
  "bayat ekmek": 80,
  "tahin": 90,
  "tavuk but": 180,
  "yeşil soğan": 8,
  "bezelye": 60,
  "kuru fasulye": 170,
  "sumak": 3,
  "çörek otu": 5,
  "ıspanak": 14,
  "badem sütü": 24,
  "baklava yufkası": 120,
  "gül suyu": 2,
  "tofu": 76,
  "yumurta sarısı": 55,
  "hindistan cevizi": 100,
  "hindistan cevizi sütü": 80,
  "ince bulgur": 170,
  "krema": 150,
  "nar": 40,
  "pekmez": 50,
  "soya yoğurdu": 40,
  "susam": 50,
  "tel kadayıf": 140,
  "vegan kaşar": 70,
  "çilek": 16,
  "et suyu": 15,
  "hindistan cevizi krema": 120,
  "karabuğday": 150,
  "kuru üzüm": 60,
  "lor peyniri": 50,
  "salatalık": 8,
  "soya kuşbaşı": 80,
  "çam fıstığı": 70,
  "antep fıstığı": 90,
  "güllaç yaprağı": 50,
  "karides": 85,
  "kuş üzümü": 50,
  "marul": 5,
  "muz": 90,
  "mısır": 60,
  "taze fasulye": 25,
  "turşu": 10,
  "vegan bitter çikolata": 120,
  "yeşil mercimek": 170,
  "badem": 100,
  "barbunya": 160,
  "bisküvi": 80,
  "bitter çikolata": 130,
  "buğday": 160,
  "börülce": 140,
  "ekmek": 80,
  "firik": 150,
  "glutensiz tarhana": 60,
  "kereviz": 20,
  "kinoa": 160,
  "kuru kayısı": 50,
  "kırmızı biber": 12,
  "limon kabuğu": 3,
  "mantar": 15,
  "midye": 70,
  "nori yosunu": 5,
  "pudra şekeri": 60,
  "somon fileto": 200,
  "soya yoğurt": 40,
  "arpacık soğan": 12,
  "asma yaprağı": 10,
  "aşurelik buğday": 160,
  "badem unu": 120,
  "balık fileto": 150,
  "bayat pide": 90,
  "beyaz lahana": 15,
  "beşamel sos": 100,
  "biberiye": 3,
  "buz": 0,
  "bütün tavuk": 400,
  "damla sakızı": 3,
  "dolmalık biber": 14,
  "enginar": 25,
  "galeta unu": 80,
  "gendime": 160,
  "hamburger ekmeği": 130,
  "hamsi": 120,
  "hindi but": 170,
  "kalamar": 80,
  "kaymak": 150,
  "kuru bakla": 160,
  "kuru bamya": 30,
  "kuzu bağırsak": 130,
  "kuzu but": 280,
  "kuzu döner eti": 300,
  "kuzu kol": 260,
  "künefe peyniri": 120,
  "midye eti": 70,
  "pide": 100,
  "portakal suyu": 45,
  "pırasa": 20,
  "salep": 40,
  "semizotu": 10,
  "sosis": 150,
  "soya sosu": 10,
  "sucuk": 180,
  "tavuk ciğeri": 120,
  "taze bakla": 40,
  "taze barbunya": 50,
  "taze kaşar peyniri": 110,
  "tost ekmeği": 70,
  "uskumru fileto": 190,
  "vegan bisküvi": 70,
  "yenibahar": 3,
  "yeşil zeytin": 40,
  "yoğunlaştırılmış süt": 130,
  "şehriye": 80,
  "agar agar": 3,
  "bira": 40,
  "dolmalık fıstık": 80,
  "glutensiz ekmek": 70,
  "glutensiz hamburger ekmeği": 110,
  "hindi göğsü": 150,
  "işkembe": 100,
  "jelatin": 10,
  "karalahana": 18,
  "kuru incir": 60,
  "levrek": 140,
  "levrek fileto": 140,
  "maraş tarhanası": 60,
  "mayonez": 100,
  "mezgit fileto": 120,
  "mısır gevreği kırığı": 80,
  "mısır tortilla": 70,
  "palamut": 160,
  "pastırma": 100,
  "penne makarna": 180,
  "soda": 0,
  "süzme yoğurt": 50,
  "tarhana": 60,
  "tavuk baget": 170,
  "tavuk kanat": 160,
  "tavuk pirzola": 170,
  "trabzon peyniri": 90,
  "tuzsuz lor": 45,
  "vegan beyaz peynir": 60,
  "yeşil biber": 10,
  "yeşil domates": 14,
  "çeçil peyniri": 90,
  "çiğ köftelik bulgur": 170
}
````

## File: src/data/cleanedIngredients.json
````json
[
  {
    "name": "tuz",
    "count": 385
  },
  {
    "name": "soğan",
    "count": 238
  },
  {
    "name": "karabiber",
    "count": 219
  },
  {
    "name": "zeytinyağı",
    "count": 217
  },
  {
    "name": "su",
    "count": 170
  },
  {
    "name": "pul biber",
    "count": 148
  },
  {
    "name": "tereyağı",
    "count": 140
  },
  {
    "name": "toz şeker",
    "count": 125
  },
  {
    "name": "domates",
    "count": 115
  },
  {
    "name": "domates salçası",
    "count": 111
  },
  {
    "name": "yumurta",
    "count": 107
  },
  {
    "name": "un",
    "count": 94
  },
  {
    "name": "patates",
    "count": 73
  },
  {
    "name": "sarımsak",
    "count": 73
  },
  {
    "name": "sivri biber",
    "count": 68
  },
  {
    "name": "limon",
    "count": 62
  },
  {
    "name": "maydanoz",
    "count": 62
  },
  {
    "name": "vanilya",
    "count": 58
  },
  {
    "name": "pirinç",
    "count": 57
  },
  {
    "name": "süt",
    "count": 51
  },
  {
    "name": "kimyon",
    "count": 48
  },
  {
    "name": "mısır unu",
    "count": 48
  },
  {
    "name": "biber salçası",
    "count": 46
  },
  {
    "name": "kıyma",
    "count": 46
  },
  {
    "name": "nane",
    "count": 38
  },
  {
    "name": "yulaf sütü",
    "count": 35
  },
  {
    "name": "limon suyu",
    "count": 34
  },
  {
    "name": "kekik",
    "count": 33
  },
  {
    "name": "kızartma yağı",
    "count": 31
  },
  {
    "name": "mısır nişastası",
    "count": 31
  },
  {
    "name": "yoğurt",
    "count": 30
  },
  {
    "name": "patlıcan",
    "count": 29
  },
  {
    "name": "yaş maya",
    "count": 27
  },
  {
    "name": "şeker",
    "count": 27
  },
  {
    "name": "havuç",
    "count": 26
  },
  {
    "name": "sıvı yağ",
    "count": 24
  },
  {
    "name": "kabartma tozu",
    "count": 23
  },
  {
    "name": "yufka",
    "count": 21
  },
  {
    "name": "dereotu",
    "count": 20
  },
  {
    "name": "margarin",
    "count": 20
  },
  {
    "name": "beyaz peynir",
    "count": 18
  },
  {
    "name": "pirinç unu",
    "count": 18
  },
  {
    "name": "dana eti",
    "count": 17
  },
  {
    "name": "kuzu eti",
    "count": 17
  },
  {
    "name": "kırmızı mercimek",
    "count": 17
  },
  {
    "name": "nişasta",
    "count": 17
  },
  {
    "name": "nohut",
    "count": 17
  },
  {
    "name": "ceviz",
    "count": 16
  },
  {
    "name": "glutensiz un karışımı",
    "count": 16
  },
  {
    "name": "lavaş",
    "count": 16
  },
  {
    "name": "nar ekşisi",
    "count": 15
  },
  {
    "name": "sebze suyu",
    "count": 14
  },
  {
    "name": "kakao",
    "count": 13
  },
  {
    "name": "instant maya",
    "count": 12
  },
  {
    "name": "irmik",
    "count": 12
  },
  {
    "name": "tavuk suyu",
    "count": 12
  },
  {
    "name": "kabak",
    "count": 11
  },
  {
    "name": "kaşar peyniri",
    "count": 11
  },
  {
    "name": "sirke",
    "count": 11
  },
  {
    "name": "tarçın",
    "count": 11
  },
  {
    "name": "tavuk göğsü",
    "count": 11
  },
  {
    "name": "biber",
    "count": 10
  },
  {
    "name": "bulgur",
    "count": 10
  },
  {
    "name": "dana kıyma",
    "count": 10
  },
  {
    "name": "istiridye mantarı",
    "count": 10
  },
  {
    "name": "soya kıyma",
    "count": 10
  },
  {
    "name": "zerdeçal",
    "count": 10
  },
  {
    "name": "bayat ekmek",
    "count": 9
  },
  {
    "name": "tahin",
    "count": 9
  },
  {
    "name": "tavuk but",
    "count": 9
  },
  {
    "name": "yeşil soğan",
    "count": 9
  },
  {
    "name": "bezelye",
    "count": 8
  },
  {
    "name": "kuru fasulye",
    "count": 8
  },
  {
    "name": "sumak",
    "count": 8
  },
  {
    "name": "çörek otu",
    "count": 8
  },
  {
    "name": "ıspanak",
    "count": 8
  },
  {
    "name": "badem sütü",
    "count": 7
  },
  {
    "name": "baklava yufkası",
    "count": 7
  },
  {
    "name": "gül suyu",
    "count": 7
  },
  {
    "name": "tofu",
    "count": 7
  },
  {
    "name": "yumurta sarısı",
    "count": 7
  },
  {
    "name": "hindistan cevizi",
    "count": 6
  },
  {
    "name": "hindistan cevizi sütü",
    "count": 6
  },
  {
    "name": "ince bulgur",
    "count": 6
  },
  {
    "name": "krema",
    "count": 6
  },
  {
    "name": "nar",
    "count": 6
  },
  {
    "name": "pekmez",
    "count": 6
  },
  {
    "name": "soya yoğurdu",
    "count": 6
  },
  {
    "name": "susam",
    "count": 6
  },
  {
    "name": "tel kadayıf",
    "count": 6
  },
  {
    "name": "vegan kaşar",
    "count": 6
  },
  {
    "name": "çilek",
    "count": 6
  },
  {
    "name": "et suyu",
    "count": 5
  },
  {
    "name": "hindistan cevizi krema",
    "count": 5
  },
  {
    "name": "karabuğday",
    "count": 5
  },
  {
    "name": "kuru üzüm",
    "count": 5
  },
  {
    "name": "lor peyniri",
    "count": 5
  },
  {
    "name": "salatalık",
    "count": 5
  },
  {
    "name": "soya kuşbaşı",
    "count": 5
  },
  {
    "name": "çam fıstığı",
    "count": 5
  },
  {
    "name": "antep fıstığı",
    "count": 4
  },
  {
    "name": "güllaç yaprağı",
    "count": 4
  },
  {
    "name": "karides",
    "count": 4
  },
  {
    "name": "kuş üzümü",
    "count": 4
  },
  {
    "name": "marul",
    "count": 4
  },
  {
    "name": "muz",
    "count": 4
  },
  {
    "name": "mısır",
    "count": 4
  },
  {
    "name": "taze fasulye",
    "count": 4
  },
  {
    "name": "turşu",
    "count": 4
  },
  {
    "name": "vegan bitter çikolata",
    "count": 4
  },
  {
    "name": "yeşil mercimek",
    "count": 4
  },
  {
    "name": "badem",
    "count": 3
  },
  {
    "name": "barbunya",
    "count": 3
  },
  {
    "name": "bisküvi",
    "count": 3
  },
  {
    "name": "bitter çikolata",
    "count": 3
  },
  {
    "name": "buğday",
    "count": 3
  },
  {
    "name": "börülce",
    "count": 3
  },
  {
    "name": "ekmek",
    "count": 3
  },
  {
    "name": "firik",
    "count": 3
  },
  {
    "name": "glutensiz tarhana",
    "count": 3
  },
  {
    "name": "kereviz",
    "count": 3
  },
  {
    "name": "kinoa",
    "count": 3
  },
  {
    "name": "kuru kayısı",
    "count": 3
  },
  {
    "name": "kırmızı biber",
    "count": 3
  },
  {
    "name": "limon kabuğu",
    "count": 3
  },
  {
    "name": "mantar",
    "count": 3
  },
  {
    "name": "midye",
    "count": 3
  },
  {
    "name": "nori yosunu",
    "count": 3
  },
  {
    "name": "pudra şekeri",
    "count": 3
  },
  {
    "name": "somon fileto",
    "count": 3
  },
  {
    "name": "soya yoğurt",
    "count": 3
  },
  {
    "name": "arpacık soğan",
    "count": 2
  },
  {
    "name": "asma yaprağı",
    "count": 2
  },
  {
    "name": "aşurelik buğday",
    "count": 2
  },
  {
    "name": "badem unu",
    "count": 2
  },
  {
    "name": "balık fileto",
    "count": 2
  },
  {
    "name": "bayat pide",
    "count": 2
  },
  {
    "name": "beyaz lahana",
    "count": 2
  },
  {
    "name": "beşamel sos",
    "count": 2
  },
  {
    "name": "biberiye",
    "count": 2
  },
  {
    "name": "buz",
    "count": 2
  },
  {
    "name": "bütün tavuk",
    "count": 2
  },
  {
    "name": "damla sakızı",
    "count": 2
  },
  {
    "name": "dolmalık biber",
    "count": 2
  },
  {
    "name": "enginar",
    "count": 2
  },
  {
    "name": "galeta unu",
    "count": 2
  },
  {
    "name": "gendime",
    "count": 2
  },
  {
    "name": "hamburger ekmeği",
    "count": 2
  },
  {
    "name": "hamsi",
    "count": 2
  },
  {
    "name": "hindi but",
    "count": 2
  },
  {
    "name": "kalamar",
    "count": 2
  },
  {
    "name": "kaymak",
    "count": 2
  },
  {
    "name": "kuru bakla",
    "count": 2
  },
  {
    "name": "kuru bamya",
    "count": 2
  },
  {
    "name": "kuzu bağırsak",
    "count": 2
  },
  {
    "name": "kuzu but",
    "count": 2
  },
  {
    "name": "kuzu döner eti",
    "count": 2
  },
  {
    "name": "kuzu kol",
    "count": 2
  },
  {
    "name": "künefe peyniri",
    "count": 2
  },
  {
    "name": "midye eti",
    "count": 2
  },
  {
    "name": "pide",
    "count": 2
  },
  {
    "name": "portakal suyu",
    "count": 2
  },
  {
    "name": "pırasa",
    "count": 2
  },
  {
    "name": "salep",
    "count": 2
  },
  {
    "name": "semizotu",
    "count": 2
  },
  {
    "name": "sosis",
    "count": 2
  },
  {
    "name": "soya sosu",
    "count": 2
  },
  {
    "name": "sucuk",
    "count": 2
  },
  {
    "name": "tavuk ciğeri",
    "count": 2
  },
  {
    "name": "taze bakla",
    "count": 2
  },
  {
    "name": "taze barbunya",
    "count": 2
  },
  {
    "name": "taze kaşar peyniri",
    "count": 2
  },
  {
    "name": "tost ekmeği",
    "count": 2
  },
  {
    "name": "uskumru fileto",
    "count": 2
  },
  {
    "name": "vegan bisküvi",
    "count": 2
  },
  {
    "name": "yenibahar",
    "count": 2
  },
  {
    "name": "yeşil zeytin",
    "count": 2
  },
  {
    "name": "yoğunlaştırılmış süt",
    "count": 2
  },
  {
    "name": "şehriye",
    "count": 2
  },
  {
    "name": "agar agar",
    "count": 1
  },
  {
    "name": "bira",
    "count": 1
  },
  {
    "name": "dolmalık fıstık",
    "count": 1
  },
  {
    "name": "glutensiz ekmek",
    "count": 1
  },
  {
    "name": "glutensiz hamburger ekmeği",
    "count": 1
  },
  {
    "name": "hindi göğsü",
    "count": 1
  },
  {
    "name": "işkembe",
    "count": 1
  },
  {
    "name": "jelatin",
    "count": 1
  },
  {
    "name": "karalahana",
    "count": 1
  },
  {
    "name": "kuru incir",
    "count": 1
  },
  {
    "name": "levrek",
    "count": 1
  },
  {
    "name": "levrek fileto",
    "count": 1
  },
  {
    "name": "maraş tarhanası",
    "count": 1
  },
  {
    "name": "mayonez",
    "count": 1
  },
  {
    "name": "mezgit fileto",
    "count": 1
  },
  {
    "name": "mısır gevreği kırığı",
    "count": 1
  },
  {
    "name": "mısır tortilla",
    "count": 1
  },
  {
    "name": "palamut",
    "count": 1
  },
  {
    "name": "pastırma",
    "count": 1
  },
  {
    "name": "penne makarna",
    "count": 1
  },
  {
    "name": "soda",
    "count": 1
  },
  {
    "name": "süzme yoğurt",
    "count": 1
  },
  {
    "name": "tarhana",
    "count": 1
  },
  {
    "name": "tavuk baget",
    "count": 1
  },
  {
    "name": "tavuk kanat",
    "count": 1
  },
  {
    "name": "tavuk pirzola",
    "count": 1
  },
  {
    "name": "trabzon peyniri",
    "count": 1
  },
  {
    "name": "tuzsuz lor",
    "count": 1
  },
  {
    "name": "vegan beyaz peynir",
    "count": 1
  },
  {
    "name": "yeşil biber",
    "count": 1
  },
  {
    "name": "yeşil domates",
    "count": 1
  },
  {
    "name": "çeçil peyniri",
    "count": 1
  },
  {
    "name": "çiğ köftelik bulgur",
    "count": 1
  }
]
````

## File: src/data/recipes.ts
````typescript

````

## File: src/hooks/useIngredientSearch.ts
````typescript
import { useMemo, useEffect, useState, useCallback } from 'react';
import cleanedIngredients from '../data/cleanedIngredients.json';
⋮----
interface CleanedIngredient {
  name: string;
  count: number;
}
⋮----
interface UseIngredientSearchOptions {
  maxResults?: number;
  minQueryLength?: number;
  enableFuzzy?: boolean;
}
⋮----
interface UseIngredientSearchResult {
  suggestions: CleanedIngredient[];
  totalMatches: number;
  isSearching: boolean;
  recentIngredients: string[];
}
⋮----
function levenshteinDistance(str1: string, str2: string): number
⋮----
function matchesQuery(
  ingredient: CleanedIngredient,
  query: string,
  enableFuzzy: boolean
):
⋮----
function getRecentIngredients(): string[]
⋮----
function addRecentIngredient(ingredient: string): void
⋮----
export function useIngredientSearch(
  query: string,
  options: UseIngredientSearchOptions = {}
): UseIngredientSearchResult
⋮----
export function useTrackIngredient()
````

## File: src/lib/supabase.ts
````typescript
import { createClient } from '@supabase/supabase-js';
````

## File: src/pages/PreferencesPage.tsx
````typescript
import React, { useState } from 'react';
import { useFridge } from '../store/FridgeContext';
import { useIngredientSearch } from '../hooks/useIngredientSearch';
import { getIngredientDetails } from '../constants/ingredientData';
⋮----
const handleToggle = (key: keyof typeof dietaryPreferences) =>
⋮----
{/* Page Header */}
⋮----
{/* Dietary Preferences Section */}
⋮----
onClick=
⋮----
onChange=
⋮----
toggleExcludedIngredient(ingredient.name);
setExclusionSearch('');
````

## File: src/pages/ProfilePage.tsx
````typescript
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { deleteInteraction, getInteractionHistory, getRecipes, recordInteraction } from '../utils/api';
import type { InteractionResponse, InteractionType } from '../types';
⋮----
type Tab = Extract<InteractionType, 'like' | 'skip' | 'save' | 'cook'>;
⋮----
const formatDate = (dateStr: string) =>
⋮----
const handleAddRecipe = async (title: string) =>
⋮----
// silently ignore
⋮----
const handleDelete = async (id: number) =>
⋮----
// If it fails we already removed from UI; reload would restore — acceptable trade-off
⋮----
{/* Recipe search / add */}
⋮----
onClick=
````

## File: src/pages/ShoppingListPage.tsx
````typescript
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useShoppingList } from '../store/ShoppingListContext';
import { useFridge } from '../store/FridgeContext';
import { useIngredientSearch } from '../hooks/useIngredientSearch';
import type { ShoppingListItem } from '../utils/api';
⋮----
const handleSelectSuggestion = (name: string) =>
⋮----
const handleManualAdd = () =>
⋮----
const handleKeyDown = (e: React.KeyboardEvent) =>
⋮----
const transferPurchasedToFridge = () =>
⋮----
const handleClearAll = () =>
⋮----
onChange=
onFocus=
⋮----
onMouseDown=
⋮----
onClick=
````

## File: src/store/RecipeContext.tsx
````typescript
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { useFridge } from './FridgeContext';
import { getRAGRecommendations, getRecommendations, ApiError } from '../utils/api';
import { RecipeWithMatch } from '../types';
import { estimateRecipeCalories } from '../utils/calorieEstimator';
import type { CalorieRange } from '../utils/recipeFilter';
⋮----
export type CalorieFilterKey = 'all' | 'low' | 'medium' | 'high';
⋮----
function enrichWithCalories(recipes: RecipeWithMatch[]): RecipeWithMatch[]
⋮----
interface RecipeContextType {
    rawRecipes: RecipeWithMatch[];
    loading: boolean;
    error: string | null;
    explanation: string | null;
    metadata: Record<string, unknown> | null;
    responseTime: number | null;
    useRAG: boolean;
    setUseRAG: (v: boolean) => void;
    calorieFilter: CalorieFilterKey;
    setCalorieFilter: (v: CalorieFilterKey) => void;
    page: number;
    loadMore: () => void;
    fetchRecipes: () => Promise<void>;
    hasSearched: boolean;
}
⋮----
export const RecipeProvider: React.FC<
⋮----
const fetchRecipes = async () =>
⋮----
const loadMore = ()
⋮----
export const useRecipes = () =>
````

## File: src/tests/helpers.test.ts
````typescript
import { describe, it, expect } from 'vitest';
import {
    parseIngredientList,
    ingredientMatches,
    computeRecipeAvailability,
    getRecipeImageUrl,
} from '../utils/helpers';
````

## File: src/tests/setup.ts
````typescript

````

## File: src/tests/shoppingList.test.ts
````typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
⋮----
const normalize = (s: string)
⋮----
interface Item {
    name: string;
    display_name: string;
    purchased: boolean;
    from_recipes: string[];
}
⋮----
function mergeItems(a: Item[], b: Item[]): Item[]
⋮----
function addItemsFromRecipe(prev: Item[], recipeTitle: string, missingIngredients: string[]): Item[]
⋮----
// ── mergeItems ────────────────────────────────────────────────────────────────
````

## File: src/tests/utils.test.ts
````typescript
import { describe, it, expect } from 'vitest';
import { parseIngredientList } from '../utils/helpers';
````

## File: src/utils/calorieEstimator.ts
````typescript
import calorieData from '../data/calorieData.json';
import { parseIngredientList } from './helpers';
⋮----
export type CalorieLabel = 'Düşük' | 'Orta' | 'Yüksek';
⋮----
export function getIngredientCalories(ingredientName: string): number | undefined
⋮----
export function estimateRecipeCalories(cleanedIngredientsStr: string): number | null
⋮----
export function getCalorieLabel(kcal: number): CalorieLabel
````

## File: src/utils/dietaryRules.ts
````typescript
export interface DietaryPreferences {
    glutenFree: boolean;
    vegetarian: boolean;
    vegan: boolean;
    dairyFree: boolean;
    nutAllergy: boolean;
}
⋮----
export function getForbiddenIngredients(preferences: DietaryPreferences): string[]
⋮----
export function getAllForbiddenIngredients(
    preferences: DietaryPreferences,
    excludedIngredients: string[]
): string[]
⋮----
export function getActiveDietaryLabels(preferences: DietaryPreferences): string[]
````

## File: src/utils/helpers.ts
````typescript
export const parseIngredientList = (str: string): string[] =>
⋮----
export const ingredientMatches = (fridgeIngredient: string, recipeIngredient: string): boolean =>
⋮----
export interface RecipeAvailability {
    missing: string[];
    allMatching: string[];
    coveredCount: number;
    totalCount: number;
    isFullyAvailable: boolean;
}
⋮----
export const computeRecipeAvailability = (
    cleanedIngredients: string[],
    fridgeIngredients: string[],
    backendMatchingIngredients: string[]
): RecipeAvailability =>
⋮----
export const getRecipeImageUrl = (imageName: string) =>
````

## File: src/utils/ingredientNormalizer.ts
````typescript
export function getIngredientVariations(cleanedIngredient: string): string[]
⋮----
export function matchesExcludedIngredient(
    recipeIngredient: string,
    excludedIngredients: string[]
): boolean
````

## File: src/utils/recipeFilter.ts
````typescript
import { RecipeWithMatch } from '../types';
import { getAllForbiddenIngredients } from './dietaryRules';
import { matchesExcludedIngredient } from './ingredientNormalizer';
import { DietaryPreferences } from './dietaryRules';
⋮----
export interface CalorieRange {
    min?: number;
    max?: number;
}
⋮----
export function filterRecipes(
    recipes: RecipeWithMatch[],
    dietaryPreferences: DietaryPreferences,
    excludedIngredients: string[],
    calorieRange?: CalorieRange
): RecipeWithMatch[]
⋮----
export function getActiveFilterLabels(
    dietaryPreferences: DietaryPreferences,
    excludedIngredients: string[],
    calorieRange?: CalorieRange
): string[]
````

## File: src/index.css
````css
.animate-shimmer {
````

## File: src/index.tsx
````typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
````

## File: src/vite-env.d.ts
````typescript

````

## File: README.md
````markdown
# Buzdolabı Şefi 

Buzdolabınızdaki malzemelere göre yapay zeka destekli tarif öneren web uygulaması. Kullanıcı hesapları, beğeni/atlama takibi, tüketim kaydı ve haftalık tekrar analizi destekler. Türk yemeklerine ve Türkçe özelinde geliştirilmiştir. -Belen

## Özellikler

- **Tarif Önerisi:** Buzdolabı malzemelerine göre FAISS vektör araması ile tarif önerisi
- **RAG Pipeline:** FAISS → Reranker → Gemini LLM ile açıklamalı öneriler
- **Kullanıcı Hesapları:** E-posta ile magic link girişi (şifresiz)
- **Geri Bildirim:** Beğeni/atlama, tüketim saati, porsiyon, haftalık tekrar takibi
- **Tercihler:** Vegan, vejetaryen, glutensiz, süt ürünü yok, kuruyemiş alerjisi filtreleri
- **İkame Önerileri:** Eksik malzemeler için LLM tabanlı ikame önerileri

## Gereksinimler

- **Node.js** 18+
- **Python** 3.10+
- **Gemini API anahtarı** (LLM özellikleri için)

## Kurulum

### 1. Bağımlılıkları yükle

```bash
npm install

cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Ortam değişkenleri

**Backend** (`backend/.env`):

```env
GEMINI_API_KEY=your_gemini_api_key
SESSION_SECRET=rastgele-guvenli-bir-string
```

**Magic Link E-posta (SMTP)** – Giriş bağlantısı e-posta ile gönderilsin istiyorsanız:

```env
SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
FRONTEND_URL=http://localhost:3000
```

Gmail için "Uygulama şifresi" (App Password) kullanın; normal şifre çalışmaz.

**Frontend** (opsiyonel, `.env.local`):

```env
VITE_API_URL=http://localhost:3001/api
```

### 3. FAISS indeksini oluştur (ilk kurulumda)

```bash
cd backend
python scripts/build_faiss_index.py
```

## Çalıştırma

**Terminal 1 – Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 3001 --reload-exclude 'venv/*'
```
veya `npm run dev:backend`

**Terminal 2 – Frontend:**
```bash
npm run dev
```

Tarayıcıda: http://127.0.0.1:3000

> **Not:** `--reload-exclude 'venv/*'` venv klasöründeki değişikliklerin uvicorn'u sürekli yeniden başlatmasını önler.

## Testler

```bash
npm run test:backend

npm run test
```

## Proje Yapısı

```
smart-fridge-chef/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── middleware/
│   ├── data/
│   ├── scripts/
│   └── tests/
├── components/
├── pages/
├── store/
├── utils/
└── tests/
```

## Canlıya Almadan Önce Bunlara Bakın

- [ ] **Oturum güvenliği:** `SESSION_SECRET` için rastgele, güçlü bir değer kullanın (varsayılan değeri değiştirin)
- [ ] **AI özellikleri:** `GEMINI_API_KEY` tanımlı olsun; aksi halde tarif açıklamaları ve ikame önerileri çalışmaz
- [ ] **Production modu:** Backend'i `NODE_ENV=production` ile çalıştırın
- [ ] **CORS:** `FRONTEND_URL` veya `allow_origins` içinde canlı frontend adresiniz (örn. `https://uygulama.com`) tanımlı olsun
- [ ] **E-posta girişi:** Magic link göndermek istiyorsanız SMTP ayarlarını yapın (`backend/.env.example` referans alınabilir)
- [ ] **Veri güvenliği:** SQLite veritabanınızı düzenli yedekleyin

## API Dokümantasyonu

Backend çalışırken: http://localhost:3001/docs

## Lisans

MIT
````

## File: backend/app/models/auth.py
````python
class MagicLinkRequest(BaseModel)
⋮----
email: str = Field(..., min_length=5, pattern=r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
⋮----
class MagicLinkVerifyRequest(BaseModel)
⋮----
token: str
⋮----
class UserResponse(BaseModel)
⋮----
id: str
email: str
display_name: Optional[str] = None
created_at: str
⋮----
class SessionInfo(BaseModel)
⋮----
user: UserResponse
expires_at: str
⋮----
class MagicLinkResponse(BaseModel)
⋮----
message: str
dev_token: Optional[str] = None
⋮----
class SupabaseSessionRequest(BaseModel)
⋮----
access_token: str
````

## File: backend/app/services/recipe_service.py
````python
logger = logging.getLogger(__name__)
⋮----
class RecipeService
⋮----
def __init__(self)
⋮----
def _load_recipes(self)
⋮----
data_path = os.path.join(
⋮----
recipes_data = json.load(f)
⋮----
valid_recipes = []
skipped = 0
⋮----
def _ensure_loaded(self)
⋮----
"""Ensure recipes are loaded (lazy loading)"""
⋮----
def _count_matches(self, recipe: Recipe, user_ingredients: List[str]) -> List[str]
⋮----
"""
        Count matching ingredients between recipe and user ingredients

        Args:
            recipe: Recipe object
            user_ingredients: List of user ingredient names

        Returns:
            List of matching ingredient names
        """
recipe_ingredients_lower = recipe.Ingredients.lower()
matching_ingredients = []
⋮----
def _string_matching_search(self, user_ingredients: List[str]) -> List[RecipeWithMatch]
⋮----
"""
        Fallback search method using string matching
        Used when FAISS index is not available

        Args:
            user_ingredients: List of ingredient names

        Returns:
            List of RecipeWithMatch objects sorted by matching count
        """
⋮----
results = []
⋮----
matching_ingredients = self._count_matches(recipe, user_ingredients)
⋮----
# Sort by matching count (descending)
⋮----
"""
        Find recipes that match user ingredients using vector search or string matching

        Args:
            user_ingredients: List of ingredient names
            use_vector_search: Whether to use FAISS vector search (default: True)
            top_k: Number of top results to return (default: 50)

        Returns:
            List of RecipeWithMatch objects sorted by relevance
        """
# Check cache first
# Combine all parameters into a single dict for cache key generation
cache_data = {
cache_key = cache._generate_key("recipes", cache_data)
cached_result = cache.get(cache_key)
⋮----
# Use vector search if available and requested
⋮----
# Search using FAISS
⋮----
# Convert results to RecipeWithMatch
⋮----
recipe = self.recipes[idx]
⋮----
# Count actual matching ingredients for display
⋮----
results = self._string_matching_search(user_ingredients)
⋮----
# Limit results to top_k
results = results[:top_k]
⋮----
# Cache result for 5 minutes
⋮----
def get_all_recipes(self, limit: int = 50, offset: int = 0) -> List[Recipe]
⋮----
"""Get all recipes with pagination"""
⋮----
def get_recipe_by_title(self, title: str) -> Optional[Recipe]
⋮----
"""Get a recipe by title"""
⋮----
def get_total_count(self) -> int
⋮----
"""Get total number of recipes"""
⋮----
recipe_service = RecipeService()
````

## File: backend/evaluation/systems.py
````python
logger = logging.getLogger(__name__)
⋮----
def jaccard_recommend(query_ingredients: List[str], top_k: int = 10) -> List[str]
⋮----
result = rag_pipeline.process(
⋮----
def rag_no_personalization(query_ingredients: List[str], top_k: int = 10) -> List[str]
⋮----
def rag_faiss_only(query_ingredients: List[str], top_k: int = 10) -> List[str]
⋮----
def rag_hybrid(query_ingredients: List[str], top_k: int = 10) -> List[str]
````

## File: backend/scripts/download_recipe_images.py
````python
ROOT = Path(__file__).resolve().parent.parent.parent
RECIPES_JSON = ROOT / "backend" / "data" / "recipes.json"
IMG_DIR = ROOT / "public" / "images" / "recipies"
⋮----
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; recipe-image-downloader/1.0)"}
⋮----
TITLE_SUFFIXES = [
⋮----
PREFIXES = [
⋮----
def clean_title(title: str) -> str
⋮----
title = title.replace(s, "")
⋮----
def base_title(title: str) -> str
⋮----
"""Strip dietary prefix words from title for a cleaner search query."""
⋮----
def search_image_url(ddgs, query: str)
⋮----
"""Search using an existing DDGS instance (shared across all calls)."""
⋮----
results = list(ddgs.images(query, max_results=3))
⋮----
url = r.get("image", "")
⋮----
msg = str(e)
⋮----
wait = 10 * (attempt + 1)
⋮----
def download(url: str, dest: Path) -> bool
⋮----
req = urllib.request.Request(url, headers=HEADERS)
⋮----
data = r.read()
⋮----
def main()
⋮----
data = json.loads(RECIPES_JSON.read_text(encoding="utf-8"))
existing = {f.name for f in IMG_DIR.iterdir() if f.suffix in (".jpg", ".jpeg")}
⋮----
missing = []
⋮----
img_name = recipe.get("Image_Name", "")
⋮----
title = clean_title(recipe.get("Title", ""))
⋮----
downloaded = 0
not_found = []
⋮----
ddgs = DDGS()
⋮----
dest = IMG_DIR / f"{img_name}.jpg"
short_title = base_title(title)
⋮----
url = None
⋮----
url = search_image_url(ddgs, query)
⋮----
size_kb = dest.stat().st_size // 1024
````

## File: backend/tests/test_auth.py
````python
async def test_magic_link_request(client)
⋮----
r = await client.post("/api/auth/magic-link", json={"email": "test@example.com"})
⋮----
data = r.json()
⋮----
async def test_magic_link_invalid_email(client)
⋮----
r = await client.post("/api/auth/magic-link", json={"email": "gecersiz"})
⋮----
async def test_magic_link_missing_email_field(client)
⋮----
r = await client.post("/api/auth/magic-link", json={})
⋮----
async def test_verify_magic_link(client)
⋮----
r1 = await client.post("/api/auth/magic-link", json={"email": "verify-test@example.com"})
⋮----
token = r1.json().get("dev_token")
⋮----
r2 = await client.post("/api/auth/verify", json={"token": token})
⋮----
data = r2.json()
⋮----
async def test_me_requires_auth(client)
⋮----
r = await client.get("/api/auth/me")
⋮----
async def test_me_after_login(client)
⋮----
r1 = await client.post("/api/auth/magic-link", json={"email": "me-test@example.com"})
token = r1.json()["dev_token"]
⋮----
async def test_logout_clears_session(client)
⋮----
r1 = await client.post("/api/auth/magic-link", json={"email": "logout-test@example.com"})
⋮----
r = await client.post("/api/auth/logout")
⋮----
async def test_invalid_token_rejected(client)
⋮----
r = await client.post("/api/auth/verify", json={"token": "not-a-real-token"})
⋮----
async def test_token_cannot_be_reused(client)
⋮----
r1 = await client.post("/api/auth/magic-link", json={"email": "reuse-test@example.com"})
⋮----
r3 = await client.post("/api/auth/verify", json={"token": token})
````

## File: backend/tests/test_feedback.py
````python
async def test_interaction_requires_auth(client)
⋮----
r = await client.post(
⋮----
async def test_consumption_requires_auth(client)
⋮----
async def test_features_requires_auth(client)
⋮----
r = await client.get("/api/feedback/features")
⋮----
async def test_history_requires_auth(client)
⋮----
r = await client.get("/api/feedback/history")
⋮----
async def test_recipe_status_requires_auth(client)
⋮----
r = await client.get("/api/feedback/recipe-status/Karnıyarık")
⋮----
async def test_feedback_flow_with_auth(auth_client)
⋮----
like_id = r.json()["id"]
⋮----
data = r.json()
⋮----
async def test_like_is_idempotent_upsert(auth_client)
⋮----
recipe = "Upsert Test Tarifi"
⋮----
ids = []
⋮----
# History must contain exactly 1 like for this recipe
r = await client.get("/api/feedback/history?limit=200")
⋮----
likes = [
⋮----
async def test_toggle_like_unlike(auth_client)
⋮----
"""Like then unlike → no record remains."""
⋮----
recipe = "Toggle Test Tarifi"
⋮----
r = await client.request(
⋮----
r = await client.get(f"/api/feedback/recipe-status/{recipe}")
⋮----
async def test_recipe_status_tracks_last_interaction(auth_client)
⋮----
recipe = "Status Track Tarifi"
⋮----
# Should reflect most recent: skip
⋮----
async def test_interaction_history_pagination(auth_client)
⋮----
r = await client.get("/api/feedback/history?limit=5&offset=0")
⋮----
async def test_delete_nonexistent_interaction_returns_zero(auth_client)
````

## File: backend/tests/test_health.py
````python
async def test_health_ok(client)
⋮----
r = await client.get("/health")
⋮----
data = r.json()
⋮----
async def test_health_includes_rag_pipeline(client)
⋮----
async def test_root(client)
⋮----
r = await client.get("/")
````

## File: src/components/Navbar.tsx
````typescript
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useFridge } from '../store/FridgeContext';
import { useAuth } from '../store/AuthContext';
import { useShoppingList } from '../store/ShoppingListContext';
⋮----
const isActive = (path: string)
````

## File: src/components/RecipeImage.tsx
````typescript
import React, { useState } from 'react';
⋮----
function buildFallbackChain(imageName: string): string[]
⋮----
interface RecipeImageProps {
    imageName: string;
    alt: string;
    className?: string;
    size?: 'card' | 'hero';
}
⋮----
const handleError = () =>
⋮----
onLoad=
````

## File: src/pages/FridgePage.tsx
````typescript
import React, { useState, useMemo, useEffect } from 'react';
import { useFridge } from '../store/FridgeContext';
import { useRecipes } from '../store/RecipeContext';
import { checkHealth } from '../utils/api';
import { Link, useNavigate } from 'react-router-dom';
import {
    getIngredientDetails,
    groupIngredientsByCategory,
    sortCategories,
    CATEGORY_EMOJIS
} from '../constants/ingredientData';
import { useIngredientSearch, useTrackIngredient } from '../hooks/useIngredientSearch';
import cleanedIngredients from '../data/cleanedIngredients.json';
⋮----
const handleAdd = (ingredientName: string) =>
⋮----
// Group ingredients by category
⋮----
// Sort categories: Alphabetically, but "Other" always last
⋮----
const checkBackendStatus = async () =>
⋮----
setSearchTerm(e.target.value);
setIsDropdownOpen(true);
⋮----
onFocus=
⋮----
onClick=
````

## File: src/pages/LoginPage.tsx
````typescript
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
⋮----
type Mode = 'signin' | 'signup';
⋮----
const handleSubmit = async (e: React.FormEvent) =>
⋮----
const switchMode = () =>
⋮----
onClick=
````

## File: src/store/AuthContext.tsx
````typescript
import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import type { User } from '../types';
import { supabase } from '../lib/supabase';
import { getCurrentUser, logoutUser } from '../utils/api';
⋮----
async function bridgeToBackend(accessToken: string): Promise<User>
⋮----
export const AuthProvider: React.FC<
⋮----
const login = async (email: string, password: string) =>
⋮----
const signup = async (email: string, password: string) =>
⋮----
const logout = async () =>
⋮----
export const useAuth = () =>
````

## File: src/store/ShoppingListContext.tsx
````typescript
import React, { createContext, useContext, useState, useEffect, useRef, ReactNode } from 'react';
import { useAuth } from './AuthContext';
import { getShoppingList, saveShoppingList, ShoppingListItem } from '../utils/api';
⋮----
interface ShoppingListContextType {
    items: ShoppingListItem[];
    addItem: (name: string, displayName?: string, fromRecipe?: string) => void;
    addItemsFromRecipe: (recipeTitle: string, missingIngredients: string[]) => number;
    removeItem: (name: string) => void;
    togglePurchased: (name: string) => void;
    clearPurchased: () => void;
    clearAll: () => void;
    totalCount: number;
    pendingCount: number;
    isItemInList: (name: string) => boolean;
}
⋮----
const normalize = (s: string)
⋮----
export const ShoppingListProvider: React.FC<
⋮----
const mergeItems = (a: ShoppingListItem[], b: ShoppingListItem[]): ShoppingListItem[] =>
⋮----
const addItem = (name: string, displayName?: string, fromRecipe?: string) =>
⋮----
const addItemsFromRecipe = (recipeTitle: string, missingIngredients: string[]): number =>
⋮----
const removeItem = (name: string)
⋮----
const togglePurchased = (name: string)
⋮----
const clearPurchased = ()
const clearAll = ()
⋮----
const isItemInList = (name: string)
⋮----
export const useShoppingList = () =>
````

## File: src/tests/calorieEstimator.test.ts
````typescript
import { describe, it, expect } from 'vitest';
import { estimateRecipeCalories, getCalorieLabel } from '../utils/calorieEstimator';
````

## File: src/tests/recipeFilter.test.ts
````typescript
import { describe, it, expect } from 'vitest';
import { filterRecipes, getActiveFilterLabels } from '../utils/recipeFilter';
import type { RecipeWithMatch } from '../types';
⋮----
function makeRecipe(overrides: Partial<RecipeWithMatch> =
````

## File: src/types.ts
````typescript
export interface Recipe {
    Title: string;
    Ingredients: string;
    Instructions: string;
    Image_Name: string;
    Cleaned_Ingredients: string;
}
⋮----
export interface RecipeWithMatch extends Recipe {
    matchingCount: number;
    matchingIngredients: string[];
    estimatedCalories?: number | null;
}
⋮----
export interface Ingredient {
    name: string;
}
⋮----
export interface DietaryPreferences {
    vegan?: boolean;
    vegetarian?: boolean;
    glutenFree?: boolean;
    dairyFree?: boolean;
    nutAllergy?: boolean;
}
⋮----
export interface RAGRecommendRequest {
    ingredients: string[];
    preferences?: DietaryPreferences;
    excluded_ingredients?: string[];
    explain?: boolean;
    top_k?: number;
    retrieval_top_k?: number;
}
⋮----
export interface RAGMetadata {
    retrieval_count: number;
    reranked_count: number;
    pipeline_stages: string[];
    retriever_used: boolean;
    reranker_used: boolean;
    llm_used: boolean;
    personalized?: boolean;
}
⋮----
export interface MatchScore {
    best_match_count: number;
    total_ingredients: number;
    label: string;
}
⋮----
export interface RAGRecommendResponse {
    recipes: RecipeWithMatch[];
    explanation: string | null;
    metadata: RAGMetadata;
    count: number;
    match_score: MatchScore | null;
}
⋮----
export interface SubstitutionRequest {
    recipe_title: string;
    missing_ingredients: string[];
    available_ingredients: string[];
}
⋮----
export interface SubstitutionResponse {
    substitutions: Record<string, string[]>;
    explanation: string | null;
}
⋮----
export interface User {
    id: string;
    email: string;
    display_name: string | null;
    created_at: string;
}
⋮----
export interface SessionInfo {
    user: User;
    expires_at: string;
}
⋮----
export type InteractionType = 'like' | 'skip' | 'view' | 'cook' | 'save';
export type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack';
⋮----
export interface InteractionResponse {
    id: number;
    recipe_title: string;
    interaction_type: InteractionType;
    created_at: string;
}
⋮----
export interface InteractionCreate {
    recipe_title: string;
    interaction_type: InteractionType;
    context_ingredients?: string[];
}
⋮----
export interface ConsumptionCreate {
    recipe_title: string;
    meal_type: MealType;
    portion_size?: number;
    rating?: number;
    notes?: string;
}
⋮----
export interface UserFeatures {
    user_id: string;
    email: string;
    total_likes: number;
    total_skips: number;
    total_cooked: number;
    avg_portion: number | null;
    preferred_meal_type: string | null;
    weekly_repeat_count: number;
    like_skip_ratio: number | null;
    top_liked_recipes: string[];
    weekly_repeats: string[];
}
````

## File: vite.config.ts
````typescript
import path from 'path';
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
````

## File: backend/app/models/feedback.py
````python
class InteractionCreate(BaseModel)
⋮----
recipe_title: str
interaction_type: Literal["like", "skip", "view", "cook", "save"]
context_ingredients: Optional[List[str]] = None
⋮----
class InteractionDelete(BaseModel)
⋮----
interaction_type: Literal["like", "skip", "save", "cook"]
⋮----
class ConsumptionCreate(BaseModel)
⋮----
meal_type: Literal["breakfast", "lunch", "dinner", "snack"]
portion_size: float = Field(default=1.0, ge=0.25, le=5.0)
rating: Optional[int] = Field(None, ge=1, le=5)
notes: Optional[str] = None
⋮----
class InteractionResponse(BaseModel)
⋮----
id: int
⋮----
interaction_type: str
created_at: str
⋮----
class ConsumptionResponse(BaseModel)
⋮----
consumed_at: str
meal_type: str
portion_size: float
rating: Optional[int] = None
⋮----
class SurveyRequest(BaseModel)
⋮----
rating: int = Field(..., ge=1, le=5)
cook_intent: Literal["yes", "maybe", "no"]
comment: Optional[str] = Field(None, max_length=500)
⋮----
recipe_titles: Optional[List[str]] = None
⋮----
class SurveyResponse(BaseModel)
⋮----
class SurveyStats(BaseModel)
⋮----
total_responses: int
average_rating: float
cook_intent_breakdown: dict
rating_distribution: dict
⋮----
class UserFeatures(BaseModel)
⋮----
user_id: str
email: str
total_likes: int
total_skips: int
total_cooked: int
avg_portion: Optional[float]
preferred_meal_type: Optional[str]
weekly_repeat_count: int
like_skip_ratio: Optional[float]
top_liked_recipes: List[str]
weekly_repeats: List[str]
````

## File: backend/app/services/llm_service.py
````python
logger = logging.getLogger(__name__)
⋮----
class LLMService
⋮----
def __init__(self)
⋮----
def _load_model(self)
⋮----
def is_available(self) -> bool
⋮----
def _try_generate_with_retry(self, prompt: str, config: types.GenerateContentConfig, max_retries: int = 1)
⋮----
models_to_try = [self.model_name]
⋮----
msg = str(e)
⋮----
match = re.search(r'retry in (\d+(?:\.\d+)?)s', msg, re.I)
delay = min(float(match.group(1)) if match else 20, 60)
⋮----
# Interaction type → human-readable Turkish label for prompt injection
_HISTORY_LABELS: Dict[str, str] = {
⋮----
history_note = ""
⋮----
liked_titles = [t for t, a in user_history.items() if a in ("like", "cook", "save")]
skipped_titles = [t for t, a in user_history.items() if a == "skip"]
⋮----
system_prompt = f"""Sen profesyonel bir Türk şefisin ve kullanıcının yemek alışkanlıklarını hatırlayan kişisel şefisin. Kullanıcıya elindeki malzemelere en uygun tarifi neden önerdiğini, malzemelerin uyumunu vurgulayarak, samimi ve iştah açıcı bir Türkçe ile açıkla.{history_note}
⋮----
context_parts = [f"**Mevcut Malzemeler:** {', '.join(user_ingredients)}"]
⋮----
active_prefs = []
⋮----
recipes_text = "\n\nÖnerilen Tarifler:\n"
⋮----
ingredients_text = recipe.Cleaned_Ingredients or recipe.Ingredients
ingredients_clean = ingredients_text.replace('[', '').replace(']', '').replace("'", '')
recipe_note = ""
⋮----
interaction = user_history.get(recipe.Title)
label = self._HISTORY_LABELS.get(interaction, "")
⋮----
recipe_note = f" [Kullanıcı bu tarifi daha önce {label}]"
⋮----
prompt = f"""{system_prompt}
⋮----
prompt = self._build_prompt(
⋮----
config = types.GenerateContentConfig(
response = self._try_generate_with_retry(prompt, config, max_retries=0)
explanation = response.text.strip()
⋮----
subs_example = {ing: ["ikame1", "ikame2"] for ing in missing_ingredients[:2]}
⋮----
example_str = _json.dumps({"substitutions": subs_example, "explanation": "Örnek açıklama"}, ensure_ascii=False)
⋮----
prompt = f"""Sen profesyonel bir Türk mutfağı şefisin. Sadece geçerli JSON döndür, başka metin yazma.
⋮----
response = self._try_generate_with_retry(prompt, config)
⋮----
raw = response.text.strip()
⋮----
raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
⋮----
raw = raw[:-3].rstrip()
⋮----
raw = raw[4:].lstrip()
⋮----
def _normalize_llm_json(text: str) -> str
⋮----
text = re.sub(r'\bNone\b', 'null', text)
text = re.sub(r'\bTrue\b', 'true', text)
text = re.sub(r'\bFalse\b', 'false', text)
text = re.sub(r',\s*}', '}', text)
text = re.sub(r',\s*]', ']', text)
⋮----
result = None
⋮----
result = json.loads(_normalize_llm_json(raw))
⋮----
match = re.search(r'\{[\s\S]*\}', raw)
⋮----
candidate = _normalize_llm_json(match.group(0))
result = json.loads(candidate)
⋮----
def get_model_info(self) -> dict
⋮----
llm_service = LLMService()
````

## File: backend/app/config.py
````python
class Settings(BaseSettings)
⋮----
PORT: int = 3001
FRONTEND_URL: str = "http://localhost:3000"
GEMINI_API_KEY: Optional[str] = None
NODE_ENV: str = "development"
⋮----
EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_DIMENSION: int = 384
⋮----
FAISS_INDEX_TYPE: str = "IndexFlatL2"
FAISS_METRIC: str = "L2"
FAISS_INDEX_PATH: str = "data/recipe_index.faiss"
⋮----
TFIDF_VECTORIZER_PATH: str = "data/tfidf_vectorizer.pkl"
TFIDF_MATRIX_PATH: str = "data/tfidf_matrix.npz"
RRF_K: int = 60
HYBRID_RETRIEVAL_ENABLED: bool = True
⋮----
RERANKER_MODEL: str = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
RERANKER_BATCH_SIZE: int = 32
RERANKER_ENABLED: bool = True
⋮----
GEMINI_MODEL: str = "models/gemini-2.5-flash"
GEMINI_FALLBACK_MODEL: Optional[str] = "models/gemini-2.0-flash"
GEMINI_MAX_TOKENS: int = 2000
GEMINI_TEMPERATURE: float = 0.7
GEMINI_ENABLED: bool = True
⋮----
DATABASE_URL: str = ""
⋮----
# Supabase Auth (frontend doğrulama için)
SUPABASE_URL: str = ""
SUPABASE_ANON_KEY: str = ""
⋮----
# CORS — add comma-separated origins in .env for custom clients (e.g. Capacitor iOS)
CORS_EXTRA_ORIGINS: str = ""
⋮----
# Auth & Session
SESSION_SECRET: str = "change-me-in-production"
MAGIC_LINK_EXPIRY: int = 600
SESSION_EXPIRY_DAYS: int = 30
SMTP_ENABLED: bool = False
⋮----
SMTP_HOST: str = "smtp.gmail.com"
SMTP_PORT: int = 587
SMTP_USER: Optional[str] = None
SMTP_PASSWORD: Optional[str] = None
SMTP_FROM: Optional[str] = None
SMTP_FROM_NAME: str = "Buzdolabı Şefi"
⋮----
class Config
⋮----
env_file = ".env"
case_sensitive = True
⋮----
settings = Settings()
````

## File: backend/tests/conftest.py
````python
async def _setup_db()
⋮----
@pytest.fixture(autouse=True)
async def _dispose_after_each()
⋮----
@pytest.fixture
async def client()
⋮----
@pytest.fixture
async def auth_client(client)
⋮----
email = f"test-{uuid.uuid4().hex[:12]}@example.com"
r1 = await client.post("/api/auth/magic-link", json={"email": email})
⋮----
token = r1.json()["dev_token"]
r2 = await client.post("/api/auth/verify", json={"token": token})
````

## File: src/store/FridgeContext.tsx
````typescript
import React, { createContext, useContext, useState, useEffect, useRef, useCallback, ReactNode } from 'react';
import { useAuth } from './AuthContext';
import { getFridgeIngredients, saveFridgeIngredients, getPreferences, savePreferences } from '../utils/api';
⋮----
export interface DietaryPreferences {
    glutenFree: boolean;
    vegetarian: boolean;
    vegan: boolean;
    dairyFree: boolean;
    nutAllergy: boolean;
    [key: string]: boolean;
}
⋮----
interface FridgeContextType {
    fridgeIngredients: string[];
    addIngredient: (ingredient: string) => void;
    removeIngredient: (ingredient: string) => void;
    dietaryPreferences: DietaryPreferences;
    setDietaryPreferences: (prefs: DietaryPreferences) => void;
    excludedIngredients: string[];
    toggleExcludedIngredient: (ingredient: string) => void;
}
⋮----
export const FridgeProvider: React.FC<
⋮----
const addIngredient = (ingredient: string) =>
⋮----
const removeIngredient = (ingredient: string) =>
⋮----
const setDietaryPreferences = (prefs: DietaryPreferences) =>
⋮----
const toggleExcludedIngredient = (ingredient: string) =>
⋮----
export const useFridge = () =>
````

## File: src/App.tsx
````typescript
import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import FridgePage from './pages/FridgePage';
import RecipesPage from './pages/RecipesPage';
import RecipeDetailPage from './pages/RecipeDetailPage';
import PreferencesPage from './pages/PreferencesPage';
import LoginPage from './pages/LoginPage';
import ProfilePage from './pages/ProfilePage';
import ShoppingListPage from './pages/ShoppingListPage';
import { FridgeProvider } from './store/FridgeContext';
import { AuthProvider } from './store/AuthContext';
import { RecipeProvider } from './store/RecipeContext';
import { ShoppingListProvider } from './store/ShoppingListContext';
````

## File: package.json
````json
{
  "name": "smart-fridge-chef",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "dev:backend": "cd backend && ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 3001",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:backend": "cd backend && ./venv/bin/python -m pytest tests/ -v"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.105.4",
    "react": "^19.2.3",
    "react-dom": "^19.2.3",
    "react-router-dom": "^7.11.0"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.2",
    "@types/node": "^22.14.0",
    "@types/react": "^19.2.15",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^5.0.0",
    "jsdom": "^28.1.0",
    "tsx": "^4.19.2",
    "typescript": "~5.8.2",
    "vite": "^6.2.0",
    "vitest": "^4.1.0"
  }
}
````

## File: backend/app/models/recipe.py
````python
class Recipe(BaseModel)
⋮----
Title: str
Ingredients: str
Instructions: Optional[str] = ""  # Some recipes might not have instructions
Image_Name: str
Cleaned_Ingredients: str  # Stored as a stringified list
⋮----
class RecipeWithMatch(Recipe)
⋮----
matchingCount: int
matchingIngredients: List[str]
⋮----
class RecipeSearchParams(BaseModel)
⋮----
ingredients: List[str] = []
limit: int = 50
offset: int = 0
⋮----
class RecipeRecommendRequest(BaseModel)
⋮----
ingredients: List[str]
use_vector_search: Optional[bool] = True
top_k: Optional[int] = 50
⋮----
class RecipeRecommendResponse(BaseModel)
⋮----
recommendations: List[RecipeWithMatch]
count: int
userIngredients: List[str]
search_method: str  # "vector" or "string_matching"
⋮----
class RecipeSearchRequest(BaseModel)
⋮----
query: str
top_k: Optional[int] = 20
⋮----
class RecipeSearchResponse(BaseModel)
⋮----
recipes: List[RecipeWithMatch]
⋮----
search_method: str
⋮----
class DietaryPreferences(BaseModel)
⋮----
vegan: Optional[bool] = False
vegetarian: Optional[bool] = False
glutenFree: Optional[bool] = False
dairyFree: Optional[bool] = False
nutAllergy: Optional[bool] = False
⋮----
class RAGRecommendRequest(BaseModel)
⋮----
preferences: Optional[DietaryPreferences] = None
excluded_ingredients: Optional[List[str]] = None
explain: Optional[bool] = True
top_k: Optional[int] = 10
retrieval_top_k: Optional[int] = 50
⋮----
class RAGMetadata(BaseModel)
⋮----
retrieval_count: int
reranked_count: int
pipeline_stages: List[str]
retriever_used: bool
reranker_used: bool
llm_used: bool
personalized: bool = False
cf_used: bool = False
tfidf_used: bool = False
⋮----
class MatchScore(BaseModel)
⋮----
best_match_count: int
total_ingredients: int
label: str
⋮----
class RAGRecommendResponse(BaseModel)
⋮----
explanation: Optional[str] = None
metadata: RAGMetadata
⋮----
match_score: Optional[MatchScore] = None
⋮----
class SubstitutionRequest(BaseModel)
⋮----
recipe_title: str
missing_ingredients: List[str]
available_ingredients: List[str]
⋮----
class SubstitutionResponse(BaseModel)
⋮----
substitutions: Dict[str, List[str]]
````

## File: backend/app/routes/feedback.py
````python
logger = logging.getLogger(__name__)
⋮----
router = APIRouter(prefix="/feedback", tags=["feedback"])
⋮----
@router.post("/interaction", response_model=InteractionResponse)
async def record_interaction(body: InteractionCreate, user: dict = Depends(get_current_user))
⋮----
row_id = await database_service.record_interaction(
⋮----
@router.post("/consumption", response_model=ConsumptionResponse)
async def log_consumption(body: ConsumptionCreate, user: dict = Depends(get_current_user))
⋮----
row_id = await database_service.log_consumption(
⋮----
@router.get("/features", response_model=UserFeatures)
async def get_features(user: dict = Depends(get_current_user))
⋮----
features = await database_service.get_user_features(user["id"])
⋮----
interactions = await database_service.get_interaction_history(user["id"], limit, offset)
⋮----
logs = await database_service.get_consumption_history(user["id"], limit, offset)
⋮----
@router.get("/weekly-repeats")
async def get_weekly_repeats(user: dict = Depends(get_current_user))
⋮----
repeats = await database_service.get_weekly_repeats(user["id"])
⋮----
deleted = await database_service.delete_interaction_by_recipe(
⋮----
deleted = await database_service.delete_interaction(user["id"], interaction_id)
⋮----
@router.get("/recipe-status/{recipe_title}")
async def get_recipe_status(recipe_title: str, user: dict = Depends(get_current_user))
⋮----
status = await database_service.get_recipe_interaction_status(user["id"], recipe_title)
⋮----
@router.post("/survey", response_model=SurveyResponse)
@limiter.limit("5/minute")
async def submit_survey(request: Request, body: SurveyRequest, user: dict = Depends(get_current_user))
⋮----
@router.get("/survey/stats", response_model=SurveyStats)
async def get_survey_stats(user: dict = Depends(get_current_user))
⋮----
stats = await database_service.get_survey_stats()
````

## File: backend/app/routes/recipes.py
````python
logger = logging.getLogger(__name__)
⋮----
router = APIRouter(prefix="/recipes", tags=["recipes"])
⋮----
ingredient_list = [ing.strip() for ing in ingredients.split(',')]
filtered_recipes = recipe_service.find_suitable_recipes(ingredient_list)
⋮----
filtered_recipes = recipe_service.get_all_recipes(limit=500, offset=0)
⋮----
filtered_recipes = [r for r in filtered_recipes if q.lower() in r.Title.lower()]
⋮----
total = len(filtered_recipes)
recipes = filtered_recipes[offset:offset + limit]
⋮----
@router.get("/{title}", response_model=Recipe)
async def get_recipe(title: str)
⋮----
"""
    Get a specific recipe by title
    """
⋮----
recipe = recipe_service.get_recipe_by_title(title)
⋮----
@router.post("/recommend", response_model=RecipeRecommendResponse)
@limiter.limit("30/minute")
async def recommend_recipes(request: Request, body: RecipeRecommendRequest)
⋮----
start_time = time.time()
⋮----
use_vector_search = body.use_vector_search if body.use_vector_search is not None else True
top_k = body.top_k if body.top_k is not None else 50
⋮----
search_method = "vector" if (use_vector_search and faiss_service.is_loaded()) else "string_matching"
⋮----
# Get recommendations
recommendations = recipe_service.find_suitable_recipes(
⋮----
process_time = time.time() - start_time
⋮----
@router.post("/search", response_model=RecipeSearchResponse)
@limiter.limit("30/minute")
async def search_recipes(request: Request, body: RecipeSearchRequest)
⋮----
top_k = body.top_k if body.top_k is not None else 20
⋮----
results = []
recipes = recipe_service.get_all_recipes(limit=recipe_service.get_total_count())
⋮----
recipe = recipes[idx]
⋮----
query_lower = body.query.lower()
⋮----
preferences_dict = None
⋮----
preferences_dict = {
⋮----
top_k = body.top_k if body.top_k is not None else 10
retrieval_top_k = body.retrieval_top_k if body.retrieval_top_k is not None else 50
explain = body.explain if body.explain is not None else True
⋮----
user_history: Optional[dict] = None
user_id: Optional[str] = None
cf_scores: Optional[dict] = None
⋮----
user_id = user["id"]
⋮----
user_history = await database_service.get_user_interaction_map(user_id)
⋮----
all_titles = [r.Title for r in recipe_service.get_all_recipes(
cf_scores = await cf_service.get_cf_scores(user_id, all_titles)
⋮----
result = rag_pipeline.process(
⋮----
@router.post("/substitutions", response_model=SubstitutionResponse)
@limiter.limit("10/minute")
async def get_substitutions(request: Request, body: SubstitutionRequest)
⋮----
result = llm_service.generate_substitutions(
⋮----
subs = result.get("substitutions", {})
⋮----
subs = {}
````

## File: backend/app/services/rag_pipeline.py
````python
logger = logging.getLogger(__name__)
⋮----
_HISTORY_ADJUSTMENTS: Dict[str, float] = {
⋮----
class RAGPipeline
⋮----
scores: Dict[int, float] = {}
⋮----
fused = sorted(scores.items(), key=lambda x: -x[1])
⋮----
faiss_loaded = self.retriever.is_loaded()
tfidf_loaded = self.tfidf.is_loaded() and use_hybrid
⋮----
# Her ikisi de yüklü → hibrit RRF
⋮----
all_recipes = self.recipe_service.get_all_recipes(
n = len(all_recipes)
⋮----
fused_indices = self._rrf_fuse(
retrieved = [all_recipes[i] for i in fused_indices if i < n]
⋮----
retrieved = [all_recipes[i] for i in indices if i < len(all_recipes)]
⋮----
results = self.recipe_service.find_suitable_recipes(
⋮----
reranked_results = self.reranker.rerank_by_ingredients(
⋮----
adjusted = []
⋮----
interaction = user_history.get(recipe.Title)
delta = _HISTORY_ADJUSTMENTS.get(interaction, 0.0) if interaction else 0.0
⋮----
"""Benzer kullanıcıların tercihleriyle hesaplanan CF deltasını skora ekle."""
⋮----
delta = cf_scores.get(recipe.Title, 0.0)
⋮----
recipes = [recipe for recipe, score in reranked_recipes]
⋮----
explanation = self.generator.generate_explanation(
⋮----
"""
        Complete RAG pipeline: Retrieve → Rerank → Personalize → Generate

        user_history: {recipe_title: most_recent_interaction_type} — pre-fetched
                      by the caller (route) from the database.
        """
personalized = bool(user_history)
cf_used = bool(cf_scores)
⋮----
# Step 1: Retrieval
⋮----
reranked_results = self._rerank(
⋮----
reranked_results = self._apply_history_scores(reranked_results, user_history)
⋮----
reranked_results = self._apply_cf_scores(reranked_results, cf_scores)
⋮----
final_recipes = []
⋮----
recipe_ingredients_lower = recipe.Ingredients.lower()
matching_ingredients = [
⋮----
explanation = None
⋮----
explanation = self._generate(
⋮----
total_ingredients = len(user_ingredients)
best_match = max((r.matchingCount for r in final_recipes), default=0)
match_score = MatchScore(
⋮----
stages = ["retrieval", "reranking"]
⋮----
rag_pipeline = RAGPipeline()
````

## File: src/pages/RecipeDetailPage.tsx
````typescript
import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useLocation } from 'react-router-dom';
import recipes from '../data/recipes';
import { parseIngredientList, computeRecipeAvailability } from '../utils/helpers';
import { SubstitutionResponse, Recipe } from '../types';
import type { MealType } from '../types';
import RecipeImage from '../components/RecipeImage';
import { estimateRecipeCalories, getCalorieLabel, getIngredientCalories } from '../utils/calorieEstimator';
import { useFridge } from '../store/FridgeContext';
import { useAuth } from '../store/AuthContext';
import { useShoppingList } from '../store/ShoppingListContext';
import { getSubstitutions, recordInteraction, deleteInteractionByRecipe, logConsumption, getRecipeStatus, getRecipeByTitle, type ApiError } from '../utils/api';
⋮----
// view kaydı kritik değil; 401'da logout yapma
⋮----
const handleSubstitution = async () =>
⋮----
{/* Add to Shopping List Button */}
⋮----
onClick=
⋮----
{/* Substitution Button */}
⋮----
{/* Substitution Explanation */}
⋮----
{/* Main Content: Instructions + Feedback */}
⋮----
{/* Feedback Panel */}
⋮----
{/* Like / Skip */}
⋮----
{/* Cook Logging */}
````

## File: backend/app/routes/auth.py
````python
logger = logging.getLogger(__name__)
⋮----
router = APIRouter(prefix="/auth", tags=["auth"])
⋮----
def _set_session_cookie(response: Response, session_id: str)
⋮----
is_production = settings.NODE_ENV != "development"
⋮----
@router.post("/supabase-session", response_model=SessionInfo)
@limiter.limit("10/minute")
async def create_supabase_session(request: Request, body: SupabaseSessionRequest, response: Response)
⋮----
resp = await client.get(
⋮----
supabase_user = resp.json()
email = supabase_user.get("email")
⋮----
user = await auth_service.create_or_get_user(email)
session_id = await auth_service.create_session(user["id"])
⋮----
session_data = await auth_service.validate_session(session_id)
⋮----
@router.post("/magic-link", response_model=MagicLinkResponse)
async def request_magic_link(body: MagicLinkRequest)
⋮----
user = await auth_service.create_or_get_user(body.email)
token = await auth_service.generate_magic_link(user["id"])
⋮----
dev_token = None
⋮----
dev_token = token if settings.NODE_ENV == "development" else None
⋮----
@router.post("/verify", response_model=SessionInfo)
async def verify_magic_link(body: MagicLinkVerifyRequest, response: Response)
⋮----
user = await auth_service.verify_magic_link(body.token)
⋮----
@router.get("/me", response_model=SessionInfo)
async def get_me(user: dict = Depends(get_current_user))
⋮----
@router.post("/logout")
async def logout(response: Response, user: dict = Depends(get_current_user))
````

## File: backend/app/services/database_service.py
````python
logger = logging.getLogger(__name__)
⋮----
def _as_str(val)
⋮----
class DatabaseService
⋮----
async def init_db(self)
⋮----
ctx_json = json.dumps(context_ingredients, ensure_ascii=False) if context_ingredients else None
⋮----
result = await conn.execute(
row = result.fetchone()
⋮----
async def _query_weekly_repeats(self, conn, user_id: str) -> list[str]
⋮----
async def get_user_features(self, user_id: str) -> dict
⋮----
row = result.mappings().fetchone()
⋮----
features = dict(row)
⋮----
total_likes = features.get("total_likes", 0)
total_skips = features.get("total_skips", 0)
⋮----
async def get_weekly_repeats(self, user_id: str) -> list[str]
⋮----
async def get_recipe_interaction_status(self, user_id: str, recipe_title: str) -> dict
⋮----
async def delete_interaction(self, user_id: str, interaction_id: int) -> bool
⋮----
async def get_user_interaction_map(self, user_id: str) -> dict[str, str]
⋮----
async def get_fridge_ingredients(self, user_id: str) -> list[str]
⋮----
async def save_fridge_ingredients(self, user_id: str, ingredients: list[str]) -> None
⋮----
async def get_shopping_list(self, user_id: str) -> list[dict]
⋮----
items = []
⋮----
async def save_shopping_list(self, user_id: str, items: list[dict]) -> None
⋮----
name = (it.get("name") or "").strip().lower()
⋮----
async def get_user_preferences(self, user_id: str) -> dict
⋮----
async def save_user_preferences(self, user_id: str, dietary: dict, excluded: list) -> None
⋮----
ctx = json.dumps(context_ingredients, ensure_ascii=False) if context_ingredients else None
titles = json.dumps(recipe_titles, ensure_ascii=False) if recipe_titles else None
⋮----
async def get_survey_stats(self) -> dict
⋮----
total = int(row[0])
avg_rating = round(float(row[1]), 2)
⋮----
cook_breakdown: dict = {"yes": 0, "maybe": 0, "no": 0}
⋮----
rating_dist: dict = {str(i): 0 for i in range(1, 6)}
⋮----
database_service = DatabaseService()
````

## File: backend/requirements.txt
````
--extra-index-url https://download.pytorch.org/whl/cpu

# PyTorch CPU-only (CUDA yok, ~200MB vs ~2GB)
torch==2.2.2+cpu
torchvision==0.17.2+cpu

# Sentence Transformers + uyumlu bağımlılıklar
sentence-transformers==2.7.0
transformers==4.40.2
tokenizers==0.19.1
huggingface-hub==0.23.2

# Numerik
numpy==1.26.4
scikit-learn>=1.3,<2
scipy>=1.11,<2

# Vector search
faiss-cpu==1.8.0

# FastAPI stack
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6

# Config & Auth
python-dotenv==1.0.0
itsdangerous==2.1.2

# Database
sqlalchemy==2.0.30
asyncpg==0.29.0

# Google AI
google-genai==1.10.0
# HTTP client
httpx==0.28.1


# Rate limiting
slowapi==0.1.9

# Test
pytest==7.4.4
pytest-asyncio==0.23.3
````

## File: src/pages/RecipesPage.tsx
````typescript
import React, { useMemo, useCallback, useState, useEffect } from 'react';
import { useFridge } from '../store/FridgeContext';
import { useAuth } from '../store/AuthContext';
import { useShoppingList } from '../store/ShoppingListContext';
import { useRecipes, CALORIE_RANGES, CALORIE_FILTER_LABELS, CalorieFilterKey } from '../store/RecipeContext';
import { recordInteraction, deleteInteractionByRecipe, getInteractionHistory } from '../utils/api';
import RecipeImage from '../components/RecipeImage';
import RecipeSurvey from '../components/RecipeSurvey';
import { Link } from 'react-router-dom';
import { filterRecipes, getActiveFilterLabels } from '../utils/recipeFilter';
import { getCalorieLabel } from '../utils/calorieEstimator';
import { parseIngredientList, computeRecipeAvailability, type RecipeAvailability } from '../utils/helpers';
⋮----
onComplete=
⋮----
onClick=
⋮----
e.preventDefault();
e.stopPropagation();
addItemsFromRecipe(recipe.Title, availability.missing);
````

## File: src/utils/api.ts
````typescript
import type {
    RAGRecommendRequest, RAGRecommendResponse,
    SubstitutionRequest, SubstitutionResponse,
    SessionInfo, InteractionCreate, ConsumptionCreate, UserFeatures, InteractionResponse,
} from '../types';
⋮----
export interface ApiError {
    message: string
    status: number;
}
⋮----
const handleApiError = async (response: Response): Promise<never> =>
⋮----
export const getRecipes = async (params?: {
    ingredients?: string[];
    q?: string;
    limit?: number;
    offset?: number;
}) =>
⋮----
export const getRecipeByTitle = async (title: string) =>
⋮----
export const getRecommendations = async (ingredients: string[]) =>
⋮----
export const getRAGRecommendations = async (
    request: RAGRecommendRequest
): Promise<RAGRecommendResponse> =>
⋮----
export const getSubstitutions = async (
    request: SubstitutionRequest
): Promise<SubstitutionResponse> =>
⋮----
export const checkHealth = async () =>
⋮----
export const signupUser = async (email: string, password: string): Promise<SessionInfo> =>
⋮----
export const signinUser = async (email: string, password: string): Promise<SessionInfo> =>
⋮----
export const requestMagicLink = async (email: string): Promise<
⋮----
export const verifyMagicLink = async (token: string): Promise<SessionInfo> =>
⋮----
export const getCurrentUser = async (): Promise<SessionInfo | null> =>
⋮----
export const logoutUser = async (): Promise<void> =>
⋮----
export const recordInteraction = async (data: InteractionCreate): Promise<void> =>
⋮----
export const logConsumption = async (data: ConsumptionCreate): Promise<void> =>
⋮----
export const getUserFeatures = async (): Promise<UserFeatures> =>
⋮----
export const getFridgeIngredients = async (): Promise<
⋮----
export interface ShoppingListItem {
    name: string;
    display_name: string;
    purchased: boolean;
    from_recipes: string[];
}
⋮----
export const getShoppingList = async (): Promise<
⋮----
export const saveShoppingList = async (items: ShoppingListItem[]): Promise<void> =>
⋮----
export const saveFridgeIngredients = async (ingredients: string[]): Promise<void> =>
⋮----
export const getRecipeStatus = async (recipeTitle: string): Promise<
⋮----
export const deleteInteractionByRecipe = async (
    recipe_title: string,
    interaction_type: 'like' | 'skip' | 'save' | 'cook'
): Promise<
⋮----
export const deleteInteraction = async (id: number): Promise<void> =>
⋮----
export interface SurveyPayload {
    rating: number;
    cook_intent: 'yes' | 'maybe' | 'no';
    comment?: string;
    context_ingredients?: string[];
    recipe_titles?: string[];
}
⋮----
export const submitSurvey = async (data: SurveyPayload): Promise<void> =>
⋮----
export const getInteractionHistory = async (
    limit = 50, offset = 0
): Promise<
⋮----
export interface PreferencesPayload {
    dietary: Record<string, boolean>;
    excluded: string[];
}
⋮----
export const getPreferences = async (): Promise<PreferencesPayload> =>
⋮----
export const savePreferences = async (payload: PreferencesPayload): Promise<void> =>
````

## File: backend/app/database.py
````python
logger = logging.getLogger(__name__)
⋮----
_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1).split("?")[0]
⋮----
engine = create_async_engine(
⋮----
async def init_db() -> None
````

## File: backend/app/main.py
````python
logger = logging.getLogger(__name__)
⋮----
app = FastAPI(
⋮----
@app.middleware("http")
async def add_process_time_header(request: Request, call_next)
⋮----
start_time = time.time()
response = await call_next(request)
process_time = time.time() - start_time
⋮----
_cors_origins = [
⋮----
@app.on_event("startup")
async def startup_event()
⋮----
# Step 1: Load FAISS index (Retriever)
⋮----
success = faiss_service.load_index()
⋮----
index_info = faiss_service.get_index_info()
⋮----
success = tfidf_service.load_index()
⋮----
# Step 1.6: Pre-load embedding model (used for FAISS query encoding)
⋮----
# Step 2: Pre-load Reranker model at startup (avoids cold-start timeout on first request)
⋮----
# Step 3: Initialize LLM service (API-based, no local model to load)
⋮----
# Step 4: RAG Pipeline summary
⋮----
@app.get("/health")
async def health_check()
⋮----
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception)
⋮----
@app.get("/")
async def root()
````
