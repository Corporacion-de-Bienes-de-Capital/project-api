# Descripción del Proyecto

Este proyecto es una API desarrollada con Django y Django REST Framework para la gestión de proyectos y empresas. Utiliza modelos ORM conectados a una base de datos MySQL y sigue una arquitectura modular para separar la lógica de negocio, la infraestructura y los endpoints de la API.


# Estructura del Proyecto

```
ProyectoApi3/
│
├── manage.py
├── requirements.txt
│
├── project/
│   ├── .env
│   ├── __init__.py
│   ├── adapters/
│   ├── api/
│   │   └── serializers/
│   ├── domain/
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   └── django_models/
│   │       ├── __init__.py
│   │       ├── empresa.py
│   │       └── proyecto.py
│   └── tests.py
│
└── proapi/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

# Configuración

1. Clona el repositorio.
2. Crea un entorno virtual y actívalo.
3. Instala dependencias:
   ```sh
   pip install -r requirements.txt
   ```
4. Configura el archivo `.env` con los datos de tu base de datos.

---

# Ejecución

Para iniciar el servidor de desarrollo:
```sh
python manage.py runserver
```

---

# Lógica de las Funcionalidades

## 1. Gestión de Proyectos

La aplicación permite crear, consultar, actualizar y eliminar (lógicamente) proyectos. Cada proyecto está representado por el modelo `ProyectoORM`, que contiene información relevante como nombre, producto, capacidad de producción, ubicación, montos de inversión, estado, y otros atributos específicos del dominio. Los proyectos pueden estar asociados a una empresa mediante una clave foránea.

- **Creación:** Se reciben los datos del proyecto y se almacena un nuevo registro en la base de datos.
- **Consulta:** Se pueden listar todos los proyectos o consultar el detalle de uno específico.
- **Actualización:** Permite modificar los datos de un proyecto existente.
- **Eliminación lógica:** En vez de borrar físicamente el registro, se marca como eliminado usando el campo `is_deleted`.

## 2. Gestión de Empresas

Las empresas están representadas por el modelo `EmpresaORM`. Cada empresa puede tener múltiples proyectos asociados. Las funcionalidades permiten crear, consultar, actualizar y eliminar empresas, así como listar los proyectos relacionados a cada una.

## 3. Relación Proyecto-Empresa

Cada proyecto puede estar vinculado a una empresa mediante la relación de clave foránea (`empresa = models.ForeignKey(EmpresaORM, ...)`). Esto permite consultar fácilmente todos los proyectos de una empresa y viceversa.

## 4. Seguridad y Configuración

- **Variables de entorno:** El archivo `.env` almacena información sensible como la clave secreta de Django y las credenciales de la base de datos.
- **Eliminación lógica:** Se utiliza el campo `is_deleted` para evitar la eliminación física de los datos, permitiendo mantener un historial y facilitar auditorías.

## 5. Arquitectura

El proyecto sigue una arquitectura modular:
- **infrastructure/django_models/**: Define los modelos ORM que representan las tablas de la base de datos.
- **adapters/**: Contiene las vistas y endpoints de la API.
- **api/serializers/**: Serializadores para transformar los datos entre el modelo y el formato JSON.
- **domain/**: Lógica de negocio y reglas del dominio.

## 6. Endpoints

Los endpoints principales permiten:
- Listar, crear, actualizar y eliminar proyectos.
- Listar, crear, actualizar y eliminar empresas.
- Consultar los proyectos asociados a una empresa específica.

---

# Notas

- Los modelos usan `managed = False`, por lo que las tablas deben existir previamente en la base de datos.
- El archivo `.env` contiene las credenciales y configuración de conexión.
- Los endpoints principales permiten gestionar proyectos y empresas.
- El diseño modular facilita la escalabilidad y el mantenimiento del sistema.

```<!-- filepath: c:\ProyectoApi3\prompt.md -->

--- QUERY QUE LISTA PROEYCTOS POR FILTRO DE UNA EMPRESA
select p.pro_id, p.pro_nombre, p.empr_id, e.empr_id, e.empr_nombre
 from 
cbcdb.tbl_proyecto as p
inner join cbcdb.tbl_empresas as e on p.empr_id = e.empr_id
where p.empr_id = 4975 




