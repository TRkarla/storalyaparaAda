# models/poema.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base


class Poema(Base):
    __tablename__ = "poemas"

    id             = Column(Integer, primary_key=True, index=True)
    titulo         = Column(String(100), nullable=False)    # ← ya estaba
    contenido      = Column(String(5000), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id     = Column(Integer, ForeignKey("usuarios.id"))  # ← corregido: era autor_id

    autor = relationship("Usuario", back_populates="poemas")

    def __repr__(self):
        return f"<Poema id={self.id} titulo='{self.titulo}'>"