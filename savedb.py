from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("uri")
client = MongoClient(MONGO_URI)
db = client["tesla_financials"]
collection = db["quarterly_reports"]

def save_to_db(data):
    
    try:
        result = collection.insert_one({"data": data})
        return str(result.inserted_id)
    except Exception as e:
        print(f"Error saving to database: {e}")
        return None


