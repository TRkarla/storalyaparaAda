# database/database_poemas.py
from sqlalchemy.orm import Session
from models.poema import Poema


# ─── CREATE ───────────────────────────────────────────────────────
def publicar_poema(
    db: Session,
    titulo: str,
    contenido: str,
    usuario_id: int   # ← corregido: era autor_id
) -> Poema:
    nuevo = Poema(titulo=titulo, contenido=contenido, usuario_id=usuario_id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ─── READ ─────────────────────────────────────────────────────────
def obtener_poemas_de_usuario(db: Session, usuario_id: int) -> list[Poema]:
    return db.query(Poema).filter(
        Poema.usuario_id == usuario_id
    ).order_by(Poema.fecha_creacion.desc()).all()


def obtener_todos_los_poemas(db: Session) -> list[Poema]:
    return db.query(Poema).order_by(Poema.fecha_creacion.desc()).all()


def obtener_poema_por_id(db: Session, poema_id: int) -> Poema | None:
    return db.query(Poema).filter(Poema.id == poema_id).first()


# ─── DELETE ───────────────────────────────────────────────────────
def eliminar_poema(db: Session, poema_id: int) -> bool:
    poema = obtener_poema_por_id(db, poema_id)
    if not poema:
        return False
    db.delete(poema)
    db.commit()
    return True