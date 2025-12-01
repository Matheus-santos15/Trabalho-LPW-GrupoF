from fastapi import APIRouter, Depends, HTTPException
from main import bcrypt_context, ALGORITHM, SECRET_KEY, ACESS_TOKEN_EXPIRE_MINUTES
from dependencies import pegar_sessao, verificar_token
from models import Usuario
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token = timedelta(minutes= int(ACESS_TOKEN_EXPIRE_MINUTES))):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        "sub": str(id_usuario),
        "exp": data_expiracao
    }
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email: str, senha: str, sessao: Session):
    usuario = sessao.query(Usuario).filter(Usuario.email == email).first()
    if usuario and bcrypt_context.verify(senha, usuario.senha):
        return usuario
    return None

@auth_router.get("/")
async def user_root():
    return {"mensagem": "Você está na rota de usuários"}

@auth_router.post("/registrar")
async def registrar_usuario(usuarioModelo: UsuarioSchema, sessao: Session = Depends(pegar_sessao)):
    usuario_existente = sessao.query(Usuario).filter(Usuario.email == usuarioModelo.email).first()
    
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuarioModelo.senha)
        novo_usuario = Usuario(usuarioModelo.nome, usuarioModelo.email, senha_criptografada)
        sessao.add(novo_usuario)
        sessao.commit()
        return {"mensagem": "cadastro realizado com sucesso"}
    
@auth_router.post("/login")
async def login_usuario(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario_existente = autenticar_usuario(login_schema.email, login_schema.senha, session)
    
    if not usuario_existente:
        raise HTTPException(status_code=400, detail = "Email não está cadastrado ou credenciais incorretas")
    else:
        acess_token = criar_token(usuario_existente.id)
        refresh_token = criar_token(usuario_existente.id, duracao_token=timedelta(days=7))
        return {"acess_token": acess_token, "token_type": "bearer", "refresh_token": refresh_token}
    
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario_existente = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    
    if not usuario_existente:
        raise HTTPException(status_code=400, detail = "Email não está cadastrado ou credenciais incorretas")
    else:
        acess_token = criar_token(usuario_existente.id)
        return {"acess_token": acess_token, "token_type": "bearer"}
    
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario.id)
    return {"acess_token": acess_token, "token_type": "bearer"}
        