from sqlmodel import Session
from uuid import UUID
from app.repositories import progreso as repo
from app.repositories import estudiante as est_repo
from app.repositories import carrera as carrera_repo
from app.repositories import estudiante_carrera as est_carrera_repo
from app.schemas.progreso import ProgresoRead, MateriaProgressRead
from app.enums.status_materia import StatusMaterias
from fastapi import HTTPException

def get_progreso(session: Session, id_estudiante: UUID, id_carrera: UUID) -> ProgresoRead:
    estudiante = est_repo.get_by_id(session, id_estudiante)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    carrera = carrera_repo.get_by_id(session, id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    matricula = est_carrera_repo.get_by_ids(session, id_estudiante, id_carrera)
    if not matricula:
        raise HTTPException(status_code=404, detail="El estudiante no está matriculado en esta carrera")

    materias = repo.get_materias_con_status(session, id_estudiante, id_carrera)

    total_materias = len(materias)
    materias_aprobadas = sum(1 for m in materias if m["status"] == StatusMaterias.aprobada)
    materias_en_curso = sum(1 for m in materias if m["status"] == StatusMaterias.encurso)
    materias_reprobadas = sum(1 for m in materias if m["status"] == StatusMaterias.reprobada)
    materias_pendientes = total_materias - materias_aprobadas - materias_en_curso - materias_reprobadas

    creditos_totales = sum(m["creditos"] for m in materias)
    creditos_aprobados = sum(m["creditos"] for m in materias if m["status"] == StatusMaterias.aprobada)
    porcentaje_avance = round((creditos_aprobados / creditos_totales * 100), 2) if creditos_totales > 0 else 0.0

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