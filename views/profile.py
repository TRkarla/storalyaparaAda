import flet as ft

def ProfileView(page):

    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.CircleAvatar(
                    radius=50,
                    content=ft.Icon(ft.Icons.PERSON)
                ),

                ft.Text(
                    "gatolibros",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Ciudad de México"
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.STAR,
                            color="amber"
                        ),
                        ft.Text("4.8")
                    ]
                ),

                ft.Divider(),

                ft.Text(
                    "🐱 Reto del día",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Text(
                            "Escribe un poema sobre la esperanza."
                        )
                    )
                ),

                ft.Text(
                    "Poemas publicados"
                ),

                ft.Text(
                    "18 poemas"
                ),

                ft.Text(
                    "Libros publicados"
                ),

                ft.Text(
                    "12 libros"
                )
            ]
        )
    )