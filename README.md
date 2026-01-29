# Patient Trial Enrichment
Demo: ML‑based clinical patient trial enrichment (synthetic data)

**Goal:** Demonstrate how genetics + clinical covariates can enrich a trial population and reduce screening failures using **synthetic cohorts** (no IP, no disease‑specific details).

## What this shows
- Building a PRS‑style risk model from simulated genetic features
- Integrating clinical covariates (age/sex/BMI/comorbidities)
- How enrichment shifts eligibility yield and screening burden

## Notes
Everything here uses **synthetic data** and generic labels. The focus is on methodology, validation, and trial‑operations impact.

## Repo structure
```
patient-trial-enrichment/
  data/                 # synthetic data (optional)
  notebooks/            # exploration + demo
  src/                  # reusable code
  reports/              # figures + short report
  README.md
  LICENSE
```

## Quick start
```bash
pip install -r requirements.txt
python src/run_pipeline.py
```

Outputs:
- `reports/enrichment_yield.png`
- `reports/enrichment_curve.csv`
- `reports/summary.md`

## Tech
- Python (primary)
- R (optional, if you want to extend with PRS tools)

---
*Author: Sahar Esmaeeli, PhD*
