"""
Formats evaluation results as a Markdown table for the thesis report.
"""

from datetime import date
from typing import Any, Dict, List, Optional


def generate_markdown_report(
    synthetic_results: Dict[str, Dict[str, float]],
    interaction_results: Optional[Dict[str, Dict[str, float]]],
    k_values: List[int],
    n_synthetic: int,
    n_interaction: int,
) -> str:
    today = date.today().isoformat()
    lines: List[str] = [f"# Recommender Offline Evaluation — {today}\n"]

    def _table(results: Dict[str, Dict[str, float]]) -> str:
        headers = ["Sistem"]
        for k in k_values:
            headers += [f"P@{k}", f"HitRate@{k}", f"nDCG@{k}"]
        headers += ["Coverage", "Novelty"]

        sep = ["---"] + ["---:"] * (len(headers) - 1)
        rows = [headers, sep]
        for system_name, metrics in results.items():
            row = [system_name]
            for k in k_values:
                row.append(str(metrics.get(f"P@{k}", "—")))
                row.append(str(metrics.get(f"HitRate@{k}", "—")))
                row.append(str(metrics.get(f"nDCG@{k}", "—")))
            row.append(str(metrics.get("Coverage", "—")))
            row.append(str(metrics.get("Novelty", "—")))
            rows.append(row)

        return "\n".join("| " + " | ".join(r) + " |" for r in rows)

    lines.append(f"## Sentetik Sorgular (N={n_synthetic})\n")
    if synthetic_results:
        lines.append(_table(synthetic_results))
    else:
        lines.append("> No synthetic results.")
    lines.append("")

    if interaction_results:
        lines.append(f"\n## Gerçek Etkileşim Sorguları (N={n_interaction})\n")
        lines.append(_table(interaction_results))
        lines.append("")
    else:
        lines.append("\n## Gerçek Etkileşim Sorguları\n")
        lines.append(
            "> Skipped: DB'de yeterli etkileşim verisi bulunamadı "
            "(≥3 like/cook + context_ingredients gerekli).\n"
        )

    lines.append("\n---")
    lines.append(f"*k değerleri: {k_values}*")
    return "\n".join(lines)
