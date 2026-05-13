from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.middleware.auth import get_current_user
from app.services.database_service import database_service

router = APIRouter(prefix="/user", tags=["user"])


class PreferencesPayload(BaseModel):
    dietary: dict
    excluded: list[str]


@router.get("/preferences")
async def get_preferences(user: dict = Depends(get_current_user)):
    return await database_service.get_user_preferences(user["id"])


@router.post("/preferences")
async def save_preferences(body: PreferencesPayload, user: dict = Depends(get_current_user)):
    await database_service.save_user_preferences(user["id"], body.dietary, body.excluded)
    return {"ok": True}
