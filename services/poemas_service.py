# services/poemas_service.py
from database.connection import SessionLocal
import models  # noqa: F401

from database.database_poemas import (
    publicar_poema,
    obtener_poemas_de_usuario,
    obtener_todos_los_poemas,
    obtener_poema_por_id,
    eliminar_poema,
)
from utils.validators import validar_texto_no_vacio
from utils.constants import MAX_CONTENIDO_POEMA


def _get_session():
    return SessionLocal()


def crear_poema(usuario_id: int, titulo: str, contenido: str) -> dict:
    """
    Publica un nuevo poema del usuario.

    Uso desde views/poems.py:
        resultado = crear_poema(usuario_id, "Mi poema", "Había una vez...")
        if resultado["ok"]:
            poema = resultado["poema"]
    """
    ok, msg = validar_texto_no_vacio(titulo, "Título")
    if not ok:
        return {"ok": False, "error": msg}

    ok, msg = validar_texto_no_vacio(contenido, "Contenido")
    if not ok:
        return {"ok": False, "error": msg}

    if len(contenido) > MAX_CONTENIDO_POEMA:
        return {
            "ok": False,
            "error": f"El poema no puede superar {MAX_CONTENIDO_POEMA} caracteres"
        }

    db = _get_session()
    try:
        poema = publicar_poema(
            db=db,
            titulo=titulo.strip(),
            contenido=contenido.strip(),
            usuario_id=usuario_id
        )
        return {"ok": True, "poema": poema}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_feed_poemas() -> dict:
    """
    Retorna todos los poemas para el feed de la comunidad.

    Uso desde views/poems.py:
        resultado = obtener_feed_poemas()
        poemas = resultado["poemas"]
    """
    db = _get_session()
    try:
        poemas = obtener_todos_los_poemas(db)
        return {"ok": True, "poemas": poemas}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_mis_poemas(usuario_id: int) -> dict:
    """Retorna los poemas escritos por el usuario."""
    db = _get_session()
    try:
        poemas = obtener_poemas_de_usuario(db, usuario_id)
        return {"ok": True, "poemas": poemas}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def eliminar_mi_poema(usuario_id: int, poema_id: int) -> dict:
    """Elimina un poema verificando que pertenezca al usuario."""
    db = _get_session()
    try:
        poema = obtener_poema_por_id(db, poema_id)
        if not poema:
            return {"ok": False, "error": "Poema no encontrado"}
        if poema.usuario_id != usuario_id:
            return {"ok": False, "error": "No tienes permiso para eliminar este poema"}

        eliminar_poema(db, poema_id)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()