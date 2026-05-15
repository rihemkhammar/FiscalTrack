import pdfplumber
import pandas as pd
import pickle
from pathlib import Path

# 1️⃣ Chemin des PDF source
PDF_DIR = Path(r"C:\Users\mariem\workspace\FiscalTrack\input\GROUPE_LANDOR")

# 2️⃣ Chemin où sauvegarder les tables extraites
OUTPUT_DIR = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\raw\GROUPE_LANDOR")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("DEBUG — PDF_DIR =", PDF_DIR)
print("DEBUG — Exists:", PDF_DIR.exists())
print("DEBUG — PDFs found:", list(PDF_DIR.glob("*.pdf")))

def extract_tables_from_pdf(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for t in page.extract_tables():
                df = pd.DataFrame(t)
                tables.append(df)
    return tables


def extract_all_pdfs():
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    print("DEBUG — Extracting these files:", pdf_files)

    for pdf in pdf_files:
        print(f"Extracting: {pdf.name}")
        tables = extract_tables_from_pdf(pdf)

        # Sauvegarde dans data/raw/
        out_path = OUTPUT_DIR / f"{pdf.stem}_raw.pkl"
        with open(out_path, "wb") as f:
            pickle.dump(tables, f)

        print(f"Saved raw extraction:", out_path)


if __name__ == "__main__":
    extract_all_pdfs()
