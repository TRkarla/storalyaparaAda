# config/settings.py
from decouple import config

# ─── Base de Datos ───────────────────────────────────────
DB_HOST     = config("DB_HOST",     default="localhost")
DB_PORT     = config("DB_PORT",     default="5432")
DB_NAME     = config("DB_NAME",     default="storalya")
DB_USER     = config("DB_USER",     default="postgres")
DB_PASSWORD = config("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ─── Aplicación ──────────────────────────────────────────
APP_NAME   = config("APP_NAME",   default="STORALYA")
APP_DEBUG  = config("APP_DEBUG",  default=False, cast=bool)
SECRET_KEY = config("SECRET_KEY")

# ─── Fallback SQLite ─────────────────────────────────────
USE_SQLITE_FALLBACK = config("USE_SQLITE_FALLBACK", default=False, cast=bool)

if USE_SQLITE_FALLBACK:
    DATABASE_URL = "sqlite:///storalya.db"