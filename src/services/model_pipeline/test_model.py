import logging
import joblib as jl
import math
import pandas as pd

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

logger = logging.getLogger("app")


def proceed_testing(test_X_path, test_y_path, model_path):
    model = jl.load(model_path)

    X_test = pd.read_csv(test_X_path)
    y_test = pd.read_csv(test_y_path).squeeze()

    preds = model.predict(X_test)

    metrics = {
        "rmse": math.sqrt(mean_squared_error(y_test, preds)),
        "mae": mean_absolute_error(y_test, preds),
        "r2": r2_score(y_test, preds),
    }

    logger.info("Evaluation metrics:", metrics)

    return metrics
