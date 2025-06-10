import logging

import pandas as pd
import numpy as np
import pandas as pd

from src.config import settings

logger = logging.getLogger('app')

def download_and_save_titanic(output_dir):
    data = pd.read_csv(settings.DATASET_URL)
    
    output_path = f"{output_dir}/titanic.csv"
    data.to_csv(output_path, index=False)
    logger.info(f"Download Data | Titanic dataset saved to {output_path}")
    
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

def generate_datasets(dataset_path: str = settings.DATA_DIR / "titanic.csv") -> None:
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"Файл {dataset_path} не найден.")
        exit(1)

    df.to_csv(settings.DATA_DIR / "raw" / "titanic_original.csv", index=False)

    df_noise = add_noise(df)
    df_noise = clean_missing(df_noise)
    df_noise.to_csv(settings.DATA_DIR / "raw" / "titanic_noise.csv", index=False)

    df_noname = remove_names(df)
    df_noname.to_csv(settings.DATA_DIR / "raw" / "titanic_noname.csv", index=False)

    df_binned = bin_age(df)
    df_binned.to_csv(settings.DATA_DIR / "raw" / "titanic_binned.csv", index=False)
    
def main():
    download_and_save_titanic(settings.DATA_DIR)

    generate_datasets(settings.DATA_DIR / "titanic.csv")