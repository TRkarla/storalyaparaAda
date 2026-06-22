# models/reto_asignado.py
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base


class RetoAsignado(Base):
    __tablename__ = "retos_asignados"

    id               = Column(Integer, primary_key=True, index=True)
    estado           = Column(String(20), default="Pendiente")  # Pendiente, En progreso, Completado
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now())

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    reto_id    = Column(Integer, ForeignKey("retos.id"))  # ← apunta a tabla "retos"

    usuario = relationship("Usuario", back_populates="retos_asignados")
    reto    = relationship("Reto",    back_populates="usuarios_asignados")

    def __repr__(self):
        return f"<RetoAsignado id={self.id} estado='{self.estado}'>"