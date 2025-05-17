from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.inventory import InventoryUpdate, InventoryRead
from app.crud import inventory as crud_inventory


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/update", response_model=InventoryRead)
def update_inventory(update: InventoryUpdate, db: Session = Depends(get_db)):
    return crud_inventory.update_inventory(db, update)

@router.get("/", response_model=List[InventoryRead])
def read_inventory(db: Session = Depends(get_db)):
    return crud_inventory.get_inventory(db)

@router.get("/status", response_model=List[InventoryRead])
def get_inventory_status(
    low_stock_threshold: Optional[int] = Query(None, description="Return items with stock less than this number"),
    db: Session = Depends(get_db)
    ):
    return crud_inventory.get_inventory_status(db, low_stock_threshold)

@router.post("/update", response_model=InventoryRead)
def update_inventory(update: InventoryUpdate, db: Session = Depends(get_db)):
    return crud_inventory.update_inventory(db, update)