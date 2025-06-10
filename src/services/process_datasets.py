from pathlib import Path
import pandas as pd
import numpy as np

from src.config import settings

def download_and_save_titanic(output_dir):
    data = pd.read_csv(settings.DATASET_URL)
    
    output_path = f"{output_dir}/titanic.csv"
    data.to_csv(output_path, index=False)
    print(f"Download Data | Titanic dataset saved to {output_path}")
    
    return output_path

def add_noise(df: pd.DataFrame, noise_level: float = 0.01) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "Survived" in numeric_cols:
        numeric_cols.remove("Survived")
    noise = np.random.normal(0, noise_level, size=df[numeric_cols].shape)
    df.loc[:, numeric_cols] += noise
    return df

def remove_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=["Name"])

def bin_age(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0, 12, 18, 40, 60, np.inf]
    labels = ['child', 'teen', 'adult', 'senior', 'elder']
    df = df.copy()
    df['Age_binned'] = pd.cut(df['Age'], bins=bins, labels=labels)
    return df

def clean_missing(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()

def save_dataset(df: pd.DataFrame, output_path: str) -> None:
    df.columns = df.columns.str.replace(" ", "_")
    
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")

def generate_datasets(dataset_path: Path = settings.DATA_DIR / "titanic.csv") -> None:
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"Файл {dataset_path} не найден.")
        exit(1)

    save_dataset(df, settings.DATA_DIR / "raw" / "titanic_original.csv")

    df_noise = add_noise(df)
    df_noise = clean_missing(df_noise)
    save_dataset(df_noise, settings.DATA_DIR / "raw" / "titanic_noise.csv")
    
    df_noname = remove_names(df)
    save_dataset(df_noname, settings.DATA_DIR / "raw" / "titanic_noname.csv")

    df_binned = bin_age(df)
    save_dataset(df_binned, settings.DATA_DIR / "raw" / "titanic_binned.csv")
    
if __name__ == "__main__":
    download_and_save_titanic(settings.DATA_DIR)

    generate_datasets(settings.DATA_DIR / "titanic.csv")