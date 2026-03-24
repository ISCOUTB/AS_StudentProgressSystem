from enum import Enum

class StatusEstudiante(str, Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    egresado = "Egresado"