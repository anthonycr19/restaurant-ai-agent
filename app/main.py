from fastapi import FastAPI

from app.api.routes.chat import router as chat_router


app = FastAPI(
    title="Restaurant AI API",
    version="1.0.0",
    description="API de agente inteligente para restaurante"
)


app.include_router(
    chat_router,
    prefix="/api/v1"
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }