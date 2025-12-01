from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Text, func
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy_utils.types import ChoiceType
import pymysql, os
from dotenv import load_dotenv

load_dotenv()

SQL_DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

db = create_engine(SQL_DATABASE_URL)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(200), nullable=False)
    email = Column("email", String(200), nullable=False, unique=True)
    senha = Column("senha", String(300), nullable=False)
    criado_em = Column("criado_em", DateTime, server_default=func.now())
    seguindo_nomes = Column("seguindo_nomes", String(500))
    seguidores_nomes = Column("seguidores_nomes", String(500))
    seguidores_contagem = Column("seguidores_contagem", Integer)
    
    def __init__(self, nome, email, senha, criado_em = func.now(), seguindo_nomes="", seguidores_nomes="", seguidores_contagem=0):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.criado_em = criado_em
        self.seguindo_nomes = seguindo_nomes
        self.seguidores_nomes = seguidores_nomes
        self.seguidores_contagem = seguidores_contagem
        
class Comentario(Base):
    __tablename__ = "comentarios"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column("titulo", String(500), nullable=True)
    midia = Column("midia", String(500))
    conteudo = Column("conteudo", Text, nullable=False)
    criado_em = Column("criado_em", DateTime, server_default=func.now())
    
    def __init__(self, usuario_id, titulo, conteudo, midia, criado_em=func.now()):
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.conteudo = conteudo
        self.midia = midia
        self.criado_em = criado_em
        
class Enquete(Base):
    __tablename__ = "enquetes"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(100), nullable=False, unique=True)
    titulo = Column("titulo", String(200), nullable=True)
    conteudo = Column("conteudo", Text, nullable=False)
    midia = Column("midia", String(500))
    criado_em = Column("criado_em", DateTime, server_default=func.now())
    opcoes = relationship("Opcoes", back_populates="enquete", cascade="all, delete-orphan")
    
    def __init__(self, nome, titulo, conteudo, midia, criado_em=func.now()):
        self.nome = nome
        self.titulo = titulo
        self.conteudo = conteudo
        self.midia = midia
        self.criado_em = criado_em

class Opcoes(Base):
    __tablename__ = "opcoes_enquete"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    conteudo = Column("titulo", String(200), nullable=False)
    votos = Column("votos", Integer, default=0)
    enquete_id = Column("enquete_id", Integer, ForeignKey("enquetes.id"), nullable=False)
    enquete = relationship("Enquete", back_populates="opcoes")
    
    def __init__(self, conteudo, votos=0):
        self.conteudo = conteudo
        self.votos = votos
        
Base.metadata.create_all(db)