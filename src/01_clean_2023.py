from pathlib import Path
import pandas as pd
import numpy as np


RAW_FILE_PATH = Path("data/raw/2023/2023_data.csv")
CLEANED_FILE_PATH = Path("data/processed/2023/data.csv")

df = pd.read_csv("data\\raw\\2023\\2023_data.csv")

REQUIRED_COLUMNS = [
    # Identification / Survey Design
    "IOBS",
    "P_METHOD_TYPE",
    "OS1B",
    "S4",
    "S5",

    # Social Economic Group
    "QS6A",
    "QS6B",
    "QS6C",
    "QS6D",
    "QS6E",

    # Employment
    "QS7A",
    "QS7B",
    "QS7C",
    "QS7D",
    "QS7E",
    "QS7F",
    "QS7G",
    "QS7H",
    "QS7I",

    # Switching outcomes
    "QLLSUMA",
    "QBBSUMA",
    "QMPSUMA",
    "QPTVSUMA",

    # Income
    "C6",

    # Disability
    "C1A",
    "C1B",
    "C1C",
    "C1D",
    "C1E",
    "C1F",
    "C1G",
    "C1H",
    "C1I",
    "C1J",
    "C1K",
    "C1L",

    # Weight
    "WT1"
]

missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

if missing_columns:
    for col in missing_columns:
        print(f"{col}")

    raise ValueError(f"{len(missing_columns)} required columns are missing")

print(f"Number of rows: {df.shape[0]:,}\n Number of columns: {df.shape[1]:,}") # comma seperated


# Dupe checks

print(f"ID data type: {df['IOBS'].dtype}")
print(f"Missing IDs: {df['IOBS'].isna().sum():,}")
print(f"Duplicate IDs: {df['IOBS'].duplicated().sum():,}")
print(f"Unique IDs: {df['IOBS'].nunique():,}")

print(df.dtypes)

"""
def clean_numeric(series: pd.Series):
    return pd.to_numeric(series, errors="coerce")


def check_binary(df, columns):
    non_binary = {}

    for col in columns:
        values = set(clean_numeric(df[col]).dropna().unique().tolist()) # drop NaN and dupes
        invalid = values - {0, 1}

        if invalid: # if non-emptyt, hence eval truthy, then non-binary left
            non_binary[col] = sorted(invalid) # in order

    if non_binary:
        raise ValueError(
            "Found unexpected variables outside of 0/1: \n"
            + str(non_binary)
        )


def recode_switch(variable: pd.Series) -> pd.Series:
    
    #switched_landline_12m/switched_broadband_12m/switched_mobile_12m/switched_paytv_12m
    #QLLSUMA/QBBSUMA/QMPSUMA/QPTVSUMA:
    
    cleaned = clean_numeric(variable)
    res = cleaned.where(cleaned.isin([0, 1]), np.nan) # keep original value where value is 0 or 1, else use NaN

    return res.astype('Int64') # pandas Int64 and not numpy type to allow nullable


def derive_social_economic_group(df: pd.DataFrame):
    social_economic_group_types = ['QS6A', 'QS6B', 'QS6C', 'QS6D']
    values = df[social_economic_group_types].apply(pd.to_numeric, errors = 'coerce')
    pass
"""