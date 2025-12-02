from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ComentarioBase(BaseModel):
    titulo: Optional[str] = None
    conteudo: str
    midia: Optional[str] = None

class ComentarioCriar(ComentarioBase):
    pass

class ComentarioResposta(BaseModel):
    id: int
    usuario_id: int
    titulo: Optional[str]
    conteudo: str
    midia: Optional[str]
    criado_em: datetime
    
    class Config:
        from_attributes = True

class ComentarioDetalhes(ComentarioResposta):
    curtidas_count: int = 0
    respostas_count: int = 0


class RespostaBase(BaseModel):
    conteudo: str

class RespostaCriar(RespostaBase):
    pass

class RespostaResposta(BaseModel):
    id: int
    usuario_id: int
    comentario_id: int
    conteudo: str
    criado_em: datetime
    
    class Config:
        from_attributes = True


class CurtidaCriar(BaseModel):
    comentario_id: Optional[int] = None
    enquete_id: Optional[int] = None

class CurtidaResposta(BaseModel):
    id: int
    usuario_id: int
    comentario_id: Optional[int]
    enquete_id: Optional[int]
    criado_em: datetime
    
    class Config:
        from_attributes = True


class VotoCriar(BaseModel):
    opcao_id: int

class VotoResposta(BaseModel):
    id: int
    usuario_id: int
    enquete_id: int
    opcao_id: int
    criado_em: datetime
    
    class Config:
        from_attributes = True


class OpcaoEnqueteBase(BaseModel):
    conteudo: str

class OpcaoEnqueteResposta(OpcaoEnqueteBase):
    id: int
    votos: int
    
    class Config:
        from_attributes = True


class EnqueteBase(BaseModel):
    nome: str
    titulo: Optional[str] = None
    conteudo: str
    midia: Optional[str] = None

class EnqueteCriar(EnqueteBase):
    opcoes_list: List[OpcaoEnqueteBase]

class EnqueteResposta(EnqueteBase):
    id: int
    usuario_id: int
    criado_em: datetime
    opcoes: List[OpcaoEnqueteResposta] = []
    
    class Config:
        from_attributes = True

class EnqueteDetalhes(EnqueteResposta):
    votos_total: int = 0
    curtidas_count: int = 0


class SeguidorCriar(BaseModel):
    usuario_id_a_seguir: int

class SeguidorResposta(BaseModel):
    id: int
    nome: str
    email: str
    
    class Config:
        from_attributes = True


class UsuarioPublico(BaseModel):
    id: int
    nome: str
    email: str
    criado_em: datetime
    
    class Config:
        from_attributes = True

class UsuarioPerfil(UsuarioPublico):
    seguidores_count: int = 0
    seguindo_count: int = 0
    comentarios_count: int = 0
    enquetes_count: int = 0
