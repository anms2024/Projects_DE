import pandas as pd
import pymongo
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

#MongoDB Config
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "retail_sales"
COLLECTION_NAME = "processed_sales"
MODEL_DIR = "models"
MIN_REQUIRED_DAYS = 20  #For Starting 



#1. Load Data 
def load_data():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    data = pd.DataFrame(list(collection.find()))

    if "_id" in data.columns:
        data.drop(columns=["_id"], inplace=True)

    data["date"] = pd.to_datetime(data["date"])
    return data


#2. Train Model 
def train_model_for_store(store_id, df_store):
    df_store = df_store.sort_values("date")

    print(f"[{store_id}] Available rows: {len(df_store)}")

    if len(df_store) < MIN_REQUIRED_DAYS:
        print(f"[{store_id}] Still too little data. Skipping.")
        return None

    FEATURES = ["day_of_week", "month", "is_weekend"]
    TARGET = "sales"

    X = df_store[FEATURES]
    y = df_store[TARGET]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    print(f"[{store_id}]  Model trained (no test set)")

    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, f"{store_id.replace(' ', '_')}_model.pkl")
    joblib.dump(model, model_path)

    return {
        "store": store_id,
        "trained_on_days": len(df_store),
        "model_path": model_path
    }



#4. Main 
def main():
    df = load_data()

    required_cols = {"store", "date", "sales", "day_of_week", "month", "is_weekend"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")

    results = []

    for store_id in df["store"].unique():
        df_store = df[df["store"] == store_id].copy()
        result = train_model_for_store(store_id, df_store)
        if result:
            results.append(result)

    if results:
        summary_df = pd.DataFrame(results)
        os.makedirs(MODEL_DIR, exist_ok=True)
        summary_df.to_csv(os.path.join(MODEL_DIR, "training_summary.csv"), index=False)


if __name__ == "__main__":
    main()