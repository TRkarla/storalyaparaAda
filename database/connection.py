# database/connection.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator
from sqlalchemy.exc import OperationalError
from config.settings import DATABASE_URL, APP_DEBUG

engine = create_engine(
    DATABASE_URL,
    echo=APP_DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verificar_conexion() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Conexión a PostgreSQL exitosa")
        return True
    except OperationalError as e:
        print(f"❌ Error al conectar con PostgreSQL: {e}")
        return False

def crear_tablas() -> None:
    # ── Esta línea carga todos los modelos antes de crear tablas ──
    import models  # noqa: F401 ← LÍNEA NUEVA
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas verificadas/creadas correctamente")