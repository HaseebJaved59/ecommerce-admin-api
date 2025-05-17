from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.schemas.sale import SaleCreate

def create_sale(db: Session, sale: SaleCreate):
    db_sale = Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sales(db: Session):
    return db.query(Sale).all()

