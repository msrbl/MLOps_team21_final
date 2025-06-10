import pandas as pd
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.config import settings

def preprocess_dataset(dataset_path: str) -> None:
    df = pd.read_csv(dataset_path)

    columns = df.columns

    if 'Sex' in columns:
        df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

    if 'Age_binned' in columns:
        df['Age_binned'] = df['Age_binned'].astype('category').cat.codes

    drop_cols = []
    if 'Name' in columns:
        drop_cols.append('Name')
    X = df.drop(columns=['Survived'] + drop_cols)
    y = df['Survived']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=None
    )

    num_cols = X_train.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    processed_dir = settings.DATA_DIR / "processed"
    os.makedirs(processed_dir, exist_ok=True)
    base = dataset_path.split('/')[-1].split('\\')[-1].replace('.csv', '')

    X_train_path = processed_dir / f"{base}_X_train.csv"
    X_test_path = processed_dir / f"{base}_X_test.csv"
    y_train_path = processed_dir / f"{base}_y_train.csv"
    y_test_path = processed_dir / f"{base}_y_test.csv"
    
    X_train.to_csv(X_train_path, index=False)
    X_test.to_csv(X_test_path, index=False)
    y_train.to_csv(y_train_path, index=False)
    y_test.to_csv(y_test_path, index=False)
    
    return [(X_train_path, y_train_path), (X_test_path, y_test_path)]