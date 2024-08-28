import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection

# Load environment variables from the .env file
load_dotenv()

# Retrieve MongoDB credentials from environment variables
mongodb_host = os.getenv("MONGODB_HOST")
mongodb_user = os.getenv("MONGODB_USER")
mongodb_password = os.getenv("MONGODB_PASSWORD")
mongodb_app_name = os.getenv("MONGODB_APP_NAME")

# Construct the MongoDB URI
uri = f"mongodb+srv://{mongodb_user}:{mongodb_password}@{mongodb_host}/?retryWrites=true&w=majority&appName={mongodb_app_name}"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def get_collection(database_name: str, collection_name: str) -> Collection:
    """
    Get a collection from the MongoDB database.

    :param database_name: The name of the database.
    :param collection_name: The name of the collection.
    :return: The MongoDB collection.
    """
    db = client[database_name]
    return db[collection_name]
