from enum import Enum

# Escuelas académicas disponibles en la universidad
class Escuelas(str, Enum):
    etd = "Escuela de Transformación Digital"
    eiad = "Escuela de ingeneniría, Arquitectura y Diseño"
    enls = "Escuela de Negocios, Leyes y Sociedad"
