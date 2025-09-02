import os
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

# Archivo de conexion. Carga las variables del .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

COSMOS_ENDPOINT = os.getenv('COSMOS_ENDPOINT')
COSMOS_KEY = os.getenv('COSMOS_KEY')
COSMOS_DATABASE = os.getenv('COSMOS_DATABASE')
COSMOS_CONTAINER = os.getenv('COSMOS_CONTAINER')

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(COSMOS_DATABASE)
container = database.get_container_client(COSMOS_CONTAINER)