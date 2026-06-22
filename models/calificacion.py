# models/calificacion.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base


class Calificacion(Base):
    __tablename__ = "calificaciones"

    # ─── Campos ───────────────────────────────────────────────────
    id         = Column(Integer, primary_key=True, index=True)
    estrellas  = Column(Integer, nullable=False)   # 1 al 5
    comentario = Column(String(500))
    fecha      = Column(DateTime(timezone=True), server_default=func.now())

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    libro_id   = Column(Integer, ForeignKey("libros.id"))

    # ─── Relaciones ───────────────────────────────────────────────
    autor = relationship("Usuario", back_populates="calificaciones")
    libro = relationship("Libro",   back_populates="calificaciones")

    def __repr__(self):
        return f"<Calificacion id={self.id} estrellas={self.estrellas}>"