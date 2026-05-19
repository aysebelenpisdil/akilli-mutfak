"""
Collaborative Filtering Service
Kullanıcı tabanlı CF: benzer kullanıcıların beğendiği tariflere skor ekler.

Algoritma:
  1. Tüm kullanıcıların etkileşim vektörlerini çek
  2. Mevcut kullanıcıyla cosine benzerliği hesapla
  3. En benzer N kullanıcının ağırlıklı oyları → aday tariflere CF skoru
  4. Skor [0,1] aralığına normalize edilir

Etkileşim ağırlıkları:
  like / cook → +1.0
  save        → +0.5
  view        →  0.1
  skip        → -0.5
"""

import logging
import math
from typing import Dict, List, Optional

from sqlalchemy import text

logger = logging.getLogger(__name__)

# Etkileşim türü → vektör ağırlığı
_WEIGHTS: Dict[str, float] = {
    "like":  1.0,
    "cook":  1.0,
    "save":  0.5,
    "view":  0.1,
    "skip": -0.5,
}

# Reranker skoruna eklenen CF katkısının maksimum değeri
CF_MAX_DELTA = 0.20

# Benzer kullanıcı sayısı (top-k)
TOP_N_SIMILAR = 5


def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
    """İki seyrek vektör arasındaki cosine benzerliği."""
    if not a or not b:
        return 0.0
    shared = set(a) & set(b)
    if not shared:
        return 0.0
    dot = sum(a[k] * b[k] for k in shared)
    mag_a = math.sqrt(sum(x * x for x in a.values()))
    mag_b = math.sqrt(sum(x * x for x in b.values()))
    denom = mag_a * mag_b
    return dot / denom if denom > 0 else 0.0


class CFService:

    async def _fetch_all_interaction_vectors(self) -> Dict[str, Dict[str, float]]:
        """
        DB'den tüm kullanıcıların etkileşimlerini çekip
        {user_id: {recipe_title: weight}} olarak döndürür.
        """
        from app.database import engine
        async with engine.connect() as conn:
            result = await conn.execute(
                text("""
                    SELECT user_id, recipe_title, interaction_type
                    FROM recipe_interactions
                    WHERE interaction_type IN ('like','cook','save','view','skip')
                """)
            )
            rows = result.fetchall()

        vectors: Dict[str, Dict[str, float]] = {}
        for user_id, recipe_title, itype in rows:
            weight = _WEIGHTS.get(itype, 0.0)
            if weight == 0.0:
                continue
            if user_id not in vectors:
                vectors[user_id] = {}
            # Aynı tarife birden fazla etkileşim varsa en yüksek ağırlığı al
            existing = vectors[user_id].get(recipe_title, 0.0)
            vectors[user_id][recipe_title] = max(existing, weight) if weight > 0 else min(existing, weight)
        return vectors

    async def get_cf_scores(
        self,
        user_id: str,
        candidate_titles: List[str],
        top_n_similar: int = TOP_N_SIMILAR,
    ) -> Dict[str, float]:
        """
        Aday tarif listesi için CF skorlarını hesaplar.

        Returns:
            {recipe_title: cf_delta} — pipeline'daki reranker skoruna eklenecek delta.
            Boş dict döner: yeterli veri yoksa veya cold-start durumunda.
        """
        if not candidate_titles:
            return {}

        try:
            all_vectors = await self._fetch_all_interaction_vectors()
        except Exception as exc:
            logger.warning(f"CF: etkileşim verisi çekilemedi: {exc}")
            return {}

        user_vec = all_vectors.get(user_id)
        if not user_vec:
            logger.debug(f"CF: {user_id} için etkileşim yok (cold-start)")
            return {}

        # Benzer kullanıcıları bul (kendisi hariç)
        similarities: List[tuple] = []
        for other_id, other_vec in all_vectors.items():
            if other_id == user_id:
                continue
            sim = _cosine(user_vec, other_vec)
            if sim > 0:
                similarities.append((other_id, sim))

        if not similarities:
            return {}

        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similar = similarities[:top_n_similar]

        logger.debug(
            f"CF: {user_id} için top-{len(top_similar)} benzer kullanıcı: "
            + ", ".join(f"{uid[:20]}({sim:.2f})" for uid, sim in top_similar)
        )

        # Aday tarifler için ağırlıklı CF skoru
        candidate_set = set(candidate_titles)
        raw_scores: Dict[str, float] = {}
        for other_id, sim in top_similar:
            other_vec = all_vectors[other_id]
            for title, weight in other_vec.items():
                if title not in candidate_set:
                    continue
                # Kullanıcı zaten bu tarifte etkileşim yapmışsa CF'den çıkar
                if title in user_vec:
                    continue
                raw_scores[title] = raw_scores.get(title, 0.0) + sim * weight

        if not raw_scores:
            return {}

        # [0, CF_MAX_DELTA] aralığına normalize et
        max_raw = max(raw_scores.values())
        if max_raw <= 0:
            return {}

        cf_deltas = {
            title: (score / max_raw) * CF_MAX_DELTA
            for title, score in raw_scores.items()
            if score > 0
        }

        logger.debug(f"CF: {len(cf_deltas)} tarifin skoru güncellendi")
        return cf_deltas


cf_service = CFService()
