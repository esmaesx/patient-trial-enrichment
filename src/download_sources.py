"""Utilities to download small public reference files or link to large datasets.
This script intentionally avoids auto-downloading very large files.
"""
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

SOURCES = {
    "gwas_catalog": "https://www.ebi.ac.uk/gwas/",
    "gtex_v8": "https://gtexportal.org/home/",
    "scallop_pqtl": "https://www.scallop.org/",
    "pgs_catalog": "https://www.pgscatalog.org/",
}

README = DATA / "SOURCES.md"
lines = "\n".join([f"- {k}: {v}" for k, v in SOURCES.items()])
README.write_text("# Data sources (links)\n\n" + lines + "\n")
print(f"Wrote {README}")
