```python id="f6m1qp"
# Importa uuid para generar IDs aleatorios en pruebas
import uuid

# Importa pytest para pruebas automatizadas
import pytest

# Importa repositorio de estudiante_logro (relación estudiante ↔ logro)
from app.repositories import estudiante_logro as repo

# Importa esquemas de creación y actualización
from app.schemas.estudiante_logro import EstudianteLogroCreate, EstudianteLogroUpdate

# Importa enum de estado de logro
from app.enums.status_logro import StatusLogro


# =========================
# TEST: CREAR ESTUDIANTE LOGRO
# =========================

def test_create_estudiante_logro(session, estudiante, logro_materia):

    # Se crea el objeto de relación estudiante-logro
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.obtenido
    )

    # Se inserta en la base de datos de prueba
    result = repo.create(session, data)

    # Validaciones
    assert result.id_estudiante == estudiante.id_estudiante
    assert result.id_logromateria == logro_materia.id_logromateria
    assert result.status == StatusLogro.obtenido


# =========================
# TEST: GET POR ESTUDIANTE
# =========================

def test_get_by_estudiante(session, estudiante, logro_materia):

    # Se crea relación previa
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.obtenido
    )
    repo.create(session, data)

    # Se consultan logros del estudiante
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)

    # Debe existir al menos uno
    assert len(result) == 1


# =========================
# TEST: GET VACÍO
# =========================

def test_get_by_estudiante_vacio(session, estudiante):

    # Sin datos previos
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)

    # Debe retornar lista vacía
    assert result == []


# =========================
# TEST: GET POR IDS (EXISTE)
# =========================

def test_get_by_ids_existente(session, estudiante, logro_materia):

    # Se crea relación
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.obtenido
    )
    repo.create(session, data)

    # Se busca por claves compuestas
    found = repo.get_by_ids(session, estudiante.id_estudiante, logro_materia.id_logromateria)

    # Debe existir
    assert found is not None


# =========================
# TEST: GET POR IDS (NO EXISTE)
# =========================

def test_get_by_ids_inexistente(session):

    # IDs aleatorios inexistentes
    result = repo.get_by_ids(session, uuid.uuid4(), uuid.uuid4())

    # Debe ser None
    assert result is None


# =========================
# TEST: ACTUALIZAR LOGRO
# =========================

def test_update_estudiante_logro(session, estudiante, logro_materia):

    # Se crea relación inicial
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.noobtenido
    )
    repo.create(session, data)

    # Se actualiza estado del logro
    updated = repo.update(
        session,
        estudiante.id_estudiante,
        logro_materia.id_logromateria,
        EstudianteLogroUpdate(status=StatusLogro.obtenido)
    )

    # Verifica actualización
    assert updated.status == StatusLogro.obtenido


# =========================
# TEST: UPDATE INEXISTENTE
# =========================

def test_update_inexistente(session):

    # Intenta actualizar algo inexistente
    result = repo.update(
        session,
        uuid.uuid4(),
        uuid.uuid4(),
        EstudianteLogroUpdate(status=StatusLogro.obtenido)
    )

    # Debe ser None
    assert result is None


# =========================
# TEST: ELIMINAR LOGRO
# =========================

def test_delete_estudiante_logro(session, estudiante, logro_materia):

    # Se crea relación
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.obtenido
    )
    repo.create(session, data)

    # Se elimina relación
    deleted = repo.delete(session, estudiante.id_estudiante, logro_materia.id_logromateria)

    # Debe eliminarse correctamente
    assert deleted is True


# =========================
# TEST: DELETE INEXISTENTE
# =========================

def test_delete_inexistente(session):

    # Intento de borrado de datos inexistentes
    result = repo.delete(session, uuid.uuid4(), uuid.uuid4())

    # Debe fallar
    assert result is False
```
