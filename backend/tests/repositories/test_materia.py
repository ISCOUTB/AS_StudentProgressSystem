Claro 💛 aquí tienes tu código **solo comentado, sin cambiar absolutamente nada de la lógica**:

```python
import uuid
import pytest
from app.repositories import materia as repo
from app.schemas.materia import MateriaCreate, MateriaUpdate


def make_data(id_categoria, **kwargs):
    # Genera datos base para crear una materia con valores por defecto
    # y permite sobrescribirlos con kwargs si es necesario
    defaults = dict(nombre="Fundamentos de Programación", creditos=3, id_categoria=id_categoria)
    defaults.update(kwargs)
    
    # Retorna un objeto MateriaCreate listo para usar en pruebas
    return MateriaCreate(**defaults)


def test_create_materia(session, categoria):
    # Prueba la creación de una materia en la base de datos
    result = repo.create(session, make_data(categoria.id_categoria))
    
    # Verifica que se haya generado un ID de materia
    assert result.id_materia is not None
    
    # Verifica que el nombre se haya guardado correctamente
    assert result.nombre == "Fundamentos de Programación"
    
    # Verifica que los créditos sean los esperados
    assert result.creditos == 3


def test_get_all_materias(session, categoria):
    # Crea dos materias para validar el listado completo
    repo.create(session, make_data(categoria.id_categoria, nombre="Materia A"))
    repo.create(session, make_data(categoria.id_categoria, nombre="Materia B"))
    
    # Obtiene todas las materias registradas
    result = repo.get_all(session)
    
    # Verifica que existan exactamente 2 materias
    assert len(result) == 2


def test_get_by_id_existente(session, categoria):
    # Crea una materia para luego buscarla por ID
    created = repo.create(session, make_data(categoria.id_categoria))
    
    # Busca la materia creada por su ID
    found = repo.get_by_id(session, created.id_materia)
    
    # Verifica que la materia exista
    assert found is not None
    
    # Verifica que el ID coincida con el creado
    assert found.id_materia == created.id_materia


def test_get_by_id_inexistente(session):
    # Intenta buscar una materia con un ID que no existe
    result = repo.get_by_id(session, uuid.uuid4())
    
    # Debe retornar None porque no existe
    assert result is None


def test_get_by_nombre_existente(session, categoria):
    # Crea una materia con nombre por defecto
    repo.create(session, make_data(categoria.id_categoria))
    
    # Busca la materia por su nombre
    found = repo.get_by_nombre(session, "Fundamentos de Programación")
    
    # Verifica que exista un resultado
    assert found is not None


def test_get_by_nombre_inexistente(session):
    # Intenta buscar una materia con un nombre inexistente
    result = repo.get_by_nombre(session, "No existe")
    
    # Debe retornar None
    assert result is None


def test_get_by_categoria(session, categoria):
    # Crea dos materias dentro de la misma categoría
    repo.create(session, make_data(categoria.id_categoria, nombre="Mat A"))
    repo.create(session, make_data(categoria.id_categoria, nombre="Mat B"))
    
    # Obtiene materias filtradas por categoría
    result = repo.get_by_categoria(session, categoria.id_categoria)
    
    # Verifica que existan dos materias en esa categoría
    assert len(result) == 2


def test_get_by_categoria_vacio(session, categoria):
    # Busca materias en una categoría que no tiene registros
    result = repo.get_by_categoria(session, uuid.uuid4())
    
    # Debe retornar una lista vacía
    assert result == []


def test_update_materia(session, categoria):
    # Crea una materia para luego actualizarla
    created = repo.create(session, make_data(categoria.id_categoria))
    
    # Actualiza solo el nombre de la materia
    updated = repo.update(session, created.id_materia, MateriaUpdate(nombre="Nuevo nombre"))
    
    # Verifica que el nombre fue actualizado correctamente
    assert updated.nombre == "Nuevo nombre"
    
    # Verifica que los créditos no cambiaron
    assert updated.creditos == 3


def test_update_inexistente(session, categoria):
    # Intenta actualizar una materia que no existe
    result = repo.update(session, uuid.uuid4(), MateriaUpdate(nombre="X"))
    
    # Debe retornar None
    assert result is None


def test_delete_materia(session, categoria):
    # Crea una materia para luego eliminarla
    created = repo.create(session, make_data(categoria.id_categoria))
    
    # Elimina la materia creada
    deleted = repo.delete(session, created.id_materia)
    
    # Verifica que la eliminación fue exitosa
    assert deleted is True
    
    # Verifica que ya no exista en la base de datos
    assert repo.get_by_id(session, created.id_materia) is None


def test_delete_inexistente(session):
    # Intenta eliminar una materia que no existe
    result = repo.delete(session, uuid.uuid4())
    
    # Debe retornar False porque no hay nada que eliminar
    assert result is False
```
