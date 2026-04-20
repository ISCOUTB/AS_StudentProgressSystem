import uuid
import pytest
from app.repositories import estudiante_logro as repo
from app.schemas.estudiante_logro import EstudianteLogroCreate, EstudianteLogroUpdate
from app.enums.status_logro import StatusLogro


def test_create_estudiante_logro(session, estudiante, logro_materia):
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.obtenido
    )
    result = repo.create(session, data)
    assert result.id_estudiante == estudiante.id_estudiante
    assert result.id_logromateria == logro_materia.id_logromateria
    assert result.status == StatusLogro.obtenido


def test_get_by_estudiante(session, estudiante, logro_materia):
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.obtenido
    )
    repo.create(session, data)
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)
    assert len(result) == 1


def test_get_by_estudiante_vacio(session, estudiante):
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)
    assert result == []


def test_get_by_ids_existente(session, estudiante, logro_materia):
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.obtenido
    )
    repo.create(session, data)
    found = repo.get_by_ids(session, estudiante.id_estudiante, logro_materia.id_logromateria)
    assert found is not None


def test_get_by_ids_inexistente(session):
    result = repo.get_by_ids(session, uuid.uuid4(), uuid.uuid4())
    assert result is None


def test_update_estudiante_logro(session, estudiante, logro_materia):
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.noobtenido
    )
    repo.create(session, data)
    updated = repo.update(
        session,
        estudiante.id_estudiante,
        logro_materia.id_logromateria,
        EstudianteLogroUpdate(status=StatusLogro.obtenido)
    )
    assert updated.status == StatusLogro.obtenido


def test_update_inexistente(session):
    result = repo.update(
        session, uuid.uuid4(), uuid.uuid4(),
        EstudianteLogroUpdate(status=StatusLogro.obtenido)
    )
    assert result is None


def test_delete_estudiante_logro(session, estudiante, logro_materia):
    data = EstudianteLogroCreate(
        id_estudiante=estudiante.id_estudiante,
        id_logromateria=logro_materia.id_logromateria,
        status=StatusLogro.obtenido
    )
    repo.create(session, data)
    deleted = repo.delete(session, estudiante.id_estudiante, logro_materia.id_logromateria)
    assert deleted is True


def test_delete_inexistente(session):
    result = repo.delete(session, uuid.uuid4(), uuid.uuid4())
    assert result is False