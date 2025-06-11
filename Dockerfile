FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . .

EXPOSE 8000
CMD ["sh", "-c", "dvc pull && uvicorn src:app --host 0.0.0.0 --port 8000"]