import uuid
import pytest
from app.repositories import categoria as repo
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


def make_data(**kwargs):
    defaults = dict(codigo="ISCO", nombre="Ingeniería de Sistemas")
    defaults.update(kwargs)
    return CategoriaCreate(**defaults)


def test_create_categoria(session):
    result = repo.create(session, make_data())
    assert result.id_categoria is not None
    assert result.nombre == "Ingeniería de Sistemas"
    assert result.codigo == "ISCO"


def test_get_all_categorias(session):
    repo.create(session, make_data(codigo="ISCO", nombre="Ingeniería de Sistemas"))
    repo.create(session, make_data(codigo="CBAS", nombre="Ciencias Básicas"))
    result = repo.get_all(session)
    assert len(result) == 2


def test_get_by_id_existente(session):
    created = repo.create(session, make_data())
    found = repo.get_by_id(session, created.id_categoria)
    assert found is not None
    assert found.id_categoria == created.id_categoria


def test_get_by_id_inexistente(session):
    result = repo.get_by_id(session, uuid.uuid4())
    assert result is None


def test_get_by_nombre_existente(session):
    repo.create(session, make_data())
    found = repo.get_by_nombre(session, "Ingeniería de Sistemas")
    assert found is not None
    assert found.nombre == "Ingeniería de Sistemas"


def test_get_by_nombre_inexistente(session):
    result = repo.get_by_nombre(session, "No existe")
    assert result is None


def test_update_categoria(session):
    created = repo.create(session, make_data())
    updated = repo.update(session, created.id_categoria, CategoriaUpdate(nombre="Nuevo"))
    assert updated.nombre == "Nuevo"
    assert updated.codigo == "ISCO"


def test_update_categoria_inexistente(session):
    result = repo.update(session, uuid.uuid4(), CategoriaUpdate(nombre="X"))
    assert result is None


def test_delete_categoria(session):
    created = repo.create(session, make_data())
    deleted = repo.delete(session, created.id_categoria)
    assert deleted is True
    assert repo.get_by_id(session, created.id_categoria) is None


def test_delete_categoria_inexistente(session):
    result = repo.delete(session, uuid.uuid4())
    assert result is False