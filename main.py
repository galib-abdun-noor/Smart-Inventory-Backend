from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import json
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime

app = FastAPI(title="Smart Inventory Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = boto3.resource("dynamodb", region_name="ca-central-1")

inventory_table = dynamodb.Table("InventoryProducts")
transactions_table = dynamodb.Table("InventoryTransactions")

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

#For Login and Access Controls
class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {"message": "Smart Inventory Management API is running"}

# @app.get("/api/inventory")
# def get_inventory():
#     response = inventory_table.scan()
#     items = response.get("Items", [])
#     return json.loads(json.dumps(items, default=decimal_default))

@app.get("/api/inventory/{stock_code}")
def get_inventory_by_product(stock_code: str):
    response = inventory_table.query(
        KeyConditionExpression=Key("StockCode").eq(stock_code)
    )
    items = response.get("Items", [])
    return json.loads(json.dumps(items, default=decimal_default))

@app.get("/api/inventory/{stock_code}/{warehouse_id}")
def get_inventory_by_product_warehouse(stock_code: str, warehouse_id: str):
    response = inventory_table.get_item(
        Key={
            "StockCode": stock_code,
            "WarehouseID": warehouse_id
        }
    )
    item = response.get("Item", {})
    return json.loads(json.dumps(item, default=decimal_default))

@app.get("/api/transactions/{stock_code}")
def get_transactions(stock_code: str):
    response = transactions_table.query(
        KeyConditionExpression=Key("StockCode").eq(stock_code)
    )
    items = response.get("Items", [])
    return json.loads(json.dumps(items, default=decimal_default))

#for the dashboard summary endpoint
@app.get("/api/dashboard/summary")
def get_dashboard_summary():
    try:
        inventory_response = inventory_table.scan()
        inventory_items = inventory_response.get("Items", [])

        transactions_response = transactions_table.scan(Select="COUNT")
        total_transactions = transactions_response.get("Count", 0)

        total_products = len(inventory_items)
        total_stock = sum(int(item.get("CurrentStock", 0)) for item in inventory_items)

        unique_warehouses = len(set(
            item.get("WarehouseID", "") for item in inventory_items if item.get("WarehouseID")
        ))

        return {
            "totalProducts": total_products,
            "totalStock": total_stock,
            "uniqueWarehouses": unique_warehouses,
            "totalTransactions": total_transactions
        }

    except Exception as e:
        return {"error": str(e)}
    
    #for transaction trend chart
@app.get("/api/dashboard/transaction-trend")
def get_transaction_trend():
    try:
        response = transactions_table.scan()
        items = response.get("Items", [])

        trend_map = {}

        for item in items:
            invoice_date = item.get("InvoiceDate", "")
            if invoice_date:
                period = invoice_date[:7]  # YYYY-MM
                trend_map[period] = trend_map.get(period, 0) + 1

        trend_data = [
            {"period": period, "count": count}
            for period, count in sorted(trend_map.items())
        ]

        return trend_data

    except Exception as e:
        return {"error": str(e)}


#for top products
@app.get("/api/dashboard/top-products")
def get_top_products():
    try:
        response = transactions_table.scan()
        items = response.get("Items", [])

        product_map = {}

        for item in items:
            stock_code = item.get("StockCode")
            description = item.get("Description", "Unknown")
            quantity = int(item.get("Quantity", 0))

            if stock_code not in product_map:
                product_map[stock_code] = {
                    "description": description,
                    "totalQuantity": 0
                }

            product_map[stock_code]["totalQuantity"] += quantity

        sorted_products = sorted(
            product_map.items(),
            key=lambda x: x[1]["totalQuantity"],
            reverse=True
        )[:5]

        result = [
            {
                "StockCode": stock_code,
                "Description": data["description"],
                "totalQuantity": data["totalQuantity"]
            }
            for stock_code, data in sorted_products
        ]

        return result

    except Exception as e:
        return {"error": str(e)}
    
#For login and access control (basic implementation)
@app.post("/api/login")
def login(request: LoginRequest):
    demo_user = {
        "admin":{"password": "@dminHi12!", "role":"admin"},
        "manager":{"password":"M@nager34^","role":"manager"},
        "viewer":{"password":"V!ewer$67","role":"viewer"}
    }

    user = demo_user.get(request.username)

    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail = "Invalid username or password")
    
    return{
        "message":"Login Successful",
        "username":request.username,
        "role":user["role"]
    }

#Loading ML models
model = joblib.load("demand_forecast_model.pkl")
encoder = joblib.load("stockcode_encoder.pkl")

# Helper function for prediction
def predict_demand(stock_code: str, current_stock: int):
    try:
        stock_code_encoded = encoder.transform([stock_code])[0]
    except Exception:
        raise HTTPException(status_code=404, detail="StockCode not found in model encoder")

    now = datetime.now()

    # Simple placeholder lag values
    lag1 = current_stock
    lag7 = current_stock
    rolling7mean = current_stock

    features = pd.DataFrame([{
        "StockCodeEncoded": stock_code_encoded,
        "DayOfWeek": now.weekday(),
        "Month": now.month,
        "Year": now.year,
        "Lag1": lag1,
        "Lag7": lag7,
        "Rolling7Mean": rolling7mean
    }])

    prediction = model.predict(features)[0]

    return max(0, round(prediction))

# Forecast endpoint
@app.get("/api/forecast/{stock_code}")
def get_forecast(stock_code: str):
    response = inventory_table.query(
        KeyConditionExpression=Key("StockCode").eq(stock_code)
    )
    items = response.get("Items", [])

    if not items:
        raise HTTPException(status_code=404, detail="Product not found")

    # Use total stock across warehouses as approximation
    total_stock = sum(int(item.get("CurrentStock", 0)) for item in items)

    predicted_demand = predict_demand(stock_code, total_stock)

    return {
        "success": True,
        "data": {
            "stockCode": stock_code,
            "predictedDemand": predicted_demand,
            "forecastWindowDays": 7
        }
    }

# Reorder recommendation endpoint
@app.get("/api/reorder/{stock_code}/{warehouse_id}")
def get_reorder_recommendation(stock_code: str, warehouse_id: str):
    response = inventory_table.get_item(
        Key={
            "StockCode": stock_code,
            "WarehouseID": warehouse_id
        }
    )

    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    current_stock = int(item.get("CurrentStock", 0))
    predicted_demand = predict_demand(stock_code, current_stock)

    safety_stock = max(5, round(predicted_demand * 0.2))
    recommended_reorder_qty = max(0, predicted_demand + safety_stock - current_stock)
    low_stock_alert = current_stock < (predicted_demand + safety_stock)

    return {
        "success": True,
        "data": {
            "stockCode": stock_code,
            "WarehouseID": warehouse_id,
            "currentStock": current_stock,
            "predictedDemand": predicted_demand,
            "safetyStock": safety_stock,
            "recommendedReorderQty": recommended_reorder_qty,
            "lowStockAlert": low_stock_alert
        }
    }