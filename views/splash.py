# views/splash.py
import flet as ft
from themes.colors import TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, LAVANDA, BORDE_INPUT


def splash_view(page: ft.Page, ir_a_registro, ir_a_login) -> ft.Column:
    w = int(page.window.width or 390)
    h = int(page.window.height or 844)

    return ft.Column(
        width=w, height=h,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        controls=[
            ft.Container(expand=True),
            ft.Image(src="assets/logo/logo.png", width=220, fit="contain"),
            ft.Container(height=16),
            ft.Column(controls=[
                ft.Text("Lectura que conecta,", size=16, color=TEXTO_SECUNDARIO,
                        text_align=ft.TextAlign.CENTER, italic=True),
                ft.Text("Historias que permanecen.", size=16, color="#C49ABF",
                        text_align=ft.TextAlign.CENTER, italic=True),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            ft.Container(expand=True),
            ft.GestureDetector(
                on_tap=lambda e: ir_a_registro(),
                content=ft.Container(
                    width=300,
                    content=ft.Row(controls=[
                        ft.Text("Crear cuenta", color="#FFF", size=16,
                                weight=ft.FontWeight.W_500),
                        ft.Text("→", color="#FFF", size=16),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=LAVANDA, border_radius=30,
                    padding=ft.Padding(left=28, right=28, top=16, bottom=16),
                ),
            ),
            ft.Container(height=12),
            ft.GestureDetector(
                on_tap=lambda e: ir_a_login(),
                content=ft.Container(
                    width=300,
                    content=ft.Row(controls=[
                        ft.Text("Inicia sesión", color=TEXTO_PRINCIPAL, size=16,
                                weight=ft.FontWeight.W_500),
                        ft.Text("→", color=TEXTO_PRINCIPAL, size=16),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    border=ft.Border(
                        top=ft.BorderSide(1.5, BORDE_INPUT),
                        bottom=ft.BorderSide(1.5, BORDE_INPUT),
                        left=ft.BorderSide(1.5, BORDE_INPUT),
                        right=ft.BorderSide(1.5, BORDE_INPUT),
                    ),
                    border_radius=30, bgcolor="#FFFFFF",
                    padding=ft.Padding(left=28, right=28, top=16, bottom=16),
                ),
            ),
            ft.Container(height=48),
        ],
    )