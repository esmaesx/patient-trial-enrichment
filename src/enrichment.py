import numpy as np
import pandas as pd


def enrichment_curve(y_true, y_score, percentiles=None):
    if percentiles is None:
        percentiles = np.arange(5, 51, 5)

    df = pd.DataFrame({"y": y_true, "score": y_score})
    df = df.sort_values("score", ascending=False).reset_index(drop=True)

    base_rate = df["y"].mean()

    rows = []
    for p in percentiles:
        k = int(len(df) * (p / 100.0))
        subset = df.iloc[:k]
        yield_rate = subset["y"].mean()
        enrichment = yield_rate / base_rate if base_rate > 0 else np.nan
        rows.append(
            {
                "percentile": p,
                "selected_n": k,
                "yield_rate": yield_rate,
                "enrichment": enrichment,
            }
        )

    return pd.DataFrame(rows), base_rate


def screening_savings(base_rate, enriched_rate, target_n=500):
    """Compute how many people need to be screened to reach target_n."""
    base_needed = target_n / base_rate if base_rate > 0 else np.inf
    enriched_needed = target_n / enriched_rate if enriched_rate > 0 else np.inf
    reduction = 1.0 - (enriched_needed / base_needed) if base_needed > 0 else np.nan
    return base_needed, enriched_needed, reduction
