from pathlib import Path
import pandas as pd

FILE_2023 = Path("data/processed/2023/data.csv")
FILE_2025 = Path("data/processed/2025/data.csv")
OUTPUT_FILE_PATH = Path("data/processed/merged/data.csv")

EXPECTED_COLUMNS = [
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
    "disability_flag"
]

OUTCOME_COLUMNS = [
    "switched_landline_12m",
    "switched_broadband_12m",
    "switched_mobile_12m",
    "switched_paytv_12m"
]


def validate_wave(df: pd.DataFrame, wave: int, post_ots: int) -> None:
    if list(df.columns) != EXPECTED_COLUMNS: # expects df to be same as expected
        raise ValueError(f"{wave} dataset does not match the harmonised schema.")

    # specifs for debugging
    if not (df["wave"] == wave).all():
        raise ValueError(f"{wave} dataset contains incorrect wave values.")

    if not (df["post_ots"] == post_ots).all():
        raise ValueError(f"{wave} dataset contains incorrect post_ots values.")

    if df["respondent_id"].isna().any():
        raise ValueError(f"{wave} dataset contains missing respondent IDs.")

    if df["respondent_id"].duplicated().any():
        raise ValueError(f"{wave} dataset contains duplicate respondent IDs.")

    if df["survey_weight"].isna().any():
        raise ValueError(f"{wave} dataset contains missing survey weights.")

    if (df["survey_weight"] <= 0).any():
        raise ValueError(f"{wave} dataset contains non-positive survey weights.")

    for col in OUTCOME_COLUMNS:
        values = set(df[col].dropna().unique())
        unexpected = values.difference({0, 1})

        if unexpected:
            raise ValueError(f"{wave} {col} contains unexpected values: {sorted(unexpected)}")


def main() -> None:
    df_2023 = pd.read_csv(FILE_2023, low_memory=False)
    df_2025 = pd.read_csv(FILE_2025, low_memory=False)

    print(f"Loaded 2023: {len(df_2023):,} rows")
    print(f"Loaded 2025: {len(df_2025):,} rows")

    validate_wave(df_2023, 2023, 0)
    validate_wave(df_2025, 2025, 1)

    df = pd.concat( # merge together
        [df_2023, df_2025],
        ignore_index=True,
    )

    df["wave_respondent_id"] = (
        df["wave"].astype(str) # e.g. 2023_id
        + "_"
        + df["respondent_id"].astype(str)
    )

    if df["wave_respondent_id"].duplicated().any():
        raise ValueError("Merged dataset contains duplicate wave-respondent IDs.")

    expected_row_count = len(df_2023) + len(df_2025)

    if len(df) != expected_row_count:
        raise ValueError("Merged row count does not equal the sum of the two input datasets.")

    OUTPUT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE_PATH, index=False)

    print(f"Saved merged dataset to {OUTPUT_FILE_PATH}")
    print(f"Final shape: {df.shape[0]:,} rows x {df.shape[1]:,} columns")
    print(df["wave"].value_counts().sort_index())


if __name__ == "__main__":
    main()