import streamlit as st
import pandas as pd

FORECAST_FILE = "store_forecasts.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(FORECAST_FILE)
        df['date'] = pd.to_datetime(df['date'])  # Ensure proper date format
        return df
    except Exception as e:
        st.error(f"Error loading forecast data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

st.title("📈 Retail Sales Forecast Dashboard")

stores = df['store'].unique()
selected_store = st.selectbox("Select Store", stores)

filtered = df[df['store'] == selected_store]

# Fix: convert Timestamp → datetime.datetime
date_options = filtered['date'].sort_values().unique()
selected_date = st.slider(
    "Select Date",
    min_value=min(date_options).to_pydatetime(),
    max_value=max(date_options).to_pydatetime(),
    value=min(date_options).to_pydatetime()
)

# Show line chart
st.line_chart(filtered.set_index('date')['predicted_sales'])
