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
        "revenue": None,
        "net_income": None,
        "total_assets": None,
        "total_liabilities": None,
        "equity": None,
        "cash_end": None
    }

    # ---------------------------------------------------------
    # 1) YEAR DETECTION (robust: scans ALL text in ALL tables)
    # ---------------------------------------------------------
    for df in tables:
        text = " ".join(df.astype(str).fillna("").values.flatten())
        for year in range(2000, 2035):
            if str(year) in text:
                data["year"] = year
                break

    # ---------------------------------------------------------
    # 2) KPI EXTRACTION (adapted to your actual PKL structure)
    # ---------------------------------------------------------
    for df in tables:
        df = df.fillna("").astype(str)

        # -------------------------
        # NET INCOME
        # -------------------------
        mask = df[0].str.contains("Résultat Net", case=False)
        if mask.any():
            row = df.loc[mask].iloc[0]
            # take the last numeric column
            for col in reversed(df.columns):
                val = clean_number(row[col])
                if val is not None:
                    data["net_income"] = val
                    break

        # -------------------------
        # TOTAL ASSETS
        # -------------------------
        mask = df[0].str.contains("ACTIFS", case=False)
        if mask.any():
            # search for a row containing "Total"
            total_mask = df[0].str.contains("Total", case=False)
            if total_mask.any():
                row = df.loc[total_mask].iloc[-1]
                for col in reversed(df.columns):
                    val = clean_number(row[col])
                    if val is not None:
                        data["total_assets"] = val
                        break

        # -------------------------
        # TOTAL LIABILITIES
        # -------------------------
        mask = df[0].str.contains("PASSIFS", case=False)
        if mask.any():
            total_mask = df[0].str.contains("Total", case=False)
            if total_mask.any():
                row = df.loc[total_mask].iloc[-1]
                for col in reversed(df.columns):
                    val = clean_number(row[col])
                    if val is not None:
                        data["total_liabilities"] = val
                        break

        # -------------------------
        # EQUITY
        # -------------------------
        mask = df[0].str.contains("capitaux propres", case=False)
        if mask.any():
            row = df.loc[mask].iloc[0]
            for col in reversed(df.columns):
                val = clean_number(row[col])
                if val is not None:
                    data["equity"] = val
                    break

        # -------------------------
        # CASH AT END
        # -------------------------
        mask = df[0].str.contains("Trésorerie à la clôture", case=False)
        if mask.any():
            row = df.loc[mask].iloc[0]
            for col in reversed(df.columns):
                val = clean_number(row[col])
                if val is not None:
                    data["cash_end"] = val
                    break

        # -------------------------
        # REVENUE (fallback)
        # -------------------------
        mask = df[0].str.contains("Chiffre d'affaires|Revenus", case=False)
        if mask.any():
            row = df.loc[mask].iloc[0]
            for col in reversed(df.columns):
                val = clean_number(row[col])
                if val is not None:
                    data["revenue"] = val
                    break

    return data
