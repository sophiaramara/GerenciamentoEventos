from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class EventoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_evento: datetime
    capacidade: int = 50  
    status: str = "ATIVO"
    categoria_id: Optional[int] = None

    @field_validator('data_evento')
    @classmethod
    def validar_data_futura(cls, v: datetime) -> datetime:
        v_comparacao = v.replace(tzinfo=None) if v.tzinfo else v
        if v_comparacao < datetime.now():
            raise ValueError('A data do evento não pode ser no passado.')
        return v

    @field_validator('capacidade')
    @classmethod
    def validar_capacidade(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('A capacidade do evento deve ser maior que zero.')
        return v

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_evento: Optional[datetime] = None
    capacidade: Optional[int] = None
    status: Optional[str] = None
    categoria_id: Optional[int] = None

    @field_validator('data_evento')
    @classmethod
    def validar_data_futura(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None:
            v_comparacao = v.replace(tzinfo=None) if v.tzinfo else v
            if v_comparacao < datetime.now():
                raise ValueError('A data do evento não pode ser no passado.')
        return v

    @field_validator('capacidade')
    @classmethod
    def validar_capacidade(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError('A capacidade do evento deve ser maior que zero.')
        return v

class EventoResponse(EventoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True