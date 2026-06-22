# services/auth_service.py
# ──────────────────────────────────────────────────────────────────
# Responsabilidad: Manejo de la sesión activa del usuario en la app.
# Guarda en memoria quién está logueado actualmente.
# No hace operaciones de BD — eso es responsabilidad de
# usuarios_service.py. Este servicio es el "estado global" de sesión.
# ──────────────────────────────────────────────────────────────────

from models.usuario import Usuario


# ─── Estado de sesión (en memoria mientras la app está abierta) ───
_usuario_activo: Usuario | None = None


def iniciar_sesion(usuario: Usuario) -> None:
    """
    Guarda el usuario logueado en memoria.
    Llamar DESPUÉS de que usuarios_service.login_usuario() sea exitoso.

    Uso desde views/login.py:
        resultado = login_usuario(email, password)
        if resultado["ok"]:
            iniciar_sesion(resultado["usuario"])
            # navegar a home
    """
    global _usuario_activo
    _usuario_activo = usuario


def cerrar_sesion() -> None:
    """
    Limpia la sesión activa.

    Uso desde components/navbar.py o views/profile.py:
        cerrar_sesion()
        # navegar a login
    """
    global _usuario_activo
    _usuario_activo = None


def obtener_usuario_activo() -> Usuario | None:
    """
    Retorna el usuario actualmente logueado, o None si no hay sesión.

    Uso en cualquier view o componente que necesite saber quién es el usuario:
        usuario = obtener_usuario_activo()
        if not usuario:
            # redirigir a login
        else:
            print(f"Bienvenido {usuario.nombre_usuario}")
    """
    return _usuario_activo


def hay_sesion_activa() -> bool:
    """Retorna True si hay un usuario logueado."""
    return _usuario_activo is not None


def obtener_id_activo() -> int | None:
    """
    Retorna solo el ID del usuario activo.
    Útil para operaciones de BD sin cargar el objeto completo.

    Uso en services/ cuando necesitas el id:
        usuario_id = obtener_id_activo()
        if usuario_id:
            resultado = obtener_mis_libros(usuario_id)
    """
    return _usuario_activo.id if _usuario_activo else None