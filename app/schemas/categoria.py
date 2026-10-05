from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class CategoriaResponse(CategoriaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True