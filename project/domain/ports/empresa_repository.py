from abc import ABC, abstractmethod
from typing import List, Optional
from project.domain.models.empresa import Empresa

class IEmpresaRepository(ABC):
    
    @abstractmethod
    def list_all(self) -> List[Empresa]:
        """Obtiene todas las empresas"""
        pass
    
    @abstractmethod
    def list_active(self) -> List[Empresa]:
        """Obtiene solo las empresas activas"""
        pass
    
    @abstractmethod
    def get_by_id(self, pk: int) -> Optional[Empresa]:
        """Obtiene una empresa por su ID"""
        pass