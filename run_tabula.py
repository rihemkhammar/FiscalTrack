"""
test_tabula.py
--------------
Test global tabula-py sur tous les PDFs de toutes les entreprises.
Affiche le nombre de tableaux trouvés et un aperçu des 3 premiers.

Usage :
    python app/test_tabula.py
"""

import json
from pathlib import Path
import tabula


def load_config(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():

    # 🔥 racine du projet (financial_scraper_app/)
    base_dir = Path(__file__).resolve().parent

    # ✅ bon chemin config
    config_path = base_dir / "app" / "config" / "companies.json"

    config = load_config(config_path)
    global_cfg = config.get("global", {})
    companies = config["companies"]

    min_year = global_cfg.get("min_year", 2014)
    max_year = global_cfg.get("max_year", 2024)

    for company in companies:
        name = company["name"]
        folder = company["folder"]
        prefix = company["filename_prefix"]

        print("\n" + "=" * 60)
        print(f"🏢  {name}")
        print("=" * 60)

        # 📁 chemin dossier société
        folder_path = base_dir / "input" / folder

        if not folder_path.exists():
            print(f"❌ dossier introuvable : {folder_path}")
            continue

        # 🔥 on parcourt uniquement les vrais PDFs existants
        pdf_files = sorted(folder_path.glob("*.pdf"))

        if not pdf_files:
            print("⚠️ aucun PDF trouvé dans ce dossier")
            continue

        for pdf_path in pdf_files:

            print(f"\n  📄 {pdf_path.name}")

            try:
                tables = tabula.read_pdf(
                    str(pdf_path),
                    pages="all",
                    multiple_tables=True,
                    silent=True,
                )

                print(f"  {len(tables)} tableaux trouvés")

                for i, df in enumerate(tables[:3]):
                    print(f"\n    --- Table {i} : {df.shape} ---")
                    print(df.head().to_string())

            except Exception as e:
                print(f"  ❌ erreur lecture PDF : {e}")


if __name__ == "__main__":
    main()