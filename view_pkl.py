import pickle
from pathlib import Path
import pandas as pd

PKL_DIR = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\raw\GROUPE_LANDOR")

# List all PKL files
pkl_files = list(PKL_DIR.glob("*_raw.pkl"))

print("Available PKL files:")
for i, pkl in enumerate(pkl_files):
    print(f"{i} → {pkl.name}")

choice = input("\nEnter the number of the PKL you want to open (or 'all'): ")

if choice.lower() == "all":
    for pkl in pkl_files:
        print(f"\n\n===== {pkl.name} =====")
        with open(pkl, "rb") as f:
            tables = pickle.load(f)
        print(f"Number of tables: {len(tables)}")
        for i, df in enumerate(tables):
            print(f"\n--- TABLE {i} ---")
            print(df)
else:
    idx = int(choice)
    pkl = pkl_files[idx]
    print(f"\nLoading: {pkl.name}")

    with open(pkl, "rb") as f:
        tables = pickle.load(f)

    print(f"\nNumber of tables: {len(tables)}")
    for i, df in enumerate(tables):
        print(f"\n--- TABLE {i} ---")
        print(df)
