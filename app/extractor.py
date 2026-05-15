"""
app/extractor.py
----------------
Point d'entrée pour l'extraction PDF → Excel + PKL.
Consomme app/data_Extraction/extract_all.py

Usage :
    python app/extractor.py                        # toutes les entreprises
    python app/extractor.py --company DELICE       # une seule entreprise
    python app/extractor.py --year 2021            # une seule année
    python app/extractor.py --company DELICE --year 2021
"""

import argparse
from pathlib import Path

from data_Extraction import extract


def main():
    parser = argparse.ArgumentParser(description="Extraction PDF → Excel/PKL")
    parser.add_argument("--company", help="Prefix entreprise (ex: DELICE)", default=None)
    parser.add_argument("--year",    help="Année (ex: 2021)", type=int, default=None)
    args = parser.parse_args()

    base_dir   = Path(__file__).resolve().parents[1]   # racine du projet
    output_dir = base_dir / "output"                   # → financial_scraper_app/output/

    extract(
        base_dir       = base_dir,
        output_dir     = output_dir,
        company_filter = args.company,
        year_filter    = args.year,
    )


if __name__ == "__main__":
    main()