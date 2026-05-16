from enum import Enum

# Estado académico del estudiante
class StatusEstudiante(str, Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    egresado = "Egresado"
