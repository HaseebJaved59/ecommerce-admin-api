import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, Base, engine
from app.models.product import Product
from app.models.sale import Sale
from app.models.inventory import Inventory

# Create all tables
Base.metadata.create_all(bind=engine)

def seed():
    db: Session = SessionLocal()

    try:
        # Clear existing data
        db.query(Sale).delete()
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.commit()

        # Add products
        products = [
            Product(name="Apple iPhone 14", description="Latest iPhone model", category="Electronics", price=999.99),
            Product(name="Samsung Galaxy S23", description="New Galaxy phone", category="Electronics", price=899.99),
            Product(name="Sony WH-1000XM5", description="Noise Cancelling Headphones", category="Audio", price=349.99),
            Product(name="Dell XPS 13", description="Compact laptop", category="Computers", price=1249.99),
            Product(name="Nintendo Switch", description="Gaming console", category="Gaming", price=299.99),
        ]
        db.add_all(products)
        db.commit()

        # Add inventory and sales
        for product in products:
            quantity = random.randint(10, 100)
            db.add(Inventory(product_id=product.id, quantity_in_stock=quantity))

            for i in range(30):
                days_ago = random.randint(0, 29)
                sale_date = datetime.utcnow() - timedelta(days=days_ago)
                quantity_sold = random.randint(1, 5)
                total_price = quantity_sold * product.price
                db.add(Sale(product_id=product.id, quantity=quantity_sold, total_price=total_price, sale_date=sale_date))

        db.commit()
        print("Database seeded with demo data.")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
