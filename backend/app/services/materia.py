```python id="q2m9qp"
# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa repositorios de materia y categoría
from app.repositories import materia as repo
from app.repositories import categoria as cat_repo

# Importa esquemas de materia
from app.schemas.materia import MateriaCreate, MateriaUpdate, MateriaRead

# Importa HTTPException para manejo de errores HTTP
from fastapi import HTTPException


# Mensajes estándar de error
MATERIA_NO_ENCONTRADA = "Materia no encontrada"
CATEGORIA_NO_ENCONTRADA = "Categoría no encontrada"


# Obtiene todas las materias
def get_all(session: Session) -> list[MateriaRead]:
    return repo.get_all(session)


# Obtiene una materia por ID
def get_by_id(session: Session, id_materia: UUID) -> MateriaRead:

    # Busca la materia en la base de datos
    materia = repo.get_by_id(session, id_materia)

    # Si no existe, lanza error 404
    if not materia:
        raise HTTPException(status_code=404, detail=MATERIA_NO_ENCONTRADA)

    return materia


# Obtiene materias por categoría
def get_by_categoria(session: Session, id_categoria: UUID) -> list[MateriaRead]:
    return repo.get_by_categoria(session, id_categoria)


# Crea una nueva materia
def create(session: Session, data: MateriaCreate) -> MateriaRead:

    # Valida que la categoría exista
    categoria = cat_repo.get_by_id(session, data.id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail=CATEGORIA_NO_ENCONTRADA)

    # Verifica si ya existe una materia con el mismo nombre
    existing = repo.get_by_nombre(session, data.nombre)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una materia con ese nombre"
        )

    return repo.create(session, data)


# Actualiza una materia existente
def update(session: Session, id_materia: UUID, data: MateriaUpdate) -> MateriaRead:

    # Si se está cambiando la categoría, valida su existencia
    if data.id_categoria:
        categoria = cat_repo.get_by_id(session, data.id_categoria)
        if not categoria:
            raise HTTPException(status_code=404, detail=CATEGORIA_NO_ENCONTRADA)

    # Intenta actualizar la materia
    materia = repo.update(session, id_materia, data)

    # Si no existe, lanza error 404
    if not materia:
        raise HTTPException(status_code=404, detail=MATERIA_NO_ENCONTRADA)

    return materia


# Elimina una materia
def delete(session: Session, id_materia: UUID) -> dict:

    # Intenta eliminar la materia
    deleted = repo.delete(session, id_materia)

    # Si no existe, lanza error 404
    if not deleted:
        raise HTTPException(status_code=404, detail=MATERIA_NO_ENCONTRADA)

    # Mensaje de confirmación
    return {"message": "Materia eliminada correctamente"}
```
