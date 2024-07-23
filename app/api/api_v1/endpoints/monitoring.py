from time import time

from fastapi import APIRouter, Depends, __version__

from app.dependencies import api_key_auth

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"res": "pong", "version": __version__, "time": time()}


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/protected", dependencies=[Depends(api_key_auth)])
def protected():
    return {"data": "You used a valid API key."}
