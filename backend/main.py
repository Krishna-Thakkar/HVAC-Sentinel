from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.health import router as health_router
from app.routes.systems import router as systems_router
from app.routes.alerts import router as alerts_router

app = FastAPI(
    title="HVAC Sentinel API",
    description="AI-powered HVAC maintenance prioritization system.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(systems_router)
app.include_router(alerts_router)


@app.get("/")
def root():
    return {
        "service": "HVAC Sentinel API",
        "version": "0.1.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
