# database/database_mensajes.py
from sqlalchemy.orm import Session
from models.mensaje import Mensaje


# ─── CREATE ───────────────────────────────────────────────────────
def enviar_mensaje(
    db: Session,
    remitente_id: int,
    destinatario_id: int,
    contenido: str
) -> Mensaje:
    nuevo = Mensaje(
        remitente_id=remitente_id,
        destinatario_id=destinatario_id,
        contenido=contenido
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ─── READ ─────────────────────────────────────────────────────────
def obtener_conversacion(
    db: Session,
    usuario_a: int,
    usuario_b: int
) -> list[Mensaje]:
    """Retorna todos los mensajes entre dos usuarios ordenados por fecha."""
    return db.query(Mensaje).filter(
        ((Mensaje.remitente_id == usuario_a) & (Mensaje.destinatario_id == usuario_b)) |
        ((Mensaje.remitente_id == usuario_b) & (Mensaje.destinatario_id == usuario_a))
    ).order_by(Mensaje.fecha_envio.asc()).all()


def obtener_ultimos_contactos(db: Session, usuario_id: int) -> list[int]:
    """
    Retorna IDs de usuarios con quienes el usuario ha hablado,
    ordenados por el mensaje más reciente.
    """
    from sqlalchemy import func, or_
    subq = db.query(
        func.max(Mensaje.id).label("ultimo")
    ).filter(
        or_(
            Mensaje.remitente_id == usuario_id,
            Mensaje.destinatario_id == usuario_id
        )
    ).group_by(
        func.least(Mensaje.remitente_id, Mensaje.destinatario_id),
        func.greatest(Mensaje.remitente_id, Mensaje.destinatario_id)
    ).subquery()

    mensajes = db.query(Mensaje).join(
        subq, Mensaje.id == subq.c.ultimo
    ).order_by(Mensaje.fecha_envio.desc()).all()

    contactos = []
    for m in mensajes:
        otro = m.destinatario_id if m.remitente_id == usuario_id else m.remitente_id
        if otro not in contactos:
            contactos.append(otro)
    return contactos