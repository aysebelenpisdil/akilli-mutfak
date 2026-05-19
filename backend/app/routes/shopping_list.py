from fastapi import APIRouter, Depends
from app.models.shopping_list import ShoppingListPayload
from app.middleware.auth import get_current_user
from app.services.database_service import database_service

router = APIRouter(prefix="/shopping-list", tags=["shopping-list"])


@router.get("/items")
async def get_items(user: dict = Depends(get_current_user)):
    items = await database_service.get_shopping_list(user["id"])
    return {"items": items}


@router.post("/items")
async def save_items(payload: ShoppingListPayload, user: dict = Depends(get_current_user)):
    await database_service.save_shopping_list(
        user["id"],
        [it.model_dump() for it in payload.items],
    )
    return {"success": True, "count": len(payload.items)}
