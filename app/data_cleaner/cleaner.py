from pathlib import Path
import pandas as pd

# Year-specific rules for LANDOR
YEAR_RULES_LANDOR = {
    2020: {"sheets": ["2020_T00", "2020_T02", "2020_T03", "2020_T04"], "cols": [0, 2]},
    2021: {"sheets": ["2021_T00", "2021_T01", "2021_T02"],
           "cols_map": {"2021_T00": [0, 1], "2021_T01": [0, 2], "2021_T02": [0, 2]}},
    2022: {"sheets": ["2022_T00", "2022_T0A", "2022_T02", "2022_T03", "2022_T04"], "cols": [0, 2]},
    2023: {"skip": True},
    2024: {"sheets": ["2024_T00", "2024_T01", "2024_T02", "2024_T03"], "cols": [0, 2, 3]},
}

# Year-specific rules for DELICE
YEAR_RULES_DELICE = {
    2021: {
        "sheets": ["2021_T00", "2021_T01", "2021_T02", "2021_T03"],
        "cols_map": {
            "2021_T00": [0, 1, 2],
            "2021_T01": [0, 2, 3],
            "2021_T02": [0, 1, 3],
            "2021_T03": [0, 2, 3],
        },
    },
    2022: {"sheets": ["2022_T00", "2022_T09"], "cols": [0, 2]},
    2023: {
        "sheets": ["2023_T00", "2023_T01", "2023_T02", "2023_T03", "2023_T10"],
        "cols_map": {
            "2023_T00": [0, 2],
            "2023_T01": [0, 2],
            "2023_T02": [0, 2],
            "2023_T03": [0, 1],
            "2023_T10": [0, 2],
        },
    },
    2024: {"sheets": ["2024_T00"], "cols": [0, 2]},
}

def apply_rules(xls, year, rules):
    """Apply year-specific sheet/column rules."""
    if rules.get("skip"):
        print(f"⏭️ Skipping {year}")
        return None

    frames = []
    for sheet in rules["sheets"]:
        if sheet not in xls.sheet_names:
            print(f"⚠️ Sheet {sheet} not found for {year}")
            continue

        df = pd.read_excel(xls, sheet_name=sheet)
        df = df.dropna(how="all", axis=0).dropna(how="all", axis=1)

        if "cols_map" in rules:
            cols = rules["cols_map"].get(sheet, [])
        else:
            cols = rules["cols"]

        cols = [c for c in cols if c < df.shape[1]]
        if not cols:
            continue

        df = df.iloc[:, cols]
        df.columns = ["Label"] + [f"Value{i}" for i in range(1, len(cols))]
        frames.append(df)

    if not frames:
        return None
    return pd.concat(frames, axis=0, ignore_index=True)

def generic_clean(xls, year):
    """Generic cleaner: first + third columns from first two sheets."""
    year_sheets = [s for s in xls.sheet_names if s.startswith(str(year))]
    if len(year_sheets) < 2:
        print(f"⚠️ Not enough sheets for {year}")
        return None

    table1 = pd.read_excel(xls, sheet_name=year_sheets[0])
    table2 = pd.read_excel(xls, sheet_name=year_sheets[1])

    table1 = table1.dropna(how="all", axis=0).dropna(how="all", axis=1)
    table2 = table2.dropna(how="all", axis=0).dropna(how="all", axis=1)

    def keep_first_third(df):
        if df.shape[1] >= 3:
            df = df.iloc[:, [0, 2]]
        elif df.shape[1] >= 2:
            df = df.iloc[:, [0, 1]]
        else:
            return None
        df.columns = ["Label", "Value"]
        return df

    table1 = keep_first_third(table1)
    table2 = keep_first_third(table2)

    frames = [t for t in [table1, table2] if t is not None]
    if not frames:
        return None

    return pd.concat(frames, axis=0, ignore_index=True)

def clean_excel(input_path: Path, year: int, company: str = None):
    """
    Load an Excel file for a given year.
    - LANDOR 2020–2024: apply YEAR_RULES_LANDOR
    - DELICE 2021–2024: apply YEAR_RULES_DELICE
    - Otherwise: use generic cleaner
    """
    xls = pd.ExcelFile(input_path)

    if company == "GROUPE_LANDOR" and year in YEAR_RULES_LANDOR:
        return apply_rules(xls, year, YEAR_RULES_LANDOR[year])

    if company == "GROUPE_DELICE" and year in YEAR_RULES_DELICE:
        return apply_rules(xls, year, YEAR_RULES_DELICE[year])

    return generic_clean(xls, year)
