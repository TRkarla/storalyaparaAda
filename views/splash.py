# views/splash.py
import flet as ft
from themes.styles import boton_primario, boton_secundario, GRADIENTE_FONDO
from themes.colors import TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, MALVA, ROSA


def splash_view(page: ft.Page, ir_a_registro, ir_a_login):
    """
    Pantalla de bienvenida de STORALYA.
    Diseño: logo grande, slogan en dos colores, botones y olas decorativas.
    """

    # ── Logo ──────────────────────────────────────────────────────
    logo = ft.Image(
        src="assets/logo/logo.png",
        width=260,
        fit="contain",
    )

    # ── Slogan en dos colores ─────────────────────────────────────
    slogan = ft.Column(
        controls=[
            ft.Text(
                "Lectura que conecta,",
                size=17,
                color=TEXTO_SECUNDARIO,
                text_align=ft.TextAlign.CENTER,
                italic=True,
                weight=ft.FontWeight.W_400,
            ),
            ft.Text(
                "Historias que permanecen.",
                size=17,
                color="#C49ABF",   # malva rosado del PDF
                text_align=ft.TextAlign.CENTER,
                italic=True,
                weight=ft.FontWeight.W_400,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=2,
    )

    # ── Olas decorativas abajo ────────────────────────────────────
    olas = ft.Container(
        height=120,
        content=ft.Stack(
            controls=[
                # Ola lavanda
                ft.Container(
                    width=page.window.width or 390,
                    height=100,
                    bottom=0,
                    left=0,
                    bgcolor="#ABA4C6",
                    border_radius=ft.BorderRadius(
                        top_left=80,
                        top_right=120,
                        bottom_left=0,
                        bottom_right=0,
                    ),
                ),
                # Ola rosa
                ft.Container(
                    width=(page.window.width or 390) * 0.6,
                    height=70,
                    bottom=0,
                    right=0,
                    bgcolor="#F0BFCE",
                    border_radius=ft.BorderRadius(
                        top_left=100,
                        top_right=0,
                        bottom_left=0,
                        bottom_right=0,
                    ),
                ),
                # Ola verde agua
                ft.Container(
                    width=(page.window.width or 390) * 0.35,
                    height=50,
                    bottom=0,
                    right=0,
                    bgcolor="#A1CACF",
                    border_radius=ft.BorderRadius(
                        top_left=60,
                        top_right=0,
                        bottom_left=0,
                        bottom_right=0,
                    ),
                ),
            ],
            expand=True,
        ),
    )

    # ── Botones ───────────────────────────────────────────────────
    botones = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            "Crear cuenta",
                            color="#FFFFFF",
                            size=16,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Text("→", color="#FFFFFF", size=16),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1, 0),
                    end=ft.Alignment(1, 0),
                    colors=["#ABA4C6", "#D4A5C0"],
                ),
                border_radius=30,
                padding=ft.Padding(left=28, right=28, top=16, bottom=16),
                on_click=lambda _: ir_a_registro(),
                ink=True,
                width=280,
            ),
            ft.Container(height=12),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            "Inicia sesión",
                            color=TEXTO_PRINCIPAL,
                            size=16,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Text("→", color=TEXTO_PRINCIPAL, size=16),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                border=ft.Border(
                    top=ft.BorderSide(1.5, "#D6CADD"),
                    bottom=ft.BorderSide(1.5, "#D6CADD"),
                    left=ft.BorderSide(1.5, "#D6CADD"),
                    right=ft.BorderSide(1.5, "#D6CADD"),
                ),
                border_radius=30,
                padding=ft.Padding(left=28, right=28, top=16, bottom=16),
                on_click=lambda _: ir_a_login(),
                ink=True,
                width=280,
                bgcolor="#FFFFFF",
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # ── Layout principal ──────────────────────────────────────────
    contenido = ft.Column(
        controls=[
            ft.Container(expand=True),   # espacio superior flexible
            logo,
            ft.Container(height=16),
            slogan,
            ft.Container(expand=True),   # espacio medio flexible
            botones,
            ft.Container(height=16),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        expand=True,
    )

    return ft.Container(
        expand=True,
        gradient=GRADIENTE_FONDO,
        content=ft.Column(
            controls=[
                ft.Container(
                    content=contenido,
                    padding=ft.Padding(left=32, right=32, top=0, bottom=0),
                    expand=True,
                ),
                olas,
            ],
            spacing=0,
            expand=True,
        ),
    )