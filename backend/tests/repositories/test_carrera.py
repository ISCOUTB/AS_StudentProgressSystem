import uuid
import pytest
from app.repositories import carrera as repo
from app.schemas.carrera import CarreraCreate, CarreraUpdate
from app.enums.escuela import Escuelas


def make_data(**kwargs):
    defaults = dict(nombre="Ingeniería de Sistemas", codigo="ISCO", escuela=Escuelas.etd)
    defaults.update(kwargs)
    return CarreraCreate(**defaults)


def test_create_carrera(session):
    data = make_data()
    result = repo.create(session, data)
    assert result.id_carrera is not None
    assert result.nombre == "Ingeniería de Sistemas"
    assert result.codigo == "ISCO"


def test_get_all_carreras(session):
    repo.create(session, make_data(codigo="ISCO"))
    repo.create(session, make_data(nombre="Ingeniería Civil", codigo="ICIV"))
    result = repo.get_all(session)
    assert len(result) == 2


def test_get_by_id_existente(session):
    created = repo.create(session, make_data())
    found = repo.get_by_id(session, created.id_carrera)
    assert found is not None
    assert found.id_carrera == created.id_carrera


def test_get_by_id_inexistente(session):
    result = repo.get_by_id(session, uuid.uuid4())
    assert result is None


def test_get_by_codigo_existente(session):
    repo.create(session, make_data())
    found = repo.get_by_codigo(session, "ISCO")
    assert found is not None
    assert found.codigo == "ISCO"


def test_get_by_codigo_inexistente(session):
    result = repo.get_by_codigo(session, "XXXX")
    assert result is None


def test_update_carrera(session):
    created = repo.create(session, make_data())
    updated = repo.update(session, created.id_carrera, CarreraUpdate(nombre="Nuevo Nombre"))
    assert updated.nombre == "Nuevo Nombre"
    assert updated.codigo == "ISCO"


def test_update_carrera_inexistente(session):
    result = repo.update(session, uuid.uuid4(), CarreraUpdate(nombre="X"))
    assert result is None


def test_delete_carrera(session):
    created = repo.create(session, make_data())
    deleted = repo.delete(session, created.id_carrera)
    assert deleted is True
    assert repo.get_by_id(session, created.id_carrera) is None


def test_delete_carrera_inexistente(session):
    result = repo.delete(session, uuid.uuid4())
    assert result is False