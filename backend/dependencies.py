from sqlalchemy.orm import sessionmaker
from models import db, Usuario
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from main import SECRET_KEY, ALGORITHM, bearer_scheme

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
        
def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), session: Session = Depends(pegar_sessao)):
    try:
        token = credentials.credentials
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info.get("sub"))
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Negado")
    return usuario