import uuid
import pytest
from app.repositories import progreso as repo
from app.models.carrera_materia import CarreraMateria
from app.models.estudiante_materia import EstudianteMateria
from app.enums.status_materia import StatusMaterias


def test_get_materias_con_status_aprobada(session, estudiante, carrera, materia):
    session.add(CarreraMateria(id_carrera=carrera.id_carrera, id_materia=materia.id_materia))
    session.add(EstudianteMateria(
        id_estudiante=estudiante.id_estudiante,
        id_materia=materia.id_materia,
        status=StatusMaterias.aprobada,
        nota=4.5,
        semestre="PRIMER PERIODO 2026 PREGRADO"
    ))
    session.commit()

    result = repo.get_materias_con_status(session, estudiante.id_estudiante, carrera.id_carrera)
    assert len(result) == 1
    assert result[0]["status"] == StatusMaterias.aprobada
    assert result[0]["nombre"] == materia.nombre
    assert result[0]["creditos"] == materia.creditos


def test_get_materias_con_status_sin_registro(session, estudiante, carrera, materia):
    session.add(CarreraMateria(id_carrera=carrera.id_carrera, id_materia=materia.id_materia))
    session.commit()

    result = repo.get_materias_con_status(session, estudiante.id_estudiante, carrera.id_carrera)
    assert len(result) == 1
    assert result[0]["status"] == StatusMaterias.encurso


def test_get_materias_con_status_carrera_vacia(session, estudiante, carrera):
    result = repo.get_materias_con_status(session, estudiante.id_estudiante, carrera.id_carrera)
    assert result == []


def test_get_materias_con_status_multiples(session, estudiante, carrera, categoria):
    from app.models.materia import Materias

    mat2 = Materias(
        id_materia=uuid.uuid4(),
        nombre="Programación",
        codigo="C03A",
        creditos=3,
        id_categoria=categoria.id_categoria
    )
    session.add(mat2)
    session.commit()

    session.add(CarreraMateria(id_carrera=carrera.id_carrera, id_materia=mat2.id_materia))
    session.add(EstudianteMateria(
        id_estudiante=estudiante.id_estudiante,
        id_materia=mat2.id_materia,
        status=StatusMaterias.reprobada,
        nota=2.0,
        semestre="PRIMER PERIODO 2025 PREGRADO"
    ))
    session.commit()

    result = repo.get_materias_con_status(session, estudiante.id_estudiante, carrera.id_carrera)
    assert len(result) == 1
    assert result[0]["status"] == StatusMaterias.reprobada