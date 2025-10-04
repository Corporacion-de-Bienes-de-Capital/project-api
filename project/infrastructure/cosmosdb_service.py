from project.infrastructure.cosmosdb import container
from datetime import datetime, timezone 
from datetime import datetime
import pytz

def crear_documento(data):
    container.create_item(body=data)

def obtener_documentos():
    return list(container.read_all_items())

#Probar la conexión a CosmosDB desde "py manage.py shell"
# from project.infrastructure.cosmosdb_service import crear_documento, obtener_documentos

# # Crear un documento de prueba
# crear_documento({"id": "1", "mensaje": "Prueba de conexión"})

# # Obtener y mostrar todos los documentos
# print(obtener_documentos())



def log_event(user, endpoint, method, extra=None):
    chile_tz = pytz.timezone('America/Santiago')
    timestamp = datetime.now(chile_tz).isoformat()
    log_item = {
        "id": str(datetime.now(timezone.utc).timestamp()).replace('.', ''),
        "timestamp": timestamp,
        "user": str(user) if user else "Huguito",
        "endpoint": endpoint,
        "method": method,
        "ip": extra.get("ip") if extra else None,
        "user_pk": extra.get("user_pk") if extra else None,
        "username": extra.get("username") if extra else None,
        "query_params": extra.get("query_params") if extra else None,
        "body": extra.get("body") if extra else None,
    }
    container.create_item(body=log_item)


