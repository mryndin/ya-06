import os
import uvicorn
from fastapi import FastAPI

# Импорты OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# 1. Настройка трассировки
provider = TracerProvider()
endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://simplest-collector:4317")
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()

# 2. Инструментация
FastAPIInstrumentor.instrument_app(app)

@app.get("/order")
async def get_order():
    return {"order_id": 12345, "status": "In Progress", "item": "Golden Ring"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)