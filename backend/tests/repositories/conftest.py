"""
Fixtures compartidas para todos los tests de repositorios.
Usa SQLite en memoria para no requerir PostgreSQL al correr los tests.
"""
import pytest
import uuid
from datetime import date
from sqlmodel import SQLModel, Session, create_engine
from app.models import (
    Carreras, Categorias, Materias, CarreraMateria,
    Estudiantes, EstudiantesCarreras, EstudianteMateria,
    Logros, LogroMaterias, EstudianteLogros
)
from app.enums.escuela import Escuelas
from app.enums.status_estudiante import StatusEstudiante
from app.enums.status_materia import StatusMaterias
from app.enums.status_logro import StatusLogro


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def categoria(session):
    cat = Categorias(
        id_categoria=uuid.uuid4(),
        codigo="ISCO",
        nombre="Ingeniería de Sistemas"
    )
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@pytest.fixture
def carrera(session):
    car = Carreras(
        id_carrera=uuid.uuid4(),
        nombre="Ingeniería de Sistemas y Computación",
        codigo="ISCO",
        escuela=Escuelas.etd
    )
    session.add(car)
    session.commit()
    session.refresh(car)
    return car


@pytest.fixture
def materia(session, categoria):
    mat = Materias(
        id_materia=uuid.uuid4(),
        nombre="Fundamentos de Programación",
        codigo="C02A",
        creditos=3,
        id_categoria=categoria.id_categoria
    )
    session.add(mat)
    session.commit()
    session.refresh(mat)
    return mat


@pytest.fixture
def estudiante(session):
    est = Estudiantes(
        id_estudiante=uuid.uuid4(),
        nombre="Juan",
        apellido="Pérez",
        codigo="T00076001",
        correo="juanperez@utb.edu.co",
        status=StatusEstudiante.activo,
        hash_password="hashed"
    )
    session.add(est)
    session.commit()
    session.refresh(est)
    return est


@pytest.fixture
def logro(session):
    l = Logros(
        id_logro=uuid.uuid4(),
        nombre_logro="Materia aprobada",
        descripcion="Aprobaste tu primera materia"
    )
    session.add(l)
    session.commit()
    session.refresh(l)
    return l


@pytest.fixture
def logro_materia(session, logro, materia):
    lm = LogroMaterias(
        id_logromateria=uuid.uuid4(),
        id_logro=logro.id_logro,
        id_materia=materia.id_materia
    )
    session.add(lm)
    session.commit()
    session.refresh(lm)
    return lm