# models/usuario.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    # ─── Campos de identidad ──────────────────────────────────────
    id               = Column(Integer, primary_key=True, index=True)
    nombre_usuario   = Column(String(50),  unique=True, index=True, nullable=False)
    email    = Column(String(150), unique=True, index=True, nullable=True)
    telefono = Column(String(10),  unique=True, index=True, nullable=True)
    password         = Column(String(255), nullable=False)  # hasheda con bcrypt

    # ─── Campos de perfil ─────────────────────────────────────────
    edad             = Column(Integer,     nullable=False)
    genero           = Column(String(50),  nullable=False)
    ciudad           = Column(String(100), nullable=False)
    estado           = Column(String(100), nullable=False)
    activo           = Column(Boolean,     default=True)
    fecha_registro   = Column(DateTime(timezone=True), server_default=func.now())

    # ─── Relaciones simples (uno a muchos) ────────────────────────
    libros           = relationship("Libro",       back_populates="propietario")
    poemas           = relationship("Poema",       back_populates="autor")
    calificaciones   = relationship("Calificacion", back_populates="autor")

    # ─── Relaciones de retos ──────────────────────────────────────
    # Tus archivos son reto_asignado.py y reto_cumplido.py, no "Reto"
    retos_asignados  = relationship("RetoAsignado", back_populates="usuario")
    retos_cumplidos  = relationship("RetoCumplido", back_populates="usuario")

    # ─── Relaciones de mensajes (remitente / destinatario) ────────
    mensajes_enviados = relationship(
        "Mensaje",
        foreign_keys="[Mensaje.remitente_id]",
        back_populates="remitente"
    )
    mensajes_recibidos = relationship(
        "Mensaje",
        foreign_keys="[Mensaje.destinatario_id]",
        back_populates="destinatario"
    )

    # ─── Relaciones de intercambios (solicitante / propietario) ───
    intercambios_solicitados = relationship(
        "Intercambio",
        foreign_keys="[Intercambio.solicitante_id]",
        back_populates="solicitante"
    )
    intercambios_recibidos = relationship(
        "Intercambio",
        foreign_keys="[Intercambio.propietario_id]",
        back_populates="propietario"
    )

    def __repr__(self):
        return f"<Usuario id={self.id} nombre='{self.nombre_usuario}'>"