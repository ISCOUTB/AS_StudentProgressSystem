```python id="c9m4qp"
# Importa uuid para generar IDs aleatorios en pruebas
import uuid

# Importa pytest para ejecutar pruebas automatizadas
import pytest

# Importa el repositorio de carreras (capa de acceso a datos)
from app.repositories import carrera as repo

# Importa esquemas de creación y actualización de carrera
from app.schemas.carrera import CarreraCreate, CarreraUpdate

# Importa enumeración de escuelas
from app.enums.escuela import Escuelas


# =========================
# UTILIDAD PARA CREAR DATOS
# =========================

def make_data(**kwargs):

    # Datos por defecto para una carrera válida
    defaults = dict(
        nombre="Ingeniería de Sistemas",
        codigo="ISCO",
        escuela=Escuelas.etd
    )

    # Permite sobrescribir valores en los tests
    defaults.update(kwargs)

    # Retorna objeto schema listo para insertar
    return CarreraCreate(**defaults)


# =========================
# TEST: CREAR CARRERA
# =========================

def test_create_carrera(session):

    # Crea una carrera en la base de datos de prueba
    data = make_data()
    result = repo.create(session, data)

    # Verifica que se haya creado correctamente
    assert result.id_carrera is not None
    assert result.nombre == "Ingeniería de Sistemas"
    assert result.codigo == "ISCO"


# =========================
# TEST: OBTENER TODAS
# =========================

def test_get_all_carreras(session):

    # Inserta dos carreras
    repo.create(session, make_data(codigo="ISCO"))
    repo.create(session, make_data(nombre="Ingeniería Civil", codigo="ICIV"))

    # Obtiene todas las carreras
    result = repo.get_all(session)

    # Verifica cantidad
    assert len(result) == 2


# =========================
# TEST: GET POR ID (EXISTE)
# =========================

def test_get_by_id_existente(session):

    # Crea una carrera
    created = repo.create(session, make_data())

    # La busca por ID
    found = repo.get_by_id(session, created.id_carrera)

    # Verifica que exista
    assert found is not None
    assert found.id_carrera == created.id_carrera


# =========================
# TEST: GET POR ID (NO EXISTE)
# =========================

def test_get_by_id_inexistente(session):

    # Busca un ID aleatorio inexistente
    result = repo.get_by_id(session, uuid.uuid4())

    # Debe retornar None
    assert result is None


# =========================
# TEST: GET POR CÓDIGO (EXISTE)
# =========================

def test_get_by_codigo_existente(session):

    # Crea carrera
    repo.create(session, make_data())

    # Busca por código
    found = repo.get_by_codigo(session, "ISCO")

    # Verifica resultado
    assert found is not None
    assert found.codigo == "ISCO"


# =========================
# TEST: GET POR CÓDIGO (NO EXISTE)
# =========================

def test_get_by_codigo_inexistente(session):

    # Busca código inexistente
    result = repo.get_by_codigo(session, "XXXX")

    # Debe ser None
    assert result is None


# =========================
# TEST: ACTUALIZAR CARRERA
# =========================

def test_update_carrera(session):

    # Crea carrera
    created = repo.create(session, make_data())

    # Actualiza nombre
    updated = repo.update(
        session,
        created.id_carrera,
        CarreraUpdate(nombre="Nuevo Nombre")
    )

    # Verifica cambios
    assert updated.nombre == "Nuevo Nombre"
    assert updated.codigo == "ISCO"


# =========================
# TEST: UPDATE INEXISTENTE
# =========================

def test_update_carrera_inexistente(session):

    # Intenta actualizar ID inexistente
    result = repo.update(
        session,
        uuid.uuid4(),
        CarreraUpdate(nombre="X")
    )

    # Debe ser None
    assert result is None


# =========================
# TEST: ELIMINAR CARRERA
# =========================

def test_delete_carrera(session):

    # Crea carrera
    created = repo.create(session, make_data())

    # Elimina carrera
    deleted = repo.delete(session, created.id_carrera)

    # Verifica eliminación
    assert deleted is True
    assert repo.get_by_id(session, created.id_carrera) is None


# =========================
# TEST: DELETE INEXISTENTE
# =========================

def test_delete_carrera_inexistente(session):

    # Intenta eliminar ID inexistente
    result = repo.delete(session, uuid.uuid4())

    # Debe fallar
    assert result is False
```
