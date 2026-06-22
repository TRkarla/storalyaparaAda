# database/database_intercambios.py
from sqlalchemy.orm import Session
from models.intercambio import Intercambio


# ─── CREATE ───────────────────────────────────────────────────────
def crear_intercambio(
    db: Session,
    libro_id: int,
    solicitante_id: int,
    propietario_id: int,
    lugar_acordado: str = ""
) -> Intercambio:
    nuevo = Intercambio(
        libro_id=libro_id,
        solicitante_id=solicitante_id,
        propietario_id=propietario_id,
        lugar_acordado=lugar_acordado,
        estado="Pendiente"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ─── READ ─────────────────────────────────────────────────────────
def obtener_intercambios_de_usuario(
    db: Session,
    usuario_id: int
) -> list[Intercambio]:
    """Retorna todos los intercambios donde el usuario participa."""
    return db.query(Intercambio).filter(
        (Intercambio.solicitante_id == usuario_id) |
        (Intercambio.propietario_id == usuario_id)
    ).order_by(Intercambio.fecha.desc()).all()


def obtener_intercambio_por_id(
    db: Session,
    intercambio_id: int
) -> Intercambio | None:
    return db.query(Intercambio).filter(
        Intercambio.id == intercambio_id
    ).first()


# ─── UPDATE ───────────────────────────────────────────────────────
def actualizar_estado_intercambio(
    db: Session,
    intercambio_id: int,
    nuevo_estado: str   # Pendiente, Aceptado, Finalizado
) -> Intercambio | None:
    intercambio = obtener_intercambio_por_id(db, intercambio_id)
    if not intercambio:
        return None
    intercambio.estado = nuevo_estado
    db.commit()
    db.refresh(intercambio)
    return intercambio