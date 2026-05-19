"""
Uniform recommend(query_ingredients, top_k) -> List[str] interface for each system.
Systems:
  1. jaccard_recommend   — content-based Jaccard baseline
  2. rag_recommend       — FAISS + cross-encoder reranker, no personalization
  3. rag_personalized_recommend — full pipeline with user history, no LLM

All wrappers call explain=False so Gemini is never invoked during evaluation.
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def jaccard_recommend(query_ingredients: List[str], top_k: int = 10) -> List[str]:
    from evaluation.baselines import jaccard_recommender
    return jaccard_recommender.recommend(query_ingredients, top_k)


def rag_recommend(
    query_ingredients: List[str],
    top_k: int = 10,
    user_history: Optional[Dict[str, str]] = None,
) -> List[str]:
    """
    Calls the full RAG pipeline (FAISS → reranker → optional personalization).
    LLM generation is always disabled (explain=False).
    """
    from app.services.rag_pipeline import rag_pipeline
    result = rag_pipeline.process(
        user_ingredients=query_ingredients,
        top_k=top_k,
        retrieval_top_k=50,
        explain=False,
        user_history=user_history,
    )
    return [r.Title for r in result.get("recipes", [])]


def rag_no_personalization(query_ingredients: List[str], top_k: int = 10) -> List[str]:
    return rag_recommend(query_ingredients, top_k, user_history=None)


def rag_faiss_only(query_ingredients: List[str], top_k: int = 10) -> List[str]:
    """FAISS-only retrieval (TF-IDF kapalı) — A/B karşılaştırması için."""
    from app.services.rag_pipeline import rag_pipeline
    result = rag_pipeline.process(
        user_ingredients=query_ingredients,
        top_k=top_k,
        retrieval_top_k=50,
        explain=False,
        use_hybrid=False,
    )
    return [r.Title for r in result.get("recipes", [])]


def rag_hybrid(query_ingredients: List[str], top_k: int = 10) -> List[str]:
    """FAISS + TF-IDF hibrit retrieval (RRF) — tfidf_service yüklüyse aktif."""
    from app.services.rag_pipeline import rag_pipeline
    result = rag_pipeline.process(
        user_ingredients=query_ingredients,
        top_k=top_k,
        retrieval_top_k=50,
        explain=False,
        use_hybrid=True,
    )
    return [r.Title for r in result.get("recipes", [])]
