from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    average: float
#esto define como se va a ver un estudiante, con su id, nombre y promedio. Esto es lo que se va a usar para mostrar la informacion del estudiante en la aplicacion.    