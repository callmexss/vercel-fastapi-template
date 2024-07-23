import os
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import settings

router = APIRouter()


@router.get("/", response_model=List[str])
async def list_files():
    static_dir = settings.STATIC_PATH
    files = os.listdir(static_dir)
    return files


@router.get("/{file_path:path}")
async def download_file(file_path: str):
    file_full_path = settings.STATIC_PATH / file_path
    if file_full_path.is_file():
        return FileResponse(file_full_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")
