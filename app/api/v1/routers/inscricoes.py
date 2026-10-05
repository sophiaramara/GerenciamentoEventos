from fastapi import APIRouter, HTTPException, status
from app.schemas.inscricao import InscricaoCreate, InscricaoResponse
from app.database.connection import supabase

router = APIRouter(prefix="/inscricoes", tags=["Inscrições"])

@router.get("/", response_model=list[InscricaoResponse])
def listar_inscricoes():
    """Listar todas as inscrições efetuadas."""
    response = supabase.table("inscricoes").select("*").execute()
    return response.data

@router.post("/", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
def realizar_inscricao(inscricao: InscricaoCreate):
    """Realizar inscrição em um evento (RF07)."""

    evento_resp = supabase.table("eventos").select("*").eq("id", inscricao.evento_id).execute()
    if not evento_resp.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento informado não existe.")
    
    evento = evento_resp.data[0]

    if evento.get("status") != "ATIVO":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível se inscrever em eventos inativos ou cancelados.")

    inscricao_existente = supabase.table("inscricoes") \
        .select("*") \
        .eq("evento_id", inscricao.evento_id) \
        .eq("email_participante", inscricao.email_participante) \
        .execute()
    
    if inscricao_existente.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este participante já está inscrito neste evento.")

    inscritos_atuais = supabase.table("inscricoes") \
        .select("id", count="exact") \
        .eq("evento_id", inscricao.evento_id) \
        .execute()
    
    total_inscritos = inscritos_atuais.count if inscritos_atuais.count is not None else len(inscritos_atuais.data)
    capacidade_maxima = evento.get("capacidade", 50)

    if total_inscritos >= capacidade_maxima:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Capacidade máxima do evento já foi atingida.")

    dados = inscricao.model_dump()
    dados["status"] = "ATIVA"
    
    response = supabase.table("inscricoes").insert(dados).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao realizar inscrição.")
    
    return response.data[0]

@router.delete("/{inscricao_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_inscricao(inscricao_id: int):
    """Cancelar inscrição (RF08, RN05)."""
    response = supabase.table("inscricoes").delete().eq("id", inscricao_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada.")
    return None