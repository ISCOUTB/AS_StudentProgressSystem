# Importaciones centralizadas de todos los modelos.
# Este archivo debe importarse antes de llamar a SQLModel.metadata.create_all()
# para garantizar que todas las tablas queden registradas en el metadata.
from app.models.carrera_materia import CarreraMateria
from app.models.carrera import Carreras
from app.models.categorias import Categorias
from app.models.estudiante_carrera import EstudiantesCarreras
from app.models.estudiante_logro import EstudianteLogros
from app.models.estudiante_materia import EstudianteMateria
from app.models.estudiante import Estudiantes
from app.models.logro_materia import LogroMaterias
from app.models.logro import Logros
from app.models.materia import Materias