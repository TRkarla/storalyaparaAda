# services/chat_service.py
from database.connection import SessionLocal
import models  # noqa: F401

from database.database_mensajes import (
    enviar_mensaje,
    obtener_conversacion,
    obtener_ultimos_contactos,
)
from database.database_usuarios import obtener_usuario_por_id
from utils.validators import validar_texto_no_vacio
from utils.constants import MAX_CONTENIDO_POEMA   # reutilizamos como límite


def _get_session():
    return SessionLocal()

LIMITE_MENSAJE = 1000


def enviar_mensaje_a_usuario(
    remitente_id: int,
    destinatario_id: int,
    contenido: str
) -> dict:
    """
    Envía un mensaje de un usuario a otro.

    Uso desde views/chat.py:
        resultado = enviar_mensaje_a_usuario(mi_id, su_id, "Hola!")
        if resultado["ok"]:
            mensaje = resultado["mensaje"]
    """
    ok, msg = validar_texto_no_vacio(contenido, "Mensaje")
    if not ok:
        return {"ok": False, "error": msg}

    if len(contenido) > LIMITE_MENSAJE:
        return {"ok": False, "error": f"El mensaje no puede superar {LIMITE_MENSAJE} caracteres"}

    if remitente_id == destinatario_id:
        return {"ok": False, "error": "No puedes enviarte mensajes a ti mismo"}

    db = _get_session()
    try:
        # Verificar que el destinatario exista
        destinatario = obtener_usuario_por_id(db, destinatario_id)
        if not destinatario or not destinatario.activo:
            return {"ok": False, "error": "El usuario destinatario no existe"}

        mensaje = enviar_mensaje(db, remitente_id, destinatario_id, contenido.strip())
        return {"ok": True, "mensaje": mensaje}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_chat(usuario_id: int, otro_usuario_id: int) -> dict:
    """
    Retorna la conversación completa entre dos usuarios.

    Uso desde views/chat.py al abrir una conversación:
        resultado = obtener_chat(mi_id, su_id)
        mensajes = resultado["mensajes"]
    """
    db = _get_session()
    try:
        mensajes = obtener_conversacion(db, usuario_id, otro_usuario_id)
        return {"ok": True, "mensajes": mensajes}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_lista_chats(usuario_id: int) -> dict:
    """
    Retorna los usuarios con quienes ha hablado, con sus datos.
    Ordenados por el mensaje más reciente.

    Uso desde views/chat.py para mostrar la lista de conversaciones:
        resultado = obtener_lista_chats(mi_id)
        contactos = resultado["contactos"]
        # cada contacto: {"usuario": <Usuario>, "ultimo_mensaje": <Mensaje>}
    """
    db = _get_session()
    try:
        ids_contactos = obtener_ultimos_contactos(db, usuario_id)
        contactos = []
        for contacto_id in ids_contactos:
            usuario = obtener_usuario_por_id(db, contacto_id)
            if usuario and usuario.activo:
                # Traer último mensaje entre ambos
                mensajes = obtener_conversacion(db, usuario_id, contacto_id)
                ultimo = mensajes[-1] if mensajes else None
                contactos.append({
                    "usuario": usuario,
                    "ultimo_mensaje": ultimo
                })
        return {"ok": True, "contactos": contactos}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()