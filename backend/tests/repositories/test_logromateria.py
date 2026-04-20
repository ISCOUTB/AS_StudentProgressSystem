import uuid
import pytest
from app.repositories import logro_materia as repo
from app.schemas.logro_materia import LogroMateriaCreate


def test_create_logro_materia(session, logro, materia):
    data = LogroMateriaCreate(id_logro=logro.id_logro, id_materia=materia.id_materia)
    result = repo.create(session, data)
    assert result.id_logromateria is not None
    assert result.id_logro == logro.id_logro
    assert result.id_materia == materia.id_materia


def test_create_logro_materia_sin_materia(session, logro):
    data = LogroMateriaCreate(id_logro=logro.id_logro, id_materia=None)
    result = repo.create(session, data)
    assert result.id_logromateria is not None
    assert result.id_materia is None


def test_get_all(session, logro, materia):
    repo.create(session, LogroMateriaCreate(id_logro=logro.id_logro, id_materia=materia.id_materia))
    result = repo.get_all(session)
    assert len(result) == 1


def test_get_by_id_existente(session, logro, materia):
    created = repo.create(session, LogroMateriaCreate(id_logro=logro.id_logro, id_materia=materia.id_materia))
    found = repo.get_by_id(session, created.id_logromateria)
    assert found is not None
    assert found.id_logromateria == created.id_logromateria


def test_get_by_id_inexistente(session):
    result = repo.get_by_id(session, uuid.uuid4())
    assert result is None


def test_get_by_logro(session, logro, materia):
    repo.create(session, LogroMateriaCreate(id_logro=logro.id_logro, id_materia=materia.id_materia))
    result = repo.get_by_logro(session, logro.id_logro)
    assert len(result) == 1
    assert result[0].id_logro == logro.id_logro


def test_get_by_logro_vacio(session, logro):
    result = repo.get_by_logro(session, logro.id_logro)
    assert result == []


def test_delete_logro_materia(session, logro, materia):
    created = repo.create(session, LogroMateriaCreate(id_logro=logro.id_logro, id_materia=materia.id_materia))
    deleted = repo.delete(session, created.id_logromateria)
    assert deleted is True
    assert repo.get_by_id(session, created.id_logromateria) is None


def test_delete_inexistente(session):
    result = repo.delete(session, uuid.uuid4())
    assert result is False