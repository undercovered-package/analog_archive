from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.core.models.item import Item

router = APIRouter()


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = {"from_attributes": True}


@router.get("/items", response_model=list[ItemResponse])
async def get_items():
    return await Item.all()


@router.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    return await Item.create(**item.model_dump())


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    item = await Item.get_or_none(id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    item = await Item.get_or_none(id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.delete()
