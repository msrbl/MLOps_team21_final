from pathlib import Path

ROOT_DIR   = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATASET_PATH = DATA_DIR / "winequality-red.csv"

PROC_DATA_DIR = DATA_DIR / "processed"
PROC_DATA_DIR.mkdir(exist_ok=True)

MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR/ "model.pkl"

REPORT_DIR = ROOT_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

DATASET_URL = "https://archive.ics.uci.edu/static/public/186/wine+quality.zip"