import flet as ft

def ChatView(page):

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Chat",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Chip(label=ft.Text("¿Sigue disponible?")),
                ft.Chip(label=ft.Text("Acepto el intercambio")),
                ft.Chip(label=ft.Text("¿Dónde podemos reunirnos?")),
                ft.Chip(label=ft.Text("Gracias por la donación"))
            ]
        )
    )