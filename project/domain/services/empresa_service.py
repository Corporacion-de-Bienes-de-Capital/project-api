from typing import List, Optional
from project.domain.ports.empresa_repository import IEmpresaRepository
from project.domain.models.empresa import Empresa

class EmpresaService:
    
    def __init__(self, repository: IEmpresaRepository):
        self.repository = repository
    
    def listar_empresas(self) -> List[Empresa]:
        """Obtiene todas las empresas"""
        return self.repository.list_all()
    
    def listar_empresas_activas(self) -> List[Empresa]:
        """Obtiene solo las empresas activas"""
        return self.repository.list_active()
    
    def obtener(self, empresa_id: int) -> Optional[Empresa]:
        """Obtiene una empresa específica por ID"""
        return self.repository.get_by_id(empresa_id)