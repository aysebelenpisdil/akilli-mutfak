"""
Offline evaluation metrics for the recommendation system.
All functions are pure — no I/O, no singletons.

Metrics implemented (matching the thesis proposal):
  Precision@k, HitRate@k, nDCG@k, Coverage, Novelty
"""

import math
from typing import Dict, List, Set


def precision_at_k(recommended: List[str], relevant: Set[str], k: int) -> float:
    """Fraction of top-k recommendations that are relevant."""
    if k <= 0:
        return 0.0
    hits = sum(1 for r in recommended[:k] if r in relevant)
    return hits / k


def hit_rate_at_k(recommended: List[str], relevant: Set[str], k: int) -> float:
    """1 if any relevant item appears in top-k, else 0."""
    return 1.0 if any(r in relevant for r in recommended[:k]) else 0.0


def ndcg_at_k(recommended: List[str], relevant: Set[str], k: int) -> float:
    """Normalized Discounted Cumulative Gain with binary relevance."""
    if k <= 0 or not relevant:
        return 0.0
    dcg = sum(
        1.0 / math.log2(i + 2)
        for i, r in enumerate(recommended[:k])
        if r in relevant
    )
    # Ideal DCG: all min(|relevant|, k) hits at the top positions
    n_ideal = min(len(relevant), k)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(n_ideal))
    return dcg / idcg if idcg > 0 else 0.0


def coverage(all_recommendations: List[List[str]], catalog_size: int) -> float:
    """Fraction of the catalog that appears in any recommendation list."""
    if catalog_size <= 0:
        return 0.0
    unique = {item for recs in all_recommendations for item in recs}
    return len(unique) / catalog_size


def novelty(
    all_recommendations: List[List[str]],
    item_popularity: Dict[str, int],
) -> float:
    """
    Mean self-information: -log2(pop / total_interactions).
    Higher value = more novel (less popular) recommendations.
    Items absent from item_popularity are treated as popularity=1.
    """
    total = sum(item_popularity.values()) or 1
    scores: List[float] = []
    for recs in all_recommendations:
        for item in recs:
            pop = item_popularity.get(item, 1)
            scores.append(-math.log2(max(pop, 1) / total))
    return sum(scores) / len(scores) if scores else 0.0
