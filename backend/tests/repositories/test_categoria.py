
# Importa uuid para generar identificadores aleatorios en pruebas
import uuid

# Importa pytest para ejecutar tests automatizados
import pytest

# Importa el repositorio de categorías (capa de acceso a datos)
from app.repositories import categoria as repo

# Importa esquemas de creación y actualización de categoría
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


# =========================
# UTILIDAD PARA CREAR DATOS
# =========================

def make_data(**kwargs):

    # Valores por defecto para una categoría válida
    defaults = dict(
        codigo="ISCO",
        nombre="Ingeniería de Sistemas"
    )

    # Permite sobrescribir valores desde los tests
    defaults.update(kwargs)

    # Retorna objeto schema listo para insertar
    return CategoriaCreate(**defaults)


# =========================
# TEST: CREAR CATEGORÍA
# =========================

def test_create_categoria(session):

    # Inserta una categoría en la base de datos de prueba
    result = repo.create(session, make_data())

    # Verifica que se haya creado correctamente
    assert result.id_categoria is not None
    assert result.nombre == "Ingeniería de Sistemas"
    assert result.codigo == "ISCO"


# =========================
# TEST: OBTENER TODAS
# =========================

def test_get_all_categorias(session):

    # Crea dos categorías de prueba
    repo.create(session, make_data(codigo="ISCO", nombre="Ingeniería de Sistemas"))
    repo.create(session, make_data(codigo="CBAS", nombre="Ciencias Básicas"))

    # Obtiene todas las categorías
    result = repo.get_all(session)

    # Verifica que existan dos registros
    assert len(result) == 2


# =========================
# TEST: GET POR ID (EXISTE)
# =========================

def test_get_by_id_existente(session):

    # Crea categoría
    created = repo.create(session, make_data())

    # La busca por ID
    found = repo.get_by_id(session, created.id_categoria)

    # Verifica que exista
    assert found is not None
    assert found.id_categoria == created.id_categoria


# =========================
# TEST: GET POR ID (NO EXISTE)
# =========================

def test_get_by_id_inexistente(session):

    # Busca ID aleatorio inexistente
    result = repo.get_by_id(session, uuid.uuid4())

    # Debe ser None
    assert result is None


# =========================
# TEST: GET POR NOMBRE (EXISTE)
# =========================

def test_get_by_nombre_existente(session):

    # Crea categoría
    repo.create(session, make_data())

    # Busca por nombre
    found = repo.get_by_nombre(session, "Ingeniería de Sistemas")

    # Verifica resultado
    assert found is not None
    assert found.nombre == "Ingeniería de Sistemas"


# =========================
# TEST: GET POR NOMBRE (NO EXISTE)
# =========================

def test_get_by_nombre_inexistente(session):

    # Busca nombre inexistente
    result = repo.get_by_nombre(session, "No existe")

    # Debe retornar None
    assert result is None


# =========================
# TEST: ACTUALIZAR CATEGORÍA
# =========================

def test_update_categoria(session):

    # Crea categoría
    created = repo.create(session, make_data())

    # Actualiza nombre
    updated = repo.update(
        session,
        created.id_categoria,
        CategoriaUpdate(nombre="Nuevo")
    )

    # Verifica cambios
    assert updated.nombre == "Nuevo"
    assert updated.codigo == "ISCO"


# =========================
# TEST: UPDATE INEXISTENTE
# =========================

def test_update_categoria_inexistente(session):

    # Intenta actualizar ID inexistente
    result = repo.update(
        session,
        uuid.uuid4(),
        CategoriaUpdate(nombre="X")
    )

    # Debe ser None
    assert result is None


# =========================
# TEST: ELIMINAR CATEGORÍA
# =========================

def test_delete_categoria(session):

    # Crea categoría
    created = repo.create(session, make_data())

    # Elimina categoría
    deleted = repo.delete(session, created.id_categoria)

    # Verifica eliminación
    assert deleted is True
    assert repo.get_by_id(session, created.id_categoria) is None


# =========================
# TEST: DELETE INEXISTENTE
# =========================

def test_delete_categoria_inexistente(session):

    # Intenta eliminar ID inexistente
    result = repo.delete(session, uuid.uuid4())

    # Debe fallar
    assert result is False

