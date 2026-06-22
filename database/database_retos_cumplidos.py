# database/database_retos_cumplidos.py
from sqlalchemy.orm import Session
from models.reto_cumplido import RetoCumplido


# ─── CREATE ───────────────────────────────────────────────────────
def registrar_cumplimiento_reto(
    db: Session,
    usuario_id: int,
    reto_id: int
) -> RetoCumplido:
    nuevo = RetoCumplido(usuario_id=usuario_id, reto_id=reto_id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ─── READ ─────────────────────────────────────────────────────────
def obtener_historial_retos_usuario(
    db: Session,
    usuario_id: int
) -> list[RetoCumplido]:
    return db.query(RetoCumplido).filter(
        RetoCumplido.usuario_id == usuario_id
    ).order_by(RetoCumplido.fecha_completado.desc()).all()


def usuario_ya_cumplio_reto(
    db: Session,
    usuario_id: int,
    reto_id: int
) -> bool:
    """Verifica si un usuario ya completó un reto específico."""
    return db.query(RetoCumplido).filter(
        RetoCumplido.usuario_id == usuario_id,
        RetoCumplido.reto_id == reto_id
    ).first() is not None