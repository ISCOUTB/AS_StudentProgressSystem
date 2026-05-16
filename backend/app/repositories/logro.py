from sqlmodel import Session, select
from uuid import UUID

# Importa el modelo de la tabla Logros
from app.models.logro import Logros

# Importa los esquemas para crear y actualizar logros
from app.schemas.logro import LogroCreate, LogroUpdate


# Obtiene todos los registros de la tabla Logros
def get_all(session: Session) -> list[Logros]:
    # Ejecuta una consulta SELECT * FROM logros
    return session.exec(select(Logros)).all()


# Obtiene un logro específico por su ID
def get_by_id(session: Session, id_logro: UUID) -> Logros | None:
    # Busca el logro usando la clave primaria
    return session.get(Logros, id_logro)


# Crea un nuevo logro en la base de datos
def create(session: Session, data: LogroCreate) -> Logros:
    
    # Crea una instancia del modelo Logros
    # usando los datos recibidos
    logro = Logros(
        nombre=data.nombre,
        descripcion=data.descripcion,
        icon=data.icon
    )

    # Agrega el objeto a la sesión
    session.add(logro)

    # Guarda los cambios en la base de datos
    session.commit()

    # Refresca el objeto para obtener datos actualizados
    # como el ID generado automáticamente
    session.refresh(logro)

    # Retorna el logro creado
    return logro


# Actualiza un logro existente
def update(session: Session, id_logro: UUID, data: LogroUpdate) -> Logros | None:
    
    # Busca el logro por ID
    logro = session.get(Logros, id_logro)

    # Si no existe, retorna None
    if not logro:
        return None

    # Convierte los datos recibidos en un diccionario
    # excluyendo los campos no enviados
    update_data = data.model_dump(exclude_unset=True)

    # Recorre cada campo enviado y actualiza el atributo
    for key, value in update_data.items():
        setattr(logro, key, value)

    # Agrega nuevamente el objeto actualizado a la sesión
    session.add(logro)

    # Guarda los cambios
    session.commit()

    # Refresca el objeto con la información actualizada
    session.refresh(logro)

    # Retorna el logro actualizado
    return logro


# Elimina un logro de la base de datos
def delete(session: Session, id_logro: UUID) -> bool:
    
    # Busca el logro por ID
    logro = session.get(Logros, id_logro)

    # Si no existe, retorna False
    if not logro:
        return False

    # Elimina el registro
    session.delete(logro)

    # Guarda los cambios
    session.commit()

    # Retorna True indicando eliminación exitosa
    return True