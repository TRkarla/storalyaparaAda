# database/database_usuarios.py
# ──────────────────────────────────────────────────────────────────
# Responsabilidad: operaciones CRUD directas sobre la tabla usuarios.
# NO define engine ni sesión propia — usa connection.py para eso.
# ──────────────────────────────────────────────────────────────────

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.usuario import Usuario


# ─── CREATE ───────────────────────────────────────────────────────
def crear_usuario(
    db: Session,
    nombre_usuario: str,
    email: str,
    password_hash: str,
    edad: int,
    genero: str,
    ciudad: str,
    estado: str,
    telefono: str = "",
) -> Usuario | None:
    try:
        nuevo = Usuario(
            nombre_usuario=nombre_usuario,
            email=email if email else None,       # ← None en lugar de ""
            telefono=telefono if telefono else None,  # ← None en lugar de ""
            password=password_hash,
            edad=edad,
            genero=genero,
            ciudad=ciudad,
            estado=estado,
            activo=True,
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except IntegrityError:
        db.rollback()
        return None  # nombre_usuario o email duplicado


# ─── READ ─────────────────────────────────────────────────────────
def obtener_usuario_por_id(db: Session, usuario_id: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def obtener_usuario_por_nombre(db: Session, nombre_usuario: str) -> Usuario | None:
    return db.query(Usuario).filter(
        Usuario.nombre_usuario == nombre_usuario
    ).first()


def obtener_usuario_por_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def obtener_todos_los_usuarios(db: Session) -> list[Usuario]:
    return db.query(Usuario).filter(Usuario.activo == True).all()


# ─── UPDATE ───────────────────────────────────────────────────────
def actualizar_usuario(
    db: Session,
    usuario_id: int,
    **campos   # pasa solo los campos que quieres actualizar
) -> Usuario | None:
    """
    Actualiza campos específicos de un usuario.
    
    Uso desde el servicio:
        actualizar_usuario(db, 5, ciudad="CDMX", estado="CDMX")
    """
    usuario = obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        return None

    campos_permitidos = {"nombre_usuario", "email", "edad", "genero", "ciudad", "estado"}
    for campo, valor in campos.items():
        if campo in campos_permitidos:
            setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario


def actualizar_password(
    db: Session,
    usuario_id: int,
    nuevo_password_hash: str
) -> bool:
    """Actualiza solo el password. Retorna True si tuvo éxito."""
    usuario = obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        return False
    usuario.password = nuevo_password_hash
    db.commit()
    return True


# ─── DELETE (soft delete) ─────────────────────────────────────────
def desactivar_usuario(db: Session, usuario_id: int) -> bool:
    """
    No elimina el registro — lo marca como inactivo.
    Preserva historial de libros, poemas e intercambios.
    Retorna True si tuvo éxito.
    """
    usuario = obtener_usuario_por_id(db, usuario_id)
    if not usuario:
        return False
    usuario.activo = False
    db.commit()
    return True