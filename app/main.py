from fastapi import FastAPI
from app.api.v1.routers import eventos, inscricoes, categorias

app = FastAPI(
    title="API de Gerenciamento de Eventos Acadêmicos",
    version="1.0.0"
)

app.include_router(categorias.router, prefix="/api/v1")
app.include_router(eventos.router, prefix="/api/v1")
app.include_router(inscricoes.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API de Eventos Acadêmicos rodando com sucesso!"}