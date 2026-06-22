# services/usuarios_service.py
# ──────────────────────────────────────────────────────────────────
# Responsabilidad: Lógica de negocio de usuarios.
# Esta capa es la única que habla con database_usuarios.py
# Las views/ y los endpoints FastAPI SOLO llaman a este servicio.
# ──────────────────────────────────────────────────────────────────

# services/usuarios_service.py
import bcrypt
from sqlalchemy.orm import Session

from database.connection import SessionLocal
import models  # ← LÍNEA NUEVA: registra todos los modelos con SQLAlchemy

from database.database_usuarios import (
    crear_usuario,
    obtener_usuario_por_id,
    obtener_usuario_por_nombre,
    obtener_usuario_por_email,
    obtener_todos_los_usuarios,
    actualizar_usuario,
    actualizar_password,
    desactivar_usuario,
)
from models.usuario import Usuario
from utils.validators import validar_email, validar_password


# ─── Helpers internos de password ─────────────────────────────────

def _hashear_password(password_plano: str) -> str:
    """
    Convierte el password en texto plano a un hash seguro con bcrypt.
    El resultado es una cadena lista para guardar en la BD.
    """
    sal = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_plano.encode("utf-8"), sal)
    return hash_bytes.decode("utf-8")


def _verificar_password(password_plano: str, password_hash: str) -> bool:
    """
    Compara un password en texto plano contra el hash guardado en BD.
    Retorna True si coinciden, False si no.
    """
    return bcrypt.checkpw(
        password_plano.encode("utf-8"),
        password_hash.encode("utf-8")
    )


# ─── Helper interno de sesión ─────────────────────────────────────

def _get_session() -> Session:
    """Abre una sesión de BD para uso interno del servicio."""
    return SessionLocal()


# ─── REGISTRO ─────────────────────────────────────────────────────

def registrar_usuario(
    nombre_usuario: str,
    email: str,
    password_plano: str,
    edad: int,
    genero: str,
    ciudad: str,
    estado: str,
    telefono: str = "",    # ← NUEVO
) -> dict:
    """
    Registra un nuevo usuario en STORALYA.

    Retorna un dict con el resultado:
        {"ok": True,  "usuario": <Usuario>}
        {"ok": False, "error": "mensaje de error"}

    Uso desde views/registro_usuario.py:
        resultado = registrar_usuario("lector01", "a@b.com", "Pass123", 25, ...)
        if resultado["ok"]:
            usuario = resultado["usuario"]
        else:
            mostrar_error(resultado["error"])
    """
    # ── Validaciones antes de tocar la BD ─────────────────────────
    if not nombre_usuario or not nombre_usuario.strip():
        return {"ok": False, "error": "El nombre de usuario no puede estar vacío"}

    if len(nombre_usuario) < 3:
        return {"ok": False, "error": "El nombre de usuario debe tener al menos 3 caracteres"}

    if len(nombre_usuario) > 50:
        return {"ok": False, "error": "El nombre de usuario no puede superar 50 caracteres"}

    if not validar_email(email):
        return {"ok": False, "error": "El formato del email no es válido"}

    es_valida, msg_error = validar_password(password_plano)
    if not es_valida:
        return {"ok": False, "error": msg_error}

    if not isinstance(edad, int) or edad < 13 or edad > 120:
        return {"ok": False, "error": "La edad debe estar entre 13 y 120 años"}

    # ── Hashear password ANTES de guardar ─────────────────────────
    password_hash = _hashear_password(password_plano)

    # ── Intentar crear en BD ───────────────────────────────────────
    db = _get_session()
    try:
        usuario = crear_usuario(
    db=db,
    nombre_usuario=nombre_usuario.strip(),
    email=email.strip().lower(),
    password_hash=password_hash,
    edad=edad,
    genero=genero,
    ciudad=ciudad,
    estado=estado,
    telefono=telefono,    # ← NUEVO
)

        if usuario is None:
            # crear_usuario retorna None cuando hay duplicado
            return {
                "ok": False,
                "error": "El nombre de usuario o email ya está registrado"
            }

        return {"ok": True, "usuario": usuario}

    except Exception as e:
        return {"ok": False, "error": f"Error inesperado al registrar: {str(e)}"}
    finally:
        db.close()  # siempre cerramos la sesión


# ─── LOGIN ────────────────────────────────────────────────────────

