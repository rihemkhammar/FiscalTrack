"""Module utilitaire pour télécharger les états financiers CMF."""

from pathlib import Path
import requests
from bs4 import BeautifulSoup
import json
import csv


def load_companies(config_path: Path) -> dict:
    """Charge la config JSON ou CSV avec support de global config."""
    suffix = config_path.suffix.lower()

    if suffix == ".json":
        with open(config_path, encoding="utf-8") as f:
            return json.load(f)

    elif suffix == ".csv":
        with open(config_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            companies = []
            for row in reader:
                row["min_year"] = int(row["min_year"])
                row["max_year"] = int(row["max_year"])
                companies.append(row)

        return {
            "global": {},
            "companies": companies
        }

    else:
        raise ValueError(f"Format non supporté : {suffix}. Utilisez .json ou .csv")

def download_company(company: dict, global_config: dict, base_dir: Path) -> int:
    """Télécharge les PDFs pour une entreprise donnée."""

    # --- merge global + company ---
    name = company["name"]
    folder = company.get("folder", name.replace("'", "").replace(" ", "_"))
    prefix = company.get("filename_prefix", folder)

    min_year = int(company.get("min_year", global_config.get("min_year", 2014)))
    max_year = int(company.get("max_year", global_config.get("max_year", 2024)))

    url = company.get("url", global_config["url"])
    param_key = company.get("param_key", global_config.get("param_key", "field_societesape_value"))

    save_dir = base_dir / "input" / folder
    save_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 50}")
    print(f"Entreprise : {name}")
    print(f"Dossier    : {save_dir}")
    print(f"Années     : {min_year} → {max_year}")
    print(f"{'=' * 50}")

    params = {param_key: name, "page": 0}
    downloaded = 0
    page = 0

    while True:
        params["page"] = page
        response = requests.get(url, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("div", class_="views-row")

        if not rows:
            print(f"  Fin des résultats à la page {page}.")
            break

        for row in rows:
            year_div = row.select_one(".field-name-field-exercice .field-item")
            if not year_div:
                continue

            try:
                year = int(year_div.text.strip())
            except ValueError:
                continue

            if not (min_year <= year <= max_year):
                continue

            pdf_tag = row.find("a", href=True)
            if not pdf_tag:
                continue

            pdf_link = pdf_tag["href"]
            if pdf_link.startswith("/"):
                base_url = "/".join(url.split("/")[:3])
                pdf_link = base_url + pdf_link

            pdf_response = requests.get(pdf_link)
            pdf_response.raise_for_status()

            filename = save_dir / f"{prefix}_{year}.pdf"
            filename.write_bytes(pdf_response.content)

            print(f"  ✓ Sauvegardé : {filename.name}")
            downloaded += 1

        page += 1

    print(f"  → {downloaded} PDF(s) téléchargé(s) pour {name}")
    return downloaded