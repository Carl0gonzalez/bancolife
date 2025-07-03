from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelos Pydantic para validación de datos

class ClienteBase(BaseModel):
    nombre: str
    correo: str

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    
    class Config:
        from_attributes = True

class CuentaBase(BaseModel):
    cliente_id: int
    saldo: float = 0.0

class CuentaCreate(CuentaBase):
    pass

class Cuenta(CuentaBase):
    id: int
    
    class Config:
        from_attributes = True

class TransferenciaBase(BaseModel):
    cuenta_origen: int
    cuenta_destino: int
    monto: float

class TransferenciaCreate(TransferenciaBase):
    pass

class Transferencia(TransferenciaBase):
    id: int
    fecha: datetime
    
    class Config:
        from_attributes = True

# Modelos para respuestas de API
class TransferenciaResponse(BaseModel):
    id: int
    cuenta_origen: int
    cuenta_destino: int
    monto: float
    fecha: datetime
    mensaje: str
    
    class Config:
        from_attributes = True 