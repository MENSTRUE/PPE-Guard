import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, models, predict
from app.core.config import get_settings

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s: %(message)s")
settings=get_settings()
app=FastAPI(title="PPE Guard Inference API",description="Day 21, actual checkpoint inference. Human-review decision support only.",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=False,allow_methods=["GET","POST"],allow_headers=["Content-Type"])
app.include_router(health.router,prefix="/api/v1")
app.include_router(models.router,prefix="/api/v1")
app.include_router(predict.router,prefix="/api/v1")

@app.get("/",include_in_schema=False)
def root():
    return {"service":"PPE Guard API","docs":"/docs"}
