from project.infrastructure.cosmosdb import container 
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
    # Hora de Chile
    chile_tz = pytz.timezone('America/Santiago')
    timestamp = datetime.now(chile_tz).isoformat()
    log_item = {
        "id": str(datetime.utcnow().timestamp()).replace('.', ''),
        "timestamp": timestamp,
        "user": str(user) if user else "Huguito",
        "endpoint": endpoint,
        "method": method,
        "extra": extra or {},
    }
    container.create_item(body=log_item)