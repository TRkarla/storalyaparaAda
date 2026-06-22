# views/login.py
import flet as ft
from services.usuarios_service import login_usuario
from services.auth_service import iniciar_sesion
from themes.styles import (
    input_redondeado, boton_primario, boton_secundario,
    texto_titulo, texto_subtitulo, texto_error,
    GRADIENTE_FONDO,
)
from themes.colors import FONDO_APP, TEXTO_SECUNDARIO, LAVANDA

def login_view(page, ir_a_registro, ir_a_home):
    """
    Pantalla de inicio de sesión.

    Args:
        page:           instancia de la página Flet
        ir_a_registro:  función que navega a registro
        ir_a_home:      función que navega al home tras login exitoso
    """

    # ─── Campos ───────────────────────────────────────────────────
    campo_email = input_redondeado(
        "Email o nombre de usuario",
        hint="Ingresa tu email o usuario",
        icono="person_outline",
    )
    campo_password = input_redondeado(
        "Contraseña",
        hint="Ingresa tu contraseña",
        password=True,
        icono="lock_outline",
    )
    mensaje_error = texto_error("")

    # ─── Lógica ───────────────────────────────────────────────────
    def handle_login(e):
        mensaje_error.visible = False
        campo_email.border_color = None
        campo_password.border_color = None

        email    = campo_email.value.strip()
        password = campo_password.value

        if not email or not password:
            mensaje_error.value   = "Completa todos los campos"
            mensaje_error.visible = True
            page.update()
            return

        resultado = login_usuario(email, password)

        if resultado["ok"]:
            iniciar_sesion(resultado["usuario"])
            ir_a_home()
        else:
            mensaje_error.value   = resultado["error"]
            mensaje_error.visible = True
            campo_password.value  = ""
            page.update()

    # ─── UI ───────────────────────────────────────────────────────
    logo = ft.Image(
        src="assets/logo/logo.png",
        width=180,
        fit="contain",
    )

    contenido = ft.Column(
        controls=[
            ft.Container(height=20),
            logo,
            ft.Container(height=8),
            texto_titulo("Bienvenido de vuelta", size=22),
            texto_subtitulo("Lectura que conecta, Historias que permanecen."),
            ft.Container(height=24),
            campo_email,
            ft.Container(height=12),
            campo_password,
            ft.Container(height=4),
            mensaje_error,
            ft.Container(height=20),
            boton_primario("Inicia sesión →", handle_login),
            ft.Container(height=12),
            boton_secundario("Crear cuenta →", lambda _: ir_a_registro()),
            ft.Container(height=24),
            ft.TextButton(
                "¿Olvidaste tu contraseña?",
                style=ft.ButtonStyle(color=TEXTO_SECUNDARIO),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.Container(
        expand=True,
        gradient=GRADIENTE_FONDO,   # ← aquí
        content=ft.Container(
            content=contenido,
            padding=ft.Padding(left=32, right=32, top=24, bottom=24),
            expand=True,
        ),
    )