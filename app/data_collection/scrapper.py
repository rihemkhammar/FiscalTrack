from pathlib import Path
import argparse
from .downloader import load_companies, download_company


BASE_DIR = Path(__file__).resolve().parents[3]
CONFIG_DIR = Path(__file__).resolve().parent


def scrapper():
    parser = argparse.ArgumentParser(
        description="Télécharge les états financiers CMF depuis un fichier de config."
    )

    parser.add_argument(
        "--config",
        default=str(CONFIG_DIR / "companies.json"),
        help="Chemin vers le fichier de config JSON ou CSV"
    )

    parser.add_argument(
        "--company",
        default=None,
        help="Nom exact d'une entreprise (optionnel)"
    )

    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Config introuvable : {config_path}")

    config = load_companies(config_path)

    global_config = config.get("global", {})
    companies = config["companies"]

    # filtrer une seule entreprise si besoin
    if args.company:
        companies = [c for c in companies if c["name"] == args.company]

        if not companies:
            raise ValueError(f"Aucune entreprise trouvée : {args.company}")

    total = 0
    for company in companies:
        total += download_company(company, global_config, BASE_DIR)

    print(f"\n✅ Terminé. Total : {total} PDF(s) téléchargé(s).")


if __name__ == "__main__":
    scrapper()