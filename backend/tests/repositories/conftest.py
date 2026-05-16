
"""
Fixtures compartidas para todos los tests de repositorios.
Usa SQLite en memoria para no requerir PostgreSQL al correr los tests.
"""

# Pytest para crear fixtures reutilizables en pruebas
import pytest

# UUID para generar identificadores únicos en los datos de prueba
import uuid

# Date por si se necesitan fechas en otros tests
from datetime import date

# SQLModel para manejar modelos y sesiones de base de datos
from sqlmodel import SQLModel, Session, create_engine

# Importación de modelos del sistema
from app.models import (
    Carreras, Categorias, Materias, CarreraMateria,
    Estudiantes, EstudiantesCarreras, EstudianteMateria,
    Logros, LogroMaterias, EstudianteLogros
)

# Enumeraciones del sistema
from app.enums.escuela import Escuelas
from app.enums.status_estudiante import StatusEstudiante
from app.enums.status_materia import StatusMaterias
from app.enums.status_logro import StatusLogro


# =========================
# FIXTURE DE BASE DE DATOS
# =========================

@pytest.fixture(name="session")
def session_fixture():

    # Crea una base de datos SQLite en memoria (ideal para tests)
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )

    # Crea todas las tablas en la base de datos de prueba
    SQLModel.metadata.create_all(engine)

    # Abre una sesión de base de datos para los tests
    with Session(engine) as session:
        yield session  # entrega la sesión al test

    # Limpia las tablas al terminar el test
    SQLModel.metadata.drop_all(engine)


# =========================
# FIXTURE: CATEGORIA
# =========================

@pytest.fixture
def categoria(session):

    # Crea una categoría de prueba
    cat = Categorias(
        id_categoria=uuid.uuid4(),
        codigo="ISCO",
        nombre="Ingeniería de Sistemas"
    )

    # Guarda en base de datos
    session.add(cat)
    session.commit()
    session.refresh(cat)

    return cat


# =========================
# FIXTURE: CARRERA
# =========================

@pytest.fixture
def carrera(session):

    # Crea una carrera de prueba
    car = Carreras(
        id_carrera=uuid.uuid4(),
        nombre="Ingeniería de Sistemas y Computación",
        codigo="ISCO",
        escuela=Escuelas.etd
    )

    # Guarda en base de datos
    session.add(car)
    session.commit()
    session.refresh(car)

    return car


# =========================
# FIXTURE: MATERIA
# =========================

@pytest.fixture
def materia(session, categoria):

    # Crea una materia asociada a una categoría
    mat = Materias(
        id_materia=uuid.uuid4(),
        nombre="Fundamentos de Programación",
        creditos=3,
        id_categoria=categoria.id_categoria
    )

    # Guarda en base de datos
    session.add(mat)
    session.commit()
    session.refresh(mat)

    return mat


# =========================
# FIXTURE: ESTUDIANTE
# =========================

@pytest.fixture
def estudiante(session):

    # Crea un estudiante de prueba
    est = Estudiantes(
        id_estudiante=uuid.uuid4(),
        nombre="Juan",
        apellido="Pérez",
        codigo="T00076001",
        correo="juanperez@utb.edu.co",
        status=StatusEstudiante.activo,
        hash_password="hashed"
    )

    # Guarda en base de datos
    session.add(est)
    session.commit()
    session.refresh(est)

    return est


# =========================
# FIXTURE: LOGRO
# =========================

@pytest.fixture
def logro(session):

    # Crea un logro de prueba
    l = Logros(
        id_logro=uuid.uuid4(),
        nombre="Materia aprobada",
        descripcion="Aprobaste tu primera materia"
    )

    # Guarda en base de datos
    session.add(l)
    session.commit()
    session.refresh(l)

    return l


# =========================
# FIXTURE: LOGRO-MATERIA
# =========================

@pytest.fixture
def logro_materia(session, logro, materia):

    # Relación entre logro y materia
    lm = LogroMaterias(
        id_logromateria=uuid.uuid4(),
        id_logro=logro.id_logro,
        id_materia=materia.id_materia
    )

    # Guarda en base de datos
    session.add(lm)
    session.commit()
    session.refresh(lm)

    return lm

