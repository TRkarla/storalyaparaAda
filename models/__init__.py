# models/__init__.py
from database.connection import Base  # noqa: F401

from models.usuario import Usuario            # noqa: F401
from models.libro import Libro                # noqa: F401
from models.poema import Poema               # noqa: F401
from models.imagen import Imagen             # noqa: F401
from models.calificacion import Calificacion # noqa: F401
from models.mensaje import Mensaje           # noqa: F401
from models.intercambio import Intercambio   # noqa: F401
from models.reto import Reto                 # noqa: F401  ← NUEVO
from models.reto_asignado import RetoAsignado   # noqa: F401
from models.reto_cumplido import RetoCumplido   # noqa: F401