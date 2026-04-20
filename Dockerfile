FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_NAME=/app/data/Tender.db

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "mkdir -p \"$(dirname \"${DB_NAME}\")\" && touch \"${DB_NAME}\" && alembic upgrade head && python -m app"]
