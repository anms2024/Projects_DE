import pandas as pd
from  pymongo  import MongoClient
import os 
from datetime import datetime
from db_utils import get_db

db = get_db() #check
raw_collection =db["raw_sales"]
processed_collection = db["processed_sales"]

#Load Raw Data
cursor = raw_collection.find()
df = pd.DataFrame(list(cursor))

if df.empty:
    raise ValueError('No Data found in MongoDB Collection.')

#Preprocess
df['date']=pd.to_datetime(df['date'])
df['sales']=pd.to_numeric(df['sales'], errors='coerce')
df.dropna(subset=['store', 'date', 'sales'], inplace=True)

#Feature Engineering 
df['day_of_week']=df['date'].dt.day_of_week
df['month']=df['date'].dt.month
df['is_weekend']=df['date'].isin([5, 6]).astype(int)  #check

processed_records=df.to_dict(orient='records')
processed_collection.insert_many(processed_records)
print('Processed data written into database.')