# views/login.py
import flet as ft
from services.usuarios_service import login_usuario
from services.auth_service import iniciar_sesion
from themes.colors import LAVANDA, TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, BORDE_INPUT, FONDO_INPUT


def login_view(page: ft.Page, ir_a_registro, ir_a_home) -> ft.Column:
    w = int(page.window.width or 390)
    h = int(page.window.height or 844)

    campo_contacto = ft.TextField(
        label="Email o número de teléfono",
        hint_text="tucorreo@email.com o 10 dígitos",
        prefix_icon="person_outline",
        border_radius=20, border_color=BORDE_INPUT,
        focused_border_color=LAVANDA, bgcolor=FONDO_INPUT, filled=True,
        label_style=ft.TextStyle(color=TEXTO_SECUNDARIO, weight=ft.FontWeight.BOLD),
        text_style=ft.TextStyle(color=TEXTO_PRINCIPAL), cursor_color=LAVANDA,
    )
    campo_password = ft.TextField(
        label="Contraseña", hint_text="Tu contraseña",
        prefix_icon="lock_outline", password=True, can_reveal_password=True,
        border_radius=20, border_color=BORDE_INPUT,
        focused_border_color=LAVANDA, bgcolor=FONDO_INPUT, filled=True,
        label_style=ft.TextStyle(color=TEXTO_SECUNDARIO, weight=ft.FontWeight.BOLD),
        text_style=ft.TextStyle(color=TEXTO_PRINCIPAL), cursor_color=LAVANDA,
    )
    msg_error = ft.Text("", size=12, color="#E07B8A", visible=False)

    def handle_login(e):
        msg_error.visible = False
        contacto = campo_contacto.value.strip() if campo_contacto.value else ""
        password  = campo_password.value
        if not contacto or not password:
            msg_error.value = "Completa todos los campos"
            msg_error.visible = True
            page.update()
            return
        resultado = login_usuario(contacto, password)
        if resultado["ok"]:
            iniciar_sesion(resultado["usuario"])
            ir_a_home()
        else:
            msg_error.value = resultado["error"]
            msg_error.visible = True
            campo_password.value = ""
            page.update()

    return ft.Column(
        width=w, height=h,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(height=32),
            ft.Image(src="assets/logo/logo.png", width=160, fit="contain"),
            ft.Container(height=8),
            ft.Text("Bienvenido de vuelta", size=22, weight=ft.FontWeight.BOLD,
                    color=TEXTO_PRINCIPAL, text_align=ft.TextAlign.CENTER),
            ft.Text("Lectura que conecta, historias que permanecen.",
                    size=13, color=TEXTO_SECUNDARIO, text_align=ft.TextAlign.CENTER),
            ft.Container(height=24),
            campo_contacto,
            ft.Container(height=12),
            campo_password,
            ft.Container(height=4),
            msg_error,
            ft.Container(height=20),
            ft.GestureDetector(
                on_tap=handle_login,
                content=ft.Container(
                    content=ft.Text("Inicia sesión →", color="#FFF", size=15,
                                    weight=ft.FontWeight.W_500,
                                    text_align=ft.TextAlign.CENTER),
                    bgcolor=LAVANDA, border_radius=30,
                    padding=ft.Padding(left=32, right=32, top=14, bottom=14),
                    width=w - 64,
                ),
            ),
            ft.Container(height=12),
            ft.GestureDetector(
                on_tap=lambda e: ir_a_registro(),
                content=ft.Container(
                    content=ft.Text("Crear cuenta →", color=TEXTO_PRINCIPAL, size=15,
                                    weight=ft.FontWeight.W_500,
                                    text_align=ft.TextAlign.CENTER),
                    border=ft.Border(
                        top=ft.BorderSide(1.5, BORDE_INPUT),
                        bottom=ft.BorderSide(1.5, BORDE_INPUT),
                        left=ft.BorderSide(1.5, BORDE_INPUT),
                        right=ft.BorderSide(1.5, BORDE_INPUT),
                    ),
                    border_radius=30, bgcolor="#FFFFFF",
                    padding=ft.Padding(left=32, right=32, top=14, bottom=14),
                    width=w - 64,
                ),
            ),
            ft.Container(height=24),
        ],
    )