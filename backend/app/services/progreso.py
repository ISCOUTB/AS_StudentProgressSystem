```python id="p7m4qp"
# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa repositorios necesarios para validar datos y obtener progreso
from app.repositories import progreso as repo
from app.repositories import estudiante as est_repo
from app.repositories import carrera as carrera_repo
from app.repositories import estudiante_carrera as est_carrera_repo

# Importa esquemas de respuesta del progreso
from app.schemas.progreso import ProgresoRead, MateriaProgressRead

# Importa enumeración de estados de materia
from app.enums.status_materia import StatusMaterias

# Importa HTTPException para manejo de errores HTTP
from fastapi import HTTPException


# Obtiene el progreso académico de un estudiante en una carrera
def get_progreso(session: Session, id_estudiante: UUID, id_carrera: UUID) -> ProgresoRead:

    # Valida que el estudiante exista
    estudiante = est_repo.get_by_id(session, id_estudiante)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Valida que la carrera exista
    carrera = carrera_repo.get_by_id(session, id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    # Valida que el estudiante esté matriculado en la carrera
    matricula = est_carrera_repo.get_by_ids(session, id_estudiante, id_carrera)
    if not matricula:
        raise HTTPException(
            status_code=404,
            detail="El estudiante no está matriculado en esta carrera"
        )

    # Obtiene las materias con su estado para ese estudiante y carrera
    materias = repo.get_materias_con_status(session, id_estudiante, id_carrera)

    # Calcula métricas generales del progreso
    total_materias = len(materias)

    materias_aprobadas = sum(
        1 for m in materias if m["status"] == StatusMaterias.aprobada
    )

    materias_en_curso = sum(
        1 for m in materias if m["status"] == StatusMaterias.encurso
    )

    materias_reprobadas = sum(
        1 for m in materias if m["status"] == StatusMaterias.reprobada
    )

    materias_pendientes = (
        total_materias
        - materias_aprobadas
        - materias_en_curso
        - materias_reprobadas
    )

    # Cálculo de créditos
    creditos_totales = sum(m["creditos"] for m in materias)

    creditos_aprobados = sum(
        m["creditos"] for m in materias if m["status"] == StatusMaterias.aprobada
    )

    # Porcentaje de avance académico
    porcentaje_avance = (
        round((creditos_aprobados / creditos_totales * 100), 2)
        if creditos_totales > 0
        else 0.0
    )

    # Construcción del objeto de respuesta
    return ProgresoRead(
        id_estudiante=id_estudiante,
        nombre_estudiante=f"{estudiante.nombre} {estudiante.apellido}",
        id_carrera=id_carrera,
        nombre_carrera=carrera.nombre,
        total_materias=total_materias,
        materias_aprobadas=materias_aprobadas,
        materias_en_curso=materias_en_curso,
        materias_reprobadas=materias_reprobadas,
        materias_pendientes=materias_pendientes,
        creditos_totales=creditos_totales,
        creditos_aprobados=creditos_aprobados,
        porcentaje_avance=porcentaje_avance,
        materias=[MateriaProgressRead(**m) for m in materias]
    )
```
