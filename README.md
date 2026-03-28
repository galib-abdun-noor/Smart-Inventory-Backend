# Smart Inventory Management System — Backend

This repository contains the **backend service** for the Smart Inventory Management System.  
It is built using **FastAPI**, connects to **AWS DynamoDB**, and integrates a **machine learning model** to provide demand forecasting and reorder recommendations.

https://github.com/user-attachments/assets/0b4c3378-6680-49b0-8f1a-6f66c62e5676

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

- Python 3.9+
- pip
- AWS CLI
- Git

---

## Setup Instructions
1. Clone the Repository
git clone <your-backend-repo-link>
cd Smart-Inventory-Backend
2. Install Dependencies

```

pip install fastapi uvicorn boto3 pandas joblib scikit-learn xgboost

```


## AWS Configuration

The backend uses boto3 to connect to DynamoDB.

#### Step 1 — Configure AWS CLI

Run:

```

aws configure

```

Enter:

```

AWS Access Key ID:        <your-access-key>
AWS Secret Access Key:    <your-secret-key>
Default region name:      ca-central-1
Default output format:    json

```


#### Start the server:

```

uvicorn main:app --reload

```

You should see:

```

Uvicorn running on http://127.0.0.1:8000

```

#### API Documentation

FastAPI automatically generates API docs.

Open in browser:

```

http://127.0.0.1:8000/docs

```

You can test all endpoints from here.

---

## Project Structure

```text
Smart-Inventory-Backend/
│
├── main.py
├── demand_forecast_model.pkl
├── stockcode_encoder.pkl
└── README.md


