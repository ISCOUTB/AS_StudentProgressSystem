import uuid
import pytest
from app.repositories import malla as repo


def test_create_malla(session, carrera, materia):
    result = repo.create(session, carrera.id_carrera, materia.id_materia)
    assert result.id_carrera == carrera.id_carrera
    assert result.id_materia == materia.id_materia


def test_get_materias_by_carrera(session, carrera, materia):
    repo.create(session, carrera.id_carrera, materia.id_materia)
    result = repo.get_materias_by_carrera(session, carrera.id_carrera)
    assert len(result) == 1
    assert result[0].id_materia == materia.id_materia


def test_get_materias_by_carrera_vacio(session, carrera):
    result = repo.get_materias_by_carrera(session, carrera.id_carrera)
    assert result == []


def test_get_by_ids_existente(session, carrera, materia):
    repo.create(session, carrera.id_carrera, materia.id_materia)
    found = repo.get_by_ids(session, carrera.id_carrera, materia.id_materia)
    assert found is not None
    assert found.id_carrera == carrera.id_carrera
    assert found.id_materia == materia.id_materia


def test_get_by_ids_inexistente(session):
    result = repo.get_by_ids(session, uuid.uuid4(), uuid.uuid4())
    assert result is None


def test_delete_malla(session, carrera, materia):
    repo.create(session, carrera.id_carrera, materia.id_materia)
    deleted = repo.delete(session, carrera.id_carrera, materia.id_materia)
    assert deleted is True
    assert repo.get_by_ids(session, carrera.id_carrera, materia.id_materia) is None


def test_delete_malla_inexistente(session):
    result = repo.delete(session, uuid.uuid4(), uuid.uuid4())
    assert result is False