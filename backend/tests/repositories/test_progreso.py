
import uuid
import pytest
from app.repositories import progreso as repo
from app.models.carrera_materia import CarreraMateria
from app.models.estudiante_materia import EstudianteMateria
from app.enums.status_materia import StatusMaterias


def test_get_materias_con_status_aprobada(session, estudiante, carrera, materia):
    # Inserta la relación carrera-materia en la base de datos de prueba
    session.add(CarreraMateria(id_carrera=carrera.id_carrera, id_materia=materia.id_materia))
    
    # Inserta el progreso del estudiante en la materia con estado aprobada
    session.add(EstudianteMateria(
        id_estudiante=estudiante.id_estudiante,
        id_materia=materia.id_materia,
        status=StatusMaterias.aprobada,
        nota=4.5,
        semestre="PRIMER PERIODO 2026 PREGRADO"
    ))
    
    # Confirma los cambios en la base de datos de prueba
    session.commit()

    # Ejecuta la consulta del repositorio para obtener materias con estado del estudiante
    result = repo.get_materias_con_status(session, estudiante.id_estudiante, carrera.id_carrera)
    
    # Verifica que solo haya una materia en el resultado
    assert len(result) == 1
    
    # Verifica que el estado sea "aprobada"
    assert result[0]["status"] == StatusMaterias.aprobada
    
    # Verifica que el nombre de la materia sea el correcto
    assert result[0]["nombre"] == materia.nombre
    
    # Verifica que los créditos sean correctos
    assert result[0]["creditos"] == materia.creditos


def test_get_materias_con_status_sin_registro(session, estudiante, carrera, materia):
    # Crea relación carrera-materia sin progreso del estudiante
    session.add(CarreraMateria(id_carrera=carrera.id_carrera, id_materia=materia.id_materia))
    
    # Guarda cambios en la base de datos de prueba
    session.commit()

    # Consulta materias del estudiante en la carrera sin registros de progreso
    result = repo.get_materias_con_status(session, estudiante.id_estudiante, carrera.id_carrera)
    
    # Debe devolver una materia con estado por defecto (encurso)
    assert len(result) == 1
    assert result[0]["status"] == StatusMaterias.encurso


def test_get_materias_con_status_carrera_vacia(session, estudiante, carrera):
    # Consulta sin que existan materias en la carrera
    result = repo.get_materias_con_status(session, estudiante.id_estudiante, carrera.id_carrera)
    
    # Debe retornar lista vacía
    assert result == []


def test_get_materias_con_status_multiples(session, estudiante, carrera, categoria):
    # Importa el modelo de materias para crear una nueva materia manualmente
    from app.models.materia import Materias

    # Crea una segunda materia para la prueba
    mat2 = Materias(
        id_materia=uuid.uuid4(),
        nombre="Programación",
        codigo="C03A",
        creditos=3,
        id_categoria=categoria.id_categoria
    )
    
    # Agrega la materia a la sesión
    session.add(mat2)
    
    # Guarda la materia en la base de datos de prueba
    session.commit()

    # Relaciona la nueva materia con la carrera
    session.add(CarreraMateria(id_carrera=carrera.id_carrera, id_materia=mat2.id_materia))
    
    # Registra el progreso del estudiante con estado reprobada
    session.add(EstudianteMateria(
        id_estudiante=estudiante.id_estudiante,
        id_materia=mat2.id_materia,
        status=StatusMaterias.reprobada,
        nota=2.0,
        semestre="PRIMER PERIODO 2025 PREGRADO"
    ))
    
    # Confirma cambios en la base de datos de prueba
    session.commit()

    # Obtiene materias con estado del estudiante en la carrera
    result = repo.get_materias_con_status(session, estudiante.id_estudiante, carrera.id_carrera)
    
    # Verifica que solo haya una materia en el resultado
    assert len(result) == 1
    
    # Verifica que el estado sea "reprobada"
    assert result[0]["status"] == StatusMaterias.reprobada

