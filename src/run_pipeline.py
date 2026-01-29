from pathlib import Path
import json

import pandas as pd

from simulate import generate_synthetic_cohort
from modeling import train_models
from enrichment import enrichment_curve, screening_savings
from plotting import plot_enrichment_curve


def main():
    root = Path(__file__).resolve().parents[1]
    reports = root / "reports"
    reports.mkdir(exist_ok=True)

    # 1) Generate synthetic cohort
    df = generate_synthetic_cohort(n=6000, n_snps=60, seed=7)

    # 2) Train models
    results = train_models(df.drop(columns=["risk_score_true"], errors="ignore"), seed=7)

    # 3) Choose best model (ROC AUC)
    best_name = max(results, key=lambda k: results[k]["roc_auc"])
    best = results[best_name]

    # 4) Enrichment curve
    curve, base_rate = enrichment_curve(best["y_test"], best["proba"])
    curve_path = reports / "enrichment_curve.csv"
    curve.to_csv(curve_path, index=False)

    plot_path = reports / "enrichment_yield.png"
    plot_enrichment_curve(curve, plot_path)

    # 5) Screening savings at a realistic selection point
    # Example: top 20% predicted risk
    row20 = curve[curve["percentile"] == 20].iloc[0]
    base_needed, enriched_needed, reduction = screening_savings(
        base_rate, row20["yield_rate"], target_n=500
    )

    summary = {
        "best_model": best_name,
        "roc_auc": round(best["roc_auc"], 3),
        "pr_auc": round(best["pr_auc"], 3),
        "brier": round(best["brier"], 3),
        "base_rate": round(base_rate, 4),
        "selected_percentile": 20,
        "selected_yield": round(float(row20["yield_rate"]), 4),
        "enrichment": round(float(row20["enrichment"]), 2),
        "screened_base": int(base_needed),
        "screened_enriched": int(enriched_needed),
        "screening_reduction": round(float(reduction), 2),
    }

    (reports / "summary.json").write_text(json.dumps(summary, indent=2))

    # Human-readable summary
    lines = [
        "# Trial enrichment summary",
        f"Best model: **{best_name}** (ROC AUC {summary['roc_auc']}, PR AUC {summary['pr_auc']})",
        f"Base event rate: **{summary['base_rate']}**",
        f"Top {summary['selected_percentile']}% selection yield: **{summary['selected_yield']}**",
        f"Enrichment vs base: **{summary['enrichment']}x**",
        f"Estimated screening need for n=500:",
        f"- Baseline: **{summary['screened_base']}**",
        f"- Enriched: **{summary['screened_enriched']}**",
        f"- Reduction: **{summary['screening_reduction']}**",
    ]
    (reports / "summary.md").write_text("\n".join(lines) + "\n")

    print("Wrote:", plot_path, curve_path)


if __name__ == "__main__":
    main()
