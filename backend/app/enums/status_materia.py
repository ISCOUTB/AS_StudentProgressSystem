from enum import Enum

# Estado de una materia cursada por un estudiante
class StatusMaterias(str, Enum):
    aprobada = "Aprobada"
    reprobada = "Reprobada"
    encurso = "En Curso"
