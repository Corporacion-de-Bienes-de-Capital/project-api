from abc import ABC, abstractmethod
from typing import List
from project.domain.models.proyecto import Proyecto

class IProyectoRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[Proyecto]:
        raise NotImplementedError

    @abstractmethod
    def list_with_companies(self) -> List[Proyecto]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, pk: int) -> Proyecto | None:
        raise NotImplementedError
