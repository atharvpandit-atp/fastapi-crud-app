import json
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.utils.cache import redis_client

def get_item(db: Session, item_id: int):
    cached = redis_client.get(f"item:{item_id}")
    if cached:
        return json.loads(cached)
    
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        redis_client.setex(f"item:{item_id}", 300, json.dumps({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price
        }))
    return item

def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        for key, value in item.dict().items():
            if value is not None:
                setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        redis_client.delete(f"item:{item_id}")
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        redis_client.delete(f"item:{item_id}")
        return True
    return False