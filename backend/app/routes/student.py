from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from uuid import UUID

from app.db.db import get_session
from app.schemas.student import Student, StudentResponse
from app.models.estudiante import Estudiantes
from app.models.estudiante_materia import EstudianteMateria
from app.enum.status_materia import StatusMaterias

router = APIRouter(prefix="/students", tags=["Estudiantes"])


# ─── GET /students ────────────────────────────────────────────────────────────
@router.get("/", response_model=list[Student])
def get_students(db: Session = Depends(get_session)):
    """
    Retorna todos los estudiantes con su promedio calculado desde la BD.
    Mantiene el contrato de respuesta original (id, name, average).
    """
    estudiantes = db.execute(select(Estudiantes)).scalars().all()

    resultado = []
    for idx, est in enumerate(estudiantes, start=1):
        # Calcular promedio de notas del estudiante
        notas = db.execute(
            select(EstudianteMateria.nota).where(
                EstudianteMateria.id_estudiante == est.id_estudiante
            )
        ).scalars().all()

        promedio = round(sum(notas) / len(notas), 2) if notas else 0.0

        resultado.append(
            Student(
                id=idx,
                name=f"{est.nombre} {est.apellido}",
                average=promedio,
            )
        )

    return resultado


# ─── GET /students/{id_estudiante} ───────────────────────────────────────────
@router.get("/{id_estudiante}", response_model=StudentResponse)
def get_student(id_estudiante: UUID, db: Session = Depends(get_session)):
    """Retorna el detalle completo de un estudiante por su UUID."""
    estudiante = db.get(Estudiantes, id_estudiante)

    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudiante con id {id_estudiante} no encontrado.",
        )

    return estudiante