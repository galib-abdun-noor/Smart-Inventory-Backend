from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import json

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