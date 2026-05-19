"""
Unit tests for the offline evaluation metrics.
All tests use hand-computed expected values so correctness is verifiable.
"""

import math
import sys
from pathlib import Path

import pytest

# Allow imports from backend/ when pytest runs from backend/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluation.metrics import (
    coverage,
    hit_rate_at_k,
    ndcg_at_k,
    novelty,
    precision_at_k,
)

# ── precision_at_k ───────────────────────────────────────────────────────────

def test_precision_at_k_basic():
    recs = ["A", "B", "C", "D", "E"]
    relevant = {"B", "D"}
    # top-3: A, B, C  →  1 hit (B)  →  1/3
    assert precision_at_k(recs, relevant, 3) == pytest.approx(1 / 3)


def test_precision_at_k_all_relevant():
    recs = ["A", "B"]
    relevant = {"A", "B"}
    assert precision_at_k(recs, relevant, 2) == 1.0


def test_precision_at_k_no_relevant():
    recs = ["A", "B", "C"]
    relevant = {"X", "Y"}
    assert precision_at_k(recs, relevant, 3) == 0.0


def test_precision_at_k_zero_k():
    assert precision_at_k(["A", "B"], {"A"}, 0) == 0.0


def test_precision_at_k_k_larger_than_list():
    # Denominator is always k, even if fewer items are recommended
    recs = ["A", "B"]
    relevant = {"A"}
    assert precision_at_k(recs, relevant, 5) == pytest.approx(1 / 5)


# ── hit_rate_at_k ────────────────────────────────────────────────────────────

def test_hit_rate_hit():
    recs = ["A", "B", "C", "D", "E"]
    relevant = {"B", "D"}
    assert hit_rate_at_k(recs, relevant, 5) == 1.0


def test_hit_rate_miss():
    recs = ["A", "B", "C"]
    relevant = {"X"}
    assert hit_rate_at_k(recs, relevant, 3) == 0.0


def test_hit_rate_relevant_outside_k():
    # B is at index 3, so not in top-3 but is in top-4
    recs = ["A", "C", "D", "B", "E"]
    relevant = {"B"}
    assert hit_rate_at_k(recs, relevant, 3) == 0.0
    assert hit_rate_at_k(recs, relevant, 4) == 1.0


# ── ndcg_at_k ────────────────────────────────────────────────────────────────

def test_ndcg_perfect_ranking():
    # Relevant item at rank 1 → DCG = IDCG = 1/log2(2) → nDCG = 1.0
    recs = ["A", "B", "C"]
    relevant = {"A"}
    assert ndcg_at_k(recs, relevant, 3) == pytest.approx(1.0)


def test_ndcg_relevant_at_position_2():
    # recs[1] is relevant → DCG = 1/log2(3); IDCG = 1/log2(2)
    recs = ["X", "A", "Y"]
    relevant = {"A"}
    expected = (1 / math.log2(3)) / (1 / math.log2(2))
    assert ndcg_at_k(recs, relevant, 3) == pytest.approx(expected)


def test_ndcg_no_relevant_in_top_k():
    recs = ["A", "B", "C"]
    relevant = {"X"}
    assert ndcg_at_k(recs, relevant, 3) == 0.0


def test_ndcg_empty_relevant():
    recs = ["A", "B"]
    assert ndcg_at_k(recs, set(), 2) == 0.0


# ── coverage ─────────────────────────────────────────────────────────────────

def test_coverage_basic():
    # 8 unique items out of catalog of 20
    all_recs = [["A", "B", "C"], ["D", "E", "F"], ["A", "G", "H"]]
    assert coverage(all_recs, 20) == pytest.approx(8 / 20)


def test_coverage_full():
    all_recs = [["A", "B"], ["C", "D"]]
    assert coverage(all_recs, 4) == 1.0


def test_coverage_zero_catalog():
    assert coverage([["A"]], 0) == 0.0


def test_coverage_empty_recs():
    assert coverage([], 10) == 0.0


# ── novelty ──────────────────────────────────────────────────────────────────

def test_novelty_uniform_popularity():
    popularity = {"A": 5, "B": 5, "C": 5}
    all_recs = [["A", "B"], ["C"]]
    total = 15
    expected = -math.log2(5 / total)
    assert novelty(all_recs, popularity) == pytest.approx(expected)


def test_novelty_less_popular_is_more_novel():
    popularity = {"popular": 100, "niche": 1}
    score_popular = novelty([["popular"]], popularity)
    score_niche = novelty([["niche"]], popularity)
    assert score_niche > score_popular


def test_novelty_unknown_item_gets_pop1():
    # Items absent from popularity are treated as pop=1
    popularity = {"A": 10}
    total = 10
    expected_a = -math.log2(10 / total)   # = 0.0
    expected_u = -math.log2(1 / total)
    expected = (expected_a + expected_u) / 2
    assert novelty([["A", "UNKNOWN"]], popularity) == pytest.approx(expected)


def test_novelty_empty():
    assert novelty([], {}) == 0.0
