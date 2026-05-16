from sqlmodel import Session, select
from uuid import UUID

# Importa la tabla intermedia entre carreras y materias
from app.models.carrera_materia import CarreraMateria

# Importa la relación entre estudiantes y materias
from app.models.estudiante_materia import EstudianteMateria

# Importa el modelo de materias
from app.models.materia import Materias

# Importa el enum con los posibles estados de una materia
from app.enums.status_materia import StatusMaterias


# Obtiene todas las materias de una carrera
# junto con el estado de cada materia para un estudiante
def get_materias_con_status(
    session: Session,
    id_estudiante: UUID,
    id_carrera: UUID
) -> list[dict]:

    # Consulta todas las materias asociadas a la carrera
    materias_carrera = session.exec(
        select(Materias)

        # Realiza un JOIN entre Materias y CarreraMateria
        .join(CarreraMateria, CarreraMateria.id_materia == Materias.id_materia)

        # Filtra por la carrera seleccionada
        .where(CarreraMateria.id_carrera == id_carrera)
    ).all()

    # Lista donde se almacenará el resultado final
    resultado = []

    # Recorre cada materia encontrada
    for materia in materias_carrera:

        # Busca si el estudiante tiene un registro
        # asociado a esa materia
        est_materia = session.exec(
            select(EstudianteMateria)

            # Filtra por estudiante
            .where(EstudianteMateria.id_estudiante == id_estudiante)

            # Filtra por materia
            .where(EstudianteMateria.id_materia == materia.id_materia)
        ).first()

        # Agrega la información de la materia al resultado
        resultado.append({

            # ID de la materia
            "id_materia": materia.id_materia,

            # Nombre de la materia
            "nombre": materia.nombre,

            # Créditos de la materia
            "creditos": materia.creditos,

            # Estado de la materia:
            # - Si existe registro del estudiante, usa su status
            # - Si no existe, asigna "encurso" por defecto
            "status": est_materia.status if est_materia else StatusMaterias.encurso
        })

    # Retorna la lista completa de materias con estado
    return resultado