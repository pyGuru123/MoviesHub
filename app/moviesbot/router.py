from fastapi import APIRouter, BackgroundTasks
from typing import Union
from fastapi.responses import Response
from loguru import logger

from app.moviesbot.main import main
from app.moviesbot.session import cleanup_sessions

router = APIRouter()


@router.post("/getMovies")
async def reply(request: dict, background_tasks: BackgroundTasks):
    """Replying to bot commands"""
    try:
        background_tasks.add_task(main, request)
        background_tasks.add_task(cleanup_sessions)
        return {"message": "success"}
    except Exception as e:
        return {"message": "error", "error": str(e)}