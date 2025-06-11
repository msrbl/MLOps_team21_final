import joblib as jl
import pandas as pd

from typing import Union

from src.config import settings


def predict_passenger(
    Pclass: Union[str, int] = 0,
    Sex: str = "male",
    Age: int = 15,
    Siblings_Spouses_Aboard: int = 2,
    Parents_Children_Aboard: int = 2,
    Fare: float = 10.0,
):
    """
    Делает предсказание по полям пассажира с помощью модели из settings.MODEL_DIR.
    """
    sex_map = {"male": 0, "female": 1}
    sex_mapped = sex_map.get(Sex, 0)

    if Age < 16:
        Age_binned = 0
    elif Age < 32:
        Age_binned = 1
    elif Age < 48:
        Age_binned = 2
    elif Age < 64:
        Age_binned = 3
    else:
        Age_binned = 4

    data = pd.DataFrame(
        [
            {
                "Pclass": Pclass,
                "Sex": sex_mapped,
                "Age": Age,
                "Siblings/Spouses_Aboard": Siblings_Spouses_Aboard,
                "Parents/Children_Aboard": Parents_Children_Aboard,
                "Fare": Fare,
                "Age_binned": Age_binned,
            }
        ]
    )

    model = jl.load(settings.MODEL_PATH)

    prediction = model.predict(data)[0]
    return prediction
