
# Importa uuid para generar IDs aleatorios en pruebas
import uuid

# Importa pytest para pruebas automatizadas
import pytest

# Importa el repositorio de estudiante_materia (relación estudiante ↔ materia)
from app.repositories import estudiante_materia as repo

# Importa esquemas de creación y actualización
from app.schemas.estudiante_materia import EstudianteMateriaCreate, EstudianteMateriaUpdate

# Importa enum de estados de materia
from app.enums.status_materia import StatusMaterias


# =========================
# UTILIDAD PARA CREAR DATOS
# =========================

def make_data(estudiante, materia, **kwargs):

    # Datos por defecto para matrícula de materia
    defaults = dict(
        id_estudiante=estudiante.id_estudiante,
        id_materia=materia.id_materia,
        status=StatusMaterias.encurso,
        nota=0.0,
        semestre="PRIMER PERIODO 2026 PREGRADO"
    )

    # Permite sobrescribir valores en cada test
    defaults.update(kwargs)

    # Retorna schema listo para insertar
    return EstudianteMateriaCreate(**defaults)


# =========================
# TEST: CREAR RELACIÓN
# =========================

def test_create_estudiante_materia(session, estudiante, materia):

    # Crea relación estudiante-materia
    data = make_data(estudiante, materia)
    result = repo.create(session, data)

    # Verifica creación correcta
    assert result.id_estudiante == estudiante.id_estudiante
    assert result.id_materia == materia.id_materia
    assert result.status == StatusMaterias.encurso


# =========================
# TEST: GET POR ESTUDIANTE
# =========================

def test_get_by_estudiante(session, estudiante, materia):

    # Inserta relación
    repo.create(session, make_data(estudiante, materia))

    # Consulta materias del estudiante
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)

    # Debe existir una materia
    assert len(result) == 1


# =========================
# TEST: GET VACÍO
# =========================

def test_get_by_estudiante_vacio(session, estudiante):

    # Sin relaciones creadas
    result = repo.get_by_estudiante(session, estudiante.id_estudiante)

    # Debe ser lista vacía
    assert result == []


# =========================
# TEST: GET POR IDS (EXISTE)
# =========================

def test_get_by_ids_existente(session, estudiante, materia):

    # Crea relación
    repo.create(session, make_data(estudiante, materia))

    # Busca por IDs compuestos
    found = repo.get_by_ids(session, estudiante.id_estudiante, materia.id_materia)

    # Debe existir
    assert found is not None


# =========================
# TEST: GET POR IDS (NO EXISTE)
# =========================

def test_get_by_ids_inexistente(session):

    # IDs aleatorios inexistentes
    result = repo.get_by_ids(session, uuid.uuid4(), uuid.uuid4())

    # Debe ser None
    assert result is None


# =========================
# TEST: MATERIAS APROBADAS
# =========================

def test_get_aprobadas(session, estudiante, materia):

    # Crea materia aprobada
    repo.create(
        session,
        make_data(estudiante, materia,
                  status=StatusMaterias.aprobada,
                  nota=4.0)
    )

    # Consulta aprobadas
    aprobadas = repo.get_aprobadas(session, estudiante.id_estudiante)

    # Verifica resultado
    assert len(aprobadas) == 1
    assert aprobadas[0].status == StatusMaterias.aprobada


# =========================
# TEST: APROBADAS VACÍO
# =========================

def test_get_aprobadas_vacio(session, estudiante, materia):

    # Materia en curso
    repo.create(session, make_data(estudiante, materia, status=StatusMaterias.encurso))

    # Consulta aprobadas
    aprobadas = repo.get_aprobadas(session, estudiante.id_estudiante)

    # Debe ser vacío
    assert aprobadas == []


# =========================
# TEST: ACTUALIZAR RELACIÓN
# =========================

def test_update_estudiante_materia(session, estudiante, materia):

    # Crea relación
    repo.create(session, make_data(estudiante, materia))

    # Actualiza estado y nota
    updated = repo.update(
        session,
        estudiante.id_estudiante,
        materia.id_materia,
        EstudianteMateriaUpdate(
            status=StatusMaterias.aprobada,
            nota=4.5
        )
    )

    # Verifica cambios
    assert updated.status == StatusMaterias.aprobada
    assert updated.nota == 4.5


# =========================
# TEST: UPDATE INEXISTENTE
# =========================

def test_update_inexistente(session):

    # IDs inexistentes
    result = repo.update(
        session,
        uuid.uuid4(),
        uuid.uuid4(),
        EstudianteMateriaUpdate(nota=3.0)
    )

    # Debe ser None
    assert result is None


# =========================
# TEST: ELIMINAR RELACIÓN
# =========================

def test_delete_estudiante_materia(session, estudiante, materia):

    # Crea relación
    repo.create(session, make_data(estudiante, materia))

    # Elimina relación
    deleted = repo.delete(session, estudiante.id_estudiante, materia.id_materia)

    # Verifica eliminación
    assert deleted is True
    assert repo.get_by_ids(session, estudiante.id_estudiante, materia.id_materia) is None


# =========================
# TEST: DELETE INEXISTENTE
# =========================

def test_delete_inexistente(session):

    # Intenta eliminar algo inexistente
    result = repo.delete(session, uuid.uuid4(), uuid.uuid4())

    # Debe fallar
    assert result is False

