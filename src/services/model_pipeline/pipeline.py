from src.services.model_pipeline.test_model import proceed_testing
from src.services.model_pipeline.preprocess_data import preprocess_dataset
from src.services.model_pipeline.train_model import train_and_save_model
from src.config import settings


def run_pipeline(dataset_path: str) -> None:
    train, test = preprocess_dataset(dataset_path)

    model_path = train_and_save_model(train[0], train[1])

    metrics = proceed_testing(test[0], test[1], model_path)


if __name__ == "__main__":
    dataset_path = settings.DATA_DIR / "raw" / "titanic_binned.csv"
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")

    run_pipeline(str(dataset_path))
