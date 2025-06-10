from pydantic_settings import BaseSettings
from typing import ClassVar
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "MLOps FastAPI Project"
    
    ROOT_DIR: ClassVar[Path] = Path(__file__).resolve().parents[1]

    DATA_DIR: ClassVar[Path] = ROOT_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)

    PROC_DATA_DIR: ClassVar[Path] = DATA_DIR / "processed"
    PROC_DATA_DIR.mkdir(exist_ok=True)

    MODEL_DIR: ClassVar[Path] = ROOT_DIR / "models"
    MODEL_DIR.mkdir(exist_ok=True)

    REPORT_DIR: ClassVar[Path] = ROOT_DIR / "reports"
    REPORT_DIR.mkdir(exist_ok=True)
    
    DATASET_URL: str = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    
settings = Settings()