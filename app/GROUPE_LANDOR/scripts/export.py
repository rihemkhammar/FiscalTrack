import pickle
import pandas as pd
from pathlib import Path

MERGED_PATH = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\processed\GROUPE_LANDOR\LANDOR_2014_merged.pkl")
EXPORT_PATH = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\exports\GROUPE_LANDOR\LANDOR_2014_key_metrics.xlsx")

# Ensure export directory exists
EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(MERGED_PATH, "rb") as f:
    data = pickle.load(f)

# Get the first context table
df = data["context"][0]

# Promote first row to headers
df.columns = df.iloc[0].astype(str).str.strip()
df = df.drop(0).reset_index(drop=True)
df.rename(columns={df.columns[0]: "Label"}, inplace=True)

# Extract TOTALDESACTIFS row
row = df[df["Label"].astype(str).str.contains("TOTALDESACTIFS", na=False)]
value_2014 = row["31-déc.-2014"].values[-1]  # last occurrence = grand total
value_2013 = row["31-déc.-2013"].values[-1]

# Build a clean DataFrame for export
metrics = pd.DataFrame({
    "Metric": ["TOTALDESACTIFS"],
    "2014": [value_2014],
    "2013": [value_2013]
})

# Export to Excel
metrics.to_excel(EXPORT_PATH, index=False)

print(f"Key metrics exported to: {EXPORT_PATH}")
