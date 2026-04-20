FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Используем opentelemetry-instrument для автоматической отправки трейсов без изменения кода
CMD ["python", "main.py"]