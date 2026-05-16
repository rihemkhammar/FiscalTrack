import pandas as pd

def clean_number(x):
    if not isinstance(x, str):
        return None
    x = x.replace(" ", "").replace("\u202f", "")
    x = x.replace("(", "-").replace(")", "")
    x = x.replace("<", "-").replace(">", "")
    try:
        return float(x)
    except:
        return None


def extract_financials_from_tables(tables):
    data = {
        "year": None,

        # Actifs non courants
        "immobilisations_incorporelles_brut": None,
        "amortissements_incorporelles": None,
        "immobilisations_incorporelles_net": None,
        "immobilisations_corporelles_brut": None,
        "amortissements_corporelles": None,
        "immobilisations_corporelles_net": None,
        "immobilisations_financieres_brut": None,
        "provisions_immobilisations_financieres": None,
        "immobilisations_financieres_net": None,
        "ecarts_acquisition_net": None,
        "total_actifs_immobilises": None,
        "actif_impot_differe": None,
        "autres_actifs_non_courants": None,
        "total_actifs_non_courants": None,

        # Actifs courants
        "stocks_brut": None,
        "provisions_stocks": None,
        "stocks_net": None,
        "clients_brut": None,

        # Capitaux propres
        "resultat_consolide": None,
        "capitaux_propres_avant_resultat": None,
        "capitaux_propres_total": None,
        "capitaux_propres_groupe": None,
        "interets_minorites_reserves": None,
        "interets_minorites_resultat": None,
        "interets_minorites_autres": None,
        "interets_minorites_total": None,
        "capitaux_propres_groupe_minorites": None,

        # Passifs non courants
        "emprunts_dettes_assimilees": None,
        "provisions_risques_charges": None,
        "total_passifs_non_courants": None,

        # Passifs courants
        "fournisseurs_comptes_rattaches": None,
        "autres_passifs_courants": None,
        "concours_bancaires_passifs_financiers": None,
        "total_passifs_courants": None,
        "total_passifs": None,
        "total_capitaux_propres_passifs": None,
    }

    # -------------------------
    # YEAR DETECTION
    # -------------------------
    for df in tables:
        text = " ".join(df.astype(str).fillna("").values.flatten())
        for year in range(2000, 2035):
            if str(year) in text:
                data["year"] = year
                break

    # -------------------------
    # KPI EXTRACTION
    # -------------------------
    for df in tables:
        df = df.fillna("").astype(str)

        def extract_value(keyword, key_name):
            mask = df[0].str.contains(keyword, case=False)
            if mask.any():
                row = df.loc[mask].iloc[0]
                for col in reversed(df.columns):
                    val = clean_number(row[col])
                    if val is not None:
                        data[key_name] = val
                        break

        # Actifs non courants
        extract_value("Immobilisations incorporelles.*brut", "immobilisations_incorporelles_brut")
        extract_value("Amortissements.*incorporelles", "amortissements_incorporelles")
        extract_value("Immobilisations incorporelles.*net", "immobilisations_incorporelles_net")
        extract_value("Immobilisations corporelles.*brut", "immobilisations_corporelles_brut")
        extract_value("Amortissements.*corporelles", "amortissements_corporelles")
        extract_value("Immobilisations corporelles.*net", "immobilisations_corporelles_net")
        extract_value("Immobilisations financières.*brut", "immobilisations_financieres_brut")
        extract_value("Provisions.*immobilisations financières", "provisions_immobilisations_financieres")
        extract_value("Immobilisations financières.*net", "immobilisations_financieres_net")
        extract_value("Ecarts d'acquisition.*net", "ecarts_acquisition_net")
        extract_value("Total.*actifs immobilisés", "total_actifs_immobilises")
        extract_value("Actif.*impôt différé", "actif_impot_differe")
        extract_value("Autres actifs non courants", "autres_actifs_non_courants")
        extract_value("Total.*actifs non courants", "total_actifs_non_courants")

        # Actifs courants
        extract_value("Stocks.*brut", "stocks_brut")
        extract_value("Provisions.*stocks", "provisions_stocks")
        extract_value("Stocks.*net", "stocks_net")
        extract_value("Clients.*brut", "clients_brut")

        # Capitaux propres
        extract_value("Résultat consolidé", "resultat_consolide")
        extract_value("Total des capitaux propres avant résultat", "capitaux_propres_avant_resultat")
        extract_value("Total des capitaux propres$", "capitaux_propres_total")
        extract_value("Total des capitaux propres Groupe", "capitaux_propres_groupe")
        extract_value("Intérêts des minoritaires.*reserves", "interets_minorites_reserves")
        extract_value("Intérêts des minoritaires.*résultat", "interets_minorites_resultat")
        extract_value("Intérêts des minoritaires.*autres", "interets_minorites_autres")
        extract_value("Total des intérêts des minoritaires", "interets_minorites_total")
        extract_value("Total des capitaux propres groupe et minoritaires", "capitaux_propres_groupe_minorites")

        # Passifs non courants
        extract_value("Emprunts.*dettes assimilées", "emprunts_dettes_assimilees")
        extract_value("Provisions.*risques.*charges", "provisions_risques_charges")
        extract_value("Total.*passifs non courants", "total_passifs_non_courants")

        # Passifs courants
        extract_value("Fournisseurs.*comptes rattachés", "fournisseurs_comptes_rattaches")
        extract_value("Autres passifs courants", "autres_passifs_courants")
        extract_value("Concours bancaires.*passifs financiers", "concours_bancaires_passifs_financiers")
        extract_value("Total.*passifs courants", "total_passifs_courants")
        extract_value("Total.*passifs$", "total_passifs")
        extract_value("Total des capitaux propres et des passifs", "total_capitaux_propres_passifs")

    return data
