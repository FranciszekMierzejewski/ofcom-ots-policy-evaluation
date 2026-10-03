from pathlib import Path
import pandas as pd


RAW_FILE_PATH = Path("data/raw/2023/2023_data.csv")
OUTPUT_FILE_PATH = Path("data/processed/2023/data.csv")

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

SEG_COLUMNS = {
    "QS6A": "AB",
    "QS6B": "C1",
    "QS6C": "C2",
    "QS6D": "DE"
}

EMPLOYMENT_COLUMNS = {
    "QS7A": "full_time",
    "QS7B": "part_time",
    "QS7C": "unemployed",
    "QS7D": "student",
    "QS7E": "home_family",
    "QS7F": "retired",
    "QS7G": "other"
}

SWITCH_COLUMNS = {
    "QLLSUMA": "switched_landline_12m",
    "QBBSUMA": "switched_broadband_12m",
    "QMPSUMA": "switched_mobile_12m",
    "QPTVSUMA": "switched_paytv_12m"
}

DISABILITY_CONDITION_COLUMNS = [
    "C1A",
    "C1B",
    "C1C",
    "C1D",
    "C1E",
    "C1F",
    "C1G",
    "C1H",
    "C1I"
]


def check_required_columns(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns] #iter over list and verify
    if missing:
        raise ValueError(f"2023 missing required columns: {missing}")


def check_unique_ids(df: pd.DataFrame) -> None:
    if df["IOBS"].isna().any(): # must be non-null
        raise ValueError("2023 contains missing respondent IDs.")
    if df["IOBS"].duplicated().any(): # must be unique
        raise ValueError("2023 contains duplicate respondent IDs.")


def check_binary_columns(df: pd.DataFrame, columns: list[str]) -> None:
    non_binary = {}
    for column in columns:
        values = set(df[column].dropna().unique()) # all unique val
        unexpected = values.difference({0, 1}) # return any value not in set {0,1}
        if unexpected:
            non_binary[column] = sorted(unexpected)

    if non_binary:
        raise ValueError(f"2023 contains non-binary values: {non_binary}")


def derive_seg(df: pd.DataFrame) -> pd.Series:
    check_binary_columns(df, list(SEG_COLUMNS))

    selected_count = df[list(SEG_COLUMNS)].sum(axis=1) # only 1 SEG group allowed, sum row

    if (selected_count > 1).any(): 
        raise ValueError("2023 contains respondents assigned to multiple SEG categories.")

    seg = pd.Series(pd.NA, index=df.index, dtype="string") # empty series with same index

    for col, label in SEG_COLUMNS.items(): # loop through every dict pair 
        seg.loc[df[col].eq(1)] = label # assign label to where mask set as True

    return seg


def derive_age_group(df: pd.DataFrame) -> pd.Series:
    valid_codes = {1, 2, 3, 4, 5, 6, 7, 8}
    observed_codes = set(df["S4"].dropna().unique())
    unexpected_codes = observed_codes.difference(valid_codes) # get diff/unx code

    if unexpected_codes:
        raise ValueError(f"2023 S4 contains unexpected codes: {sorted(unexpected_codes)}")

    age_group = pd.Series(pd.NA, index=df.index, dtype="string")

    age_group.loc[df["S4"].isin([1, 2])] = "16-34" # 3 age groups
    age_group.loc[df["S4"].isin([3, 4])] = "35-54"
    age_group.loc[df["S4"].isin([5, 6, 7])] = "55+"

    return age_group


def derive_employment_status(df: pd.DataFrame) -> pd.Series:
    check_binary_columns(df, list(EMPLOYMENT_COLUMNS))

    selected_count = df[list(EMPLOYMENT_COLUMNS)].sum(axis=1)

    if (selected_count > 1).any():
        raise ValueError("2023 contains respondents assigned to multiple employment categories.")

    employment_status = pd.Series(pd.NA, index=df.index, dtype="string")

    for source_column, label in EMPLOYMENT_COLUMNS.items():
        employment_status.loc[df[source_column].eq(1)] = label

    return employment_status


def derive_disability_flag(df: pd.DataFrame) -> pd.Series:
    check_binary_columns(
        df,
        DISABILITY_CONDITION_COLUMNS + ["C1J", "C1K", "C1L"],
    )

    has_condition = df[DISABILITY_CONDITION_COLUMNS].eq(1).any(axis=1)
    nothing_selected = df["C1J"].eq(1)
    declined = df["C1K"].eq(1)
    unknown = df["C1L"].eq(1)

    # selected options that contradict
    if (has_condition & nothing_selected).any():
        raise ValueError("2023 contains respondents selecting both a condition and 'Nothing'.")

    if (has_condition & (declined | unknown)).any():
        raise ValueError("2023 contains respondents selecting a condition and a non-response category.")

    if (nothing_selected & (declined | unknown)).any():
        raise ValueError("2023 contains respondents selecting 'Nothing' and a non-response category.")

    disability_flag = pd.Series(pd.NA, index=df.index, dtype="Int64")

    disability_flag.loc[has_condition] = 1
    disability_flag.loc[nothing_selected] = 0

    return disability_flag


def main() -> None:
    df = pd.read_csv(RAW_FILE_PATH, low_memory=False)

    print(f"Loaded 2023: {len(df):,} rows, {len(df.columns):,} columns")

    check_required_columns(df)
    check_unique_ids(df)

    check_binary_columns(df, list(SWITCH_COLUMNS))

    seg = derive_seg(df)
    age_group = derive_age_group(df)
    employment_status = derive_employment_status(df)
    disability_flag = derive_disability_flag(df)

    clean = pd.DataFrame(
        {
            "respondent_id": df["IOBS"],
            "wave": 2023,
            "post_ots": 0,
            "survey_weight": df["WT1"],
            "survey_method": df["P_METHOD_TYPE"],
            "switched_landline_12m": df["QLLSUMA"],
            "switched_broadband_12m": df["QBBSUMA"],
            "switched_mobile_12m": df["QMPSUMA"],
            "switched_paytv_12m": df["QPTVSUMA"],
            "age_group": age_group,
            "gender": df["S5"],
            "seg": seg,
            "employment_status": employment_status,
            "region": df["OS1B"],
            "income_band": df["C6"],
            "disability_flag": disability_flag,
        }
    )

    expected_columns = [
        "respondent_id",
        "wave",
        "post_ots",
        "survey_weight",
        "survey_method",
        "switched_landline_12m",
        "switched_broadband_12m",
        "switched_mobile_12m",
        "switched_paytv_12m",
        "age_group",
        "gender",
        "seg",
        "employment_status",
        "region",
        "income_band",
        "disability_flag",
    ]

    if list(clean.columns) != expected_columns:
        raise ValueError("2023 harmonised dataset has an unexpected column order.")

    if clean["survey_weight"].isna().any():
        raise ValueError("2023 contains missing survey weights.")

    if (clean["survey_weight"] <= 0).any():
        raise ValueError("2023 contains non-positive survey weights.")

    OUTPUT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True) 
    clean.to_csv(OUTPUT_FILE_PATH, index=False) # extract cleaned file to data/processed/2023/

    print(f"Saved 2023 harmonised data to {OUTPUT_FILE_PATH}")
    print(f"Final shape: {clean.shape[0]:,} rows x {clean.shape[1]:,} columns")


if __name__ == "__main__":
    main()