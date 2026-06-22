# models/intercambio.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base


class Intercambio(Base):
    __tablename__ = "intercambios"

    id             = Column(Integer, primary_key=True, index=True)
    estado         = Column(String(50), default="Pendiente")
    lugar_acordado = Column(String(200), nullable=True)   # ← NUEVO
    fecha          = Column(DateTime(timezone=True), server_default=func.now())

    libro_id       = Column(Integer, ForeignKey("libros.id"))
    solicitante_id = Column(Integer, ForeignKey("usuarios.id"))
    propietario_id = Column(Integer, ForeignKey("usuarios.id"))

    libro       = relationship("Libro", back_populates="intercambios")
    solicitante = relationship(
        "Usuario", foreign_keys=[solicitante_id],
        back_populates="intercambios_solicitados"
    )
    propietario = relationship(
        "Usuario", foreign_keys=[propietario_id],
        back_populates="intercambios_recibidos"
    )

    def __repr__(self):
        return f"<Intercambio id={self.id} estado='{self.estado}'>"