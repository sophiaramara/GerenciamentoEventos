from fastapi import APIRouter, HTTPException, status
from app.schemas.evento import EventoCreate, EventoResponse, EventoUpdate
from app.database.connection import supabase

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.get("/", response_model=list[EventoResponse])
def listar_eventos():
    """Listar todos os eventos cadastrados (RF05)."""
    response = supabase.table("eventos").select("*").execute()
    return response.data

@router.get("/{evento_id}", response_model=EventoResponse)
def obter_evento(evento_id: int):
    """Obter detalhes de um evento pelo ID."""
    response = supabase.table("eventos").select("*").eq("id", evento_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    return response.data[0]

@router.post("/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def criar_evento(evento: EventoCreate):
    """Cadastrar um novo evento (RF04)."""
    dados = evento.model_dump()
    dados["data_evento"] = dados["data_evento"].isoformat()
    
    response = supabase.table("eventos").insert(dados).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao cadastrar evento.")
    return response.data[0]

@router.put("/{evento_id}", response_model=EventoResponse)
def atualizar_evento(evento_id: int, evento: EventoUpdate):
    """Editar dados de um evento (RF06)."""
    dados_atualizados = {k: v for k, v in evento.model_dump().items() if v is not None}
    
    if "data_evento" in dados_atualizados and dados_atualizados["data_evento"]:
        dados_atualizados["data_evento"] = dados_atualizados["data_evento"].isoformat()

    if not dados_atualizados:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado informado para atualização.")

    response = supabase.table("eventos").update(dados_atualizados).eq("id", evento_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    return response.data[0]

@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_evento(evento_id: int):
    """Remover ou cancelar um evento (RF06, RN04)."""
    response = supabase.table("eventos").delete().eq("id", evento_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    return None