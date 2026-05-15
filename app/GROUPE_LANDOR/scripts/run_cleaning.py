import pickle
import pandas as pd
from pathlib import Path
from cleaner import extract_financials_from_tables

RAW_DIR = Path(r"/data/raw/GROUPE_LANDOR")
OUTPUT = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\processed\GROUPE_LANDOR.xlsx")

def run():
    rows = []

    for pkl in RAW_DIR.glob("*_raw.pkl"):
        print(f"Processing: {pkl.name}")

        with open(pkl, "rb") as f:
            tables = pickle.load(f)

        row = extract_financials_from_tables(tables)
        row["file"] = pkl.name
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.sort_values("year")
    df.to_excel(OUTPUT, index=False)

    print(f"\nSaved cleaned Excel to: {OUTPUT}")

run()
