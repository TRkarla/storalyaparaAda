# utils/validators.py
import re

def validar_email(email: str) -> bool:
    """Valida formato de correo electrónico."""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(patron, email))

def validar_isbn(isbn: str) -> bool:
    """Valida ISBN-10 o ISBN-13 (solo dígitos, permite guiones)."""
    limpio = isbn.replace("-", "").replace(" ", "")
    return limpio.isdigit() and len(limpio) in (10, 13)

def validar_password(password: str) -> tuple[bool, str]:
    """
    Valida que la contraseña cumpla requisitos mínimos.
    Retorna (es_valida, mensaje_error)
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    if not any(c.isupper() for c in password):
        return False, "Debe contener al menos una mayúscula"
    if not any(c.isdigit() for c in password):
        return False, "Debe contener al menos un número"
    return True, ""

def validar_texto_no_vacio(texto: str, nombre_campo: str = "Campo") -> tuple[bool, str]:
    """Valida que un texto no esté vacío o solo tenga espacios."""
    if not texto or not texto.strip():
        return False, f"{nombre_campo} no puede estar vacío"
    return True, ""