import pickle
from pathlib import Path
import pandas as pd

file_path = Path("output/GROUPE_LANDOR/LANDOR_tables.pkl")

if not file_path.exists():
    print("❌ File not found:", file_path)
else:
    with open(file_path, "rb") as f:
        tables = pickle.load(f)

    print("✅ File loaded successfully")
    print("Number of tables:", len(tables))

    for i, df in enumerate(tables):
        print("\n" + "="*50)
        print(f"📊 TABLE {i} - shape: {df.shape}")
        print("="*50)

        print(df)   # affiche le contenu complet