# database/database_calificaciones.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.calificacion import Calificacion


# ─── CREATE ───────────────────────────────────────────────────────
def agregar_calificacion(
    db: Session,
    usuario_id: int,
    libro_id: int,
    estrellas: int,
    comentario: str = ""
) -> Calificacion | None:
    """
    Agrega una calificación de un usuario a un libro.
    Retorna None si el usuario ya calificó ese libro.
    """
    try:
        nueva = Calificacion(
            usuario_id=usuario_id,
            libro_id=libro_id,
            estrellas=estrellas,
            comentario=comentario
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    except IntegrityError:
        db.rollback()
        return None


# ─── READ ─────────────────────────────────────────────────────────
def obtener_calificaciones_de_libro(
    db: Session,
    libro_id: int
) -> list[Calificacion]:
    """Retorna todas las calificaciones de un libro."""
    return db.query(Calificacion).filter(
        Calificacion.libro_id == libro_id
    ).order_by(Calificacion.fecha.desc()).all()


def obtener_promedio_libro(db: Session, libro_id: int) -> float:
    """Calcula el promedio de estrellas de un libro. Retorna 0.0 si no hay."""
    from sqlalchemy import func
    resultado = db.query(
        func.avg(Calificacion.estrellas)
    ).filter(Calificacion.libro_id == libro_id).scalar()
    return round(float(resultado), 1) if resultado else 0.0


def obtener_calificacion_usuario_libro(
    db: Session,
    usuario_id: int,
    libro_id: int
) -> Calificacion | None:
    """Verifica si un usuario ya calificó un libro específico."""
    return db.query(Calificacion).filter(
        Calificacion.usuario_id == usuario_id,
        Calificacion.libro_id == libro_id
    ).first()


# ─── UPDATE ───────────────────────────────────────────────────────
def editar_calificacion(
    db: Session,
    calificacion_id: int,
    estrellas: int,
    comentario: str
) -> Calificacion | None:
    cal = db.query(Calificacion).filter(
        Calificacion.id == calificacion_id
    ).first()
    if not cal:
        return None
    cal.estrellas = estrellas
    cal.comentario = comentario
    db.commit()
    db.refresh(cal)
    return cal


# ─── DELETE ───────────────────────────────────────────────────────
def eliminar_calificacion(db: Session, calificacion_id: int) -> bool:
    cal = db.query(Calificacion).filter(
        Calificacion.id == calificacion_id
    ).first()
    if not cal:
        return False
    db.delete(cal)
    db.commit()
    return True