import os
import pandas as pd
import joblib
from datetime import datetime, timedelta

# ---------------------
# CONFIG
# ---------------------
MODEL_DIR = "models"
FORECAST_DAYS = 30
OUTPUT_FILE = "store_forecasts.csv"

# ---------------------
# 1. Generate Future Dates & Features
# ---------------------
def generate_future_dates(n_days):
    today = pd.to_datetime(datetime.utcnow().date())
    future_dates = pd.date_range(start=today + timedelta(days=1), periods=n_days)

    df_future = pd.DataFrame({"date": future_dates})
    df_future["day_of_week"] = df_future["date"].dt.dayofweek
    df_future["month"] = df_future["date"].dt.month
    df_future["is_weekend"] = df_future["day_of_week"].isin([5, 6]).astype(int)

    return df_future


# ---------------------
# 2. Load Models and Predict
# ---------------------
def predict_for_all_stores(df_future):
    predictions = []

    for filename in os.listdir(MODEL_DIR):
        if filename.endswith("_model.pkl"):
            store_id = filename.replace("_model.pkl", "").replace("_", " ")
            model_path = os.path.join(MODEL_DIR, filename)
            model = joblib.load(model_path)

            X_future = df_future[["day_of_week", "month", "is_weekend"]]
            y_pred = model.predict(X_future)

            store_preds = df_future.copy()
            store_preds["predicted_sales"] = y_pred
            store_preds["store"] = store_id

            predictions.append(store_preds)

            print(f"[{store_id}] ✅ Forecast generated.")

    if predictions:
        full_forecast = pd.concat(predictions)
        return full_forecast
    else:
        print("⚠️ No models found.")
        return pd.DataFrame()


# ---------------------
# 3. Main
# ---------------------
def main():
    df_future = generate_future_dates(FORECAST_DAYS)
    forecast_df = predict_for_all_stores(df_future)

    if not forecast_df.empty:
        forecast_df = forecast_df[["store", "date", "predicted_sales"]]
        forecast_df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✅ Forecast saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