def login_usuario(email_o_nombre: str, password_plano: str) -> dict:
    """
    Autentica un usuario por email O por nombre de usuario.

    Retorna:
        {"ok": True,  "usuario": <Usuario>}
        {"ok": False, "error": "mensaje"}

    Uso desde views/login.py:
        resultado = login_usuario("lector01", "MiPass123")
        if resultado["ok"]:
            usuario_activo = resultado["usuario"]
    """
    if not email_o_nombre or not password_plano:
        return {"ok": False, "error": "Completa todos los campos"}

    db = _get_session()
    try:
        # Intentar encontrar por email primero, luego por nombre
        usuario = None
        if "@" in email_o_nombre:
            usuario = obtener_usuario_por_email(db, email_o_nombre.strip().lower())
        else:
            usuario = obtener_usuario_por_nombre(db, email_o_nombre.strip())

        # Usuario no existe
        if usuario is None:
            return {"ok": False, "error": "Usuario o contraseña incorrectos"}

        # Usuario desactivado
        if not usuario.activo:
            return {"ok": False, "error": "Esta cuenta ha sido desactivada"}

        # Verificar password
        if not _verificar_password(password_plano, usuario.password):
            return {"ok": False, "error": "Usuario o contraseña incorrectos"}

        return {"ok": True, "usuario": usuario}

    except Exception as e:
        return {"ok": False, "error": f"Error inesperado al iniciar sesión: {str(e)}"}
    finally:
        db.close()


# ─── CONSULTAS ────────────────────────────────────────────────────

def obtener_perfil(usuario_id: int) -> dict:
    """
    Obtiene los datos de perfil de un usuario por su ID.

    Retorna:
        {"ok": True,  "usuario": <Usuario>}
        {"ok": False, "error": "mensaje"}
    """
    db = _get_session()
    try:
        usuario = obtener_usuario_por_id(db, usuario_id)
        if not usuario:
            return {"ok": False, "error": "Usuario no encontrado"}
        return {"ok": True, "usuario": usuario}
    finally:
        db.close()


def obtener_lista_usuarios() -> dict:
    """
    Retorna todos los usuarios activos.
    Útil para búsquedas, comunidad y chat.
    """
    db = _get_session()
    try:
        usuarios = obtener_todos_los_usuarios(db)
        return {"ok": True, "usuarios": usuarios}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


# ─── ACTUALIZACIÓN ────────────────────────────────────────────────

def editar_perfil(usuario_id: int, **campos) -> dict:
    """
    Actualiza campos del perfil de un usuario.

    Uso desde views/profile.py:
        resultado = editar_perfil(3, ciudad="Monterrey", estado="NL")
        if resultado["ok"]:
            mostrar_exito("Perfil actualizado")
    """
    if not campos:
        return {"ok": False, "error": "No se enviaron campos para actualizar"}

    db = _get_session()
    try:
        usuario = actualizar_usuario(db, usuario_id, **campos)
        if not usuario:
            return {"ok": False, "error": "Usuario no encontrado"}
        return {"ok": True, "usuario": usuario}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


def cambiar_password(usuario_id: int, password_actual: str, password_nuevo: str) -> dict:
    """
    Cambia el password verificando primero el actual.

    Retorna:
        {"ok": True}
        {"ok": False, "error": "mensaje"}
    """
    # Validar que el nuevo password sea seguro
    es_valida, msg_error = validar_password(password_nuevo)
    if not es_valida:
        return {"ok": False, "error": msg_error}

    db = _get_session()
    try:
        usuario = obtener_usuario_por_id(db, usuario_id)
        if not usuario:
            return {"ok": False, "error": "Usuario no encontrado"}

        # Verificar que el password actual sea correcto
        if not _verificar_password(password_actual, usuario.password):
            return {"ok": False, "error": "La contraseña actual es incorrecta"}

        nuevo_hash = _hashear_password(password_nuevo)
        actualizar_password(db, usuario_id, nuevo_hash)
        return {"ok": True}

    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


# ─── DESACTIVAR CUENTA ────────────────────────────────────────────

def eliminar_cuenta(usuario_id: int, password_confirmacion: str) -> dict:
    """
    Desactiva la cuenta del usuario (soft delete).
    Requiere confirmar el password por seguridad.
    """
    db = _get_session()
    try:
        usuario = obtener_usuario_por_id(db, usuario_id)
        if not usuario:
            return {"ok": False, "error": "Usuario no encontrado"}

        if not _verificar_password(password_confirmacion, usuario.password):
            return {"ok": False, "error": "Contraseña incorrecta"}

        desactivar_usuario(db, usuario_id)
        return {"ok": True}

    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()