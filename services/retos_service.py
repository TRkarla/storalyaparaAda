# services/retos_service.py
from database.connection import SessionLocal
import models  # noqa: F401

from database.database_retos_asignados import (
    asignar_reto_a_usuario,
    obtener_retos_por_usuario,
    actualizar_estado_reto,
    obtener_reto_asignado_por_id,
)
from database.database_retos_cumplidos import (
    registrar_cumplimiento_reto,
    obtener_historial_retos_usuario,
    usuario_ya_cumplio_reto,
)


def _get_session():
    return SessionLocal()


def asignar_reto(usuario_id: int, reto_id: int) -> dict:
    """
    Asigna un reto a un usuario si no lo tiene ya asignado.

    Uso desde views/profile.py o donde se muestren retos:
        resultado = asignar_reto(usuario_id, reto_id)
    """
    db = _get_session()
    try:
        # Verificar si ya lo completó antes
        if usuario_ya_cumplio_reto(db, usuario_id, reto_id):
            return {"ok": False, "error": "Ya completaste este reto anteriormente"}

        # Verificar si ya lo tiene asignado
        retos_actuales = obtener_retos_por_usuario(db, usuario_id)
        ya_asignado = any(
            r.reto_id == reto_id and r.estado != "Completado"
            for r in retos_actuales
        )
        if ya_asignado:
            return {"ok": False, "error": "Ya tienes este reto asignado"}

        nuevo = asignar_reto_a_usuario(db, usuario_id, reto_id)
        return {"ok": True, "reto_asignado": nuevo}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_retos_activos(usuario_id: int) -> dict:
    """
    Retorna los retos pendientes y en progreso del usuario.

    Uso desde views/profile.py:
        resultado = obtener_retos_activos(usuario_id)
        retos = resultado["retos"]
    """
    db = _get_session()
    try:
        todos = obtener_retos_por_usuario(db, usuario_id)
        activos = [r for r in todos if r.estado != "Completado"]
        return {"ok": True, "retos": activos}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def completar_reto(usuario_id: int, asignacion_id: int) -> dict:
    """
    Marca un reto como completado y lo registra en el historial.

    Uso desde views/profile.py:
        resultado = completar_reto(usuario_id, asignacion_id)
    """
    db = _get_session()
    try:
        asignacion = obtener_reto_asignado_por_id(db, asignacion_id)
        if not asignacion:
            return {"ok": False, "error": "Reto asignado no encontrado"}
        if asignacion.usuario_id != usuario_id:
            return {"ok": False, "error": "No tienes permiso para completar este reto"}
        if asignacion.estado == "Completado":
            return {"ok": False, "error": "Este reto ya fue completado"}

        # Actualizar estado
        actualizar_estado_reto(db, asignacion_id, "Completado")

        # Registrar en historial de cumplidos
        registrar_cumplimiento_reto(db, usuario_id, asignacion.reto_id)

        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_historial(usuario_id: int) -> dict:
    """Retorna todos los retos completados por el usuario."""
    db = _get_session()
    try:
        historial = obtener_historial_retos_usuario(db, usuario_id)
        return {"ok": True, "historial": historial}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()