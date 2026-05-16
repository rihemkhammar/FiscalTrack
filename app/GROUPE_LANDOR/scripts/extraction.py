import tabula
import pandas as pd
import pickle
from pathlib import Path

PDF_DIR = Path(r"C:\Users\mariem\workspace\FiscalTrack\input\GROUPE_LANDOR")
OUTPUT_DIR = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\processed\GROUPE_LANDOR")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_tables_from_pdf(pdf_path):
    # Extract with lattice (structured tables)
    tables_lattice = tabula.read_pdf(str(pdf_path), pages="all", multiple_tables=True, lattice=True)
    # Extract with stream (narrative + footnotes)
    tables_stream = tabula.read_pdf(str(pdf_path), pages="all", multiple_tables=True, stream=True)
    return tables_lattice, tables_stream

def clean_dataframe(df):
    # Normalize formatting: remove < >, commas, spaces
    df = df.replace({r'[<>, ]':''}, regex=True)
    # Drop empty columns
    df = df.dropna(axis=1, how="all")
    # Forward-fill labels if missing
    df = df.ffill()
    return df

def merge_results(tables_lattice, tables_stream):
    cleaned_lattice = [clean_dataframe(df) for df in tables_lattice]
    cleaned_stream = [clean_dataframe(df) for df in tables_stream]

    # Strategy: lattice for numeric tables, stream for narrative
    merged = {
        "structured": cleaned_lattice,
        "context": cleaned_stream
    }
    return merged

def extract_all_pdfs():
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    for pdf in pdf_files:
        print(f"Extracting: {pdf.name}")
        tables_lattice, tables_stream = extract_tables_from_pdf(pdf)
        merged = merge_results(tables_lattice, tables_stream)

        # Save merged results
        out_path = OUTPUT_DIR / f"{pdf.stem}_merged.pkl"
        with open(out_path, "wb") as f:
            pickle.dump(merged, f)

        print(f"Saved merged extraction:", out_path)

if __name__ == "__main__":
    extract_all_pdfs()
