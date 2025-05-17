from pydantic import BaseModel
from datetime import datetime

class InventoryBase(BaseModel):
    product_id: int
    quantity_in_stock: int

class InventoryUpdate(InventoryBase):
    pass

class InventoryRead(InventoryBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True