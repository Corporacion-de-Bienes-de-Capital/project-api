from dataclasses import dataclass
from project.domain.models.empresa import Empresa
from typing import Optional

@dataclass
class Proyecto:
    id: int
    nombre: str
    empresa: Optional[Empresa] = None
