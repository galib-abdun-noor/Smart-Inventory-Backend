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

## Project Structure

```text
Smart-Inventory-Backend/
│
├── main.py
├── demand_forecast_model.pkl
├── stockcode_encoder.pkl
├── requirements.txt
└── README.md
