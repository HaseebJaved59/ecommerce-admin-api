from pydantic import BaseModel
from datetime import datetime

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float

class SaleCreate(SaleBase):
    pass

class SaleRead(SaleBase):
    id: int
    sale_date: datetime

    class Config:
        orm_mode = True