# E-commerce Admin API

## Overview
A FastAPI-based backend to power an admin dashboard for e-commerce insights including:
- Product management
- Sales tracking
- Inventory status
- Revenue reporting (daily/weekly/monthly/yearly)

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

### Inventory
- `GET /inventory` — View current stock
- `POST /inventory/update` — Update inventory quantity

### Sales
- `GET /sales` — List all sales
- `POST /sales` — Record a new sale
- `GET /sales/revenue?period=daily|weekly|monthly|yearly` — Revenue report

## 📌 Notes
- Make sure your MySQL DB is running.
- Sample product and sales data is seeded automatically.

