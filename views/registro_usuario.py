# views/registro_usuario.py
import flet as ft
from services.usuarios_service import registrar_usuario
from services.auth_service import iniciar_sesion
from themes.styles import (
    input_redondeado, boton_primario,
    boton_secundario, texto_titulo,
    texto_error, aviso_seguridad, GRADIENTE_FONDO,
)
from themes.colors import LAVANDA, TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, BORDE_INPUT, FONDO_INPUT

ESTADOS_MX = [
    "Aguascalientes", "Baja California", "Baja California Sur",
    "Campeche", "Chiapas", "Chihuahua", "Ciudad de México",
    "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero",
    "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos",
    "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro",
    "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora",
    "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán",
    "Zacatecas",
]

GENEROS = ["Masculino", "Femenino", "No binario", "Prefiero no decir"]

AVISO_TEXTO = (
    "Para mantener nuestra comunidad segura, al registrarte aceptas cumplir con las siguientes normas:\n\n"
    "🛡️ Tu Privacidad: En Storalya no solicitamos tu dirección exacta. Solo requerimos tu ciudad y estado "
    "para conectarte con personas cercanas de forma segura, así que se mostrará de qué ciudad y estado eres.\n\n"
    "🤝 Intercambios Seguros: Por tu protección, los intercambios deben realizarse siempre en lugares "
    "públicos y concurridos (nunca en lugares apartados).\n\n"
    "💬 Comunicación: Para coordinar tus encuentros, utiliza exclusivamente las respuestas predeterminadas de la app.\n\n"
    "✨ Comunidad Sana: Al formar parte de Storalya, te comprometes a mantener un entorno amable, "
    "respetuoso y libre de conductas tóxicas para todos los lectores."
)


def _dropdown_claro(label: str, opciones: list) -> ft.Dropdown:
    """Dropdown con fondo claro compatible con Flet 0.85."""
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(op) for op in opciones],
        border_radius=20,
        border_color=BORDE_INPUT,
        focused_border_color=LAVANDA,
        bgcolor="#FFFFFF",
        color=TEXTO_PRINCIPAL,
        label_style=ft.TextStyle(
            color=TEXTO_SECUNDARIO,
            weight=ft.FontWeight.BOLD,
        ),
        text_style=ft.TextStyle(color=TEXTO_PRINCIPAL),
    )


