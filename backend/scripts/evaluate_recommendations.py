"""
CLI script for offline evaluation of the recommendation system.

Usage (from backend/):
    ./venv/bin/python -m scripts.evaluate_recommendations --output reports/eval.md
    ./venv/bin/python scripts/evaluate_recommendations.py --k 5 --k 10 --seed 42

Steps:
  1. Load recipe catalog + FAISS index
  2. Build synthetic test queries (holdout from catalog)
  3. Fetch real interaction queries from DB (skipped if insufficient data)
  4. Evaluate Jaccard baseline and RAG pipeline on both query sets
  5. Write Markdown report
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Allow imports from backend/ root regardless of cwd
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s %(name)s: %(message)s",
)


async def _fetch_db_data(min_interactions: int):
    """Fetch interaction queries and item popularity in a single event loop."""
    from sqlalchemy import text

    from app.database import engine
    from evaluation.dataset import fetch_interaction_queries

    interaction_queries = await fetch_interaction_queries(min_interactions)

    item_popularity: dict = {}
    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                text(
                    "SELECT recipe_title, COUNT(*) "
                    "FROM recipe_interactions "
                    "GROUP BY recipe_title"
                )
            )
            item_popularity = {row[0]: int(row[1]) for row in result.fetchall()}
    except Exception as exc:
        logging.getLogger(__name__).warning(f"Could not fetch item popularity: {exc}")

    return interaction_queries, item_popularity


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Offline evaluation for the recipe recommender"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--holdout-ratio",
        type=float,
        default=0.2,
        help="Fraction of recipes used as synthetic test set (default 0.2)",
    )
    parser.add_argument(
        "--k",
        type=int,
        action="append",
        default=None,
        metavar="K",
        help="k value for @k metrics (repeatable, default: 5 10)",
    )
    parser.add_argument(
        "--min-interactions",
        type=int,
        default=3,
        help="Min like/cook count per user for interaction query set (default 3)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to write the Markdown report (also printed to stdout)",
    )
    args = parser.parse_args()

    k_values = sorted(args.k) if args.k else [5, 10]

    # --- 1. Load catalog + FAISS index ---
    print("Loading recipe catalog...")
    from app.services.recipe_service import recipe_service
    recipe_service._ensure_loaded()
    catalog_size = recipe_service.get_total_count()
    print(f"  {catalog_size} recipes")

    print("Loading FAISS index...")
    from app.services.faiss_service import faiss_service
    loaded = faiss_service.load_index()
    if loaded:
        print("  FAISS index loaded — using vector search")
    else:
        print("  FAISS index not found — RAG will fall back to string matching")

    # --- 2. Build synthetic queries ---
    print(f"Building synthetic queries (seed={args.seed}, holdout={args.holdout_ratio})...")
    from evaluation.dataset import build_synthetic_queries
    synthetic_queries = build_synthetic_queries(
        seed=args.seed, holdout_ratio=args.holdout_ratio
    )
    print(f"  {len(synthetic_queries)} synthetic queries")

    # --- 3. Fetch real interaction queries + popularity from DB ---
    print("Fetching interaction queries from DB...")
    try:
        interaction_queries, item_popularity = asyncio.run(
            _fetch_db_data(args.min_interactions)
        )
        if interaction_queries:
            print(f"  {len(interaction_queries)} interaction queries")
        else:
            print("  No interaction queries (insufficient data — skipped)")
    except Exception as exc:
        print(f"  DB unavailable ({exc}) — skipping interaction queries")
        interaction_queries, item_popularity = [], {}

    # --- 4. Define systems ---
    from evaluation.systems import jaccard_recommend, rag_no_personalization
    systems = {
        "Jaccard (baseline)": jaccard_recommend,
        "RAG (FAISS + reranker)": rag_no_personalization,
    }

    # --- 5. Run evaluation ---
    from evaluation.runner import run_evaluation

    print(f"\nEvaluating on {len(synthetic_queries)} synthetic queries...")
    synthetic_results = run_evaluation(
        systems=systems,
        queries=synthetic_queries,
        k_values=k_values,
        item_popularity=item_popularity,
        catalog_size=catalog_size,
    )

    interaction_results = None
    if interaction_queries:
        print(f"Evaluating on {len(interaction_queries)} interaction queries...")
        interaction_results = run_evaluation(
            systems=systems,
            queries=interaction_queries,
            k_values=k_values,
            item_popularity=item_popularity,
            catalog_size=catalog_size,
        )

    # --- 6. Generate report ---
    from evaluation.reporter import generate_markdown_report
    report = generate_markdown_report(
        synthetic_results=synthetic_results,
        interaction_results=interaction_results,
        k_values=k_values,
        n_synthetic=len(synthetic_queries),
        n_interaction=len(interaction_queries),
    )

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"\nReport written to: {args.output}")

    print("\n" + report)


if __name__ == "__main__":
    main()
