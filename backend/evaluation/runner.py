"""
Evaluation runner: calls each system on every query and aggregates metrics.
"""

import logging
from typing import Any, Callable, Dict, List

from evaluation.dataset import QuerySet
from evaluation.metrics import (
    coverage,
    hit_rate_at_k,
    ndcg_at_k,
    novelty,
    precision_at_k,
)

logger = logging.getLogger(__name__)

# recommend(query_ingredients, top_k) -> List[str]
System = Callable[[List[str], int], List[str]]


def run_evaluation(
    systems: Dict[str, System],
    queries: QuerySet,
    k_values: List[int],
    item_popularity: Dict[str, int],
    catalog_size: int,
) -> Dict[str, Dict[str, float]]:
    """
    Evaluate each system on all queries and return aggregated metrics.

    Returns:
        {system_name: {metric_label: value}}
    """
    if not queries:
        return {name: {} for name in systems}

    max_k = max(k_values)
    results: Dict[str, Dict[str, float]] = {}

    for system_name, recommend_fn in systems.items():
        logger.info(f"Evaluating: {system_name}")
        all_recs: List[List[str]] = []
        p_acc: Dict[int, List[float]] = {k: [] for k in k_values}
        hr_acc: Dict[int, List[float]] = {k: [] for k in k_values}
        ndcg_acc: Dict[int, List[float]] = {k: [] for k in k_values}

        for i, (query_ingredients, relevant) in enumerate(queries):
            try:
                recommended = recommend_fn(query_ingredients, max_k)
            except Exception as exc:
                logger.warning(f"[{system_name}] query {i} failed: {exc}")
                recommended = []
            all_recs.append(recommended)
            for k in k_values:
                p_acc[k].append(precision_at_k(recommended, relevant, k))
                hr_acc[k].append(hit_rate_at_k(recommended, relevant, k))
                ndcg_acc[k].append(ndcg_at_k(recommended, relevant, k))

        n = len(queries)
        sys_metrics: Dict[str, float] = {}
        for k in k_values:
            sys_metrics[f"P@{k}"] = round(sum(p_acc[k]) / n, 4)
            sys_metrics[f"HitRate@{k}"] = round(sum(hr_acc[k]) / n, 4)
            sys_metrics[f"nDCG@{k}"] = round(sum(ndcg_acc[k]) / n, 4)
        sys_metrics["Coverage"] = round(coverage(all_recs, catalog_size), 4)
        sys_metrics["Novelty"] = round(novelty(all_recs, item_popularity), 4)

        results[system_name] = sys_metrics
        logger.info(f"  → {sys_metrics}")

    return results
