import joblib
import pathlib
import json
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from config import PROC_DATA_DIR, DATASET_PATH

def main():
    df = pd.read_csv(DATASET_PATH, sep=';')

    X = df.drop(columns=['quality'])
    y = df['quality']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=None
    )

    scaler = StandardScaler().fit(X_train)
    X_train_s = scaler.transform(X_train)
    X_test_s  = scaler.transform(X_test)

    pd.DataFrame(X_train_s, columns=X.columns).to_csv(PROC_DATA_DIR / "X_train.csv", index=False)
    pd.DataFrame(X_test_s,  columns=X.columns).to_csv(PROC_DATA_DIR / "X_test.csv",  index=False)
    y_train.to_csv(PROC_DATA_DIR / "y_train.csv", index=False)
    y_test.to_csv(PROC_DATA_DIR / "y_test.csv",  index=False)

    joblib.dump(scaler, PROC_DATA_DIR / "scaler.pkl")

    print("Preprocess done; files saved to", PROC_DATA_DIR)

if __name__ == "__main__":
    main()
