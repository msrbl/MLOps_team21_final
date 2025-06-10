import pathlib
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from config import PROC_DATA_DIR, MODEL_DIR

def main():
    X_train = pd.read_csv(PROC_DATA_DIR / "X_train.csv")
    y_train = pd.read_csv(PROC_DATA_DIR / "y_train.csv").squeeze()

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    ).fit(X_train, y_train)

    joblib.dump(model, MODEL_DIR / "model.pkl")
    print("Model saved to models/model.pkl")

if __name__ == "__main__":
    main()
