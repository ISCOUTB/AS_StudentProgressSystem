# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa repositorios relacionados con la malla curricular
from app.repositories import malla as repo
from app.repositories import carrera as carrera_repo
from app.repositories import materia as materia_repo

# Importa esquemas de malla y materia
from app.schemas.malla import (
    MallaCreate,
    MallaRead,
    MallaCompletaRead
)
from app.schemas.materia import MateriaRead

# Importa HTTPException para manejo de errores HTTP
from fastapi import HTTPException


# Obtiene la malla curricular completa de una carrera
def get_malla_by_carrera(session: Session, id_carrera: UUID) -> MallaCompletaRead:

    # Valida que la carrera exista
    carrera = carrera_repo.get_by_id(session, id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    # Obtiene las materias asociadas a la carrera
    materias = repo.get_materias_by_carrera(session, id_carrera)

    # Construye el objeto de respuesta con la información completa
    return MallaCompletaRead(
        id_carrera=carrera.id_carrera,
        nombre=carrera.nombre,
        codigo=carrera.codigo,
        materias=[MateriaRead.model_validate(m) for m in materias]
    )


# Agrega una materia a la malla curricular de una carrera
def add_materia(session: Session, data: MallaCreate) -> MallaRead:

    # Valida que la carrera exista
    carrera = carrera_repo.get_by_id(session, data.id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    # Valida que la materia exista
    materia = materia_repo.get_by_id(session, data.id_materia)
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    # Verifica si la relación ya existe
    existing = repo.get_by_ids(session, data.id_carrera, data.id_materia)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="La materia ya está en la malla de esta carrera"
        )

    # Crea la relación en la malla
    return repo.create(session, data.id_carrera, data.id_materia)


# Elimina una materia de la malla curricular
def remove_materia(session: Session, id_carrera: UUID, id_materia: UUID) -> dict:

    # Intenta eliminar la relación
    deleted = repo.delete(session, id_carrera, id_materia)

    # Si no existe, lanza error 404
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Relación no encontrada en la malla"
        )

    # Mensaje de confirmación
    return {"message": "Materia eliminada de la malla correctamente"}