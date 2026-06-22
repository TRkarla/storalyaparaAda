import flet as ft

def MarketplaceView(page):

    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Biblioteca",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    width=70,
                                    height=100,
                                    bgcolor="#ABA4C6",
                                    border_radius=10
                                ),

                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "El susurro de las hojas",
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text("Disponible"),
                                        ft.Text("Intercambio")
                                    ]
                                )
                            ]
                        )
                    )
                )
            ]
        )
    )