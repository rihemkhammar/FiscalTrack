import pickle
from pathlib import Path
from cleaner import extract_financials_from_tables

pkl = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\raw\GROUPE_LANDOR\LANDOR_2015_raw.pkl")

with open(pkl, "rb") as f:
    tables = pickle.load(f)

result = extract_financials_from_tables(tables)
print(result)
