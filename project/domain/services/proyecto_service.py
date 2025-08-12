from typing import List
from project.domain.ports.proyecto_repository import IProyectoRepository
from project.domain.models.proyecto import Proyecto

class ProyectoService:
    def __init__(self, repo: IProyectoRepository):
        self.repo = repo

    def listar_proyectos(self) -> List[Proyecto]:
        return self.repo.list_all()

    def listar_proyectos_con_empresas(self) -> List[Proyecto]:
        return self.repo.list_with_companies()

    def obtener(self, pk: int) -> Proyecto | None:
        return self.repo.get_by_id(pk)
