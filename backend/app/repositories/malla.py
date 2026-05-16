from sqlmodel import Session, select
from uuid import UUID

# Importa el modelo intermedio que relaciona carreras y materias
from app.models.carrera_materia import CarreraMateria

# Importa el modelo de materias
from app.models.materia import Materias

# Importa el modelo de carreras
from app.models.carrera import Carreras


# Obtiene todas las materias asociadas a una carrera específica
def get_materias_by_carrera(session: Session, id_carrera: UUID) -> list[Materias]:
    
    # Construye la consulta SQL
    statement = (
        select(Materias)

        # Realiza un JOIN entre Materias y CarreraMateria
        # usando el id de la materia
        .join(CarreraMateria, CarreraMateria.id_materia == Materias.id_materia)

        # Filtra por el id de la carrera recibido
        .where(CarreraMateria.id_carrera == id_carrera)
    )

    # Ejecuta la consulta y retorna todas las materias encontradas
    return session.exec(statement).all()


# Obtiene una relación específica entre carrera y materia
def get_by_ids(session: Session, id_carrera: UUID, id_materia: UUID) -> CarreraMateria | None:
    
    # Busca el registro en la tabla intermedia
    return session.exec(
        select(CarreraMateria)

        # Filtra por id de carrera
        .where(CarreraMateria.id_carrera == id_carrera)

        # Filtra por id de materia
        .where(CarreraMateria.id_materia == id_materia)
    ).first()


# Crea una nueva relación entre carrera y materia
def create(session: Session, id_carrera: UUID, id_materia: UUID) -> CarreraMateria:
    
    # Crea una instancia de la tabla intermedia
    malla = CarreraMateria(
        id_carrera=id_carrera,
        id_materia=id_materia
    )

    # Agrega el registro a la sesión
    session.add(malla)

    # Guarda los cambios en la base de datos
    session.commit()

    # Refresca el objeto para obtener datos actualizados
    session.refresh(malla)

    # Retorna la relación creada
    return malla


# Elimina una relación entre carrera y materia
def delete(session: Session, id_carrera: UUID, id_materia: UUID) -> bool:
    
    # Busca la relación específica
    malla = session.exec(
        select(CarreraMateria)

        # Filtra por id de carrera
        .where(CarreraMateria.id_carrera == id_carrera)

        # Filtra por id de materia
        .where(CarreraMateria.id_materia == id_materia)
    ).first()

    # Si no existe la relación, retorna False
    if not malla:
        return False

    # Elimina el registro encontrado
    session.delete(malla)

    # Guarda los cambios en la base de datos
    session.commit()

    # Retorna True indicando eliminación exitosa
    return True