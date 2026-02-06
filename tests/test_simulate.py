import numpy as np

from simulate import generate_synthetic_cohort


def test_simulate_cohort_columns():
    df = generate_synthetic_cohort(n=200, n_snps=12, seed=1)
    expected = {"age", "sex", "bmi", "comorbidity_count", "risk_score_true", "outcome"}
    snp_cols = {c for c in df.columns if c.startswith("snp_")}
    assert len(snp_cols) == 12
    assert expected.issubset(df.columns)
    assert df["outcome"].dropna().isin([0, 1]).all()
    assert np.isfinite(df["risk_score_true"]).all()
