
# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa el repositorio de logros (capa de acceso a datos)
from app.repositories import logro as repo

# Importa esquemas de Logro
from app.schemas.logro import LogroCreate, LogroUpdate, LogroRead

# Importa HTTPException para manejo de errores HTTP
from fastapi import HTTPException


# Mensaje estándar cuando un logro no existe
LOGRO_NO_ENCONTRADO = "Logro no encontrado"


# Obtiene todos los logros
def get_all(session: Session) -> list[LogroRead]:
    return repo.get_all(session)


# Obtiene un logro por ID
def get_by_id(session: Session, id_logro: UUID) -> LogroRead:

    # Busca el logro en la base de datos
    logro = repo.get_by_id(session, id_logro)

    # Si no existe, lanza error 404
    if not logro:
        raise HTTPException(status_code=404, detail=LOGRO_NO_ENCONTRADO)

    return logro


# Crea un nuevo logro
def create(session: Session, data: LogroCreate) -> LogroRead:
    return repo.create(session, data)


# Actualiza un logro existente
def update(session: Session, id_logro: UUID, data: LogroUpdate) -> LogroRead:

    # Intenta actualizar el logro
    logro = repo.update(session, id_logro, data)

    # Si no existe, lanza error 404
    if not logro:
        raise HTTPException(status_code=404, detail=LOGRO_NO_ENCONTRADO)

    return logro


# Elimina un logro
def delete(session: Session, id_logro: UUID) -> dict:

    # Intenta eliminar el logro
    deleted = repo.delete(session, id_logro)

    # Si no existe, lanza error 404
    if not deleted:
        raise HTTPException(status_code=404, detail=LOGRO_NO_ENCONTRADO)

    # Mensaje de confirmación
    return {"message": "Logro eliminado correctamente"}

