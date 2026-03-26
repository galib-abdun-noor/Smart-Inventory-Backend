1. Clone repo
2. Install dependencies
3. Run - aws configure
4. Start backend:
   uvicorn main:app --reload
5. For xgboost: pip install xgboost
6. For sklearn: pip install scikit-learn

# Smart Inventory Management System — Backend

This repository contains the **backend API** for the Smart Inventory Management System project.  
The backend is built with **FastAPI** and connects to **AWS DynamoDB** to serve inventory, transaction, dashboard, forecasting, and reorder recommendation data.

---

## Overview

The backend is responsible for:

- retrieving inventory summary data from `InventoryProducts`
- retrieving transaction history from `InventoryTransactions`
- serving dashboard statistics
- loading the trained ML model for demand forecasting
- calculating reorder recommendations
- exposing REST APIs for the frontend

The backend does **not** expose AWS credentials to the frontend.  
All DynamoDB and ML interactions are handled server-side.

---

## Tech Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **boto3**
- **pandas**
- **joblib**
- **scikit-learn**
- **xgboost**
- **AWS DynamoDB**

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

## Run Instructions

This project consists of two parts:

1. **Backend** — FastAPI + DynamoDB + ML model
2. **Frontend** — Angular application

To run the full system locally, start the backend first, then the frontend.

---

## Prerequisites

Make sure the following are installed:

- Python 3.9+
- Node.js and npm
- AWS CLI
- Git

---

## 1. Clone the Repositories

### Backend
```bash
git clone <backend-repo-link>
cd Smart-Inventory-Backend
