# database/database_libros.py
from sqlalchemy.orm import Session
from models.libro import Libro


# ─── CREATE ───────────────────────────────────────────────────────
def registrar_libro(
    db: Session,
    titulo: str,
    autor: str,
    usuario_id: int,
    genero: str = "",
    descripcion: str = "",
    tipo: str = "Intercambio"   # Intercambio | Donacion
) -> Libro:
    nuevo = Libro(
        titulo=titulo,
        autor=autor,
        usuario_id=usuario_id,
        genero=genero,
        descripcion=descripcion,
        tipo=tipo,
        estado="Disponible",
        disponible=True
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ─── READ ─────────────────────────────────────────────────────────
def obtener_libros_disponibles(db: Session) -> list[Libro]:
    return db.query(Libro).filter(Libro.disponible == True).all()


def obtener_libros_de_usuario(db: Session, usuario_id: int) -> list[Libro]:
    return db.query(Libro).filter(Libro.usuario_id == usuario_id).all()


def obtener_libro_por_id(db: Session, libro_id: int) -> Libro | None:
    return db.query(Libro).filter(Libro.id == libro_id).first()


def buscar_libros(db: Session, termino: str) -> list[Libro]:
    """Busca libros por título o autor."""
    filtro = f"%{termino}%"
    return db.query(Libro).filter(
        Libro.disponible == True,
        (Libro.titulo.ilike(filtro)) | (Libro.autor.ilike(filtro))
    ).all()


# ─── UPDATE ───────────────────────────────────────────────────────
def actualizar_disponibilidad(
    db: Session,
    libro_id: int,
    disponible: bool
) -> Libro | None:
    libro = obtener_libro_por_id(db, libro_id)
    if not libro:
        return None
    libro.disponible = disponible
    db.commit()
    db.refresh(libro)
    return libro


# ─── DELETE ───────────────────────────────────────────────────────
def eliminar_libro(db: Session, libro_id: int) -> bool:
    libro = obtener_libro_por_id(db, libro_id)
    if not libro:
        return False
    db.delete(libro)
    db.commit()
    return True