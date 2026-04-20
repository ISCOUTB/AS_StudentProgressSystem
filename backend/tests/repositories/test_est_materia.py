import uuid
import pytest
from app.repositories import estudiante_materia as repo
from app.schemas.estudiante_materia import EstudianteMateriaCreate, EstudianteMateriaUpdate
from app.enums.status_materia import StatusMaterias


def make_data(estudiante, materia, **kwargs):
    defaults = dict(
        id_estudiante=estudiante.id_estudiante,
        id_materia=materia.id_materia,
        status=StatusMaterias.encurso,
        nota=0.0,
        semestre="PRIMER PERIODO 2026 PREGRADO"
    )
    defaults.update(kwargs)
    return EstudianteMateriaCreate(**defaults)


def test_create_estudiante_materia(session, estudiante, materia):
    data = make_data(estudiante, materia)
    result = repo.create(session, data)
    assert result.id_estudiante == estudiante.id_estudiante
    assert result.id_materia == materia.id_materia
    assert result.status == StatusMaterias.encurso


def test_get_by_estudiante(session, estudiante, materia):
    repo.create(session, make_data(estudiante, materia))
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)
    assert len(result) == 1


def test_get_by_estudiante_vacio(session, estudiante):
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)
    assert result == []


def test_get_by_ids_existente(session, estudiante, materia):
    repo.create(session, make_data(estudiante, materia))
    found = repo.get_by_ids(session, estudiante.id_estudiante, materia.id_materia)
    assert found is not None


def test_get_by_ids_inexistente(session):
    result = repo.get_by_ids(session, uuid.uuid4(), uuid.uuid4())
    assert result is None


def test_get_aprobadas(session, estudiante, materia):
    repo.create(session, make_data(estudiante, materia, status=StatusMaterias.aprobada, nota=4.0))
    aprobadas = repo.get_aprobadas(session, estudiante.id_estudiante)
    assert len(aprobadas) == 1
    assert aprobadas[0].status == StatusMaterias.aprobada


def test_get_aprobadas_vacio(session, estudiante, materia):
    repo.create(session, make_data(estudiante, materia, status=StatusMaterias.encurso))
    aprobadas = repo.get_aprobadas(session, estudiante.id_estudiante)
    assert aprobadas == []


def test_update_estudiante_materia(session, estudiante, materia):
    repo.create(session, make_data(estudiante, materia))
    updated = repo.update(
        session,
        estudiante.id_estudiante,
        materia.id_materia,
        EstudianteMateriaUpdate(status=StatusMaterias.aprobada, nota=4.5)
    )
    assert updated.status == StatusMaterias.aprobada
    assert updated.nota == 4.5


def test_update_inexistente(session):
    result = repo.update(
        session, uuid.uuid4(), uuid.uuid4(),
        EstudianteMateriaUpdate(nota=3.0)
    )
    assert result is None


def test_delete_estudiante_materia(session, estudiante, materia):
    repo.create(session, make_data(estudiante, materia))
    deleted = repo.delete(session, estudiante.id_estudiante, materia.id_materia)
    assert deleted is True
    assert repo.get_by_ids(session, estudiante.id_estudiante, materia.id_materia) is None


def test_delete_inexistente(session):
    result = repo.delete(session, uuid.uuid4(), uuid.uuid4())
    assert result is False