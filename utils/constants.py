# utils/constants.py

# Géneros literarios disponibles en STORALYA
GENEROS_LITERARIOS = [
    "Ficción", "No ficción", "Poesía", "Terror",
    "Romance", "Fantasía", "Ciencia ficción",
    "Misterio", "Biografía", "Historia", "Infantil"
]

# Estados posibles de un intercambio
ESTADOS_INTERCAMBIO = ["pendiente", "aceptado", "rechazado", "completado"]

# Estados de un reto literario
ESTADOS_RETO = ["activo", "completado", "expirado"]

# Límites de la app
MAX_DESCRIPCION_LIBRO = 500   # caracteres
MAX_CONTENIDO_POEMA   = 3000  # caracteres
MAX_IMAGENES_LIBRO    = 5