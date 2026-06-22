# database/database_imagenes.py
from sqlalchemy.orm import Session
from models.imagen import Imagen


# ─── CREATE ───────────────────────────────────────────────────────
def guardar_imagen_libro(
    db: Session,
    libro_id: int,
    url_imagen: str
) -> Imagen:
    nueva = Imagen(libro_id=libro_id, url=url_imagen)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# ─── READ ─────────────────────────────────────────────────────────
def obtener_imagenes_de_libro(db: Session, libro_id: int) -> list[Imagen]:
    """Retorna todas las imágenes asociadas a un libro."""
    return db.query(Imagen).filter(Imagen.libro_id == libro_id).all()


def obtener_imagen_principal(db: Session, libro_id: int) -> Imagen | None:
    """Retorna la primera imagen del libro (portada)."""
    return db.query(Imagen).filter(Imagen.libro_id == libro_id).first()


# ─── DELETE ───────────────────────────────────────────────────────
def eliminar_imagen(db: Session, imagen_id: int) -> bool:
    imagen = db.query(Imagen).filter(Imagen.id == imagen_id).first()
    if not imagen:
        return False
    db.delete(imagen)
    db.commit()
    return True


def eliminar_imagenes_de_libro(db: Session, libro_id: int) -> int:
    """Elimina todas las imágenes de un libro. Retorna cuántas eliminó."""
    cantidad = db.query(Imagen).filter(Imagen.libro_id == libro_id).delete()
    db.commit()
    return cantidad