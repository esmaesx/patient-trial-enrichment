import numpy as np
import pandas as pd


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def generate_synthetic_cohort(
    n=6000,
    n_snps=60,
    seed=7,
):
    """Generate a synthetic cohort with genetics + clinical covariates.

    Returns
    -------
    df : pd.DataFrame
        Columns include snp_*, age, sex, bmi, comorbidity_count,
        risk_score_true, outcome.
    """
    rng = np.random.default_rng(seed)

    # Genetics: minor allele dosages (0,1,2) with varying MAFs
    mafs = rng.uniform(0.05, 0.5, size=n_snps)
    snps = rng.binomial(2, mafs, size=(n, n_snps))

    # Clinical covariates
    age = rng.normal(58, 10, size=n).clip(18, 85)
    sex = rng.integers(0, 2, size=n)  # 0/1
    bmi = rng.normal(27, 4.5, size=n).clip(17, 45)
    comorb = rng.poisson(1.4, size=n).clip(0, 6)

    # True underlying risk: sparse SNP effects + clinical effects
    w = rng.normal(0, 0.15, size=n_snps)
    # Add a few stronger effects
    strong_idx = rng.choice(n_snps, size=6, replace=False)
    w[strong_idx] += rng.normal(0.6, 0.15, size=6)

    genetic_score = snps @ w
    clinical = 0.02 * (age - 50) + 0.25 * sex + 0.05 * (bmi - 25) + 0.18 * comorb

    # Base rate control
    logits = -2.2 + 0.8 * (genetic_score / np.std(genetic_score)) + clinical
    p = _sigmoid(logits)
    outcome = rng.binomial(1, p)

    df = pd.DataFrame(snps, columns=[f"snp_{i+1}" for i in range(n_snps)])
    df["age"] = age
    df["sex"] = sex
    df["bmi"] = bmi
    df["comorbidity_count"] = comorb
    df["risk_score_true"] = p
    df["outcome"] = outcome

    return df
