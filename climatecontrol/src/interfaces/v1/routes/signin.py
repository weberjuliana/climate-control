from typing import List

from fastapi import APIRouter, HTTPException

from climatecontrol.src.config.settings import settings
from climatecontrol.src.interfaces.v1.authentication.token_handler import signJWT

login_router = APIRouter(tags=["Login"])


@login_router.post("/login", response_model=dict)
def login(username: str, password: str):
    if username != settings.DB_USER or password != settings.DB_PASSWORD:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return signJWT(username)
