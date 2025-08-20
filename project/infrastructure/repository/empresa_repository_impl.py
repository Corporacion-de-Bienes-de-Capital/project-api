from typing import List, Optional
from project.domain.ports.empresa_repository import IEmpresaRepository
from project.domain.models.empresa import Empresa
from project.infrastructure.django_models.empresa import EmpresaORM


class EmpresaRepositoryImpl(IEmpresaRepository):

    def _orm_to_domain(self, orm: EmpresaORM) -> Empresa:
        return Empresa(
            id=orm.empr_id, 
            nombre=orm.empr_nombre,
            empr_rut=orm.empr_rut
        )

    def list_all(self) -> List[Empresa]:
        qs = EmpresaORM.objects.all()
        return [self._orm_to_domain(e) for e in qs]

    def list_active(self) -> List[Empresa]:
        qs = EmpresaORM.objects.filter(is_active=1, is_deleted=0)
        return [self._orm_to_domain(e) for e in qs]

    def get_by_id(self, pk: int) -> Optional[Empresa]:
        try:
            orm = EmpresaORM.objects.get(empr_id=pk)
        except EmpresaORM.DoesNotExist:
            return None
        return self._orm_to_domain(orm)