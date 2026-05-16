import pickle
import pandas as pd
from pathlib import Path

# Make pandas show all rows/columns
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

MERGED_PATH = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\processed\GROUPE_LANDOR\LANDOR_2014_merged.pkl")

with open(MERGED_PATH, "rb") as f:
    merged_data = pickle.load(f)

print("Keys in merged data:", merged_data.keys())

structured_tables = merged_data["structured"]
print("Structured tables count:", len(structured_tables))

context_tables = merged_data["context"]
print("Context tables count:", len(context_tables))

# Loop through all context tables and show full content
for i, df in enumerate(context_tables):
    print(f"\n=== Context Table {i} ===")
    print(df)   # prints the entire DataFrame
