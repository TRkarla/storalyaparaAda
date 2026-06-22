import flet as ft

def UploadBookView(page):

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Publicar libro",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),

                ft.ElevatedButton(
                    "Seleccionar foto 1"
                ),

                ft.ElevatedButton(
                    "Seleccionar foto 2"
                ),

                ft.Dropdown(
                    label="Tipo",
                    options=[
                        ft.dropdown.Option("Donación"),
                        ft.dropdown.Option("Intercambio")
                    ]
                ),

                ft.TextField(
                    label="Título del libro"
                ),

                ft.ElevatedButton(
                    "Publicar"
                )
            ]
        )
    )