import flet as ft

class ChallengeCard(ft.Card):
    def __init__(self, reto):
        super().__init__()

        self.content = ft.Container(
            padding=15,
            content=ft.Row(
                controls=[
                    ft.Text(
                        "🐱",
                        size=40
                    ),

                    ft.Column(
                        controls=[
                            ft.Text(
                                "Reto diario",
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(reto)
                        ]
                    )
                ]
            )
        )