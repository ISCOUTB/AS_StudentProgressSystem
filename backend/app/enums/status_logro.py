from enum import Enum

# Estado de un logro para un estudiante
class StatusLogro(str, Enum):
    obtenido = "Logro obtenido"
    noobtenido = "Logro sin obtener"
