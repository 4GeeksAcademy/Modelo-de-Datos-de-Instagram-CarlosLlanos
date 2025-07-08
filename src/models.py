from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy_schemadisplay import create_schema_graph

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    nombre_completo = Column(String(100))
    bio = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    posts = relationship("Post", back_populates="autor")
    comentarios = relationship("Comentario", back_populates="autor")
    likes = relationship("Like", back_populates="usuario")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    contenido_url = Column(String(255))
    descripcion = Column(Text)
    fecha_publicacion = Column(DateTime(timezone=True), server_default=func.now())
    autor = relationship("Usuario", back_populates="posts")
    comentarios = relationship("Comentario", back_populates="post")
    likes = relationship("Like", back_populates="post")

class Comentario(Base):
    __tablename__ = 'comentarios'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    texto = Column(Text, nullable=False)
    fecha_comentario = Column(DateTime(timezone=True), server_default=func.now())
    autor = relationship("Usuario", back_populates="comentarios")
    post = relationship("Post", back_populates="comentarios")

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    fecha_like = Column(DateTime(timezone=True), server_default=func.now())
    usuario = relationship("Usuario", back_populates="likes")
    post = relationship("Post", back_populates="likes")

def generar_diagrama():
    engine = create_engine('sqlite:///:memory:')
    # Referenciar clases para evitar problemas
    _ = Usuario, Post, Comentario, Like
    graph = create_schema_graph(
        metadata=Base.metadata,
        engine=engine,
        show_datatypes=True,
        show_indexes=True,
        rankdir='LR',
        concentrate=False
    )
    graph.write_png('diagram.png')
    print("Diagrama generado correctamente: diagram.png")
