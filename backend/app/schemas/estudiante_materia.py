```python id="m4k9zq"
# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa el enum de estados de materias
from app.enums.status_materia import StatusMaterias


# Esquema para crear una relación estudiante-materia
class EstudianteMateriaCreate(BaseModel):

    # ID del estudiante
    id_estudiante: UUID

    # ID de la materia
    id_materia: UUID

    # Estado de la materia (por defecto: en curso)
    status: StatusMaterias = StatusMaterias.encurso

    # Nota inicial de la materia
    nota: float = 0.0

    # Semestre en el que el estudiante cursa la materia
    semestre: str


# Esquema para leer la relación estudiante-materia
class EstudianteMateriaRead(BaseModel):

    # ID del estudiante
    id_estudiante: UUID

    # ID de la materia
    id_materia: UUID

    # Estado actual de la materia
    status: StatusMaterias

    # Nota obtenida
    nota: float

    # Semestre actual
    semestre: str

    # Permite crear el modelo desde atributos ORM
    model_config = {"from_attributes": True}


# Esquema para actualizar la relación estudiante-materia
class EstudianteMateriaUpdate(BaseModel):

    # Estado opcional de la materia
    status: StatusMaterias | None = None

    # Nota opcional
    nota: float | None = None

    # Semestre opcional
    semestre: str | None = None
```
