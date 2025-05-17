from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True