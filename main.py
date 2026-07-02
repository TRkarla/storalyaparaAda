# main.py
import flet as ft
from views.splash import splash_view
from views.login import login_view
from views.registro_usuario import registro_view
from views.poems import poems_view


def main(page: ft.Page):
    page.title        = "STORALYA"
    page.bgcolor      = "#F7F0F5"
    page.padding      = 0
    page.spacing      = 0
    page.window.width  = 390
    page.window.height = 844
    page.window.resizable = False

    vista_actual = ["splash"]

    def get_wh():
        w = int(page.window.width or 390)
        h = int(page.window.height or 844)
        return w, h

    def limpiar():
        page.controls.clear()
        page.overlay.clear()

    def build(e=None):
        w, h = get_wh()
        limpiar()
        nombre = vista_actual[0]

        if nombre == "splash":
            vista = splash_view(page, ir_registro, ir_login)
        elif nombre == "login":
            vista = login_view(page, ir_registro, ir_poemas)
        elif nombre == "registro":
            vista = registro_view(page, ir_login, ir_poemas)
        elif nombre == "poemas":
            navegador = {
                "poemas":     ir_poemas,
                "biblioteca": lambda: None,
                "publicar":   ir_poemas,
                "comunidad":  lambda: None,
                "perfil":     lambda: None,
            }
            vista = poems_view(page, navegador, w, h)
        else:
            vista = ft.Text("Vista no encontrada")

        vista.width  = w
        vista.height = h
        page.add(ft.Column(
            controls=[vista],
            width=w,
            height=h,
            spacing=0,
        ))
        page.update()

    def ir_splash():
        vista_actual[0] = "splash"
        build()

    def ir_login():
        vista_actual[0] = "login"
        build()

    def ir_registro():
        vista_actual[0] = "registro"
        build()

    def ir_poemas():
        vista_actual[0] = "poemas"
        build()

    page.on_resize = build
    build()


ft.app(main)