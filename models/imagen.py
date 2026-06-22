from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, index=True)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    url = Column(String(500), nullable=False) # Guardamos la ruta o URL de la imagen

    # Relación para volver al libro
    libro = relationship("Libro", back_populates="imagenes")