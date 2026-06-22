import sys
import os

# --- INYECCIÓN DE RUTA ---
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)
# -------------------------

from database.connection import engine, Base

# IMPORTA SOLO LO QUE EXISTE EN TU CARPETA MODELS
from models.reto_cumplido import RetoCumplido
from models.reto_asignado import RetoAsignado

def init_tables():
    print("Creando tablas para los modelos existentes...")
    Base.metadata.create_all(bind=engine)
    print("¡Base de datos inicializada con éxito!")

if __name__ == "__main__":
    init_tables()