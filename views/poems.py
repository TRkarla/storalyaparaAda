import flet as ft

def PoemsView(page):

    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Muro de poemas",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "lunah",
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    "En la quietud de esta noche..."
                                ),

                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.FAVORITE_BORDER
                                        ),
                                        ft.Text("24")
                                    ]
                                )
                            ]
                        )
                    )
                )
            ]
        )
    )