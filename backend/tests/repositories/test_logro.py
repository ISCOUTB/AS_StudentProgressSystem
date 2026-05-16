```python id="h1m3qp"
# Importa uuid para generar IDs aleatorios en pruebas
import uuid

# Importa pytest para pruebas automatizadas
import pytest

# Importa repositorio de logros (capa de acceso a datos)
from app.repositories import logro as repo

# Importa esquemas de creación y actualización de logro
from app.schemas.logro import LogroCreate, LogroUpdate


# =========================
# UTILIDAD PARA CREAR DATOS
# =========================

def make_data(**kwargs):

    # Datos por defecto de un logro válido
    defaults = dict(
        nombre="Materia aprobada",
        descripcion="Primera materia",
        icon="✅"
    )

    # Permite sobrescribir valores en tests
    defaults.update(kwargs)

    # Retorna schema listo para insertar
    return LogroCreate(**defaults)


# =========================
# TEST: CREAR LOGRO
# =========================

def test_create_logro(session):

    # Crea un logro en la base de datos de prueba
    result = repo.create(session, make_data())

    # Validaciones básicas
    assert result.id_logro is not None
    assert result.nombre == "Materia aprobada"


# =========================
# TEST: GET ALL
# =========================

def test_get_all_logros(session):

    # Inserta dos logros
    repo.create(session, make_data(nombre="Logro 1"))
    repo.create(session, make_data(nombre="Logro 2"))

    # Obtiene todos los logros
    result = repo.get_all(session)

    # Verifica cantidad
    assert len(result) == 2


# =========================
# TEST: GET POR ID (EXISTE)
# =========================

def test_get_by_id_existente(session):

    # Crea logro
    created = repo.create(session, make_data())

    # Busca por ID
    found = repo.get_by_id(session, created.id_logro)

    # Verifica existencia
    assert found is not None
    assert found.id_logro == created.id_logro


# =========================
# TEST: GET POR ID (NO EXISTE)
# =========================

def test_get_by_id_inexistente(session):

    # Busca ID aleatorio inexistente
    result = repo.get_by_id(session, uuid.uuid4())

    # Debe ser None
    assert result is None


# =========================
# TEST: ACTUALIZAR LOGRO
# =========================

def test_update_logro(session):

    # Crea logro
    created = repo.create(session, make_data())

    # Actualiza nombre
    updated = repo.update(
        session,
        created.id_logro,
        LogroUpdate(nombre="Nuevo logro")
    )

    # Verifica cambio
    assert updated.nombre == "Nuevo logro"


# =========================
# TEST: UPDATE INEXISTENTE
# =========================

def test_update_logro_inexistente(session):

    # Intenta actualizar ID inexistente
    result = repo.update(
        session,
        uuid.uuid4(),
        LogroUpdate(nombre="X")
    )

    # Debe ser None
    assert result is None


# =========================
# TEST: ELIMINAR LOGRO
# =========================

def test_delete_logro(session):

    # Crea logro
    created = repo.create(session, make_data())

    # Elimina logro
    deleted = repo.delete(session, created.id_logro)

    # Verifica eliminación
    assert deleted is True
    assert repo.get_by_id(session, created.id_logro) is None


# =========================
# TEST: DELETE INEXISTENTE
# =========================

def test_delete_logro_inexistente(session):

    # Intenta eliminar ID inexistente
    result = repo.delete(session, uuid.uuid4())

    # Debe fallar
    assert result is False
```
