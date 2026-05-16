
# Importa uuid para generar IDs aleatorios en pruebas
import uuid

# Importa pytest para pruebas automatizadas
import pytest

# Importa date para manejar fechas de admisión
from datetime import date

# Importa repositorio de estudiante_carrera (relación estudiante ↔ carrera)
from app.repositories import estudiante_carrera as repo

# Importa esquemas de creación y actualización
from app.schemas.estudiante_carrera import EstudianteCarreraCreate, EstudianteCarreraUpdate


# =========================
# TEST: CREAR ESTUDIANTE CARRERA
# =========================

def test_create_estudiante_carrera(session, estudiante, carrera):

    # Se crea la relación estudiante-carrera
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )

    # Inserta en la base de datos de prueba
    result = repo.create(session, data)

    # Validaciones
    assert result.id_estudiante == estudiante.id_estudiante
    assert result.id_carrera == carrera.id_carrera
    assert result.semestre == "Nivel I"


# =========================
# TEST: GET POR ESTUDIANTE
# =========================

def test_get_by_estudiante(session, estudiante, carrera):

    # Crea relación previa
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)

    # Consulta carreras del estudiante
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)

    # Debe existir una relación
    assert len(result) == 1
    assert result[0].id_estudiante == estudiante.id_estudiante


# =========================
# TEST: GET VACÍO
# =========================

def test_get_by_estudiante_vacio(session, estudiante):

    # Sin relaciones previas
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)

    # Debe retornar lista vacía
    assert result == []


# =========================
# TEST: GET ALL
# =========================

def test_get_all(session, estudiante, carrera):

    # Crea relación
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)

    # Obtiene todas las relaciones
    result = repo.get_all(session)

    # Verifica cantidad y contenido
    assert len(result) == 1
    assert result[0].id_estudiante == estudiante.id_estudiante


# =========================
# TEST: GET POR IDS (EXISTE)
# =========================

def test_get_by_ids_existente(session, estudiante, carrera):

    # Crea relación
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)

    # Busca por clave compuesta
    found = repo.get_by_ids(session, estudiante.id_estudiante, carrera.id_carrera)

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
# TEST: ACTUALIZAR RELACIÓN
# =========================

def test_update_estudiante_carrera(session, estudiante, carrera):

    # Crea relación
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)

    # Actualiza semestre
    updated = repo.update(
        session,
        estudiante.id_estudiante,
        carrera.id_carrera,
        EstudianteCarreraUpdate(semestre="Nivel II")
    )

    # Verifica cambio
    assert updated.semestre == "Nivel II"


# =========================
# TEST: UPDATE INEXISTENTE
# =========================

def test_update_inexistente(session):

    # Intento con IDs inexistentes
    result = repo.update(
        session,
        uuid.uuid4(),
        uuid.uuid4(),
        EstudianteCarreraUpdate(semestre="Nivel X")
    )

    # Debe ser None
    assert result is None


# =========================
# TEST: ELIMINAR RELACIÓN
# =========================

def test_delete_estudiante_carrera(session, estudiante, carrera):

    # Crea relación
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)

    # Elimina relación
    deleted = repo.delete(session, estudiante.id_estudiante, carrera.id_carrera)

    # Verifica eliminación
    assert deleted is True


# =========================
# TEST: DELETE INEXISTENTE
# =========================

def test_delete_inexistente(session):

    # Intento de eliminación de datos inexistentes
    result = repo.delete(session, uuid.uuid4(), uuid.uuid4())

    # Debe fallar
    assert result is False

