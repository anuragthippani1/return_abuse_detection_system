import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'amazon')
COLLECTION_NAME = os.getenv('MONGODB_COLLECTION', 'return_cases')

def import_csv_to_mongodb(csv_file_path):
    # Connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Read CSV file
    df = pd.read_csv(csv_file_path)

    # Convert timestamp strings to datetime objects
    df['reported_at'] = pd.to_datetime(df['reported_at'])

    # Convert DataFrame to list of dictionaries
    records = df.to_dict('records')

    # Insert records into MongoDB
    if records:
        result = collection.insert_many(records)
        print(f"Successfully imported {len(result.inserted_ids)} records")
    else:
        print("No records to import")

if __name__ == "__main__":
    csv_file_path = "return_abuse_bulk.csv"  # Update this to your CSV file path
    import_csv_to_mongodb(csv_file_path) 