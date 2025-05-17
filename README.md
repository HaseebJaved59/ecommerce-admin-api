# E-commerce Admin API

## Overview
A FastAPI-based backend to power an admin dashboard for e-commerce insights.

## 🚀 Tech Stack
- Python + FastAPI
- SQLAlchemy + MySQL
- Uvicorn (server)

## 📁 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ecommerce-admin-api.git
cd ecommerce-admin-api
```

### 2. Create `.env` file
```bash
cp .env.example .env
# Fill in your MySQL credentials
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run seed script to populate demo data
```bash
python scripts/seed.py
```

### 5. Start the API server
```bash
uvicorn app.main:app --reload
```

## 🧪 API Endpoints

### Products
- `GET /products` — List all products
- `POST /products` — Create a new product
- `GET /products/{id}` — Get product by product id

### Inventory
- `GET /inventory/status` — View current stock
- `GET /inventory/status?low_stock_threshold=5` — Alert for low stock
- `POST /inventory/update` — Update inventory quantity

### Sales
- `GET /sales/sales-filtered?start_date=2025-05-13T00:00:00&end_date=2025-05-17T00:00:00&category=Electronics` — Filter by date range and category
- `GET /sales/revenue-compare?group_by=monthly&start_date=2025-05-13T00:00:00&end_date=2025-05-17T23:59:59&categories=Electronics&categories=Audio` — Compare sales between two periods or categories
- `GET /sales` — List all sales
- `POST /sales` — Record a new sale
- `GET /sales/revenue?period=daily|weekly|monthly|yearly` — Revenue report
- `GET /sales/filter?start_date=2025-01-01T00:00:00&end_date=2025-05-17T23:59:59` — Filter sales by date range
- `GET /sales/filter?product_id=1` — Filter sales by product id
- `GET /sales/summary?start_date=2024-01-01T00:00:00` — Sales Summary
- `GET /sales/top-products?limit=3` — Top selling product
- `GET /sales/revenue-analysis?group_by=daily|weekly|monthly|yearly` — Revenuve Analysis


## 📌 Notes
- Make sure your MySQL DB is running.
- Sample data is seeded automatically.

