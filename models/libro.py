# models/libro.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.connection import Base


class Libro(Base):
    __tablename__ = "libros"

    id          = Column(Integer, primary_key=True, index=True)
    titulo      = Column(String(150), nullable=False)
    autor       = Column(String(100), nullable=False)
    genero      = Column(String(50))
    descripcion = Column(Text, nullable=True)                        # ← NUEVO
    tipo        = Column(String(20), default="Intercambio")          # ← NUEVO: Intercambio, Donacion
    estado      = Column(String(20), default="Disponible")
    disponible  = Column(Boolean, default=True)                      # ← NUEVO
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"))

    propietario    = relationship("Usuario",      back_populates="libros")
    imagenes       = relationship("Imagen",       back_populates="libro")
    calificaciones = relationship("Calificacion", back_populates="libro")
    intercambios   = relationship("Intercambio",  back_populates="libro")

    def __repr__(self):
        return f"<Libro id={self.id} titulo='{self.titulo}'>"