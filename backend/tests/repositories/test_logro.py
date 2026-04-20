import uuid
import pytest
from app.repositories import logro as repo
from app.schemas.logro import LogroCreate, LogroUpdate


def make_data(**kwargs):
    defaults = dict(nombre="Materia aprobada", descripcion="Primera materia", icon="✅")
    defaults.update(kwargs)
    return LogroCreate(**defaults)


def test_create_logro(session):
    result = repo.create(session, make_data())
    assert result.id_logro is not None
    assert result.nombre == "Materia aprobada"  # Changed from nombre_logro
    


def test_get_all_logros(session):
    repo.create(session, make_data(nombre="Logro 1"))
    repo.create(session, make_data(nombre="Logro 2"))
    result = repo.get_all(session)
    assert len(result) == 2


def test_get_by_id_existente(session):
    created = repo.create(session, make_data())
    found = repo.get_by_id(session, created.id_logro)
    assert found is not None
    assert found.id_logro == created.id_logro


def test_get_by_id_inexistente(session):
    result = repo.get_by_id(session, uuid.uuid4())
    assert result is None


def test_update_logro(session):
    created = repo.create(session, make_data())
    updated = repo.update(session, created.id_logro, LogroUpdate(nombre="Nuevo logro"))
    assert updated.nombre == "Nuevo logro"  # Changed from nombre_logro
    


def test_update_logro_inexistente(session):
    result = repo.update(session, uuid.uuid4(), LogroUpdate(nombre="X"))
    assert result is None


def test_delete_logro(session):
    created = repo.create(session, make_data())
    deleted = repo.delete(session, created.id_logro)
    assert deleted is True
    assert repo.get_by_id(session, created.id_logro) is None


def test_delete_logro_inexistente(session):
    result = repo.delete(session, uuid.uuid4())
    assert result is False