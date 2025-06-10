from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api import router
from src.utils.logger.logger_config import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = setup_logging()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "MLOps App is running"}

app.include_router(router)