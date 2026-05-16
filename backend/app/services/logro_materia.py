```python id="m5k9qp"
# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa repositorios relacionados con logro-materia y validaciones
from app.repositories import logro_materia as repo
from app.repositories import logro as logro_repo
from app.repositories import materia as mat_repo

# Importa esquemas de logro-materia
from app.schemas.logro_materia import (
    LogroMateriaCreate,
    LogroMateriaRead
)

# Importa HTTPException para manejar errores HTTP
from fastapi import HTTPException


# Obtiene todos los registros de logro-materia
def get_all(session: Session) -> list[LogroMateriaRead]:
    return repo.get_all(session)


# Obtiene registros filtrados por logro
def get_by_logro(session: Session, id_logro: UUID) -> list[LogroMateriaRead]:
    return repo.get_by_logro(session, id_logro)


# Crea una relación logro-materia
def create(session: Session, data: LogroMateriaCreate) -> LogroMateriaRead:

    # Valida que el logro exista
    logro = logro_repo.get_by_id(session, data.id_logro)
    if not logro:
        raise HTTPException(status_code=404, detail="Logro no encontrado")

    # Si se envía una materia, valida que exista
    if data.id_materia:
        materia = mat_repo.get_by_id(session, data.id_materia)
        if not materia:
            raise HTTPException(status_code=404, detail="Materia no encontrada")

    # Crea la relación en la base de datos
    return repo.create(session, data)


# Elimina una relación logro-materia
def delete(session: Session, id_logromateria: UUID) -> dict:

    # Intenta eliminar el registro
    deleted = repo.delete(session, id_logromateria)

    # Si no existe, lanza error
    if not deleted:
        raise HTTPException(status_code=404, detail="LogroMateria no encontrado")

    # Mensaje de confirmación
    return {"message": "LogroMateria eliminado correctamente"}
```
