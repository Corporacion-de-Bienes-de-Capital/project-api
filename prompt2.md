# Project-Api - Documentación y Prompt (Arquitectura Hexagonal)

## Resumen del Proyecto
API RESTful para la gestión de proyectos, empresas y entidades relacionadas, desarrollada en Django 4.x y Django REST Framework, siguiendo principios de arquitectura hexagonal (puertos y adaptadores).

## Estructura principal del proyecto
```
project/
├─ domain/
│  ├─ models/          # Clases de dominio puras (sin dependencia de Django ORM)
│  ├─ services/        # Lógica de negocio, casos de uso, orquestación
│  └─ ports/           # Interfaces abstractas (ej: IProyectoRepository)
├─ infrastructure/
│  ├─ django_models/   # Modelos Django ORM (ej: tbl_proyecto, tbl_empresa, etc.)
│  ├─ repository/      # Implementaciones concretas de los puertos usando Django ORM
│  └─ config/          # Configuración, logging, settings
├─ adapters/
│  └─ views/           # ViewSets DRF, exponen la API y llaman a domain.services vía puertos
├─ api/
│  └─ serializers/     # Serializers DRF para validación y conversión de datos
├─ manage.py
```

## Características principales
- Separación clara entre lógica de negocio (domain/services), acceso a datos (infrastructure/repository) y exposición de API (adapters/views).
- Modelos de dominio independientes del framework.
- Sincronización masiva, actualización y creación robusta de entidades relacionadas a proyectos.
- Validación y manejo de relaciones ForeignKey mediante utilidades y patrones DRY.
- Preparado para pruebas unitarias e integración (en proceso de implementación).

## Endpoints principales de la API
- `/api/proyectos/` (POST): Sincronización masiva de proyectos y entidades relacionadas.
- `/api/proyectos/sector-economico/<slug>/`: Listado filtrado por sector económico.
- Otros endpoints según necesidades del dominio.

## Patrones de sincronización y validación
- Uso de `update_or_create` para sincronización masiva.
- Normalización robusta de datos de entrada (listas/dict).
- Validación y manejo de errores detallados en la respuesta.
- Conversión automática de IDs a instancias de modelo para ForeignKey.

## Pruebas y herramientas
- Pruebas unitarias y de integración con `pytest` y `pytest-django` (en proceso).
- Uso de `APITestCase` para endpoints REST.
- Cobertura de código con `pytest-cov`.

## Cómo ejecutar y probar
1. Instala dependencias: `pip install -r requirements.txt`
2. Ejecuta migraciones: `python manage.py migrate`
3. Corre el servidor: `python manage.py runserver`
4. Ejecuta tests: `pytest`

## Notas de desarrollo
- Seguir el patrón DRY y la normalización de datos en todos los endpoints.
- Mantener la documentación y los tests actualizados ante cualquier cambio estructural.
- La arquitectura hexagonal facilita la escalabilidad, el testing y el mantenimiento.
