# Patient Trial Enrichment

Synthetic demo showing how risk-based pre-screening can improve clinical trial yield. The pipeline generates a 6,000-row cohort with 60 SNPs plus age/sex/BMI/comorbidity_count, trains two classifiers, and reports how selecting the top-risk tranche changes screening load. The focus is on enrichment math, not disease-specific results.

Why it matters
- Trial operations teams need concrete estimates of screening savings, not just model AUCs.
- Genetics + clinical covariates often move yield more than either alone.
- A simple, reproducible demo makes enrichment tradeoffs easy to communicate.

Quickstart
```bash
make setup
make demo
make test
```

What you get
- `reports/enrichment_yield.png` (yield vs. selection percentile)
- `reports/enrichment_curve.csv` (percentiles, yield rates, enrichment)
- `reports/summary.json` and `reports/summary.md` (screening savings at top 20%)

Notes / assumptions
- Synthetic cohort is generated in `src/simulate.py` (6,000 samples, 60 SNPs; seed=7).
- Base event rate is controlled by the logit intercept (-2.2) to land around ~10%.
- Model selection uses ROC AUC on a 25% holdout; screening savings are computed at the top 20% predicted risk.

Status
Ready for demo; uses only synthetic data.
