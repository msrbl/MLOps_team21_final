import os
import logging
import pickle
import pandas as pd

from sklearn.linear_model import LogisticRegression

from src.config import settings

logger = logging.getLogger('app')

def train_and_save_model(train_X_path, train_y_path, model_name="titanic_model.pkl"):
    X_train = pd.read_csv(train_X_path)
    y_train = pd.read_csv(train_y_path)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    model_path = settings.MODEL_DIR / model_name
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    logger.info(f"Модель сохранена в {model_path}")
    
    return model_path