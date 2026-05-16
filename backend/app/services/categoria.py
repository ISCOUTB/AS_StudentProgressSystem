
# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa el repositorio de categorías (capa de acceso a datos)
from app.repositories import categoria as repo

# Importa los esquemas de categoría
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaRead

# Importa HTTPException para manejar errores HTTP
from fastapi import HTTPException


# Mensaje estándar cuando una categoría no existe
CATEGORIA_NO_ENCONTRADA = "Categoría no encontrada"


# Obtiene todas las categorías
def get_all(session: Session) -> list[CategoriaRead]:
    return repo.get_all(session)


# Obtiene una categoría por ID
def get_by_id(session: Session, id_categoria: UUID) -> CategoriaRead:

    # Busca la categoría en el repositorio
    categoria = repo.get_by_id(session, id_categoria)

    # Si no existe, lanza error 404
    if not categoria:
        raise HTTPException(status_code=404, detail=CATEGORIA_NO_ENCONTRADA)

    return categoria


# Crea una nueva categoría
def create(session: Session, data: CategoriaCreate) -> CategoriaRead:

    # Valida si ya existe una categoría con el mismo nombre
    existing = repo.get_by_nombre(session, data.nombre)

    # Si existe, lanza error 400
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una categoría con ese nombre"
        )

    return repo.create(session, data)


# Actualiza una categoría existente
def update(session: Session, id_categoria: UUID, data: CategoriaUpdate) -> CategoriaRead:

    # Intenta actualizar la categoría
    categoria = repo.update(session, id_categoria, data)

    # Si no existe, lanza error 404
    if not categoria:
        raise HTTPException(status_code=404, detail=CATEGORIA_NO_ENCONTRADA)

    return categoria


# Elimina una categoría
def delete(session: Session, id_categoria: UUID) -> dict:

    # Intenta eliminar la categoría
    deleted = repo.delete(session, id_categoria)

    # Si no existe, lanza error 404
    if not deleted:
        raise HTTPException(status_code=404, detail=CATEGORIA_NO_ENCONTRADA)

    # Mensaje de confirmación
    return {"message": "Categoría eliminada correctamente"}

