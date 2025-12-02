from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Usuario, Comentario, Curtida, Resposta, Enquete, Opcoes, Voto
from schemas_rede import (
    ComentarioCriar, RespostaCriar, CurtidaCriar, VotoCriar, EnqueteCriar, SeguidorCriar
)

social_router = APIRouter(prefix="/social", tags=["rede-social"])


@social_router.post("/posts/criar")
async def criar_comentario(
    dados: ComentarioCriar,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    novo_comentario = Comentario(
        usuario_id=usuario.id,
        titulo=dados.titulo,
        conteudo=dados.conteudo,
        midia=dados.midia
    )
    session.add(novo_comentario)
    session.commit()
    session.refresh(novo_comentario)
    return {"id": novo_comentario.id, "mensagem": "Comentário criado com sucesso"}

@social_router.get("/posts/listar")
async def listar_comentarios(session: Session = Depends(pegar_sessao)):
    comentarios = session.query(Comentario).all()
    resultado = []
    for com in comentarios:
        curtidas = len(com.curtidas) if com.curtidas else 0
        respostas = len(com.respostas) if com.respostas else 0
        resultado.append({
            "id": com.id,
            "usuario": com.usuario.nome,
            "usuario_id": com.usuario.id,
            "titulo": com.titulo,
            "conteudo": com.conteudo,
            "midia": com.midia,
            "curtidas": curtidas,
            "respostas": respostas,
            "criado_em": com.criado_em
        })
    return resultado

@social_router.get("/posts/{id}")
async def obter_comentario(id: int, session: Session = Depends(pegar_sessao)):
    comentario = session.query(Comentario).filter(Comentario.id == id).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    curtidas = len(comentario.curtidas) if comentario.curtidas else 0
    respostas_data = []
    if comentario.respostas:
        for resp in comentario.respostas:
            respostas_data.append({
                "id": resp.id,
                "usuario": resp.usuario.nome,
                "conteudo": resp.conteudo,
                "criado_em": resp.criado_em
            })
    
    return {
        "id": comentario.id,
        "usuario": comentario.usuario.nome,
        "titulo": comentario.titulo,
        "conteudo": comentario.conteudo,
        "midia": comentario.midia,
        "curtidas": curtidas,
        "respostas": respostas_data,
        "criado_em": comentario.criado_em
    }

@social_router.delete("/posts/{id}")
async def deletar_comentario(
    id: int,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    comentario = session.query(Comentario).filter(Comentario.id == id).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    if comentario.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar este comentário")
    
    session.delete(comentario)
    session.commit()
    return {"mensagem": "Comentário deletado com sucesso"}



@social_router.post("/posts/{id}/curtir")
async def curtir_comentario(
    id: int,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    comentario = session.query(Comentario).filter(Comentario.id == id).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    ja_curtiu = session.query(Curtida).filter(
        Curtida.usuario_id == usuario.id,
        Curtida.comentario_id == id
    ).first()
    
    if ja_curtiu:
        raise HTTPException(status_code=400, detail="Você já curtiu este comentário")
    
    curtida = Curtida(usuario_id=usuario.id, comentario_id=id)
    session.add(curtida)
    session.commit()
    return {"mensagem": "Comentário curtido com sucesso"}

@social_router.delete("/posts/{id}/descurtir")
async def descurtir_comentario(
    id: int,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    curtida = session.query(Curtida).filter(
        Curtida.usuario_id == usuario.id,
        Curtida.comentario_id == id
    ).first()
    
    if not curtida:
        raise HTTPException(status_code=404, detail="Você não curtiu este comentário")
    
    session.delete(curtida)
    session.commit()
    return {"mensagem": "Curtida removida com sucesso"}

@social_router.get("/posts/{id}/curtidas")
async def listar_curtidas(id: int, session: Session = Depends(pegar_sessao)):
    comentario = session.query(Comentario).filter(Comentario.id == id).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    curtidas = session.query(Curtida).filter(Curtida.comentario_id == id).all()
    resultado = [
        {
            "usuario_id": c.usuario_id,
            "usuario_nome": c.usuario.nome,
            "criado_em": c.criado_em
        }
        for c in curtidas
    ]
    return {"total": len(resultado), "curtidas": resultado}



@social_router.post("/posts/{id}/responder")
async def responder_comentario(
    id: int,
    dados: RespostaCriar,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    comentario = session.query(Comentario).filter(Comentario.id == id).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    resposta = Resposta(
        usuario_id=usuario.id,
        comentario_id=id,
        conteudo=dados.conteudo
    )
    session.add(resposta)
    session.commit()
    session.refresh(resposta)
    return {"id": resposta.id, "mensagem": "Resposta criada com sucesso"}

@social_router.get("/posts/{id}/respostas")
async def listar_respostas(id: int, session: Session = Depends(pegar_sessao)):
    comentario = session.query(Comentario).filter(Comentario.id == id).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    respostas = session.query(Resposta).filter(Resposta.comentario_id == id).all()
    resultado = [
        {
            "id": r.id,
            "usuario": r.usuario.nome,
            "conteudo": r.conteudo,
            "criado_em": r.criado_em
        }
        for r in respostas
    ]
    return {"total": len(resultado), "respostas": resultado}



@social_router.post("/usuarios/{id}/seguir")
async def seguir_usuario(
    id: int,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    usuario_alvo = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario_alvo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if id == usuario.id:
        raise HTTPException(status_code=400, detail="Você não pode seguir a si mesmo")
    
    if usuario_alvo in usuario.seguindo:
        raise HTTPException(status_code=400, detail="Você já segue este usuário")
    
    usuario.seguindo.append(usuario_alvo)
    session.commit()
    return {"mensagem": f"Você agora segue {usuario_alvo.nome}"}

@social_router.delete("/usuarios/{id}/deixar-de-seguir")
async def deixar_de_seguir(
    id: int,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    usuario_alvo = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario_alvo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario_alvo not in usuario.seguindo:
        raise HTTPException(status_code=400, detail="Você não segue este usuário")
    
    usuario.seguindo.remove(usuario_alvo)
    session.commit()
    return {"mensagem": f"Você parou de seguir {usuario_alvo.nome}"}

@social_router.get("/usuarios/{id}/seguidores")
async def listar_seguidores(id: int, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    seguidores = [
        {
            "id": s.id,
            "nome": s.nome,
            "email": s.email
        }
        for s in usuario.seguidores
    ]
    return {"total": len(seguidores), "seguidores": seguidores}

@social_router.get("/usuarios/{id}/seguindo")
async def listar_seguindo(id: int, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    seguindo = [
        {
            "id": s.id,
            "nome": s.nome,
            "email": s.email
        }
        for s in usuario.seguindo
    ]
    return {"total": len(seguindo), "seguindo": seguindo}



@social_router.post("/enquetes/criar")
async def criar_enquete(
    dados: EnqueteCriar,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    enquete = Enquete(
        usuario_id=usuario.id,
        nome=dados.nome,
        titulo=dados.titulo,
        conteudo=dados.conteudo,
        midia=dados.midia
    )
    session.add(enquete)
    session.commit()
    session.refresh(enquete)
    
    for opcao_data in dados.opcoes_list:
        opcao = Opcoes(enquete_id=enquete.id, conteudo=opcao_data.conteudo)
        session.add(opcao)
    session.commit()
    
    return {"id": enquete.id, "mensagem": "Enquete criada com sucesso"}

@social_router.get("/enquetes/listar")
async def listar_enquetes(session: Session = Depends(pegar_sessao)):
    enquetes = session.query(Enquete).all()
    resultado = []
    for enq in enquetes:
        opcoes_data = [{"id": o.id, "conteudo": o.conteudo, "votos": o.votos} for o in enq.opcoes]
        resultado.append({
            "id": enq.id,
            "usuario": enq.usuario.nome,
            "nome": enq.nome,
            "titulo": enq.titulo,
            "conteudo": enq.conteudo,
            "opcoes": opcoes_data,
            "criado_em": enq.criado_em
        })
    return resultado

@social_router.post("/enquetes/{id}/votar")
async def votar_enquete(
    id: int,
    dados: VotoCriar,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    enquete = session.query(Enquete).filter(Enquete.id == id).first()
    if not enquete:
        raise HTTPException(status_code=404, detail="Enquete não encontrada")
    
    opcao = session.query(Opcoes).filter(Opcoes.id == dados.opcao_id).first()
    if not opcao:
        raise HTTPException(status_code=404, detail="Opção não encontrada")
    
    ja_votou = session.query(Voto).filter(
        Voto.usuario_id == usuario.id,
        Voto.enquete_id == id
    ).first()
    
    if ja_votou:
        raise HTTPException(status_code=400, detail="Você já votou nesta enquete")
    
    voto = Voto(usuario_id=usuario.id, enquete_id=id, opcao_id=dados.opcao_id)
    opcao.votos += 1
    session.add(voto)
    session.commit()
    
    return {"mensagem": "Voto registrado com sucesso"}

@social_router.get("/enquetes/{id}/resultado")
async def resultado_enquete(id: int, session: Session = Depends(pegar_sessao)):
    enquete = session.query(Enquete).filter(Enquete.id == id).first()
    if not enquete:
        raise HTTPException(status_code=404, detail="Enquete não encontrada")
    
    opcoes_resultado = []
    total_votos = 0
    for opcao in enquete.opcoes:
        opcoes_resultado.append({
            "id": opcao.id,
            "conteudo": opcao.conteudo,
            "votos": opcao.votos
        })
        total_votos += opcao.votos
    
    return {
        "id": enquete.id,
        "titulo": enquete.titulo,
        "total_votos": total_votos,
        "opcoes": opcoes_resultado
    }

@social_router.delete("/enquetes/{id}")
async def deletar_enquete(
    id: int,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    enquete = session.query(Enquete).filter(Enquete.id == id).first()
    if not enquete:
        raise HTTPException(status_code=404, detail="Enquete não encontrada")
    
    if enquete.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar esta enquete")
    
    session.delete(enquete)
    session.commit()
    return {"mensagem": "Enquete deletada com sucesso"}

@social_router.get("/enquetes/{id}")
async def obter_enquete(id: int, session: Session = Depends(pegar_sessao)):
    enquete = session.query(Enquete).filter(Enquete.id == id).first()
    if not enquete:
        raise HTTPException(status_code=404, detail="Enquete não encontrada")
    
    opcoes_data = [{"id": o.id, "conteudo": o.conteudo, "votos": o.votos} for o in enquete.opcoes]
    curtidas = len(enquete.curtidas) if enquete.curtidas else 0
    
    return {
        "id": enquete.id,
        "usuario": enquete.usuario.nome,
        "usuario_id": enquete.usuario.id,
        "nome": enquete.nome,
        "titulo": enquete.titulo,
        "conteudo": enquete.conteudo,
        "midia": enquete.midia,
        "opcoes": opcoes_data,
        "curtidas": curtidas,
        "criado_em": enquete.criado_em
    }
