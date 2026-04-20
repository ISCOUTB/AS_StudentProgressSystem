import uuid
import pytest
from app.repositories import materia as repo
from app.schemas.materia import MateriaCreate, MateriaUpdate


def make_data(id_categoria, **kwargs):
    defaults = dict(nombre="Fundamentos de Programación", creditos=3, id_categoria=id_categoria)
    defaults.update(kwargs)
    return MateriaCreate(**defaults)


def test_create_materia(session, categoria):
    result = repo.create(session, make_data(categoria.id_categoria))
    assert result.id_materia is not None
    assert result.nombre == "Fundamentos de Programación"
    assert result.creditos == 3


def test_get_all_materias(session, categoria):
    repo.create(session, make_data(categoria.id_categoria, nombre="Materia A"))
    repo.create(session, make_data(categoria.id_categoria, nombre="Materia B"))
    result = repo.get_all(session)
    assert len(result) == 2


def test_get_by_id_existente(session, categoria):
    created = repo.create(session, make_data(categoria.id_categoria))
    found = repo.get_by_id(session, created.id_materia)
    assert found is not None
    assert found.id_materia == created.id_materia


def test_get_by_id_inexistente(session):
    result = repo.get_by_id(session, uuid.uuid4())
    assert result is None


def test_get_by_nombre_existente(session, categoria):
    repo.create(session, make_data(categoria.id_categoria))
    found = repo.get_by_nombre(session, "Fundamentos de Programación")
    assert found is not None


def test_get_by_nombre_inexistente(session):
    result = repo.get_by_nombre(session, "No existe")
    assert result is None


def test_get_by_categoria(session, categoria):
    repo.create(session, make_data(categoria.id_categoria, nombre="Mat A"))
    repo.create(session, make_data(categoria.id_categoria, nombre="Mat B"))
    result = repo.get_by_categoria(session, categoria.id_categoria)
    assert len(result) == 2


def test_get_by_categoria_vacio(session, categoria):
    result = repo.get_by_categoria(session, uuid.uuid4())
    assert result == []


def test_update_materia(session, categoria):
    created = repo.create(session, make_data(categoria.id_categoria))
    updated = repo.update(session, created.id_materia, MateriaUpdate(nombre="Nuevo nombre"))
    assert updated.nombre == "Nuevo nombre"
    assert updated.creditos == 3


def test_update_inexistente(session, categoria):
    result = repo.update(session, uuid.uuid4(), MateriaUpdate(nombre="X"))
    assert result is None


def test_delete_materia(session, categoria):
    created = repo.create(session, make_data(categoria.id_categoria))
    deleted = repo.delete(session, created.id_materia)
    assert deleted is True
    assert repo.get_by_id(session, created.id_materia) is None


def test_delete_inexistente(session):
    result = repo.delete(session, uuid.uuid4())
    assert result is False