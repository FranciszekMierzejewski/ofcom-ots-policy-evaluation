from pathlib import Path
import pandas as pd
import numpy as np

RAW_FILE_PATH = Path("data/raw/2023/2023_data.csv")
CLEANED_FILE_PATH = Path("data/processed/2023/data.csv")

REQUIRED_COLUMNS = [
    "IOBS",
    "P_METHOD_TYPE",
    "OS1B",
    "S4",
    "S5",
    "QS6A",
    "QS6B",
    "QS6C",
    "QS6D",
    "QS6E",
    "QS7A",
    "QS7B",
    "QS7C",
    "QS7D",
    "QS7E",
    "QS7F",
    "QS7G",
    "QS7H",
    "QS7I",
    "QLLSUMA",
    "QBBSUMA",
    "QMPSUMA",
    "QPTVSUMA",
    "C6",
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
    "WT1"
]


def clean_numeric(series: pd.Series):
    return pd.to_numeric(series, errors="coerce")


def check_binary(df, columns):
    non_binary = {}

    for col in columns:
        values = set(clean_numeric(df[col]).dropna().unique().tolist()) # drop NaN and dupes
        invalid = values - {0, 1}

        if invalid: # if non-empty, hence eval truthy, then non-binary left
            non_binary[col] = sorted(invalid) # in order

    if non_binary:
        raise ValueError(
            "Found unexpected variables outside of 0/1: \n"
            + str(non_binary)
        )



