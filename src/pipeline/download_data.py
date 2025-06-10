import logging

import tensorflow_datasets as tfds
import pandas as pd

from src.config import settings

logger = logging.getLogger('app')

def download_and_save_imdb(output_dir):
    data = pd.read_csv(settings.DATASET_URL)
    
    output_path = f"{output_dir}/titanic.csv"
    data.to_csv(output_path, index=False)
    logger.info(f"Download Data | Titanic dataset saved to {output_path}")

if __name__ == "__main__":
    download_and_save_imdb(settings.DATA_DIR / "raw")