"""
TF-IDF Inverted Index Service için birim testleri.

Sentetik 3-tarif korpusu üzerinde el-hesabıyla doğrulanmış beklentiler.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.tfidf_service import TFIDFService, _clean_ingredients_text


# ---------- dummy recipe fixture ----------

class DummyRecipe:
    def __init__(self, title: str, cleaned_ingredients: str):
        self.title = title
        self.cleaned_ingredients = cleaned_ingredients

    @property
    def Title(self) -> str:
        return self.title

    @property
    def Cleaned_Ingredients(self) -> str:
        return self.cleaned_ingredients


CORPUS = [
    DummyRecipe("Domates Çorbası", "['domates', 'soğan', 'tuz']"),
    DummyRecipe("Tavuk Sote", "['tavuk', 'soğan', 'biber', 'yağ']"),
    DummyRecipe("Mercimek Çorbası", "['mercimek', 'soğan', 'tuz', 'yağ']"),
]


@pytest.fixture
def built_service(tmp_path):
    """Build ve diskten yüklenmiş TFIDFService."""
    svc = TFIDFService(
        vectorizer_path=str(tmp_path / "vec.pkl"),
        matrix_path=str(tmp_path / "mat.npz"),
    )
    svc.build_index(CORPUS)
    return svc


@pytest.fixture
def loaded_service(tmp_path):
    """Build + load roundtrip."""
    svc = TFIDFService(
        vectorizer_path=str(tmp_path / "vec.pkl"),
        matrix_path=str(tmp_path / "mat.npz"),
    )
    svc.build_index(CORPUS)

    svc2 = TFIDFService(
        vectorizer_path=str(tmp_path / "vec.pkl"),
        matrix_path=str(tmp_path / "mat.npz"),
    )
    svc2.load_index()
    return svc2


# ---------- clean helper ----------

def test_clean_ingredients_strips_brackets():
    raw = "['domates', 'soğan', 'tuz']"
    result = _clean_ingredients_text(raw)
    assert "[" not in result
    assert "]" not in result
    assert "'" not in result
    assert "domates" in result


# ---------- build ----------

def test_build_matrix_shape(built_service):
    assert built_service._matrix.shape[0] == 3  # 3 tarif


def test_build_vocab_nonempty(built_service):
    assert built_service.vocab_size > 0


def test_is_loaded_after_build(built_service):
    assert built_service.is_loaded()


# ---------- persist / load roundtrip ----------

def test_roundtrip_shape(loaded_service):
    assert loaded_service._matrix.shape[0] == 3


def test_roundtrip_vocab(loaded_service, built_service):
    assert loaded_service.vocab_size == built_service.vocab_size


def test_is_loaded_after_load(loaded_service):
    assert loaded_service.is_loaded()


def test_load_returns_false_missing_files(tmp_path):
    svc = TFIDFService(
        vectorizer_path=str(tmp_path / "nonexistent.pkl"),
        matrix_path=str(tmp_path / "nonexistent.npz"),
    )
    assert svc.load_index() is False
    assert not svc.is_loaded()


# ---------- search ----------

def test_domates_query_top_result(built_service):
    """'domates' içeren tek tarif (Domates Çorbası) en üstte olmalı."""
    _, indices = built_service.search_by_ingredients(["domates"], k=3)
    assert len(indices) > 0
    assert indices[0] == 0  # Domates Çorbası index=0


def test_mercimek_query_top_result(built_service):
    """'mercimek' içeren tek tarif (Mercimek Çorbası, index=2) en üstte olmalı."""
    _, indices = built_service.search_by_ingredients(["mercimek"], k=3)
    assert len(indices) > 0
    assert indices[0] == 2


def test_scores_descending(built_service):
    """Dönen skorlar azalan sırada olmalı."""
    scores, _ = built_service.search_by_ingredients(["soğan", "yağ"], k=3)
    assert list(scores) == sorted(scores, reverse=True)


def test_unknown_ingredient_returns_empty(built_service):
    """Vokabülerde olmayan malzeme → boş sonuç, exception değil."""
    _, indices = built_service.search_by_ingredients(["xyzzyx_yok"], k=3)
    assert len(indices) == 0


def test_k_limits_results(built_service):
    _, indices = built_service.search_by_ingredients(["soğan"], k=2)
    assert len(indices) <= 2


def test_scores_nonnegative(built_service):
    scores, _ = built_service.search_by_ingredients(["soğan", "tuz"], k=3)
    assert all(s >= 0 for s in scores)


# ---------- RRF fusion (unit) ----------

from app.services.rag_pipeline import RAGPipeline


def test_rrf_merge_two_lists():
    """
    FAISS=[0,1,2], TF-IDF=[1,0,3], rrf_k=60 →
    idx=0: 1/(61+1) + 1/(62+1) = 1/62 + 1/63
    idx=1: 1/(62+1) + 1/(61+1) = aynı (simetrik)
    Eşitlik durumunda sıra idx 0'ın önce geldiği (FAISS listesi ilk) beklenir.
    idx=3 yalnızca TF-IDF'den: 1/(64) — idx 2'den daha düşük.
    """
    result = RAGPipeline._rrf_fuse([[0, 1, 2], [1, 0, 3]], top_k=4, rrf_k=60)
    # idx 0 ve 1 en yüksek; idx 3 (sadece TF-IDF rank 2) idx 2'den düşük olmalı
    assert set(result[:2]) == {0, 1}
    assert 2 in result
    assert 3 in result
    assert result.index(2) < result.index(3)  # idx2 rank2 > idx3 rank2 (FAISS vs TF-IDF)


def test_rrf_dedup():
    """Aynı index iki listede de varsa bir kez çıkmalı."""
    result = RAGPipeline._rrf_fuse([[0, 1, 2], [0, 2, 1]], top_k=10, rrf_k=60)
    assert len(result) == len(set(result))


def test_rrf_top_k_limits(built_service):
    result = RAGPipeline._rrf_fuse([[0, 1, 2], [2, 1, 0]], top_k=2, rrf_k=60)
    assert len(result) == 2
