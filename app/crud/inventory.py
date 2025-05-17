from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryUpdate

def update_inventory(db: Session, update: InventoryUpdate):
    db_inventory = db.query(Inventory).filter(Inventory.product_id == update.product_id).first()
    if db_inventory:
        db_inventory.quantity_in_stock = update.quantity_in_stock
    else:
        db_inventory = Inventory(**update.dict())
        db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventory(db: Session):
    return db.query(Inventory).all()

def get_inventory_status(db: Session, low_stock_threshold: Optional[int] = None) -> List[Inventory]:
    query = db.query(Inventory).join(Inventory.product)
    if low_stock_threshold is not None:
        query = query.filter(Inventory.quantity_in_stock < low_stock_threshold)
    return query.order_by(Inventory.quantity_in_stock.asc()).all()
