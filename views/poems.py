# views/poems.py
import flet as ft
from services.poemas_service import obtener_feed_poemas, crear_poema, eliminar_mi_poema
from services.auth_service import obtener_usuario_activo, obtener_id_activo
from themes.colors import (
    LAVANDA, MALVA, TEXTO_PRINCIPAL, TEXTO_SECUNDARIO,
    FONDO_TARJETA, BORDE_INPUT, FONDO_APP,
)
from utils.formatters import formatear_fecha_relativa

ACENTOS = ["#ABA4C6", "#F0BFCE", "#A1CACF", "#CCA9C6", "#FADBCE"]


def poems_view(page: ft.Page, navegador: dict, w: int = 390, h: int = 844) -> ft.Column:

    usuario_activo = obtener_usuario_activo()
    likes_locales  = {}
    filtro_activo  = ["recientes"]

    lista = ft.ListView(
        spacing=12,
        padding=ft.Padding(left=16, right=16, top=8, bottom=16),
        expand=True,
    )

    def hacer_tarjeta(poema, idx):
        acento   = ACENTOS[idx % len(ACENTOS)]
        es_mio   = usuario_activo and poema.usuario_id == usuario_activo.id
        autor    = poema.autor.nombre_usuario if hasattr(poema, "autor") and poema.autor else "?"
        fecha    = formatear_fecha_relativa(poema.fecha_creacion) if poema.fecha_creacion else ""
        con_like = likes_locales.get(poema.id, False)

        def toggle_like(e):
            likes_locales[poema.id] = not likes_locales.get(poema.id, False)
            cargar()

        def pedir_eliminar(e):
            def ok(e2):
                dlg.open = False
                page.update()
                if eliminar_mi_poema(usuario_activo.id, poema.id)["ok"]:
                    cargar()
            def no(e2):
                dlg.open = False
                page.update()
            dlg = ft.AlertDialog(
                title=ft.Text("¿Eliminar poema?", color=TEXTO_PRINCIPAL),
                content=ft.Text("Esta acción no se puede deshacer.", color=TEXTO_SECUNDARIO),
                actions=[
                    ft.TextButton("Cancelar", on_click=no),
                    ft.TextButton("Eliminar", on_click=ok,
                                  style=ft.ButtonStyle(color="#E07B8A")),
                ],
            )
            page.overlay.append(dlg)
            dlg.open = True
            page.update()

        menu = ft.PopupMenuButton(
            icon="more_horiz", icon_color=TEXTO_SECUNDARIO, icon_size=18,
            items=[ft.PopupMenuItem(
                text="Eliminar", icon="delete_outline",
                on_click=pedir_eliminar,
            )],
        ) if es_mio else ft.Container(width=24)

        return ft.Container(
            width=w - 32,
            bgcolor=FONDO_TARJETA,
            border_radius=16,
            padding=16,
            border=ft.Border(
                left=ft.BorderSide(3, acento),
                top=ft.BorderSide(0, "transparent"),
                right=ft.BorderSide(0, "transparent"),
                bottom=ft.BorderSide(0, "transparent"),
            ),
            content=ft.Column(controls=[
                ft.Row(controls=[
                    ft.Container(
                        content=ft.Text(autor[0].upper(), color="#FFF", size=15,
                                        weight=ft.FontWeight.BOLD),
                        bgcolor=acento, border_radius=21, width=42, height=42,
                    ),
                    ft.Column(controls=[
                        ft.Text(autor, size=13, weight=ft.FontWeight.BOLD,
                                color=TEXTO_PRINCIPAL),
                        ft.Text(fecha, size=11, color=TEXTO_SECUNDARIO),
                    ], spacing=1, expand=True),
                    menu,
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=8),
                ft.Text(poema.contenido, size=14, color=TEXTO_PRINCIPAL,
                        max_lines=6, overflow=ft.TextOverflow.ELLIPSIS),
                ft.Container(height=8),
                ft.Row(controls=[
                    ft.Container(
                        content=ft.Text(poema.titulo, size=11, color=TEXTO_PRINCIPAL),
                        bgcolor=acento + "55", border_radius=20,
                        padding=ft.Padding(left=10, right=10, top=4, bottom=4),
                    ),
                    ft.Row(controls=[
                        ft.GestureDetector(
                            content=ft.Icon(
                                "favorite" if con_like else "favorite_border",
                                color=MALVA if con_like else TEXTO_SECUNDARIO,
                                size=18,
                            ),
                            on_tap=toggle_like,
                        ),
                        ft.Text(str(likes_locales.get(poema.id, 0)),
                                size=13, color=TEXTO_SECUNDARIO),
                    ], spacing=4),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ], spacing=0),
        )

    def cargar():
        lista.controls.clear()
        res = obtener_feed_poemas()
        if not res["ok"] or not res["poemas"]:
            lista.controls.append(ft.Container(
                content=ft.Text("Aún no hay poemas. ¡Sé el primero!",
                                color=TEXTO_SECUNDARIO,
                                text_align=ft.TextAlign.CENTER),
                padding=32,
            ))
        else:
            for i, p in enumerate(res["poemas"]):
                lista.controls.append(hacer_tarjeta(p, i))
        page.update()

    def abrir_publicar(e):
        f_titulo = ft.TextField(
            label="Título", border_radius=12, filled=True, bgcolor="#FFF",
            border_color=BORDE_INPUT, focused_border_color=LAVANDA,
            label_style=ft.TextStyle(color=TEXTO_SECUNDARIO),
            text_style=ft.TextStyle(color=TEXTO_PRINCIPAL),
        )
        f_contenido = ft.TextField(
            label="Escribe tu poema...", multiline=True,
            min_lines=5, max_lines=10, max_length=3000,
            border_radius=12, filled=True, bgcolor="#FFF",
            border_color=BORDE_INPUT, focused_border_color=LAVANDA,
            label_style=ft.TextStyle(color=TEXTO_SECUNDARIO),
            text_style=ft.TextStyle(color=TEXTO_PRINCIPAL),
        )
        msg = ft.Text("", color="#E07B8A", size=12, visible=False)

        def publicar(e):
            if not f_titulo.value or not f_titulo.value.strip():
                msg.value = "El título es obligatorio"
                msg.visible = True
                page.update()
                return
            if not f_contenido.value or not f_contenido.value.strip():
                msg.value = "Escribe el contenido"
                msg.visible = True
                page.update()
                return
            res = crear_poema(obtener_id_activo(),
                              f_titulo.value.strip(),
                              f_contenido.value.strip())
            if res["ok"]:
                dlg.open = False
                page.update()
                cargar()
            else:
                msg.value = res["error"]
                msg.visible = True
                page.update()

        def cerrar(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Publicar poema", color=TEXTO_PRINCIPAL,
                          weight=ft.FontWeight.BOLD),
            content=ft.Column(
                controls=[f_titulo, ft.Container(height=8), f_contenido, msg],
                spacing=4, tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.Container(
                    content=ft.Text("Publicar", color="#FFF", size=14),
                    bgcolor=LAVANDA, border_radius=20,
                    padding=ft.Padding(left=20, right=20, top=8, bottom=8),
                    on_click=publicar, ink=True,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    fila_filtros = ft.Row(spacing=8, scroll=ft.ScrollMode.AUTO)

    def construir_filtros():
        def sel(clave):
            def fn(e):
                filtro_activo[0] = clave
                construir_filtros()
                cargar()
            return fn
        fila_filtros.controls = [
            ft.GestureDetector(
                on_tap=sel(c),
                content=ft.Container(
                    content=ft.Text(l, size=13,
                        color="#FFF" if filtro_activo[0] == c else TEXTO_PRINCIPAL),
                    bgcolor=LAVANDA if filtro_activo[0] == c else FONDO_TARJETA,
                    border_radius=20,
                    padding=ft.Padding(left=16, right=16, top=8, bottom=8),
                    border=ft.Border(
                        top=ft.BorderSide(1, "transparent" if filtro_activo[0] == c else BORDE_INPUT),
                        bottom=ft.BorderSide(1, "transparent" if filtro_activo[0] == c else BORDE_INPUT),
                        left=ft.BorderSide(1, "transparent" if filtro_activo[0] == c else BORDE_INPUT),
                        right=ft.BorderSide(1, "transparent" if filtro_activo[0] == c else BORDE_INPUT),
                    ),
                ),
            )
            for c, l in [
                ("recientes", "Más recientes"),
                ("populares", "Populares"),
                ("seguidos",  "Seguidos"),
                ("todos",     "Todos"),
            ]
        ]
        page.update()

    construir_filtros()
    cargar()

    # ── Navbar superior ──────────────────────────────────────────
    navbar_top = ft.Container(
        width=w,
        bgcolor=FONDO_APP,
        padding=ft.Padding(left=16, right=16, top=12, bottom=8),
        content=ft.Row(
            controls=[
                ft.Row(controls=[
                    ft.Image(src="assets/logo/logo.png", width=36, fit="contain"),
                    ft.Text("Storalya", size=18, weight=ft.FontWeight.BOLD,
                            color=TEXTO_PRINCIPAL),
                ], spacing=6),
                ft.Row(controls=[
                    ft.GestureDetector(
                        content=ft.Icon("search", color=TEXTO_PRINCIPAL, size=22),
                        on_tap=lambda e: None,
                    ),
                    ft.Container(width=8),
                    ft.GestureDetector(
                        content=ft.Icon("notifications_outlined",
                                       color=TEXTO_PRINCIPAL, size=22),
                        on_tap=lambda e: None,
                    ),
                ]),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    # ── Header muro ──────────────────────────────────────────────
    header_muro = ft.Container(
        width=w,
        padding=ft.Padding(left=16, right=16, top=8, bottom=4),
        content=ft.Column(controls=[
            ft.Row(
                controls=[
                    ft.Text("Muro de poemas", size=20,
                            weight=ft.FontWeight.BOLD, color=TEXTO_PRINCIPAL),
                    ft.GestureDetector(
                        on_tap=abrir_publicar,
                        content=ft.Container(
                            content=ft.Row(controls=[
                                ft.Icon("edit_outlined", color="#FFF", size=14),
                                ft.Text("Publicar poema", color="#FFF", size=12,
                                        weight=ft.FontWeight.W_500),
                            ], spacing=4, tight=True),
                            bgcolor=LAVANDA, border_radius=20,
                            padding=ft.Padding(left=12, right=12, top=8, bottom=8),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=10),
            fila_filtros,
            ft.Container(height=4),
        ], spacing=0),
    )

    # ── Bottom nav ───────────────────────────────────────────────
    def item_nav(icono, label, clave):
        activo = clave == "poemas"
        color  = LAVANDA if activo else TEXTO_SECUNDARIO

        if clave == "publicar":
            return ft.GestureDetector(
                on_tap=abrir_publicar,
                content=ft.Column(controls=[
                    ft.Container(
                        content=ft.Icon("edit_outlined", color="#FFF", size=20),
                        bgcolor=LAVANDA, border_radius=26, width=52, height=52,
                    ),
                    ft.Text(label, size=10, color=LAVANDA,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            )

        return ft.GestureDetector(
            on_tap=lambda e, c=clave: navegador.get(c, lambda: None)(),
            content=ft.Column(controls=[
                ft.Icon(icono, color=color, size=22),
                ft.Text(label, size=10, color=color,
                        weight=ft.FontWeight.W_500 if activo else ft.FontWeight.W_400,
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        )

    nav_bottom = ft.Container(
        width=w,
        bgcolor="#FFFFFF",
        padding=ft.Padding(left=8, right=8, top=10, bottom=20),
        border=ft.Border(
            top=ft.BorderSide(1, BORDE_INPUT),
            bottom=ft.BorderSide(0, "transparent"),
            left=ft.BorderSide(0, "transparent"),
            right=ft.BorderSide(0, "transparent"),
        ),
        content=ft.Row(
            controls=[
                item_nav("home_outlined",      "Inicio",     "poemas"),
                item_nav("menu_book_outlined", "Biblioteca", "biblioteca"),
                item_nav("edit_outlined",      "Publicar",   "publicar"),
                item_nav("people_outline",     "Comunidad",  "comunidad"),
                item_nav("person_outline",     "Perfil",     "perfil"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    return ft.Column(
        controls=[navbar_top, header_muro, lista, nav_bottom],
        spacing=0,
        width=w,
        height=h,
    )