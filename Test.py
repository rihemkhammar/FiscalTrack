import run_tabula

tables = tabula.read_pdf("input/GROUPE_DELICE/DELICE_2014.pdf",
                          pages="all",
                          multiple_tables=True,
                          silent=True)

print(f"{len(tables)} tableaux trouvés")

# Voir les 3 premiers
for i, df in enumerate(tables[:3]):
    print(f"\n--- Table {i} : {df.shape} ---")
    print(df.head())