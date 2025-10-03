# Documentación Profesional: Project_Api (Arquitectura Hexagonal)

## Estructura del Proyecto

```
├─ domain/
│  ├─ models/          # Clases de dominio puras (sin Django ORM)
│  ├─ services/        # Lógica de negocio, casos de uso
│  └─ ports/           # Interfaces abstractas (ej: IProyectoRepository)
├─ infrastructure/
│  ├─ django_models/   # Modelos Django ORM (tbl_proyecto, tbl_empresa)
│  ├─ repository/      # Implementación concreta de puertos usando Django ORM
│  └─ config/          # Configuración, logging
├─ adapters/
│  └─ views/           # Django REST Framework ViewSets, llaman a domain.services vía puertos
├─ api/
│  └─ serializers/     # Serializers DRF (validación y conversión de datos)
├─ manage.py
```

## Herramientas y Tecnologías

- **Framework principal:** Django 4.x, Django REST Framework
- **Base de datos:** MySQL
- **Logs:** Azure Cosmos DB (para logs de auditoría)
- **Testing:** Postman, JMeter (carga), pytest
- **Calidad de código:** SonarQube, SonarScanner

## Endpoints principales (ejemplos)

### Empresas
- `GET /api/empresas/` — Lista todas las empresas
- `GET /api/empresas/{id}/` — Detalle de empresa por ID

### Proyectos
- `GET /proyectos/` — Lista todos los proyectos
- `GET /proyectos/{id}/` — Detalle de proyecto por ID
- `GET /proyectos/?sector_economico=XX` — Filtra proyectos por sector económico
- `/proyectos/sector-economico/<slug>/`: Listado filtrado por sector económico.

**Nota:** Todos los endpoints son de solo lectura.

#### Ejemplo de respuesta
```json
{
	"id": 1,
	"nombre": "Proyecto A",
	"empresa": "Empresa X",
	"sector_economico": "Construcción",
	...
}
```

## Despliegue y Ejecución

### 1. Instalación de dependencias
```bash
pip install -r requirements.txt
```

### 2. Configuración de variables de entorno
- `SECRET_KEY`, `DEBUG`, credenciales de base de datos, etc.

### 3. Migraciones y base de datos
```bash
python manage.py migrate
```

### 4. Levantar el servidor
```bash
python manage.py runserver
```

### 5. Acceso a la API
- Navega a: `http://127.0.0.1:8000`

## Uso de Azure Cosmos DB para logs
- Los logs de auditoría y eventos relevantes se almacenan en Azure Cosmos DB.
- Configuración en `infrastructure/config/`.

## Patrones de sincronización y validación
- Uso de `update_or_create` para sincronización masiva.
- Normalización robusta de datos de entrada (listas/dict).
- Validación y manejo de errores detallados en la respuesta.
- Conversión automática de IDs a instancias de modelo para ForeignKey.

# Notas

- Los modelos usan `managed = False`, por lo que las tablas deben existir previamente en la base de datos.
- El archivo `.env` contiene las credenciales y configuración de conexión.
- Los endpoints principales permiten gestionar proyectos y empresas.
- El diseño modular facilita la escalabilidad y el mantenimiento del sistema.

## Pruebas y Calidad

### Postman
- Colección de pruebas manuales de endpoints.

### JMeter
- Pruebas de carga sobre endpoints de lectura.

### SonarQube y SonarScanner
- Análisis de calidad de código y seguridad.
- Ejecutar `sonar-scanner` en la raíz del proyecto.

## Buenas Prácticas y Patrones

- **Arquitectura hexagonal:** Separación clara entre dominio, infraestructura y adaptadores.
- **DRY (Don't Repeat Yourself):** Reutilización de lógica en servicios y puertos.
- **Inyección de dependencias:** Los servicios usan puertos (interfaces) para acceder a repositorios.
- **Validación y serialización:** DRF Serializers para entrada/salida de datos.
- **Variables de entorno:** Nunca exponer claves ni credenciales en el código fuente.

## Troubleshooting (Errores comunes)

- **Error de conexión a base de datos:** Verifica credenciales y variables de entorno.
- **Problemas con migraciones:** Asegúrate de que los modelos Django estén sincronizados con la base de datos.
- **Fallo en análisis SonarQube:** Revisa el archivo `sonar-project.properties` y el token.
- **Logs no llegan a Cosmos DB:** Verifica la configuración y las credenciales de Azure.

## Referencias

- [Django REST Framework](https://www.django-rest-framework.org/)
- [SonarQube](https://www.sonarqube.org/)
- [JMeter](https://jmeter.apache.org/)
- [Azure Cosmos DB](https://learn.microsoft.com/es-es/azure/cosmos-db/)

---
Documentación generada para presentación profesional y auditoría técnica.
# Project-Api - Documentación y Prompt (Arquitectura Hexagonal)






