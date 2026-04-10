"""
seed.py — Poblar la base de datos con datos de prueba realistas.

Uso:
    cd backend
    python -m app.db.seed

Requiere que la base de datos ya esté corriendo y las tablas creadas.
Si quieres resetear, borra las tablas primero o usa --reset (ver abajo).
"""

import uuid
from datetime import date
from sqlalchemy.orm import Session
from app.db.db import engine, create_db_and_tables

# Importar todos los modelos para que SQLModel los registre
from app.models import (
    Carreras,
    Categorias,
    Materias,
    Logros,
    LogroMaterias,
    Estudiantes,
    EstudiantesCarreras,
    EstudianteMateria,
    EstudianteLogros,
    CarreraMateria,
)
from enums.escuela import Escuelas
from enums.status_estudiante import StatusEstudiante
from enums.status_materia import StatusMaterias
from enums.status_logro import StatusLogro

# Hash simple para datos de prueba (en producción usar bcrypt/passlib)
FAKE_HASH = "hashed_password_demo"


def seed() -> None:
    create_db_and_tables()

    with Session(engine) as db:
        # ── Evitar duplicar datos si ya existe semilla ────────────────────────
        if db.query(Carreras).first():
            print("⚠️  La base de datos ya tiene datos. Seed omitido.")
            return

        print("🌱 Iniciando seed...")

        # ── 1. Escuelas / Carreras ────────────────────────────────────────────
        ingenieria_sistemas = Carreras(
            nombre="Ingeniería de Sistemas",
            codigo="ISIS",
            escuela=Escuelas.etd,
        )
        ingenieria_industrial = Carreras(
            nombre="Ingeniería Industrial",
            codigo="IIND",
            escuela=Escuelas.eiad,
        )
        administracion = Carreras(
            nombre="Administración de Empresas",
            codigo="ADME",
            escuela=Escuelas.enls,
        )
        db.add_all([ingenieria_sistemas, ingenieria_industrial, administracion])
        db.flush()  # genera los UUIDs sin cerrar la transacción

        # ── 2. Categorías de materias ─────────────────────────────────────────
        cat_basica = Categorias(codigo="BSCA", nombre="Ciencias Básicas")
        cat_core = Categorias(codigo="CORE", nombre="Núcleo Profesional")
        cat_electiva = Categorias(codigo="ELEC", nombre="Electiva")
        db.add_all([cat_basica, cat_core, cat_electiva])
        db.flush()

        # ── 3. Materias ───────────────────────────────────────────────────────
        calculo = Materias(nombre="Cálculo I", creditos=4, id_categoria=cat_basica.id_categoria)
        algebra = Materias(nombre="Álgebra Lineal", creditos=3, id_categoria=cat_basica.id_categoria)
        prog1 = Materias(nombre="Programación I", creditos=4, id_categoria=cat_core.id_categoria)
        bd = Materias(nombre="Bases de Datos", creditos=3, id_categoria=cat_core.id_categoria)
        etica = Materias(nombre="Ética Profesional", creditos=2, id_categoria=cat_electiva.id_categoria)
        db.add_all([calculo, algebra, prog1, bd, etica])
        db.flush()

        # ── 4. Relación Carrera ↔ Materia ─────────────────────────────────────
        db.add_all([
            CarreraMateria(id_carrera=ingenieria_sistemas.id_carrera, id_materia=calculo.id_materia),
            CarreraMateria(id_carrera=ingenieria_sistemas.id_carrera, id_materia=algebra.id_materia),
            CarreraMateria(id_carrera=ingenieria_sistemas.id_carrera, id_materia=prog1.id_materia),
            CarreraMateria(id_carrera=ingenieria_sistemas.id_carrera, id_materia=bd.id_materia),
            CarreraMateria(id_carrera=ingenieria_sistemas.id_carrera, id_materia=etica.id_materia),
            CarreraMateria(id_carrera=ingenieria_industrial.id_carrera, id_materia=calculo.id_materia),
            CarreraMateria(id_carrera=administracion.id_carrera, id_materia=etica.id_materia),
        ])
        db.flush()

        # ── 5. Logros ─────────────────────────────────────────────────────────
        logro_100 = Logros(
            nombre="100% Aprovechamiento",
            descripcion="El estudiante aprobó todas las materias del semestre sin ninguna reprobación.",
        )
        logro_honor = Logros(
            nombre="Cuadro de Honor",
            descripcion="Promedio igual o superior a 4.5 en el semestre.",
        )
        db.add_all([logro_100, logro_honor])
        db.flush()

        # ── 6. Logro ↔ Materia ────────────────────────────────────────────────
        lm_prog = LogroMaterias(id_logro=logro_100.id_logro, id_materia=prog1.id_materia)
        lm_bd = LogroMaterias(id_logro=logro_honor.id_logro, id_materia=bd.id_materia)
        db.add_all([lm_prog, lm_bd])
        db.flush()

        # ── 7. Estudiantes ────────────────────────────────────────────────────
        estudiante1 = Estudiantes(
            nombre="Luis",
            apellido="Castellanos",
            codigo="T00123456",
            correo="luis.castellanos@utb.edu.co",
            status=StatusEstudiante.activo,
            hash_password=FAKE_HASH,
        )
        estudiante2 = Estudiantes(
            nombre="Valentina",
            apellido="Reyes",
            codigo="T00234567",
            correo="valentina.reyes@utb.edu.co",
            status=StatusEstudiante.activo,
            hash_password=FAKE_HASH,
        )
        estudiante3 = Estudiantes(
            nombre="Andrés",
            apellido="Martínez",
            codigo="T00345678",
            correo="andres.martinez@utb.edu.co",
            status=StatusEstudiante.egresado,
            hash_password=FAKE_HASH,
        )
        db.add_all([estudiante1, estudiante2, estudiante3])
        db.flush()

        # ── 8. Estudiante ↔ Carrera ───────────────────────────────────────────
        db.add_all([
            EstudiantesCarreras(
                semestre="2024-1",
                fechaadmision=date(2024, 1, 15),
                id_estudiante=estudiante1.id_estudiante,
                id_carrera=ingenieria_sistemas.id_carrera,
            ),
            EstudiantesCarreras(
                semestre="2024-1",
                fechaadmision=date(2024, 1, 15),
                id_estudiante=estudiante2.id_estudiante,
                id_carrera=ingenieria_sistemas.id_carrera,
            ),
            EstudiantesCarreras(
                semestre="2022-1",
                fechaadmision=date(2022, 1, 10),
                id_estudiante=estudiante3.id_estudiante,
                id_carrera=ingenieria_industrial.id_carrera,
            ),
        ])
        db.flush()

        # ── 9. Estudiante ↔ Materia ───────────────────────────────────────────
        db.add_all([
            EstudianteMateria(
                status=StatusMaterias.aprobada,
                nota=4.7,
                semestre="2024-1",
                id_estudiante=estudiante1.id_estudiante,
                Id_materia=calculo.id_materia,
            ),
            EstudianteMateria(
                status=StatusMaterias.encurso,
                nota=3.5,
                semestre="2024-1",
                id_estudiante=estudiante1.id_estudiante,
                Id_materia=prog1.id_materia,
            ),
            EstudianteMateria(
                status=StatusMaterias.aprobada,
                nota=4.9,
                semestre="2024-1",
                id_estudiante=estudiante2.id_estudiante,
                Id_materia=algebra.id_materia,
            ),
            EstudianteMateria(
                status=StatusMaterias.reprobada,
                nota=2.1,
                semestre="2024-1",
                id_estudiante=estudiante2.id_estudiante,
                Id_materia=bd.id_materia,
            ),
        ])
        db.flush()

        # ── 10. Estudiante ↔ Logro ─────────────────────────────────────────────
        db.add_all([
            EstudianteLogros(
                staus=StatusLogro.obtenido,
                id_estudiante=estudiante1.id_estudiante,
                id_logromateria=lm_prog.id_logromateria,
            ),
            EstudianteLogros(
                staus=StatusLogro.noobtenido,
                id_estudiante=estudiante2.id_estudiante,
                id_logromateria=lm_bd.id_logromateria,
            ),
        ])

        db.commit()
        print("✅ Seed completado con éxito.")
        print(f"   → {3} carreras")
        print(f"   → {5} materias")
        print(f"   → {3} estudiantes")
        print(f"   → {2} logros")


if __name__ == "__main__":
    seed()