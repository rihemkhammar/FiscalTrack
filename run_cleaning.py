import pickle
import pandas as pd
from pathlib import Path
from cleaner import extract_financials_from_tables

# Dossiers
RAW_DIR = Path(r"C:\Users\mariem\workspace\FiscalTrack\output\GROUPE_LANDOR")
OUTPUT = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\processed\GROUPE_LANDOR.xlsx")

def run():
    rows = []

    # Charger chaque PKL
    for pkl in RAW_DIR.glob("*_tables.pkl"):
        print(f"Processing: {pkl.name}")

        with open(pkl, "rb") as f:
            tables_by_year = pickle.load(f)

        # PKL est un dict {year: [tables]}
        for year, tables in tables_by_year.items():
            row = extract_financials_from_tables(tables)
            row["year"] = year
            row["file"] = pkl.name
            rows.append(row)

    # Construire DataFrame
    df = pd.DataFrame(rows)

    if "year" in df.columns:
        df = df.sort_values("year", na_position="last")
    else:
        print("⚠️ Pas de colonne 'year' trouvée")
        print(df)

    # Sauvegarde Excel
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(OUTPUT, index=False)
    print(f"\n✅ Saved cleaned Excel to: {OUTPUT}")

if __name__ == "__main__":
    run()
