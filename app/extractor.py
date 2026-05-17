"""
app/extractor.py
----------------
Point d'entrée pour l'extraction PDF → Excel + PKL
"""

import argparse
from pathlib import Path

from data_Extraction import extract


def main():
    parser = argparse.ArgumentParser(description="Extraction PDF → Excel/PKL")
    parser.add_argument("--company", help="Prefix entreprise (ex: DELICE)", default=None)
    parser.add_argument("--year", type=int, help="Année (ex: 2021)", default=None)
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parents[1]
    output_dir = base_dir / "output"

    extract(
        base_dir=base_dir,
        output_dir=output_dir,
        company_filter=args.company,
        year_filter=args.year,
    )


if __name__ == "__main__":
    main()