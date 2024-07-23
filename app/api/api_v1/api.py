from fastapi import APIRouter

from app.api.api_v1.endpoints import files, html, monitoring
from app.api.api_v1.endpoints.llm import edit, tags

api_router = APIRouter()
api_router.include_router(files.router, prefix="/f", tags=["files"])
api_router.include_router(html.router, prefix="", tags=["html"])
api_router.include_router(monitoring.router, prefix="", tags=["monitoring"])
api_router.include_router(tags.router, prefix="", tags=["llm.tags"])
api_router.include_router(edit.router, prefix="", tags=["llm.edit"])
