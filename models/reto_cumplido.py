# models/reto_cumplido.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base


class RetoCumplido(Base):
    __tablename__ = "retos_cumplidos"

    id               = Column(Integer, primary_key=True, index=True)
    fecha_completado = Column(DateTime(timezone=True), server_default=func.now())

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    reto_id    = Column(Integer, ForeignKey("retos.id"))  # ← apunta a tabla "retos"

    usuario = relationship("Usuario", back_populates="retos_cumplidos")
    reto    = relationship("Reto",    back_populates="usuarios_que_cumplieron")

    def __repr__(self):
        return f"<RetoCumplido id={self.id} usuario={self.usuario_id}>"