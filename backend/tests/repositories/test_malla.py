import uuid
import pytest
from app.repositories import malla as repo


def test_create_malla(session, carrera, materia):
    # Prueba la creación de una relación malla entre carrera y materia
    result = repo.create(session, carrera.id_carrera, materia.id_materia)
    
    # Verifica que la carrera asociada sea la correcta
    assert result.id_carrera == carrera.id_carrera
    
    # Verifica que la materia asociada sea la correcta
    assert result.id_materia == materia.id_materia


def test_get_materias_by_carrera(session, carrera, materia):
    # Crea una relación malla en la base de datos de prueba
    repo.create(session, carrera.id_carrera, materia.id_materia)
    
    # Obtiene las materias asociadas a una carrera específica
    result = repo.get_materias_by_carrera(session, carrera.id_carrera)
    
    # Verifica que solo exista una materia asociada
    assert len(result) == 1
    
    # Verifica que la materia obtenida sea la esperada
    assert result[0].id_materia == materia.id_materia


def test_get_materias_by_carrera_vacio(session, carrera):
    # Consulta materias de una carrera sin registros asociados
    result = repo.get_materias_by_carrera(session, carrera.id_carrera)
    
    # Debe devolver una lista vacía
    assert result == []


def test_get_by_ids_existente(session, carrera, materia):
    # Crea una relación malla para probar búsqueda por IDs
    repo.create(session, carrera.id_carrera, materia.id_materia)
    
    # Busca la relación usando ambos IDs
    found = repo.get_by_ids(session, carrera.id_carrera, materia.id_materia)
    
    # Verifica que sí exista el registro
    assert found is not None
    
    # Valida que los datos coincidan con los creados
    assert found.id_carrera == carrera.id_carrera
    assert found.id_materia == materia.id_materia


def test_get_by_ids_inexistente(session):
    # Intenta buscar una relación con IDs que no existen
    result = repo.get_by_ids(session, uuid.uuid4(), uuid.uuid4())
    
    # Debe retornar None porque no existe
    assert result is None


def test_delete_malla(session, carrera, materia):
    # Crea una relación antes de eliminarla
    repo.create(session, carrera.id_carrera, materia.id_materia)
    
    # Elimina la relación creada
    deleted = repo.delete(session, carrera.id_carrera, materia.id_materia)
    
    # Verifica que la eliminación fue exitosa
    assert deleted is True
    
    # Confirma que ya no existe en la base de datos
    assert repo.get_by_ids(session, carrera.id_carrera, materia.id_materia) is None


def test_delete_malla_inexistente(session):
    # Intenta eliminar una relación que no existe
    result = repo.delete(session, uuid.uuid4(), uuid.uuid4())
    
    # Debe retornar False porque no había nada que eliminar
    assert result is False