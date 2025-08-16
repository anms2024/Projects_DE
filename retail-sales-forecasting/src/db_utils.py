from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file

def get_db():
    mongo_uri = os.getenv("MONGO_URI") 
    client = MongoClient(mongo_uri)    
    return client["retail_sales"]
