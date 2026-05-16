```python id="u8m3qp"
# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa repositorios relacionados con estudiante-logro y validaciones
from app.repositories import estudiante_logro as repo
from app.repositories import estudiante as est_repo
from app.repositories import logro_materia as logro_mat_repo

# Importa esquemas de estudiante-logro
from app.schemas.estudiante_logro import (
    EstudianteLogroCreate,
    EstudianteLogroUpdate,
    EstudianteLogroRead
)

# Importa HTTPException para manejar errores HTTP
from fastapi import HTTPException


# Obtiene los logros de un estudiante
def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudianteLogroRead]:

    # Valida que el estudiante exista
    est = est_repo.get_by_id(session, id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Retorna los logros asociados al estudiante
    return repo.get_by_estudiante(session, id_estudiante)


# Crea un nuevo registro estudiante-logro
def create(session: Session, data: EstudianteLogroCreate) -> EstudianteLogroRead:

    # Valida que el estudiante exista
    est = est_repo.get_by_id(session, data.id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Valida que el logro-materia exista
    logro_mat = logro_mat_repo.get_by_id(session, data.id_logromateria)
    if not logro_mat:
        raise HTTPException(status_code=404, detail="LogroMateria no encontrado")

    # Verifica si ya existe el registro
    existing = repo.get_by_ids(session, data.id_estudiante, data.id_logromateria)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="El estudiante ya tiene registrado este logro"
        )

    # Crea el registro estudiante-logro
    return repo.create(session, data)


# Actualiza un registro estudiante-logro
def update(
    session: Session,
    id_estudiante: UUID,
    id_logromateria: UUID,
    data: EstudianteLogroUpdate
) -> EstudianteLogroRead:

    # Intenta actualizar el registro
    est_logro = repo.update(session, id_estudiante, id_logromateria, data)

    # Si no existe, lanza error
    if not est_logro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return est_logro


# Elimina un registro estudiante-logro
def delete(session: Session, id_estudiante: UUID, id_logromateria: UUID) -> dict:

    # Intenta eliminar el registro
    deleted = repo.delete(session, id_estudiante, id_logromateria)

    # Si no existe, lanza error
    if not deleted:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    # Mensaje de confirmación
    return {"message": "Logro eliminado del estudiante correctamente"}
```
