# themes/styles.py
# Compatible con Flet 0.85
import flet as ft
from themes.colors import (
    BOTON_PRIMARIO, TEXTO_PRINCIPAL, TEXTO_SECUNDARIO,
    TEXTO_CLARO, FONDO_INPUT, BORDE_INPUT, FONDO_TARJETA,
    LAVANDA, ROSA, ERROR, EXITO, DIVISOR,
    FONDO_APP, BOTON_PELIGRO,
)


# ─── Tipografía ───────────────────────────────────────────────────

def texto_titulo(texto: str, size: int = 28) -> ft.Text:
    return ft.Text(
        texto,
        size=size,
        weight=ft.FontWeight.BOLD,
        color=TEXTO_PRINCIPAL,
        text_align=ft.TextAlign.CENTER,
    )


def texto_subtitulo(texto: str, size: int = 14) -> ft.Text:
    return ft.Text(
        texto,
        size=size,
        color=TEXTO_SECUNDARIO,
        text_align=ft.TextAlign.CENTER,
    )


def texto_label(texto: str) -> ft.Text:
    return ft.Text(texto, size=12, color=TEXTO_SECUNDARIO)


def texto_error(texto: str) -> ft.Text:
    return ft.Text(texto, size=12, color=ERROR, visible=False)


def texto_exito(texto: str) -> ft.Text:
    return ft.Text(texto, size=12, color=EXITO, visible=False)


# ─── Inputs ───────────────────────────────────────────────────────

def input_redondeado(
    label: str,
    hint: str = "",
    password: bool = False,
    icono=None,
) -> ft.TextField:
    return ft.TextField(
        label=label,
        hint_text=hint,
        password=password,
        can_reveal_password=password,
        prefix_icon=icono,
        border_radius=20,
        border_color=BORDE_INPUT,
        focused_border_color=LAVANDA,
        bgcolor=FONDO_INPUT,
        label_style=ft.TextStyle(color=TEXTO_SECUNDARIO, weight=ft.FontWeight.BOLD),
        text_style=ft.TextStyle(color=TEXTO_PRINCIPAL),
        cursor_color=LAVANDA,
        filled=True,
    )


def dropdown_redondeado(label: str, opciones: list) -> ft.Dropdown:
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(op) for op in opciones],
        border_radius=20,
        border_color=BORDE_INPUT,
        focused_border_color=LAVANDA,
        bgcolor=FONDO_INPUT,
        label_style=ft.TextStyle(color=TEXTO_PRINCIPAL, weight=ft.FontWeight.BOLD),
        text_style=ft.TextStyle(color=TEXTO_PRINCIPAL),
        filled=True,
    )


# ─── Botones ──────────────────────────────────────────────────────

def boton_primario(texto: str, on_click, icono=None) -> ft.Container:
    return ft.Container(
        content=ft.Text(
            texto,
            color=TEXTO_CLARO,
            weight=ft.FontWeight.W_500,
            size=15,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=BOTON_PRIMARIO,
        border_radius=30,
        padding=ft.Padding(left=32, right=32, top=14, bottom=14),
        on_click=on_click,
        ink=True,
    )


def boton_secundario(texto: str, on_click, icono=None) -> ft.Container:
    return ft.Container(
        content=ft.Text(
            texto,
            color=TEXTO_PRINCIPAL,
            weight=ft.FontWeight.W_500,
            size=15,
            text_align=ft.TextAlign.CENTER,
        ),
        border=ft.Border(
            top=ft.BorderSide(1.5, BORDE_INPUT),
            bottom=ft.BorderSide(1.5, BORDE_INPUT),
            left=ft.BorderSide(1.5, BORDE_INPUT),
            right=ft.BorderSide(1.5, BORDE_INPUT),
        ),
        border_radius=30,
        padding=ft.Padding(left=32, right=32, top=14, bottom=14),
        on_click=on_click,
        ink=True,
    )


def boton_peligro(texto: str, on_click) -> ft.Container:
    return ft.Container(
        content=ft.Text(texto, color=BOTON_PELIGRO, size=14),
        on_click=on_click,
        ink=True,
        padding=ft.Padding(left=8, right=8, top=4, bottom=4),
    )


# ─── Tarjetas ─────────────────────────────────────────────────────

def tarjeta(contenido: ft.Control, padding: int = 16) -> ft.Container:
    return ft.Container(
        content=contenido,
        bgcolor=FONDO_TARJETA,
        border_radius=16,
        padding=padding,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color="#D6CADD33",
            offset=ft.Offset(0, 2),
        ),
    )


def chip_genero(texto: str, color: str = ROSA) -> ft.Container:
    return ft.Container(
        content=ft.Text(texto, size=11, color=TEXTO_PRINCIPAL),
        bgcolor=color,
        border_radius=20,
        padding=ft.Padding(left=10, right=10, top=4, bottom=4),
    )


# ─── Aviso de seguridad ───────────────────────────────────────────

def aviso_seguridad(mensaje: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Aviso Importante de Seguridad y Privacidad:",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO_PRINCIPAL,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    mensaje,
                    size=12,
                    color=TEXTO_SECUNDARIO,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=FONDO_APP,
        border_radius=12,
        padding=16,
        border=ft.Border(
            top=ft.BorderSide(1, BORDE_INPUT),
            bottom=ft.BorderSide(1, BORDE_INPUT),
            left=ft.BorderSide(1, BORDE_INPUT),
            right=ft.BorderSide(1, BORDE_INPUT),
        ),
    )


# ─── Divisor ──────────────────────────────────────────────────────

def divisor() -> ft.Divider:
    return ft.Divider(color=DIVISOR, thickness=1)


# ─── Fondo degradado ──────────────────────────────────────────────

GRADIENTE_FONDO = ft.LinearGradient(
    begin=ft.Alignment(-1, -1),
    end=ft.Alignment(1, 1),
    colors=["#F0E8F5", "#FCF0F5", "#EFF7F8"],
)