# components/bottom_nav.py
import flet as ft
from themes.colors import LAVANDA, TEXTO_SECUNDARIO, FONDO_TARJETA, BORDE_INPUT


def bottom_nav(page: ft.Page, vista_activa: str, navegador: dict) -> ft.Container:

    def item_nav(icono: str, label: str, clave: str):
        activo = vista_activa == clave
        color  = LAVANDA if activo else TEXTO_SECUNDARIO

        if clave == "publicar":
            return ft.GestureDetector(
                on_tap=lambda e: navegador.get(clave, lambda: None)(),
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Icon("edit_outlined", color="#FFFFFF", size=20),
                            bgcolor=LAVANDA,
                            border_radius=26,
                            width=52,
                            height=52,
                        ),
                        ft.Text(
                            label,
                            size=10,
                            color=LAVANDA,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
            )

        return ft.GestureDetector(
            on_tap=lambda e, c=clave: navegador.get(c, lambda: None)(),
            content=ft.Column(
                controls=[
                    ft.Icon(icono, color=color, size=22),
                    ft.Text(
                        label,
                        size=10,
                        color=color,
                        weight=ft.FontWeight.W_500 if activo else ft.FontWeight.W_400,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
        )

    return ft.Container(
        content=ft.Row(
            controls=[
                item_nav("home_outlined",      "Inicio",     "poemas"),
                item_nav("menu_book_outlined", "Biblioteca", "biblioteca"),
                item_nav("edit_outlined",      "Publicar",   "publicar"),
                item_nav("people_outline",     "Comunidad",  "comunidad"),
                item_nav("person_outline",     "Perfil",     "perfil"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=FONDO_TARJETA,
        padding=ft.Padding(left=8, right=8, top=10, bottom=20),
        border=ft.Border(
            top=ft.BorderSide(1, BORDE_INPUT),
            bottom=ft.BorderSide(0, "transparent"),
            left=ft.BorderSide(0, "transparent"),
            right=ft.BorderSide(0, "transparent"),
        ),
        height=72,
    )