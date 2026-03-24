from fastapi import APIRouter
from app.schemas.student import Student

router = APIRouter()

@router.get("/students", response_model=list[Student])
def get_students():
    return [
        Student(id=1, name="Juan", average=4.5),
        Student(id=2, name="Maria", average=4.2),
    ]
#endpoint, esta ruta devuelve una lista de estudiantes con su id, nombre y promedio. Esto es lo que se va a mostrar en la aplicacion cuando se haga una solicitud a esta ruta.