FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Команда по умолчанию
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]