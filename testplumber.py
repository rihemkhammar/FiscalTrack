import pdfplumber
import pandas as pd

pdf_path = "input/GROUPE_DELICE/DELICE_2014.pdf"

tables = []

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        extracted_tables = page.extract_tables()

        for table in extracted_tables:
            df = pd.DataFrame(table)
            tables.append(df)

print(f"{len(tables)} tableaux trouvés")

# Afficher les 3 premiers tableaux
for i, df in enumerate(tables[:3]):
    print(f"\n--- Table {i} : {df.shape} ---")
    print(df.head())