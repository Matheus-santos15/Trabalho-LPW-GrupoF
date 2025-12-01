from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True
        
class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True

class ComentarioSchema(BaseModel):
    usuario_id: int
    titulo: Optional[str]
    conteudo: str
    midia: Optional[str]

    class Config:
        from_attributes = True
        
class EnquetesSchema(BaseModel):
    usuario_id: int
    nome: str
    titulo: Optional[str]
    conteudo: str
    midia: Optional[str]

    class Config:
        from_attributes = True
    
class OpcoesSchema(BaseModel):
    conteudo: str
    
    class Config:
        from_attributes = True
    