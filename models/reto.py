# models/reto.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base


class Reto(Base):
    __tablename__ = "retos"

    id          = Column(Integer, primary_key=True, index=True)
    titulo      = Column(String(150), nullable=False)
    descripcion = Column(String(500))
    estado      = Column(String(20), default="activo")  # activo, completado, expirado
    fecha_inicio = Column(DateTime(timezone=True), server_default=func.now())
    fecha_fin    = Column(DateTime(timezone=True), nullable=True)

    # ← Relaciones con reto_asignado y reto_cumplido
    usuarios_asignados      = relationship("RetoAsignado", back_populates="reto")
    usuarios_que_cumplieron = relationship("RetoCumplido", back_populates="reto")

    def __repr__(self):
        return f"<Reto id={self.id} titulo='{self.titulo}'>"