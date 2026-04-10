from sqlmodel import Session, select
from uuid import UUID
from app.models.carrera_materia import CarreraMateria
from app.models.estudiante_materia import EstudianteMateria
from app.models.materia import Materias
from app.enums.status_materia import StatusMaterias

def get_materias_con_status(session: Session, id_estudiante: UUID, id_carrera: UUID) -> list[dict]:
    materias_carrera = session.exec(
        select(Materias)
        .join(CarreraMateria, CarreraMateria.id_materia == Materias.id_materia)
        .where(CarreraMateria.id_carrera == id_carrera)
    ).all()

    resultado = []
    for materia in materias_carrera:
        est_materia = session.exec(
            select(EstudianteMateria)
            .where(EstudianteMateria.id_estudiante == id_estudiante)
            .where(EstudianteMateria.id_materia == materia.id_materia)
        ).first()

        resultado.append({
            "id_materia": materia.id_materia,
            "nombre": materia.nombre,
            "creditos": materia.creditos,
            "status": est_materia.status if est_materia else StatusMaterias.encurso
        })

    return resultado