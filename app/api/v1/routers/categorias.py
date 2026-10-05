from fastapi import APIRouter, HTTPException, status
from app.schemas.categoria import CategoriaCreate, CategoriaResponse, CategoriaUpdate
from app.database.connection import supabase

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias():
    """Listar todas as categorias cadastradas (RF12)."""
    response = supabase.table("categorias").select("*").execute()
    return response.data

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obter_categoria(categoria_id: int):
    """Obter detalhes de uma categoria por ID."""
    response = supabase.table("categorias").select("*").eq("id", categoria_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    return response.data[0]

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria: CategoriaCreate):
    """Cadastrar uma nova categoria (RF12)."""
    dados = categoria.model_dump()
    response = supabase.table("categorias").insert(dados).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao cadastrar categoria.")
    return response.data[0]

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(categoria_id: int, categoria: CategoriaUpdate):
    """Editar dados de uma categoria."""
    dados = {k: v for k, v in categoria.model_dump().items() if v is not None}
    if not dados:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado informado para atualização.")

    response = supabase.table("categorias").update(dados).eq("id", categoria_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    return response.data[0]

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(categoria_id: int):
    """Excluir uma categoria."""
    response = supabase.table("categorias").delete().eq("id", categoria_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    return None