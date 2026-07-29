from typing import Optional
from pydantic import BaseModel

class Producto(BaseModel):
    referencia: str
    nombre: str
    precio_cop: float
    precio_usd: Optional[float] = None
    estado: bool