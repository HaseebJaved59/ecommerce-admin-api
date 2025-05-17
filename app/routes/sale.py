from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.session import SessionLocal
from app.schemas.sale import SaleCreate, SaleRead
from app.crud import sale as crud_sale
from app.models.sale import Sale
from sqlalchemy import func, desc, extract
from typing import List, Optional, Literal
from app.models.product import Product

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SaleRead)
def create(sale: SaleCreate, db: Session = Depends(get_db)):
    return crud_sale.create_sale(db, sale)

@router.get("/", response_model=List[SaleRead])
def read_all(db: Session = Depends(get_db)):
    return crud_sale.get_sales(db)


@router.get("/filter", response_model=List[SaleRead])
def filter_sales(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    product_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Sale)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    return query.all()

@router.get("/summary")
def sales_summary(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    query = db.query(
        func.sum(Sale.total_price).label("total_revenue"),
        func.sum(Sale.quantity).label("total_quantity")
    )
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    result = query.one()
    return {
        "total_revenue": result.total_revenue or 0,
        "total_quantity": result.total_quantity or 0
    }

@router.get("/top-products")
def top_products(
    limit: int = 5,
    db: Session = Depends(get_db)
):
    result = (
        db.query(
            Product.name,
            func.sum(Sale.quantity).label("total_sold")
        )
        .join(Sale, Product.id == Sale.product_id)
        .group_by(Product.id)
        .order_by(desc("total_sold"))
        .limit(limit)
        .all()
    )
    return [{"product": name, "quantity_sold": sold} for name, sold in result]

@router.get("/revenue-analysis")
def revenue_analysis(group_by: Literal["daily", "weekly", "monthly", "yearly"] = Query(...),db: Session = Depends(get_db)):
    if group_by == "daily":
        results = db.query(func.date(Sale.sale_date).label("period"),func.sum(Sale.total_price).label("revenue")).group_by(func.date(Sale.sale_date)).order_by(func.date(Sale.sale_date)).all()
    elif group_by == "weekly":
        results = db.query( 
            func.date_format(Sale.sale_date, "%x-W%v").label("period"),
            func.sum(Sale.total_price).label("revenue")
        ).group_by("period").order_by("period").all()

    elif group_by == "monthly":
        results = db.query(
            func.date_format(Sale.sale_date, "%Y-%m").label("period"),
            func.sum(Sale.total_price).label("revenue")
        ).group_by("period").order_by("period").all()

    elif group_by == "yearly":
        results = db.query(
            func.extract("year", Sale.sale_date).label("period"),
            func.sum(Sale.total_price).label("revenue")
        ).group_by("period").order_by("period").all()

    else:
        raise HTTPException(status_code=400, detail="Invalid group_by parameter.")

    return [{"period": row.period, "revenue": row.revenue} for row in results]

@router.get("/revenue-compare")
def revenue_compare(
    group_by: Literal["daily", "weekly", "monthly", "yearly"] = Query(...),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    categories: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query()

    if group_by == "daily":
        period_label = func.date_format(Sale.sale_date, "%Y-%m-%d").label("period")
    elif group_by == "weekly":
        period_label = func.date_format(Sale.sale_date, "%x-W%v").label("period")
    elif group_by == "monthly":
        period_label = func.date_format(Sale.sale_date, "%Y-%m").label("period")
    elif group_by == "yearly":
        period_label = func.year(Sale.sale_date).label("period")
    else:
        raise HTTPException(status_code=400, detail="Invalid group_by parameter.")

    query = db.query(
        period_label,
        Product.category,
        func.sum(Sale.total_price).label("revenue")
    ).join(Product, Sale.product_id == Product.id)

    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if categories:
        query = query.filter(Product.category.in_(categories))

    query = query.group_by("period", Product.category).order_by("period", Product.category)

    results = query.all()

    return [
        {
            "period": row.period,
            "category": row.category,
            "revenue": row.revenue
        }
        for row in results
    ]

@router.get("/sales-filtered", response_model=List[SaleRead])
def get_sales_filtered(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    product_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Sale).join(Product, Sale.product_id == Product.id)

    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if category:
        query = query.filter(Product.category == category)

    sales = query.order_by(Sale.sale_date).all()
    return sales
