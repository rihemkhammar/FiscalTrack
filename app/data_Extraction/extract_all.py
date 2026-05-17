"""
app/data_Extraction/extract_all.py
-----------------------------------
Logique d'extraction PDF → Excel + PKL (mode incrémental).
"""

import json
import pickle
from pathlib import Path

import pandas as pd
import tabula


# ── helpers ──────────────────────────────────────────────────────────────────

def load_config(config_path: Path) -> dict:
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def load_existing_pkl(path: Path) -> dict:
    """Charge les anciennes données si elles existent"""
    if path.exists():
        with open(path, "rb") as f:
            return pickle.load(f)
    return {}


def find_pdfs(base_dir: Path, folder: str, prefix: str,
              min_year: int, max_year: int) -> list[tuple[int, Path]]:
    input_dir = base_dir / "input" / folder
    results = []

    for year in range(min_year, max_year + 1):
        pdf = input_dir / f"{prefix}_{year}.pdf"
        if pdf.exists():
            results.append((year, pdf))
        else:
            print(f"  ⚠️  introuvable : {pdf.name}")

    return results


def extract_tables(pdf_path: Path) -> list[pd.DataFrame]:
    try:
        tables = tabula.read_pdf(
            str(pdf_path),
            pages="all",
            multiple_tables=True,
            silent=True,
            pandas_options={"dtype": str},
        )
        return [df for df in tables if df.shape[0] >= 3 and df.shape[1] >= 2]

    except Exception as e:
        print(f"    ❌ Erreur : {e}")
        return []


def save_excel(data: dict, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for year, tables in sorted(data.items()):
            for i, df in enumerate(tables):
                sheet_name = f"{year}_T{i:02d}"[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    total = sum(len(v) for v in data.values())
    print(f"  📊 Excel → {out_path.name} ({total} tables)")


def save_pkl(data: dict, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "wb") as f:
        pickle.dump(data, f)

    print(f"  🥒 PKL   → {out_path.name}")


def process_company(company: dict, global_cfg: dict,
                    base_dir: Path, output_dir: Path,
                    year_filter: int | None = None) -> None:

    name   = company["name"]
    folder = company["folder"]
    prefix = company["filename_prefix"]

    min_y = global_cfg.get("min_year", 2014)
    max_y = global_cfg.get("max_year", 2024)

    print(f"\n{'='*60}")
    print(f"🏢  {name}")
    print(f"{'='*60}")

    pdfs = find_pdfs(base_dir, folder, prefix, min_y, max_y)

    if year_filter:
        pdfs = [(y, p) for y, p in pdfs if y == year_filter]

    if not pdfs:
        print("  Aucun PDF trouvé.")
        return

    out_dir = output_dir / folder
    pkl_path = out_dir / f"{prefix}_tables.pkl"

    # 🔥 CHARGEMENT ANCIENNES DONNÉES
    all_data: dict[int, list[pd.DataFrame]] = load_existing_pkl(pkl_path)

    for year, pdf_path in pdfs:
        print(f"\n  📄 {pdf_path.name} …", end=" ", flush=True)

        new_tables = extract_tables(pdf_path)
        print(f"{len(new_tables)} tableau(x) utile(s)")

        if year not in all_data:
            all_data[year] = []

        # 🔥 merge sans doublons simples
        for df in new_tables:
            if not any(df.equals(old) for old in all_data[year]):
                all_data[year].append(df)

    if all_data:
        save_excel(all_data, out_dir / f"{prefix}_tables.xlsx")
        save_pkl(all_data, pkl_path)
    else:
        print("  ⚠️  Aucune donnée extraite.")


# ── API principale ───────────────────────────────────────────────────────────

def extract(base_dir: Path, output_dir: Path,
            company_filter: str | None = None,
            year_filter: int | None = None) -> None:

    config_path = Path(__file__).resolve().parents[1] / "config" / "companies.json"

    print(f"📂 Projet  : {base_dir}")
    print(f"📤 Output  : {output_dir}")
    print(f"⚙️  Config  : {config_path}")

    config     = load_config(config_path)
    global_cfg = config.get("global", {})
    companies  = config["companies"]

    if company_filter:
        companies = [
            c for c in companies
            if company_filter.upper() in c["filename_prefix"].upper()
        ]
        if not companies:
            print(f"❌ '{company_filter}' introuvable dans companies.json")
            return

    print(f"\n📊 {len(companies)} entreprise(s) à traiter")

    for company in companies:
        process_company(company, global_cfg, base_dir, output_dir, year_filter)

    print("\n✅ Extraction terminée.")