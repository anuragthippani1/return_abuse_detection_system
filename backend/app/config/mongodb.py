import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from typing import Dict, Any

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'returns_db')
COLLECTION_NAME = os.getenv('MONGODB_COLLECTION', 'return_cases')

def get_mongodb_client():
    """Create and return a MongoDB client instance."""
    try:
        client = MongoClient(MONGODB_URI)
        # Test the connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

def get_database():
    """Get database instance."""
    client = get_mongodb_client()
    return client[DB_NAME]

def get_collection():
    """Get collection instance."""
    db = get_database()
    return db[COLLECTION_NAME]

def convert_object_id(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert ObjectId to string in the response."""
    if '_id' in data:
        data['_id'] = str(data['_id'])
    return data

def parse_object_id(id_str: str) -> ObjectId:
    """Convert string ID to ObjectId."""
    try:
        return ObjectId(id_str)
    except Exception as e:
        raise ValueError(f"Invalid ObjectId: {id_str}") 