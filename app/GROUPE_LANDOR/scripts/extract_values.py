import pickle
import pandas as pd
from pathlib import Path

# Charger le fichier pkl
pkl_path = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\raw\GROUPE_LANDOR\LANDOR_2014_raw.pkl")

with open(pkl_path, "rb") as f:
    tables = pickle.load(f)

# Liste des intitulés recherchés
valeurs_recherchees = [
    "Immobilisations incorporelles (brut)",
    "Amortissements des immobilisations incorporelles",
    "Immobilisations incorporelles nettes",
    "Immobilisations corporelles (brut)",
    "Amortissements des immobilisations corporelles",
    "Immobilisations corporelles nettes",
    "Immobilisations financières (brut)",
    "Provisions sur immobilisations financières",
    "Immobilisations financières nettes",
    "Ecarts d'acquisition nets",
    "Total des actifs immobilisés",
    "Actif d'impôt différé",
    "Autres actifs non courants",
    "Total des actifs non courants",
    "Stocks (brut)",
    "Provisions pour dépréciation des stocks",
    "Stocks nets",
    "Clients et comptes rattachés (brut)",
    "Résultat consolidé",
    "Total des capitaux propres avant résultat de l'exercice",
    "Total des capitaux propres",
    "Total des capitaux propres Groupe",
    "Intérêts des minoritaires dans les reserves",
    "Intérêts des minoritaires dans le résultat",
    "Intérêts des minoritaires dans les autres capitaux propres",
    "Total des intérêts des minoritaires",
    "Total des capitaux propres groupe et minoritaires",
    "Emprunts et dettes assimilées",
    "Provisions pour risques et charges",
    "Total des passifs non courants",
    "Fournisseurs et comptes rattachés",
    "Autres passifs courants",
    "Concours bancaires et autres passifs financiers",
    "Total des passifs courants",
    "Total des passifs",
    "Total des capitaux propres et des passifs"
]

# Extraction
resultats = {}
for df in tables:
    for valeur in valeurs_recherchees:
        # Cherche la ligne dont la première colonne contient l'intitulé
        if df.shape[1] > 1:  # Vérifie qu'il y a au moins 2 colonnes
            ligne = df[df.iloc[:, 0].astype(str).str.contains(valeur, case=False, na=False, regex=False)]

            if not ligne.empty:
                resultats[valeur] = ligne.iloc[0,1]  # valeur supposée en 2ème colonne

# Affichage
print("📊 Résultats 2014")
for k,v in resultats.items():
    print(f"{k} : {v}")

# Export vers Excel
output_dir = Path(r"C:\Users\mariem\workspace\FiscalTrack\data\processed\LANDOR")
output_dir.mkdir(parents=True, exist_ok=True)  # crée le dossier si nécessaire

df_out = pd.DataFrame.from_dict(resultats, orient="index", columns=["Valeur 2014"])
df_out.to_excel(output_dir / "resultats_2014.xlsx")
