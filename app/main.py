from fastapi import FastAPI
from app.routes import product, sale, inventory

app = FastAPI(title="E-commerce Admin API")

app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(sale.router, prefix="/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])