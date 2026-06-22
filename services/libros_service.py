# services/libros_service.py
from database.connection import SessionLocal
import models  # noqa: F401

from database.database_libros import (
    registrar_libro,
    obtener_libros_disponibles,
    obtener_libros_de_usuario,
    obtener_libro_por_id,
    buscar_libros,
    actualizar_disponibilidad,
    eliminar_libro,
)
from database.database_imagenes import (
    guardar_imagen_libro,
    obtener_imagenes_de_libro,
    eliminar_imagenes_de_libro,
)
from database.database_calificaciones import (
    agregar_calificacion,
    obtener_calificaciones_de_libro,
    obtener_promedio_libro,
    obtener_calificacion_usuario_libro,
    editar_calificacion,
)
from utils.validators import validar_texto_no_vacio


def _get_session():
    return SessionLocal()


# ─── LIBROS ───────────────────────────────────────────────────────

def publicar_libro(
    usuario_id: int,
    titulo: str,
    autor: str,
    genero: str,
    descripcion: str,
    tipo: str,              # "Intercambio" | "Donacion"
    urls_imagenes: list[str] = []
) -> dict:
    """
    Publica un libro en el marketplace.
    Opcionalmente guarda sus imágenes.

    Uso desde views/upload_book.py:
        resultado = publicar_libro(usuario_id, "El Principito", ...)
        if resultado["ok"]:
            libro = resultado["libro"]
    """
    ok, msg = validar_texto_no_vacio(titulo, "Título")
    if not ok:
        return {"ok": False, "error": msg}

    ok, msg = validar_texto_no_vacio(autor, "Autor")
    if not ok:
        return {"ok": False, "error": msg}

    if tipo not in ("Intercambio", "Donacion"):
        return {"ok": False, "error": "El tipo debe ser 'Intercambio' o 'Donacion'"}

    db = _get_session()
    try:
        libro = registrar_libro(
            db=db,
            titulo=titulo.strip(),
            autor=autor.strip(),
            usuario_id=usuario_id,
            genero=genero,
            descripcion=descripcion,
            tipo=tipo,
        )
        # Guardar imágenes si las hay
        for url in urls_imagenes[:5]:   # máximo 5 por constants.py
            guardar_imagen_libro(db, libro.id, url)

        return {"ok": True, "libro": libro}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_marketplace(busqueda: str = "") -> dict:
    """
    Retorna libros disponibles para el marketplace.
    Si se pasa búsqueda, filtra por título o autor.

    Uso desde views/marketplace.py:
        resultado = obtener_marketplace("Cortázar")
        libros = resultado["libros"]
    """
    db = _get_session()
    try:
        if busqueda.strip():
            libros = buscar_libros(db, busqueda.strip())
        else:
            libros = obtener_libros_disponibles(db)
        return {"ok": True, "libros": libros}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_mis_libros(usuario_id: int) -> dict:
    """Retorna todos los libros publicados por el usuario."""
    db = _get_session()
    try:
        libros = obtener_libros_de_usuario(db, usuario_id)
        return {"ok": True, "libros": libros}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_detalle_libro(libro_id: int) -> dict:
    """
    Retorna un libro con sus imágenes y promedio de calificación.

    Uso desde components/book_card.py al hacer clic en un libro:
        resultado = obtener_detalle_libro(libro_id)
        libro     = resultado["libro"]
        imagenes  = resultado["imagenes"]
        promedio  = resultado["promedio"]
    """
    db = _get_session()
    try:
        libro = obtener_libro_por_id(db, libro_id)
        if not libro:
            return {"ok": False, "error": "Libro no encontrado"}

        imagenes = obtener_imagenes_de_libro(db, libro_id)
        promedio = obtener_promedio_libro(db, libro_id)

        return {
            "ok": True,
            "libro": libro,
            "imagenes": imagenes,
            "promedio": promedio,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def eliminar_mi_libro(usuario_id: int, libro_id: int) -> dict:
    """Elimina un libro verificando que pertenezca al usuario."""
    db = _get_session()
    try:
        libro = obtener_libro_por_id(db, libro_id)
        if not libro:
            return {"ok": False, "error": "Libro no encontrado"}
        if libro.usuario_id != usuario_id:
            return {"ok": False, "error": "No tienes permiso para eliminar este libro"}

        eliminar_imagenes_de_libro(db, libro_id)
        eliminar_libro(db, libro_id)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


# ─── CALIFICACIONES ───────────────────────────────────────────────

def calificar_libro(
    usuario_id: int,
    libro_id: int,
    estrellas: int,
    comentario: str = ""
) -> dict:
    """
    Califica un libro del 1 al 5.
    Si ya lo calificó, actualiza la calificación existente.

    Uso desde components/rating_stars.py:
        resultado = calificar_libro(usuario_id, libro_id, 4, "Muy bueno")
    """
    if not 1 <= estrellas <= 5:
        return {"ok": False, "error": "Las estrellas deben ser entre 1 y 5"}

    db = _get_session()
    try:
        # Verificar si ya calificó
        existente = obtener_calificacion_usuario_libro(db, usuario_id, libro_id)
        if existente:
            cal = editar_calificacion(db, existente.id, estrellas, comentario)
        else:
            cal = agregar_calificacion(db, usuario_id, libro_id, estrellas, comentario)

        return {"ok": True, "calificacion": cal}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def obtener_resenas_libro(libro_id: int) -> dict:
    """Retorna todas las reseñas y el promedio de un libro."""
    db = _get_session()
    try:
        calificaciones = obtener_calificaciones_de_libro(db, libro_id)
        promedio       = obtener_promedio_libro(db, libro_id)
        return {"ok": True, "calificaciones": calificaciones, "promedio": promedio}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()