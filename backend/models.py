from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Text, func, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy_utils.types import ChoiceType
import pymysql, os
from dotenv import load_dotenv

load_dotenv()

SQL_DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

db = create_engine(SQL_DATABASE_URL)
Base = declarative_base()


seguidor_association = Table(
    'seguidor',
    Base.metadata,
    Column('seguidor_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('seguindo_id', Integer, ForeignKey('usuarios.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(200), nullable=False)
    email = Column("email", String(200), nullable=False, unique=True)
    senha = Column("senha", String(300), nullable=False)
    criado_em = Column("criado_em", DateTime, server_default=func.now())
    
    
    comentarios = relationship("Comentario", foreign_keys="Comentario.usuario_id", cascade="all, delete")
    enquetes = relationship("Enquete", foreign_keys="Enquete.usuario_id", cascade="all, delete")
    curtidas = relationship("Curtida", foreign_keys="Curtida.usuario_id", cascade="all, delete")
    votos = relationship("Voto", foreign_keys="Voto.usuario_id", cascade="all, delete")
    
    
    seguidores = relationship(
        "Usuario",
        secondary=seguidor_association,
        primaryjoin=id == seguidor_association.c.seguindo_id,
        secondaryjoin=id == seguidor_association.c.seguidor_id,
        foreign_keys=[seguidor_association.c.seguidor_id, seguidor_association.c.seguindo_id],
        backref="seguindo"
    )
    
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
        
        
class Comentario(Base):
    __tablename__ = "comentarios"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column("titulo", String(500), nullable=True)
    midia = Column("midia", String(500))
    conteudo = Column("conteudo", Text, nullable=False)
    criado_em = Column("criado_em", DateTime, server_default=func.now())
    
    
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    curtidas = relationship("Curtida", foreign_keys="Curtida.comentario_id", cascade="all, delete")
    respostas = relationship("Resposta", foreign_keys="Resposta.comentario_id", cascade="all, delete")
    
    def __init__(self, usuario_id, titulo, conteudo, midia=None):
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.conteudo = conteudo
        self.midia = midia
        
class Enquete(Base):
    __tablename__ = "enquetes"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    nome = Column("nome", String(100), nullable=False, unique=True)
    titulo = Column("titulo", String(200), nullable=True)
    conteudo = Column("conteudo", Text, nullable=False)
    midia = Column("midia", String(500))
    criado_em = Column("criado_em", DateTime, server_default=func.now())
    
    
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    opcoes = relationship("Opcoes", back_populates="enquete", cascade="all, delete-orphan")
    votos = relationship("Voto", foreign_keys="Voto.enquete_id", cascade="all, delete")
    curtidas = relationship("Curtida", foreign_keys="Curtida.enquete_id", cascade="all, delete")
    
    def __init__(self, usuario_id, nome, titulo, conteudo, midia=None):
        self.usuario_id = usuario_id
        self.nome = nome
        self.titulo = titulo
        self.conteudo = conteudo
        self.midia = midia

class Opcoes(Base):
    __tablename__ = "opcoes_enquete"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    enquete_id = Column("enquete_id", Integer, ForeignKey("enquetes.id"), nullable=False)
    conteudo = Column("conteudo", String(200), nullable=False)
    votos = Column("votos", Integer, default=0)
    
    
    enquete = relationship("Enquete", back_populates="opcoes")
    votos_rel = relationship("Voto", foreign_keys="Voto.opcao_id", cascade="all, delete")
    
    def __init__(self, enquete_id, conteudo):
        self.enquete_id = enquete_id
        self.conteudo = conteudo

class Curtida(Base):
    __tablename__ = "curtidas"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    comentario_id = Column("comentario_id", Integer, ForeignKey("comentarios.id"), nullable=True)
    enquete_id = Column("enquete_id", Integer, ForeignKey("enquetes.id"), nullable=True)
    criado_em = Column("criado_em", DateTime, server_default=func.now())
    
    
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    comentario = relationship("Comentario", foreign_keys=[comentario_id])
    enquete = relationship("Enquete", foreign_keys=[enquete_id])
    
    def __init__(self, usuario_id, comentario_id=None, enquete_id=None):
        self.usuario_id = usuario_id
        self.comentario_id = comentario_id
        self.enquete_id = enquete_id

class Resposta(Base):
    __tablename__ = "respostas"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    comentario_id = Column("comentario_id", Integer, ForeignKey("comentarios.id"), nullable=False)
    conteudo = Column("conteudo", Text, nullable=False)
    criado_em = Column("criado_em", DateTime, server_default=func.now())
    
    
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    comentario = relationship("Comentario", foreign_keys=[comentario_id])
    
    def __init__(self, usuario_id, comentario_id, conteudo):
        self.usuario_id = usuario_id
        self.comentario_id = comentario_id
        self.conteudo = conteudo

class Voto(Base):
    __tablename__ = "votos"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    enquete_id = Column("enquete_id", Integer, ForeignKey("enquetes.id"), nullable=False)
    opcao_id = Column("opcao_id", Integer, ForeignKey("opcoes_enquete.id"), nullable=False)
    criado_em = Column("criado_em", DateTime, server_default=func.now())
    

    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    enquete = relationship("Enquete", foreign_keys=[enquete_id])
    opcao = relationship("Opcoes", foreign_keys=[opcao_id])
    
    def __init__(self, usuario_id, enquete_id, opcao_id):
        self.usuario_id = usuario_id
        self.enquete_id = enquete_id
        self.opcao_id = opcao_id
    