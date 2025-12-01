from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao
from models import Comentario, Enquete, Opcoes, Usuario
from schemas import ComentarioSchema, EnquetesSchema, OpcoesSchema
from sqlalchemy.orm import Session

posts_router = APIRouter(prefix="/posts", tags=["posts"])

@posts_router.post("/comentario")
async def criar_comentario(comentarioModelo: ComentarioSchema, sessao: Session = Depends(pegar_sessao)):
    novoComentario = Comentario(
        usuario_id = comentarioModelo.usuario_id,  # Substituir pelo id do usuário autenticado
        titulo=comentarioModelo.titulo,
        conteudo=comentarioModelo.conteudo,
        midia=comentarioModelo.midia
    )
    sessao.add(novoComentario)
    sessao.commit()
    return {"mensagem": f"Comentário criado com sucesso {novoComentario.id}"}