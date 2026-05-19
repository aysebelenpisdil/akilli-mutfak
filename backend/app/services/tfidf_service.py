"""
TF-IDF Inverted Index Service
Malzeme ters-indeksi: sklearn TfidfVectorizer tabanlı leksikal retrieval.
FAISS semantik retrieval ile RRF üzerinden birleştirilerek hibrit retrieval oluşturulur.
"""

import logging
import pickle
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
from scipy.sparse import save_npz, load_npz
from sklearn.feature_extraction.text import TfidfVectorizer

from app.config import settings

logger = logging.getLogger(__name__)


def _clean_ingredients_text(raw: str) -> str:
    """
    Cleaned_Ingredients alanını embedding_service.py:52-55 ile aynı şekilde temizler.
    ['domates', 'soğan'] → 'domates, soğan'
    """
    return raw.replace("[", "").replace("]", "").replace("'", "").strip()


class TFIDFService:
    """
    TF-IDF inverted index over recipe Cleaned_Ingredients.

    Recipe sırası recipe_service._load_recipes() ile deterministik şekilde belirlenir;
    FAISS index ile birebir aynı sıradadır (idx i → aynı tarif).
    """

    def __init__(self, vectorizer_path: str, matrix_path: str):
        self.vectorizer_path = Path(vectorizer_path)
        self.matrix_path = Path(matrix_path)
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._matrix = None  # scipy sparse (n_recipes × vocab)

    def build_index(self, recipes) -> None:
        """Tariflerin Cleaned_Ingredients'ından TF-IDF matrisi oluştur ve diske kaydet."""
        documents = [_clean_ingredients_text(r.Cleaned_Ingredients) for r in recipes]

        self._vectorizer = TfidfVectorizer(
            lowercase=True,
            token_pattern=r"(?u)\b\w\w+\b",  # Unicode-aware — Türkçe ç/ğ/ı/ö/ş/ü
            ngram_range=(1, 1),
            sublinear_tf=True,   # log(1+tf) — kısa belgeler için daha dengeli
        )
        self._matrix = self._vectorizer.fit_transform(documents)

        self.vectorizer_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.vectorizer_path, "wb") as f:
            pickle.dump(self._vectorizer, f)
        save_npz(str(self.matrix_path), self._matrix)

        logger.info(
            f"TF-IDF index built: {self._matrix.shape[0]} tarif, "
            f"vocab={len(self._vectorizer.vocabulary_)}"
        )

    def load_index(self) -> bool:
        """Diskten yükle. Başarılıysa True döner."""
        if not self.vectorizer_path.exists() or not self.matrix_path.exists():
            logger.warning(
                f"TF-IDF index dosyaları bulunamadı: "
                f"{self.vectorizer_path}, {self.matrix_path}"
            )
            return False
        try:
            with open(self.vectorizer_path, "rb") as f:
                self._vectorizer = pickle.load(f)
            self._matrix = load_npz(str(self.matrix_path))
            logger.info(
                f"TF-IDF index yüklendi: {self._matrix.shape[0]} tarif, "
                f"vocab={len(self._vectorizer.vocabulary_)}"
            )
            return True
        except Exception as e:
            logger.error(f"TF-IDF index yüklenemedi: {e}", exc_info=True)
            self._vectorizer = None
            self._matrix = None
            return False

    def is_loaded(self) -> bool:
        return self._vectorizer is not None and self._matrix is not None

    def search_by_ingredients(
        self, ingredients: List[str], k: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Malzemelere göre top-k tarif döndür (cosine similarity).

        TfidfVectorizer varsayılan olarak L2 normalize eder →
        cosine similarity = sparse dot product.

        Returns:
            scores: shape (k,)  — cosine similarity, azalan sırada
            indices: shape (k,) — recipe index'leri
        """
        if not self.is_loaded():
            raise RuntimeError("TF-IDF index yüklü değil")

        query = ", ".join(ingredients)
        query_vec = self._vectorizer.transform([query])
        scores = (self._matrix @ query_vec.T).toarray().ravel()

        n = self._matrix.shape[0]
        k = min(k, n)

        if np.count_nonzero(scores) == 0:
            return np.array([]), np.array([], dtype=int)

        top_indices = np.argpartition(-scores, k - 1)[:k]
        top_sorted = top_indices[np.argsort(-scores[top_indices])]
        return scores[top_sorted].astype(float), top_sorted

    @property
    def vocab_size(self) -> int:
        if self._vectorizer is None:
            return 0
        return len(self._vectorizer.vocabulary_)


tfidf_service = TFIDFService(
    vectorizer_path=settings.TFIDF_VECTORIZER_PATH,
    matrix_path=settings.TFIDF_MATRIX_PATH,
)
