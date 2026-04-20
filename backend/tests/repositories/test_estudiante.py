import uuid
import pytest
from app.repositories import estudiante as repo
from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate
from app.enums.status_estudiante import StatusEstudiante


def make_data(**kwargs):
    defaults = dict(
        nombre="Juan",
        apellido="Pérez",
        codigo="T00076001",
        correo="juan.perez@utb.edu.co",
        password="Password123!",
        status=StatusEstudiante.activo
    )
    defaults.update(kwargs)
    return EstudianteCreate(**defaults)


def test_create_estudiante(session):
    result = repo.create(session, make_data())
    assert result.id_estudiante is not None
    assert result.nombre == "Juan"
    assert result.codigo == "T00076001"
    assert result.hash_password != "Password123!"


def test_get_all_estudiantes(session):
    repo.create(session, make_data(codigo="T00076001", correo="a@utb.edu.co"))
    repo.create(session, make_data(codigo="T00076002", correo="b@utb.edu.co"))
    result = repo.get_all(session)
    assert len(result) == 2


def test_get_by_id_existente(session):
    created = repo.create(session, make_data())
    found = repo.get_by_id(session, created.id_estudiante)
    assert found is not None
    assert found.id_estudiante == created.id_estudiante


def test_get_by_id_inexistente(session):
    result = repo.get_by_id(session, uuid.uuid4())
    assert result is None


def test_get_by_codigo_existente(session):
    repo.create(session, make_data())
    found = repo.get_by_codigo(session, "T00076001")
    assert found is not None
    assert found.codigo == "T00076001"


def test_get_by_codigo_inexistente(session):
    result = repo.get_by_codigo(session, "T99999999")
    assert result is None


def test_update_estudiante(session):
    created = repo.create(session, make_data())
    updated = repo.update(session, created.id_estudiante, EstudianteUpdate(nombre="Carlos"))
    assert updated.nombre == "Carlos"
    assert updated.apellido == "Pérez"


def test_update_estudiante_inexistente(session):
    result = repo.update(session, uuid.uuid4(), EstudianteUpdate(nombre="X"))
    assert result is None


def test_delete_estudiante(session):
    created = repo.create(session, make_data())
    deleted = repo.delete(session, created.id_estudiante)
    assert deleted is True
    assert repo.get_by_id(session, created.id_estudiante) is None


def test_delete_estudiante_inexistente(session):
    result = repo.delete(session, uuid.uuid4())
    assert result is False