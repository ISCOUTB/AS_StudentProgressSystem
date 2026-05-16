```python id="i2m5qp"
# Importa uuid para generar IDs aleatorios en pruebas
import uuid

# Importa pytest para pruebas automatizadas
import pytest

# Importa repositorio de logro_materia (relación logro ↔ materia)
from app.repositories import logro_materia as repo

# Importa esquema de creación de relación logro-materia
from app.schemas.logro_materia import LogroMateriaCreate


# =========================
# TEST: CREAR LOGRO_MATERIA
# =========================

def test_create_logro_materia(session, logro, materia):

    # Se crea relación entre logro y materia
    data = LogroMateriaCreate(
        id_logro=logro.id_logro,
        id_materia=materia.id_materia
    )

    # Inserta en base de datos de prueba
    result = repo.create(session, data)

    # Validaciones
    assert result.id_logromateria is not None
    assert result.id_logro == logro.id_logro
    assert result.id_materia == materia.id_materia


# =========================
# TEST: CREAR SIN MATERIA
# =========================

def test_create_logro_materia_sin_materia(session, logro):

    # Permite crear relación solo con logro (materia opcional)
    data = LogroMateriaCreate(
        id_logro=logro.id_logro,
        id_materia=None
    )

    # Inserta en base de datos
    result = repo.create(session, data)

    # Verifica creación parcial
    assert result.id_logromateria is not None
    assert result.id_materia is None


# =========================
# TEST: GET ALL
# =========================

def test_get_all(session, logro, materia):

    # Crea relación previa
    repo.create(
        session,
        LogroMateriaCreate(
            id_logro=logro.id_logro,
            id_materia=materia.id_materia
        )
    )

    # Obtiene todas las relaciones
    result = repo.get_all(session)

    # Verifica cantidad
    assert len(result) == 1


# =========================
# TEST: GET BY ID (EXISTE)
# =========================

def test_get_by_id_existente(session, logro, materia):

    # Crea relación
    created = repo.create(
        session,
        LogroMateriaCreate(
            id_logro=logro.id_logro,
            id_materia=materia.id_materia
        )
    )

    # Busca por ID
    found = repo.get_by_id(session, created.id_logromateria)

    # Verifica existencia
    assert found is not None
    assert found.id_logromateria == created.id_logromateria


# =========================
# TEST: GET BY ID (NO EXISTE)
# =========================

def test_get_by_id_inexistente(session):

    # ID aleatorio inexistente
    result = repo.get_by_id(session, uuid.uuid4())

    # Debe ser None
    assert result is None


# =========================
# TEST: GET BY LOGRO
# =========================

def test_get_by_logro(session, logro, materia):

    # Crea relación
    repo.create(
        session,
        LogroMateriaCreate(
            id_logro=logro.id_logro,
            id_materia=materia.id_materia
        )
    )

    # Consulta por logro
    result = repo.get_by_logro(session, logro.id_logro)

    # Verifica resultado
    assert len(result) == 1
    assert result[0].id_logro == logro.id_logro


# =========================
# TEST: GET BY LOGRO VACÍO
# =========================

def test_get_by_logro_vacio(session, logro):

    # Sin relaciones previas
    result = repo.get_by_logro(session, logro.id_logro)

    # Debe retornar lista vacía
    assert result == []


# =========================
# TEST: DELETE RELACIÓN
# =========================

def test_delete_logro_materia(session, logro, materia):

    # Crea relación
    created = repo.create(
        session,
        LogroMateriaCreate(
            id_logro=logro.id_logro,
            id_materia=materia.id_materia
        )
    )

    # Elimina relación
    deleted = repo.delete(session, created.id_logromateria)

    # Verifica eliminación
    assert deleted is True
    assert repo.get_by_id(session, created.id_logromateria) is None


# =========================
# TEST: DELETE INEXISTENTE
# =========================

def test_delete_inexistente(session):

    # Intenta eliminar ID inexistente
    result = repo.delete(session, uuid.uuid4())

    # Debe fallar
    assert result is False
```
