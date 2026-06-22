import flet as ft

class BookCard(ft.Card):
    def __init__(
        self,
        titulo,
        autor,
        tipo,
        disponible=True
    ):
        super().__init__()

        estado = "Disponible" if disponible else "No disponible"

        self.content = ft.Container(
            padding=15,
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=70,
                        height=100,
                        border_radius=10,
                        bgcolor="#ABA4C6"
                    ),

                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Text(
                                titulo,
                                weight=ft.FontWeight.BOLD,
                                size=18
                            ),

                            ft.Text(autor),

                            ft.Text(f"Tipo: {tipo}"),

                            ft.Text(estado)
                        ]
                    )
                ]
            )
        )