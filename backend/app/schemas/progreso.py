```python id="p9m2xq"
# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa el enum de estado de materias
from app.enums.status_materia import StatusMaterias


# Esquema que representa el progreso individual de una materia
class MateriaProgressRead(BaseModel):

    # ID de la materia
    id_materia: UUID

    # Nombre de la materia
    nombre: str

    # Créditos de la materia
    creditos: int

    # Estado de la materia (aprobada, en curso, etc.)
    status: StatusMaterias

    # Permite construir el modelo desde atributos ORM
    model_config = {"from_attributes": True}


# Esquema general de progreso académico de un estudiante
class ProgresoRead(BaseModel):

    # ID del estudiante
    id_estudiante: UUID

    # Nombre del estudiante
    nombre_estudiante: str

    # ID de la carrera
    id_carrera: UUID

    # Nombre de la carrera
    nombre_carrera: str

    # Total de materias del plan de estudios
    total_materias: int

    # Cantidad de materias aprobadas
    materias_aprobadas: int

    # Cantidad de materias en curso
    materias_en_curso: int

    # Cantidad de materias reprobadas
    materias_reprobadas: int

    # Cantidad de materias pendientes
    materias_pendientes: int

    # Total de créditos del plan
    creditos_totales: int

    # Créditos aprobados por el estudiante
    creditos_aprobados: int

    # Porcentaje de avance en la carrera
    porcentaje_avance: float

    # Lista detallada del estado de cada materia
    materias: list[MateriaProgressRead]

    # Permite construir el modelo desde atributos ORM
    model_config = {"from_attributes": True}
```
