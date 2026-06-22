# database/database_retos_asignados.py
from sqlalchemy.orm import Session
from models.reto_asignado import RetoAsignado


# ─── CREATE ───────────────────────────────────────────────────────
def asignar_reto_a_usuario(
    db: Session,
    usuario_id: int,
    reto_id: int
) -> RetoAsignado:
    nueva = RetoAsignado(
        usuario_id=usuario_id,
        reto_id=reto_id,
        estado="Pendiente"
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# ─── READ ─────────────────────────────────────────────────────────
def obtener_retos_por_usuario(
    db: Session,
    usuario_id: int
) -> list[RetoAsignado]:
    return db.query(RetoAsignado).filter(
        RetoAsignado.usuario_id == usuario_id
    ).all()


def obtener_reto_asignado_por_id(
    db: Session,
    asignacion_id: int
) -> RetoAsignado | None:
    return db.query(RetoAsignado).filter(
        RetoAsignado.id == asignacion_id
    ).first()


# ─── UPDATE ───────────────────────────────────────────────────────
def actualizar_estado_reto(
    db: Session,
    asignacion_id: int,
    nuevo_estado: str   # Pendiente, En progreso, Completado
) -> RetoAsignado | None:
    reto = obtener_reto_asignado_por_id(db, asignacion_id)
    if not reto:
        return None
    reto.estado = nuevo_estado
    db.commit()
    db.refresh(reto)
    return reto