# recrear_tablas.py
# Ejecutar UNA SOLA VEZ para crear todas las tablas en PostgreSQL
# Borrar este archivo después de usarlo

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import models  # carga todos los modelos
from database.connection import Base, engine, verificar_conexion

print("🔌 Verificando conexión...")
if not verificar_conexion():
    print("❌ No se pudo conectar. Revisa tu .env")
    exit(1)

print("🏗️  Creando tablas...")
Base.metadata.create_all(bind=engine)
print("✅ Todas las tablas creadas correctamente")

from sqlalchemy import inspect
inspector = inspect(engine)
tablas = inspector.get_table_names()
print(f"\n📋 Tablas en la BD ({len(tablas)}):")
for tabla in sorted(tablas):
    print(f"   • {tabla}")