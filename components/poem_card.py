import flet as ft

class PoemCard(ft.Card):
    def __init__(
        self,
        usuario,
        poema,
        likes=0
    ):
        super().__init__()

        self.content = ft.Container(
            padding=15,
            content=ft.Column(
                controls=[
                    ft.Text(
                        usuario,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(poema),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Icon(
                                ft.Icons.FAVORITE_BORDER
                            ),
                            ft.Text(str(likes))
                        ]
                    )
                ]
            )
        )