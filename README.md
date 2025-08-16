#  Retail Sales Forecasting

This project is a complete pipeline for retail sales forecasting using machine learning.  
It includes data ingestion, model training, prediction, serving forecasts via an API, and visualizing them through an interactive Streamlit dashboard.

---

## Features

- Ingests sales data and stores it in MongoDB
- Trains a forecasting model (e.g., time series or regression-based)
- Generates store-level forecasts
- Serves forecasts using a FastAPI backend
- Interactive dashboard using Streamlit
- Modular script-based architecture

---

## ⚙️ Setup Instructions

### 🔧 Environment Setup

```bash
git clone https://github.com/your-username/retail-sales-forecasting.git
cd retail-sales-forecasting

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

 # Running the Project
1. Data Ingestion

Reads CSV or other raw data and stores it in MongoDB.

python ingest.py

2. Train the Forecasting Model

Trains and saves the machine learning model.

python train_model.py

3. Generate Forecasts

Runs the model and outputs store_forecasts.csv.

python predict_model.py

4. Start the FastAPI Backend

Exposes an API to get forecasts by store and date.

uvicorn app:app --reload


Example endpoint:

GET /forecast?store_id=Store%201&date=2025-08-15


Response:

{
  "store": "Store 1",
  "date": "2025-08-15",
  "predicted_sales": 3814.0
}

5. Launch Streamlit Dashboard

Interactive UI to view forecasts by store and date.

streamlit run streamlit_app.py


Features:

Dropdown for store selection

Date slider

Forecast line chart

Optional: "Get Forecast from API" button
