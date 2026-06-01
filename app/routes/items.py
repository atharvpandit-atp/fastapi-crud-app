from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import get_item, create_item, update_item, delete_item

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=Item)
def create(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.get("/{item_id}", response_model=Item)
def read(item_id: int, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Item)
def update(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    updated = update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    if not delete_item(db, item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}