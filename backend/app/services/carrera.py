# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa el repositorio de carreras (acceso a datos)
from app.repositories import carrera as repo

# Importa los esquemas de Carrera
from app.schemas.carrera import CarreraCreate, CarreraUpdate, CarreraRead

# Importa HTTPException para manejar errores HTTP
from fastapi import HTTPException


# Mensaje estándar cuando una carrera no existe
CARRERA_NO_ENCONTRADA = "Carrera no encontrada"


# Obtiene todas las carreras
def get_all(session: Session) -> list[CarreraRead]:
    return repo.get_all(session)


# Obtiene una carrera por ID
def get_by_id(session: Session, id_carrera: UUID) -> CarreraRead:
    
    # Busca la carrera en el repositorio
    carrera = repo.get_by_id(session, id_carrera)

    # Si no existe, lanza error 404
    if not carrera:
        raise HTTPException(status_code=404, detail=CARRERA_NO_ENCONTRADA)

    return carrera


# Crea una nueva carrera
def create(session: Session, data: CarreraCreate) -> CarreraRead:
    
    # Valida si ya existe una carrera con el mismo código
    existing = repo.get_by_codigo(session, data.codigo)

    # Si existe, lanza error 400
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una carrera con ese código"
        )

    return repo.create(session, data)


# Actualiza una carrera existente
def update(session: Session, id_carrera: UUID, data: CarreraUpdate) -> CarreraRead:
    
    # Intenta actualizar la carrera
    carrera = repo.update(session, id_carrera, data)

    # Si no existe, lanza error 404
    if not carrera:
        raise HTTPException(status_code=404, detail=CARRERA_NO_ENCONTRADA)

    return carrera


# Elimina una carrera
def delete(session: Session, id_carrera: UUID) -> dict:
    
    # Intenta eliminar la carrera
    deleted = repo.delete(session, id_carrera)

    # Si no existe, lanza error 404
    if not deleted:
        raise HTTPException(status_code=404, detail=CARRERA_NO_ENCONTRADA)

    # Respuesta de confirmación
    return {"message": "Carrera eliminada correctamente"}