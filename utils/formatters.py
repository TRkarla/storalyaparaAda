# utils/formatters.py
from datetime import datetime

def formatear_fecha(fecha: datetime, formato: str = "%d/%m/%Y") -> str:
    """Convierte datetime a string legible para la UI."""
    if not fecha:
        return "Fecha desconocida"
    return fecha.strftime(formato)

def formatear_fecha_relativa(fecha: datetime) -> str:
    """Retorna 'hace X días/horas' para mostrar en tarjetas."""
    ahora = datetime.now()
    diferencia = ahora - fecha
    dias = diferencia.days

    if dias == 0:
        horas = diferencia.seconds // 3600
        return f"hace {horas}h" if horas > 0 else "hace un momento"
    elif dias == 1:
        return "ayer"
    elif dias < 7:
        return f"hace {dias} días"
    elif dias < 30:
        semanas = dias // 7
        return f"hace {semanas} semana{'s' if semanas > 1 else ''}"
    else:
        return formatear_fecha(fecha)

def truncar_texto(texto: str, max_chars: int = 100) -> str:
    """Recorta texto largo para previews en tarjetas."""
    if not texto:
        return ""
    return texto[:max_chars] + "..." if len(texto) > max_chars else texto

def formatear_autor(nombre: str, apellido: str = "") -> str:
    """Combina nombre y apellido de forma segura."""
    partes = [p.strip() for p in [nombre, apellido] if p and p.strip()]
    return " ".join(partes) or "Autor desconocido"