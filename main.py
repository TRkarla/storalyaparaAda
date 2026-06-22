import flet as ft
from views.splash import splash_view
from views.login import login_view
from views.registro_usuario import registro_view


def main(page: ft.Page):
    # ─── Configuración general ────────────────────────────────────
    page.title        = "STORALYA"
    page.bgcolor      = "#F7F0F5"
    page.padding      = 0
    page.window.width  = 390
    page.window.height = 844
    page.window.resizable = False

    # ─── Funciones de navegación ──────────────────────────────────
    def mostrar_splash():
        page.controls.clear()
        page.add(splash_view(page, mostrar_registro, mostrar_login))
        page.update()

    def mostrar_login():
        page.controls.clear()
        page.add(login_view(page, mostrar_registro, mostrar_home))
        page.update()

    def mostrar_registro():
        page.controls.clear()
        page.add(registro_view(page, mostrar_login, mostrar_home))
        page.update()

    def mostrar_home():
        page.controls.clear()
        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#F0E8F5", "#FCF0F5", "#EFF7F8"],
                ),
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "🏠 Home",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#3D2C5E",
                        ),
                        ft.Text("Próximamente...", color="#7A6E8A"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
            )
        )
        page.update()

    # ─── Arranque ─────────────────────────────────────────────────
    mostrar_splash()


ft.app(main)