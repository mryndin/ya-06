import os
import uvicorn
import httpx
from fastapi import FastAPI

# Импорты OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

# 1. Настройка трассировки
provider = TracerProvider()
endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://simplest-collector:4317")
# insecure=True обязательно, так как в локальном кластере чаще всего нет TLS
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()

# 2. Инструментация
FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()

@app.get("/calculate")
async def calculate():
    # Вызов второго сервиса
    async with httpx.AsyncClient() as client:
        response = await client.get("http://service-b:8080/order")
    
    order_data = response.json()
    return {"calculation": "Success", "data": order_data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)