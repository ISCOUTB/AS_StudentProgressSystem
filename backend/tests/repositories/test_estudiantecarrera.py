import uuid
import pytest
from datetime import date
from app.repositories import estudiante_carrera as repo
from app.schemas.estudiante_carrera import EstudianteCarreraCreate, EstudianteCarreraUpdate


def test_create_estudiante_carrera(session, estudiante, carrera):
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    result = repo.create(session, data)
    assert result.id_estudiante == estudiante.id_estudiante
    assert result.id_carrera == carrera.id_carrera
    assert result.semestre == "Nivel I"


def test_get_by_estudiante(session, estudiante, carrera):
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)
    assert len(result) == 1
    assert result[0].id_estudiante == estudiante.id_estudiante


def test_get_by_estudiante_vacio(session, estudiante):
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)
    assert result == []

def test_get_all(session, estudiante, carrera):
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)
    result = repo.get_all(session)
    assert len(result) == 1
    assert result[0].id_estudiante == estudiante.id_estudiante

def test_get_by_ids_existente(session, estudiante, carrera):
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)
    found = repo.get_by_ids(session, estudiante.id_estudiante, carrera.id_carrera)
    assert found is not None


def test_get_by_ids_inexistente(session, estudiante, carrera):
    result = repo.get_by_ids(session, uuid.uuid4(), uuid.uuid4())
    assert result is None


def test_update_estudiante_carrera(session, estudiante, carrera):
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)
    updated = repo.update(
        session,
        estudiante.id_estudiante,
        carrera.id_carrera,
        EstudianteCarreraUpdate(semestre="Nivel II")
    )
    assert updated.semestre == "Nivel II"


def test_update_inexistente(session):
    result = repo.update(
        session, uuid.uuid4(), uuid.uuid4(),
        EstudianteCarreraUpdate(semestre="Nivel X")
    )
    assert result is None


def test_delete_estudiante_carrera(session, estudiante, carrera):
    data = EstudianteCarreraCreate(
        id_estudiante=estudiante.id_estudiante,
        id_carrera=carrera.id_carrera,
        semestre="Nivel I",
        fecha_admision=date(2024, 1, 15)
    )
    repo.create(session, data)
    deleted = repo.delete(session, estudiante.id_estudiante, carrera.id_carrera)
    assert deleted is True


def test_delete_inexistente(session):
    result = repo.delete(session, uuid.uuid4(), uuid.uuid4())
    assert result is False