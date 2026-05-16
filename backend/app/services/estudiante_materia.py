```python id="x9m4qp"
# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa repositorios relacionados con estudiante-materia y validaciones
from app.repositories import estudiante_materia as repo
from app.repositories import estudiante as est_repo
from app.repositories import materia as mat_repo

# Importa esquemas de estudiante-materia
from app.schemas.estudiante_materia import (
    EstudianteMateriaCreate,
    EstudianteMateriaUpdate,
    EstudianteMateriaRead
)

# Importa HTTPException para manejar errores HTTP
from fastapi import HTTPException


# Obtiene las materias de un estudiante
def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudianteMateriaRead]:

    # Valida que el estudiante exista
    est = est_repo.get_by_id(session, id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Retorna las materias asociadas al estudiante
    return repo.get_by_estudiante(session, id_estudiante)


# Crea una nueva relación estudiante-materia
def create(session: Session, data: EstudianteMateriaCreate) -> EstudianteMateriaRead:

    # Valida que el estudiante exista
    est = est_repo.get_by_id(session, data.id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Valida que la materia exista
    materia = mat_repo.get_by_id(session, data.id_materia)
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    # Verifica si ya existe la relación
    existing = repo.get_by_ids(session, data.id_estudiante, data.id_materia)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="El estudiante ya tiene registrada esta materia"
        )

    # Crea la relación estudiante-materia
    return repo.create(session, data)


# Actualiza una relación estudiante-materia
def update(
    session: Session,
    id_estudiante: UUID,
    id_materia: UUID,
    data: EstudianteMateriaUpdate
) -> EstudianteMateriaRead:

    # Intenta actualizar el registro
    est_materia = repo.update(session, id_estudiante, id_materia, data)

    # Si no existe, lanza error
    if not est_materia:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return est_materia


# Elimina una relación estudiante-materia
def delete(session: Session, id_estudiante: UUID, id_materia: UUID) -> dict:

    # Intenta eliminar el registro
    deleted = repo.delete(session, id_estudiante, id_materia)

    # Si no existe, lanza error
    if not deleted:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    # Mensaje de confirmación
    return {"message": "Materia eliminada del estudiante correctamente"}
```
