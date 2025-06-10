import pandas as pd
import glob
import pytest

csv_files = glob.glob("data/raw/*.csv")
assert csv_files, "No CSV files found in data/raw folder."

required_columns = [
    "Survived",
    "Pclass",
    "Sex",
    "Age",
    "Siblings/Spouses_Aboard",
    "Parents/Children_Aboard",
    "Fare",
]


@pytest.mark.parametrize("csv_file", csv_files)
def test_data_quality(csv_file):
    df = pd.read_csv(csv_file)

    assert len(df) > 0, f"Dataset {csv_file} is empty!"

    for col in required_columns:
        assert col in df.columns, f"Missing column '{col}' in file {csv_file}"

    missing_age = df["Age"].isnull().sum()
    assert missing_age < len(df), f"Too many missing 'Age' values in {csv_file}!"


@pytest.mark.parametrize("csv_file", csv_files)
def test_survived_binary(csv_file):
    df = pd.read_csv(csv_file)
    unique_vals = set(df["Survived"].unique())
    assert unique_vals <= {
        0,
        1,
    }, f"Non-binary values in 'Survived' column in {csv_file}: {unique_vals}"


@pytest.mark.parametrize("csv_file", csv_files)
def test_sex_values(csv_file):
    df = pd.read_csv(csv_file)
    allowed = {"male", "female"}
    unique_vals = set(df["Sex"].unique())
    assert (
        unique_vals <= allowed
    ), f"Unexpected values in 'Sex' column in {csv_file}: {unique_vals}"


@pytest.mark.parametrize("csv_file", csv_files)
def test_no_nan_in_required_columns(csv_file):
    df = pd.read_csv(csv_file)
    for col in required_columns:
        assert df[col].isnull().sum() < len(
            df
        ), f"All values missing in column '{col}' in {csv_file}"


@pytest.mark.parametrize("csv_file", csv_files)
def test_age_reasonable_range(csv_file):
    df = pd.read_csv(csv_file)
    ages = df["Age"].dropna()
    assert (
        (ages >= 0) & (ages <= 100)
    ).all(), f"Unreasonable 'Age' values in {csv_file}"


@pytest.mark.parametrize("csv_file", csv_files)
def test_pclass_range(csv_file):
    df = pd.read_csv(csv_file)
    assert (
        df["Pclass"].between(0, 4).all()
    ), f"'Pclass' values out of range in {csv_file}"
