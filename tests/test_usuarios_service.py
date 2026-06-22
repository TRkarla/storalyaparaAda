# tests/test_usuarios_service.py

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models  # ← LÍNEA NUEVA: carga todos los modelos primero

from services.usuarios_service import registrar_usuario, login_usuario


# ── Test 1: Registro ──────────────────────────────────────────────
print("🧪 Probando registro...")
resultado = registrar_usuario(
    nombre_usuario="lector_test",
    email="test@storalya.com",
    password_plano="TestPass123",
    edad=25,
    genero="Masculino",
    ciudad="Veracruz",
    estado="Veracruz"
)
print("Registro:", resultado)

# ── Test 2: Login con email ───────────────────────────────────────
print("\n🧪 Probando login con email...")
resultado = login_usuario("test@storalya.com", "TestPass123")
print("Login email:", resultado)

# ── Test 3: Login con nombre de usuario ───────────────────────────
print("\n🧪 Probando login con nombre...")
resultado = login_usuario("lector_test", "TestPass123")
print("Login nombre:", resultado)

# ── Test 4: Password incorrecto ───────────────────────────────────
print("\n🧪 Probando password incorrecto...")
resultado = login_usuario("lector_test", "wrongpass")
print("Password malo:", resultado)

# ── Test 5: Email inválido ────────────────────────────────────────
print("\n🧪 Probando email inválido...")
resultado = registrar_usuario(
    nombre_usuario="otro_user",
    email="esto_no_es_un_email",
    password_plano="TestPass123",
    edad=20,
    genero="Femenino",
    ciudad="CDMX",
    estado="CDMX"
)
print("Email inválido:", resultado)