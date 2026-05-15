from pathlib import Path
from data_collection import load_companies, download_company


def custom():
    config_path = Path("config/companies.json")
    config = load_companies(config_path)

    global_config = config.get("global", {})
    companies = config["companies"]

    print(f"📊 {len(companies)} entreprise(s) chargée(s)")

    base_dir = Path(__file__).resolve().parents[1]

    for company in companies[:3]:
        downloaded = download_company(company, global_config, base_dir)
        print(f"  → {company['name']}: {downloaded} PDF(s)")


if __name__ == "__main__":
    custom()