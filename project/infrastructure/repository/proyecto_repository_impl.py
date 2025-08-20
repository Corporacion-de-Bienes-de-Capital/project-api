from typing import List, Optional
from project.domain.ports.proyecto_repository import IProyectoRepository
from project.domain.models.proyecto import Proyecto
from project.domain.models.empresa import Empresa
from project.infrastructure.django_models.proyecto import ProyectoORM

class ProyectoRepositoryImpl(IProyectoRepository):

    def _orm_to_domain(self, orm: ProyectoORM) -> Proyecto:
        empresa = None
        if getattr(orm, 'empresa', None):
            e = orm.empresa
            empresa = Empresa(
                id=e.empr_id,
                nombre=e.empr_nombre,
                empr_rut=getattr(e, 'empr_rut', None)
            )
        return Proyecto(id=orm.pro_id, nombre=orm.pro_nombre, empresa=empresa)

    def list_all(self) -> List[Proyecto]:
        qs = ProyectoORM.objects.all()
        return [self._orm_to_domain(p) for p in qs]

    def list_with_companies(self) -> List[Proyecto]:
        qs = ProyectoORM.objects.select_related('empresa').all()
        return [self._orm_to_domain(p) for p in qs]

    def get_by_id(self, pk: int) -> Optional[Proyecto]:
        try:
            orm = ProyectoORM.objects.select_related('empresa').get(pk=pk)
        except ProyectoORM.DoesNotExist:
            return None
        return self._orm_to_domain(orm)