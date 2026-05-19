from pydantic import BaseModel
from typing import List


class ShoppingListItem(BaseModel):
    name: str
    display_name: str
    purchased: bool = False
    from_recipes: List[str] = []


class ShoppingListPayload(BaseModel):
    items: List[ShoppingListItem]
