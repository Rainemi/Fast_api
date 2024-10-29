from astrapy import DataAPIClient
import os
from dotenv import load_dotenv
from uuid import UUID

load_dotenv()

# Keyspace name
keyspace = "default_keyspace"

# Function to initialize the client session

def get_session():
    # Load environment variables
    application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    database_id = os.getenv("ASTRA_DB_ID")
    region = os.getenv("ASTRA_DB_REGION")

    # Check if any required environment variable is missing
    if not application_token or not database_id or not region:
        raise ValueError("Ensure that all environment variables are set: "
                         "ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_ID, ASTRA_DB_REGION")

    api_endpoint = f"https://{database_id}-{region}.apps.astra.datastax.com"
    
    # Initialize client with API endpoint and token
    client = DataAPIClient()
    client.set_caller(application_token)
    client.api_endpoint = api_endpoint

    print(f"API Endpoint set to: {client.api_endpoint}")

    # Test the connection
    try:
        admin_info = client.get_admin()
        print(f"Connected to Astra DB as Admin: {admin_info}")
    except Exception as e:
        print(f"Failed to connect to Astra DB: {e}")
        return None

    return client

# CRUD Methods
def get_all(table_name):
    response = client.get_all(keyspace, table_name)
    return response

def insert_row(table_name, data):
    client.insert_row(keyspace, table_name, data)

def get_by_id(table_name, row_id: str):
    return client.get_by_id(keyspace, table_name, row_id)

def update_row(table_name, row_id: str, data):
    client.update_row(keyspace, table_name, row_id, data)

def delete_row(table_name, row_id: str):
    client.delete_row(keyspace, table_name, row_id)


