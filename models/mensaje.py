# models/mensaje.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base


class Mensaje(Base):
    __tablename__ = "mensajes"

    id              = Column(Integer, primary_key=True, index=True)
    contenido       = Column(String(1000), nullable=False)
    fecha_envio     = Column(DateTime(timezone=True), server_default=func.now())

    remitente_id    = Column(Integer, ForeignKey("usuarios.id"))
    destinatario_id = Column(Integer, ForeignKey("usuarios.id"))

    # ← back_populates agregados para coincidir con usuario.py
    remitente    = relationship(
        "Usuario",
        foreign_keys=[remitente_id],
        back_populates="mensajes_enviados"
    )
    destinatario = relationship(
        "Usuario",
        foreign_keys=[destinatario_id],
        back_populates="mensajes_recibidos"
    )

    def __repr__(self):
        return f"<Mensaje id={self.id} de={self.remitente_id} a={self.destinatario_id}>"