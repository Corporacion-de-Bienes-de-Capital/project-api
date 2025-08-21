# Este archivo permite que Django descubra los modelos situados en infrastructure/django_models
from .infrastructure.django_models.proyecto import ProyectoORM
from .infrastructure.django_models.empresa import EmpresaORM
from .infrastructure.django_models.estado_sea import EstadoSeaORM

__all__ = ["ProyectoORM", "EmpresaORM"]
