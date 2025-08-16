import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from db_utils import get_db  #to connect to mongodb url



def sales_data():
    stores=['Store 1','Store 2','Store 3']
    today=datetime.today()
    salesdata=[]


    for i in range(30):
        date =(today - timedelta(days=i)).strftime('%Y-%m-%d')
        for store in stores:
            sales = random.randint(2000, 5000)
            salesdata.append({
                'store': store,
                'date': date,
                'sales': sales
            })

    return pd.DataFrame(salesdata)

if __name__=="__main__":
    df=sales_data()
    db = get_db()
    collection = db["raw_sales"]


collection.insert_many(df.to_dict(orient="records"))

print("Inserted {} records into MongoDB.".format(len(df)))