def registro_view(page: ft.Page, ir_a_login, ir_a_home):
    """Pantalla de registro en 2 pasos."""

    paso = [1]

    # ── Campos paso 1 ─────────────────────────────────────────────
    campo_nombre = input_redondeado(
        "Nombre de usuario",
        hint="Crea tu nombre de usuario",
        icono="person_outline",
    )
    campo_email = input_redondeado(
        "Email",
        hint="tucorreo@ejemplo.com",
        icono="email_outlined",
    )
    campo_telefono = ft.TextField(
    label="Número de teléfono",
    hint_text="10 dígitos",
    keyboard_type=ft.KeyboardType.PHONE,
    border_radius=20,
    border_color=BORDE_INPUT,
    focused_border_color=LAVANDA,
    bgcolor="#FFFFFF",
    label_style=ft.TextStyle(
        color=TEXTO_SECUNDARIO,
        weight=ft.FontWeight.BOLD,
    ),
    text_style=ft.TextStyle(color=TEXTO_PRINCIPAL),
    filled=True,
    prefix_icon="phone_outlined",
    max_length=10,
    )
    campo_password = input_redondeado(
        "Contraseña",
        hint="Mínimo 8 caracteres, 1 mayúscula y 1 número",
        password=True,
        icono="lock_outline",
    )
    campo_edad = ft.TextField(
        label="Edad",
        hint_text="Ingresa tu edad",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=20,
        border_color=BORDE_INPUT,
        focused_border_color=LAVANDA,
        bgcolor="#FFFFFF",
        label_style=ft.TextStyle(
            color=TEXTO_SECUNDARIO,
            weight=ft.FontWeight.BOLD,
        ),
        text_style=ft.TextStyle(color=TEXTO_PRINCIPAL),
        filled=True,
        prefix_icon="cake_outlined",
    )
    campo_genero = _dropdown_claro("Género:", GENEROS)

    # ── Campos paso 2 ─────────────────────────────────────────────
    campo_estado = _dropdown_claro("Estado:", ESTADOS_MX)
    campo_ciudad = input_redondeado(
        "Ciudad",
        hint="Ingresa tu ciudad",
        icono="location_city_outlined",
    )

    msg_error = texto_error("")

    # ── Logo ──────────────────────────────────────────────────────
    logo = ft.Column(
        controls=[
            ft.Image(
                src="assets/logo/storalya_logo.png",
                width=80,
                fit="contain",
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ── Validaciones ──────────────────────────────────────────────
    def validar_paso_1():
        if not campo_nombre.value or not campo_nombre.value.strip():
            return "El nombre de usuario es obligatorio"
        if len(campo_nombre.value.strip()) < 3:
            return "El nombre debe tener al menos 3 caracteres"
        if not campo_email.value or "@" not in campo_email.value:
            return "Ingresa un email válido"
        if not campo_telefono.value or not campo_telefono.value.isdigit():
            return "Ingresa un número de teléfono válido"
        if len(campo_telefono.value) != 10:
            return "El teléfono debe tener exactamente 10 dígitos"
        if not campo_password.value or len(campo_password.value) < 8:
            return "La contraseña debe tener al menos 8 caracteres"
        if not campo_edad.value or not campo_edad.value.isdigit():
            return "Ingresa una edad válida"
        if int(campo_edad.value) < 16 or int(campo_edad.value) > 27:   # ← cambiado
            return "Storalya es para usuarios de 16 a 27 años"
        if not campo_genero.value:
            return "Selecciona tu género"
        return None

    def validar_paso_2():
        if not campo_estado.value:
            return "Selecciona tu estado"
        if not campo_ciudad.value or not campo_ciudad.value.strip():
            return "Ingresa tu ciudad"
        return None

    # ── Navegación ────────────────────────────────────────────────
    def ir_paso_2(e):
        error = validar_paso_1()
        if error:
            msg_error.value = error
            msg_error.visible = True
            page.update()
            return
        msg_error.visible = False
        paso[0] = 2
        renderizar()

    def volver_paso_1(e):
        msg_error.visible = False
        paso[0] = 1
        renderizar()

    def handle_registro(e):
        error = validar_paso_2()
        if error:
            msg_error.value = error
            msg_error.visible = True
            page.update()
            return

        resultado = registrar_usuario(
            nombre_usuario=campo_nombre.value.strip(),
            email=campo_email.value.strip().lower(),
            password_plano=campo_password.value,
            edad=int(campo_edad.value),
            genero=campo_genero.value,
            ciudad=campo_ciudad.value.strip(),
            estado=campo_estado.value,
            telefono=campo_telefono.value.strip(),
        )

        if resultado["ok"]:
            iniciar_sesion(resultado["usuario"])
            ir_a_home()
        else:
            msg_error.value = resultado["error"]
            msg_error.visible = True
            page.update()

    # ── Paso 1 ────────────────────────────────────────────────────
    def construir_paso_1():
        return ft.Column(
        controls=[
            ft.Container(height=16),
            logo,
            ft.Container(height=16),
            texto_titulo("Registro:\nDatos Personales", size=24),
            ft.Container(height=24),
            campo_nombre,
            ft.Container(height=12),
            campo_email,
            ft.Container(height=12),
            campo_telefono,        # ← NUEVO
            ft.Container(height=12),
            campo_password,
            ft.Container(height=12),
            campo_edad,
            ft.Container(height=12),
            campo_genero,
            ft.Container(height=8),
            msg_error,
            ft.Container(height=20),
            ft.Row(
                controls=[
                    boton_secundario("← Atrás", lambda _: ir_a_login()),
                    boton_primario("Seguir →", ir_paso_2),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(height=24),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    # ── Paso 2 ────────────────────────────────────────────────────
    def construir_paso_2():
        return ft.Column(
            controls=[
                ft.Container(height=16),
                logo,
                ft.Container(height=24),
                campo_estado,
                ft.Container(height=12),
                campo_ciudad,
                ft.Container(height=16),
                aviso_seguridad(AVISO_TEXTO),
                ft.Container(height=8),
                msg_error,
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        boton_secundario("← Atrás", volver_paso_1),
                        boton_primario("Seguir →", handle_registro),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=24),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )

    # ── Contenedor raíz ───────────────────────────────────────────
    contenedor_raiz = ft.Container(
        expand=True,
        gradient=GRADIENTE_FONDO,
    )

    def renderizar():
        vista = construir_paso_1() if paso[0] == 1 else construir_paso_2()
        contenedor_raiz.content = ft.Container(
            content=vista,
            padding=ft.Padding(left=32, right=32, top=24, bottom=24),
            expand=True,
        )
        page.update()

    renderizar()
    return contenedor_raiz