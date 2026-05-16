from sqlmodel import Session, select
from uuid import UUID

# Importa el modelo de la tabla Materias
from app.models.materia import Materias

# Importa los esquemas para crear y actualizar materias
from app.schemas.materia import MateriaCreate, MateriaUpdate


# Obtiene todas las materias registradas
def get_all(session: Session) -> list[Materias]:
    
    # Ejecuta una consulta SELECT * FROM materias
    return session.exec(select(Materias)).all()


# Obtiene una materia por su ID
def get_by_id(session: Session, id_materia: UUID) -> Materias | None:
    
    # Busca la materia usando su clave primaria
    return session.get(Materias, id_materia)


# Obtiene una materia según su nombre
def get_by_nombre(session: Session, nombre: str) -> Materias | None:
    
    # Ejecuta una consulta filtrando por nombre
    return session.exec(
        select(Materias).where(Materias.nombre == nombre)
    ).first()


# Obtiene todas las materias pertenecientes a una categoría
def get_by_categoria(session: Session, id_categoria: UUID) -> list[Materias]:
    
    # Ejecuta una consulta filtrando por id_categoria
    return session.exec(
        select(Materias).where(Materias.id_categoria == id_categoria)
    ).all()


# Crea una nueva materia
def create(session: Session, data: MateriaCreate) -> Materias:
    
    # Crea una instancia del modelo Materias
    # usando los datos recibidos
    materia = Materias(
        nombre=data.nombre,
        creditos=data.creditos,
        id_categoria=data.id_categoria
    )

    # Agrega la materia a la sesión
    session.add(materia)

    # Guarda los cambios en la base de datos
    session.commit()

    # Refresca el objeto para obtener datos actualizados
    session.refresh(materia)

    # Retorna la materia creada
    return materia


# Actualiza una materia existente
def update(session: Session, id_materia: UUID, data: MateriaUpdate) -> Materias | None:
    
    # Busca la materia por ID
    materia = session.get(Materias, id_materia)

    # Si no existe, retorna None
    if not materia:
        return None

    # Convierte los datos recibidos en un diccionario
    # excluyendo los campos no enviados
    update_data = data.model_dump(exclude_unset=True)

    # Recorre cada campo enviado y actualiza sus valores
    for key, value in update_data.items():
        setattr(materia, key, value)

    # Agrega nuevamente el objeto actualizado a la sesión
    session.add(materia)

    # Guarda los cambios
    session.commit()

    # Refresca el objeto con la información actualizada
    session.refresh(materia)

    # Retorna la materia actualizada
    return materia


# Elimina una materia de la base de datos
def delete(session: Session, id_materia: UUID) -> bool:
    
    # Busca la materia por ID
    materia = session.get(Materias, id_materia)

    # Si no existe, retorna False
    if not materia:
        return False

    # Elimina el registro encontrado
    session.delete(materia)

    # Guarda los cambios
    session.commit()

    # Retorna True indicando eliminación exitosa
    return True