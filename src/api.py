import logging

from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.services.predict import predict_passenger

logger = logging.getLogger('app')
router = APIRouter(tags=["MLOps FastAPI Project"])

class TempInput(BaseModel):
    Pclass: Annotated[Union[str, int], Field(..., description="Passenger class (1st, 2nd, or 3rd)")]
    Sex: Annotated[str, Field(..., description="Passenger sex (male or female)")]
    Age: Annotated[int, Field(..., description="Passenger age in years")]
    Siblings_Spouses_Aboard: Annotated[int, Field(..., description="Number of siblings or spouses aboard")]
    Parents_Children_Aboard: Annotated[int, Field(..., description="Number of parents or children aboard")]
    Fare: Annotated[float, Field(..., description="Fare paid by the passenger")]

@router.post("/get-predictions")
async def process_model_predictions(
    payload: TempInput,
):
    try:
        result = predict_passenger(**payload.model_dump())
        result = float(result)
        
        return {
            "Survived": result
        }
    except HTTPException as e:
        logger.error(f"HTTPException: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))