FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/mlops-2sem-2025-b57a1acc8655.json

COPY . .

CMD dvc pull && uvicorn src:app --host 0.0.0.0 --port 8000