import pathlib
import json
import joblib
import math
import pandas as pd

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from config import PROC_DATA_DIR, MODEL_PATH, REPORT_DIR

def main():
    model = joblib.load(MODEL_PATH)

    X_test = pd.read_csv(PROC_DATA_DIR / "X_test.csv")
    y_test = pd.read_csv(PROC_DATA_DIR / "y_test.csv").squeeze()

    preds = model.predict(X_test)

    metrics = {
        "rmse":  math.sqrt(mean_squared_error(y_test, preds)),
        "mae":   mean_absolute_error(y_test, preds),
        "r2":    r2_score(y_test, preds)
    }
    with open(REPORT_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("Evaluation metrics:", metrics)

if __name__ == "__main__":
    main()
