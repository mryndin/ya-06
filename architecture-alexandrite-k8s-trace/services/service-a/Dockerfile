FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
#CMD ["opentelemetry-instrument", "--service-name", "service-b", "python", "main.py"]
CMD ["python", "main.py"]