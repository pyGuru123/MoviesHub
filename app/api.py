from fastapi import FastAPI
from loguru import logger

from app.moviesbot.router import router as MoviesHubRouter
from app.pirates.router import router as PiratesRouter

app = FastAPI(title="MoviesHubAPI")

# --------------------------------------------------------------------------
#                                Routers

app.include_router(MoviesHubRouter, prefix="/api/v1/movies", tags=["MoviesHub Bot"])
app.include_router(PiratesRouter, prefix="/api/v1/pirates", tags=["Pirates Bot"])

# --------------------------------------------------------------------------


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "An api for Movieshub"}


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Application is shutting down")
    logger.info("Application shutdown successfully")
