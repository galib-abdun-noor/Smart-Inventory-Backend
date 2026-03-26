# Smart Inventory Management System — Backend

This repository contains the **backend service** for the Smart Inventory Management System.  
It is built using **FastAPI**, connects to **AWS DynamoDB**, and integrates a **machine learning model** to provide demand forecasting and reorder recommendations.

---

## Overview

The backend is responsible for:

- Connecting to DynamoDB tables (`InventoryProducts`, `InventoryTransactions`)
- Serving REST APIs for frontend consumption
- Loading and using a trained ML model (`.pkl`)
- Generating demand forecasts
- Computing reorder recommendations
- Providing dashboard analytics

---

## Tech Stack

- Python
- FastAPI
- Uvicorn
- boto3 (AWS SDK)
- pandas
- joblib
- scikit-learn
- xgboost
- AWS DynamoDB

---

## Prerequisites

Before running the backend, install:

Python 3.9+
pip
AWS CLI
Git

### Setup Instructions
1. Clone the Repository
git clone <your-backend-repo-link>
cd Smart-Inventory-Backend
2. Create Virtual Environment (Recommended)
Windows
python -m venv .venv
.venv\Scripts\activate
Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies

pip install fastapi uvicorn boto3 pandas joblib scikit-learn xgboost
AWS Configuration

The backend uses boto3 to connect to DynamoDB.

### Step 1 — Configure AWS CLI

Run:

aws configure

Enter:

AWS Access Key ID:        "your-access-key"
AWS Secret Access Key:    "your-secret-key"
Default region name:      "Region name"
Default output format:    json
Step 2 — Verify Tables Exist

Make sure these DynamoDB tables are created:

InventoryProducts
InventoryTransactions

If not, create them in AWS Console with correct keys:

InventoryProducts
Partition Key: StockCode
Sort Key: WarehouseID
InventoryTransactions
Partition Key: StockCode
Sort Key: TransactionKey
ML Model Setup

Ensure the following files exist in the project root:

demand_forecast_model.pkl
stockcode_encoder.pkl

These are required for:

demand forecasting
reorder recommendation
Running the Backend

Start the server:

uvicorn main:app --reload

You should see:

Uvicorn running on http://127.0.0.1:8000
API Documentation

FastAPI automatically generates API docs.

Open in browser:

http://127.0.0.1:8000/docs

You can test all endpoints from here.

---

## Project Structure

```text
Smart-Inventory-Backend/
│
├── main.py
├── demand_forecast_model.pkl
├── stockcode_encoder.pkl
├── requirements.txt
└── README.md


