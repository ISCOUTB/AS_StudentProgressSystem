from pydantic import BaseModel
from uuid import UUID
from app.schemas.materia import MateriaRead
from app.enums.status_materia import StatusMaterias

class MateriaProgressRead(BaseModel):
    id_materia: UUID
    nombre: str
    creditos: int
    status: StatusMaterias

    model_config = {"from_attributes": True}

class ProgresoRead(BaseModel):
    id_estudiante: UUID
    nombre_estudiante: str
    id_carrera: UUID
    nombre_carrera: str
    total_materias: int
    materias_aprobadas: int
    materias_en_curso: int
    materias_reprobadas: int
    materias_pendientes: int
    creditos_totales: int
    creditos_aprobados: int
    porcentaje_avance: float
    materias: list[MateriaProgressRead]

    model_config = {"from_attributes": True}