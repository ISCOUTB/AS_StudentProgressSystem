"""
seed.py — Poblar la base de datos con datos de prueba realistas.

Estándares aplicados (estandar_de_datos_y_lista_de_logros.docx):
  - Código estudiantil : T000XXXXX  (5 dígitos, > 65000)  ej. T00065001
  - Código de materia  : 4 chars    ej. ISCO, CBAS, CHUM, CHUL
  - Formato semestre   : "PRIMER PERIODO 2026 PREGRADO"  (según Banner)
  - Nombre nivel       : Nivel I … Nivel X
  - Logros             : 38 logros distribuidos en 7 grupos

Uso:
    cd backend
    python -m app.db.seed
"""

from datetime import date
from sqlalchemy.orm import Session
from app.db.db import engine, create_db_and_tables

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
from app.enum.escuela import Escuelas
from app.enum.status_estudiante import StatusEstudiante
from app.enum.status_materia import StatusMaterias
from app.enum.status_logro import StatusLogro

FAKE_HASH = "hashed_password_demo"


# ─────────────────────────────────────────────────────────────────────────────
# LOGROS — 38 logros, 7 grupos (fuente: estandar_de_datos_y_lista_de_logros)
# ─────────────────────────────────────────────────────────────────────────────
LOGROS_DATA = [
    # Grupo 1 — Por materia (feedback inmediato)
    {"nombre": "Materia aprobada",      "descripcion": " Aprobaste tu primera materia."},
    {"nombre": "Buen desempeño",        "descripcion": " Aprobaste una materia con nota ≥ 4.0."},
    {"nombre": "Excelencia",            "descripcion": " Aprobaste una materia con nota ≥ 4.5."},
    {"nombre": "Primer paso",           "descripcion": " Primera materia del programa aprobada."},
    {"nombre": "El código empieza",     "descripcion": " Aprobaste tu primera materia de programación (ISCO C02A o ISCO C03A)."},
    {"nombre": "Base científica",       "descripcion": " Aprobaste tu primera materia de ciencias básicas (CBAS)."},
    # Grupo 2 — Por categoría
    {"nombre": "Científico formado",    "descripcion": " Todas las CBAS completadas (11 materias, 42 créditos)."},
    {"nombre": "Humanista digital",     "descripcion": " Todas las CHUM completadas (7 materias, 16 créditos)."},
    {"nombre": "Políglota",             "descripcion": " Todas las CHUL completadas (5 materias, 10 créditos)."},
    {"nombre": "Ingeniero de sistemas", "descripcion": " Núcleo ISCO completado (31 materias, 94 créditos)."},
    {"nombre": "Libre elección",        "descripcion": " Todas las electivas complementarias aprobadas."},
    # Grupo 3 — Por progreso académico
    {"nombre": "Arrancando fuerte",     "descripcion": " 25% del programa completado (≥ 40 créditos aprobados)."},
    {"nombre": "Mitad del camino",      "descripcion": " 50% del programa completado (≥ 81 créditos aprobados)."},
    {"nombre": "En la recta final",     "descripcion": " 75% del programa completado (≥ 121 créditos aprobados)."},
    {"nombre": "Programa completo",     "descripcion": " 100% del programa completado (162 créditos)."},
    {"nombre": "Décima superada",       "descripcion": " 10 materias aprobadas."},
    {"nombre": "Veinte arriba",         "descripcion": " 20 materias aprobadas."},
    {"nombre": "Treinta y contando",    "descripcion": " 30 materias aprobadas."},
    {"nombre": "Cuarenta logradas",     "descripcion": " 40 materias aprobadas."},
    {"nombre": "Graduando",             "descripcion": " 55 materias aprobadas."},
    # Grupo 4 — Por rendimiento académico
    {"nombre": "Cinco con distinción",  "descripcion": " 5 materias aprobadas con nota ≥ 4.0."},
    {"nombre": "Diez con distinción",   "descripcion": " 10 materias aprobadas con nota ≥ 4.0."},
    {"nombre": "Veinte con distinción", "descripcion": " 20 materias aprobadas con nota ≥ 4.0."},
    {"nombre": "Promedio alto",         "descripcion": " Promedio acumulado ≥ 4.0."},
    {"nombre": "Matrícula de honor",    "descripcion": " Promedio acumulado ≥ 4.5."},
    # Grupo 5 — Disciplina
    {"nombre": "Sin tropiezos",         "descripcion": " No has reprobado ninguna materia."},
    {"nombre": "Levantándome",          "descripcion": " Recuperaste una materia que habías reprobado."},
    {"nombre": "Racha ganadora",        "descripcion": " 3 semestres consecutivos sin reprobar."},
    {"nombre": "Semestre perfecto",     "descripcion": " Aprobaste todas las materias de un semestre."},
    # Grupo 6 — Hitos de la malla
    {"nombre": "Nivel I superado",          "descripcion": " Completaste el primer semestre (16 créditos, 7 materias Nivel I)."},
    {"nombre": "Fundamentos sólidos",       "descripcion": " Completaste Fundamentos de Programación (ISCO C02A)."},
    {"nombre": "Estructuras dominadas",     "descripcion": " Completaste Estructura de Datos (ISCO C05A)."},
    {"nombre": "Base de datos lista",       "descripcion": " Completaste Base de Datos (ISCO A01A)."},
    {"nombre": "Arquitecto de software",    "descripcion": " Completaste Arquitectura de Software (ISCO A04A)."},
    {"nombre": "Proyecto iniciado",         "descripcion": " Completaste Proyecto de Ingeniería I (ISCO P01A)."},
    {"nombre": "Proyecto finalizado",       "descripcion": " Completaste Proyecto de Ingeniería II (ISCO P02A)."},
    {"nombre": "Práctica completada",       "descripcion": " Completaste la Práctica Profesional (ISCO P03A)."},
    # Grupo 7 — Alto impacto
    {"nombre": "Progreso perfecto",         "descripcion": " Todas las materias cursadas están aprobadas (0 reprobadas, ≥ 1 aprobada)."},
]

# ─────────────────────────────────────────────────────────────────────────────
# MATERIAS — malla Ingeniería de Sistemas UTB
# Código categoría = 4 chars (ISCO, CBAS, CHUM, CHUL)
# ─────────────────────────────────────────────────────────────────────────────
MATERIAS_DATA = [
    # CBAS — 11 materias, 42 créditos
    {"nombre": "Cálculo Diferencial",              "cat": "CBAS", "creditos": 4},
    {"nombre": "Cálculo Integral",                 "cat": "CBAS", "creditos": 4},
    {"nombre": "Álgebra Lineal",                   "cat": "CBAS", "creditos": 3},
    {"nombre": "Ecuaciones Diferenciales",         "cat": "CBAS", "creditos": 4},
    {"nombre": "Física Mecánica",                  "cat": "CBAS", "creditos": 4},
    {"nombre": "Física Eléctrica",                 "cat": "CBAS", "creditos": 4},
    {"nombre": "Estadística y Probabilidad",       "cat": "CBAS", "creditos": 3},
    {"nombre": "Química General",                  "cat": "CBAS", "creditos": 4},
    {"nombre": "Introducción a la Ingeniería",     "cat": "CBAS", "creditos": 2},
    {"nombre": "Cálculo Vectorial",                "cat": "CBAS", "creditos": 4},
    {"nombre": "Investigación de Operaciones",     "cat": "CBAS", "creditos": 6},
    # CHUM — 7 materias, 16 créditos
    {"nombre": "Ética Profesional",                "cat": "CHUM", "creditos": 2},
    {"nombre": "Constitución Política",            "cat": "CHUM", "creditos": 2},
    {"nombre": "Cátedra UTB",                      "cat": "CHUM", "creditos": 2},
    {"nombre": "Electiva Humanidades I",           "cat": "CHUM", "creditos": 3},
    {"nombre": "Electiva Humanidades II",          "cat": "CHUM", "creditos": 3},
    {"nombre": "Emprendimiento e Innovación",      "cat": "CHUM", "creditos": 2},
    {"nombre": "Responsabilidad Social",           "cat": "CHUM", "creditos": 2},
    # CHUL — 5 materias, 10 créditos
    {"nombre": "Inglés I",                         "cat": "CHUL", "creditos": 2},
    {"nombre": "Inglés II",                        "cat": "CHUL", "creditos": 2},
    {"nombre": "Inglés III",                       "cat": "CHUL", "creditos": 2},
    {"nombre": "Inglés IV",                        "cat": "CHUL", "creditos": 2},
    {"nombre": "Inglés V",                         "cat": "CHUL", "creditos": 2},
    # ISCO — núcleo de sistemas
    {"nombre": "Fundamentos de Programación",      "cat": "ISCO", "creditos": 4},  # C02A
    {"nombre": "Programación Orientada a Objetos", "cat": "ISCO", "creditos": 4},  # C03A
    {"nombre": "Estructura de Datos",              "cat": "ISCO", "creditos": 4},  # C05A
    {"nombre": "Base de Datos",                    "cat": "ISCO", "creditos": 3},  # A01A
    {"nombre": "Arquitectura de Software",         "cat": "ISCO", "creditos": 3},  # A04A
    {"nombre": "Proyecto de Ingeniería I",         "cat": "ISCO", "creditos": 3},  # P01A
    {"nombre": "Proyecto de Ingeniería II",        "cat": "ISCO", "creditos": 3},  # P02A
    {"nombre": "Práctica Profesional",             "cat": "ISCO", "creditos": 9},  # P03A
    {"nombre": "Redes de Computadores",            "cat": "ISCO", "creditos": 3},
    {"nombre": "Sistemas Operativos",              "cat": "ISCO", "creditos": 3},
    {"nombre": "Ingeniería de Software",           "cat": "ISCO", "creditos": 3},
]


def seed() -> None:
    create_db_and_tables()

    with Session(engine) as db:
        if db.query(Carreras).first():
            print("  La base de datos ya tiene datos. Seed omitido.")
            return

        print(" Iniciando seed...")

        # ── 1. Carreras ───────────────────────────────────────────────────────
        ing_sistemas   = Carreras(nombre="Ingeniería de Sistemas",    codigo="ISIS", escuela=Escuelas.etd)
        ing_industrial = Carreras(nombre="Ingeniería Industrial",      codigo="IIND", escuela=Escuelas.eiad)
        administracion = Carreras(nombre="Administración de Empresas", codigo="ADME", escuela=Escuelas.enls)
        db.add_all([ing_sistemas, ing_industrial, administracion])
        db.flush()

        # ── 2. Categorías ─────────────────────────────────────────────────────
        cat_cbas = Categorias(codigo="CBAS", nombre="Ciencias Básicas")
        cat_chum = Categorias(codigo="CHUM", nombre="Humanidades")
        cat_chul = Categorias(codigo="CHUL", nombre="Lenguas")
        cat_isco = Categorias(codigo="ISCO", nombre="Núcleo de Sistemas")
        db.add_all([cat_cbas, cat_chum, cat_chul, cat_isco])
        db.flush()

        cat_map = {
            "CBAS": cat_cbas.id_categoria,
            "CHUM": cat_chum.id_categoria,
            "CHUL": cat_chul.id_categoria,
            "ISCO": cat_isco.id_categoria,
        }

        # ── 3. Materias ───────────────────────────────────────────────────────
        materias_obj: list[tuple[dict, Materias]] = []
        for m in MATERIAS_DATA:
            obj = Materias(nombre=m["nombre"], creditos=m["creditos"], id_categoria=cat_map[m["cat"]])
            db.add(obj)
            materias_obj.append((m, obj))
        db.flush()

        mat_by_nombre = {m.nombre: m for _, m in materias_obj}

        # ── 4. Carrera ↔ Materia ──────────────────────────────────────────────
        for _, mat in materias_obj:
            db.add(CarreraMateria(id_carrera=ing_sistemas.id_carrera, id_materia=mat.id_materia))
        for m_data, mat in materias_obj:
            if m_data["cat"] in ("CBAS", "CHUM", "CHUL"):
                db.add(CarreraMateria(id_carrera=ing_industrial.id_carrera, id_materia=mat.id_materia))
        db.flush()

        # ── 5. Logros (38) ────────────────────────────────────────────────────
        logros_obj: list[Logros] = []
        for l in LOGROS_DATA:
            obj = Logros(nombre=l["nombre"], descripcion=l["descripcion"])
            db.add(obj)
            logros_obj.append(obj)
        db.flush()

        # ── 6. LogroMaterias — hitos de la malla vinculados a materia ─────────
        def link(logro_idx: int, nombre_materia: str) -> LogroMaterias:
            lm = LogroMaterias(
                id_logro=logros_obj[logro_idx].id_logro,
                id_materia=mat_by_nombre[nombre_materia].id_materia,
            )
            db.add(lm)
            return lm

        lm_primera      = link(0,  "Fundamentos de Programación")   # Materia aprobada
        lm_buen         = link(1,  "Cálculo Diferencial")            # Buen desempeño
        lm_excelencia   = link(2,  "Álgebra Lineal")                 # Excelencia
        lm_codigo       = link(4,  "Fundamentos de Programación")    # El código empieza
        lm_base_cien    = link(5,  "Cálculo Diferencial")            # Base científica
        lm_fund_sol     = link(30, "Fundamentos de Programación")    # Fundamentos sólidos
        lm_estructuras  = link(31, "Estructura de Datos")            # Estructuras dominadas
        lm_bd           = link(32, "Base de Datos")                  # Base de datos lista
        lm_arquitecto   = link(33, "Arquitectura de Software")       # Arquitecto de software
        lm_proy_i       = link(34, "Proyecto de Ingeniería I")       # Proyecto iniciado
        lm_proy_ii      = link(35, "Proyecto de Ingeniería II")      # Proyecto finalizado
        lm_practica     = link(36, "Práctica Profesional")           # Práctica completada
        db.flush()

        # ── 7. Estudiantes ────────────────────────────────────────────────────
        # Formato : T000XXXXX — exactamente 9 chars, 5 dígitos finales > 65000
        estudiante1 = Estudiantes(
            nombre="Luis",      apellido="Castellanos",
            codigo="T00065001",                          # 65001 > 65000 ✔
            correo="luis.castellanos@utb.edu.co",
            status=StatusEstudiante.activo, hash_password=FAKE_HASH,
        )
        estudiante2 = Estudiantes(
            nombre="Valentina", apellido="Reyes",
            codigo="T00072430",                          # 72430 > 65000 ✔
            correo="valentina.reyes@utb.edu.co",
            status=StatusEstudiante.activo, hash_password=FAKE_HASH,
        )
        estudiante3 = Estudiantes(
            nombre="Andrés",    apellido="Martínez",
            codigo="T00068895",                          # 68895 > 65000 ✔
            correo="andres.martinez@utb.edu.co",
            status=StatusEstudiante.egresado, hash_password=FAKE_HASH,
        )
        estudiante4 = Estudiantes(
            nombre="Camila",    apellido="Torres",
            codigo="T00081234",                          # 81234 > 65000 ✔
            correo="camila.torres@utb.edu.co",
            status=StatusEstudiante.activo, hash_password=FAKE_HASH,
        )
        db.add_all([estudiante1, estudiante2, estudiante3, estudiante4])
        db.flush()

        # ── 8. Estudiante ↔ Carrera ───────────────────────────────────────────
        # Semestre formato Banner: "PRIMER PERIODO YYYY PREGRADO"
        db.add_all([
            EstudiantesCarreras(semestre="PRIMER PERIODO 2025 PREGRADO",  fechaadmision=date(2025, 1, 20), id_estudiante=estudiante1.id_estudiante, id_carrera=ing_sistemas.id_carrera),
            EstudiantesCarreras(semestre="PRIMER PERIODO 2025 PREGRADO",  fechaadmision=date(2025, 1, 20), id_estudiante=estudiante2.id_estudiante, id_carrera=ing_sistemas.id_carrera),
            EstudiantesCarreras(semestre="PRIMER PERIODO 2020 PREGRADO",  fechaadmision=date(2020, 1, 15), id_estudiante=estudiante3.id_estudiante, id_carrera=ing_industrial.id_carrera),
            EstudiantesCarreras(semestre="SEGUNDO PERIODO 2024 PREGRADO", fechaadmision=date(2024, 7, 10), id_estudiante=estudiante4.id_estudiante, id_carrera=ing_sistemas.id_carrera),
        ])
        db.flush()

        # ── 9. Estudiante ↔ Materia ───────────────────────────────────────────
        # Nivel semestre: "Nivel I", "Nivel II", …
        def em(est: Estudiantes, nombre_mat: str, status: StatusMaterias, nota: float, nivel: str) -> EstudianteMateria:
            return EstudianteMateria(
                status=status,
                nota=nota,
                semestre=f"Nivel {nivel}",
                id_estudiante=est.id_estudiante,
                Id_materia=mat_by_nombre[nombre_mat].id_materia,
            )

        db.add_all([
            # Luis — Nivel I aprobado por completo (semestre perfecto)
            em(estudiante1, "Cálculo Diferencial",          StatusMaterias.aprobada,  4.7, "I"),
            em(estudiante1, "Álgebra Lineal",               StatusMaterias.aprobada,  4.8, "I"),
            em(estudiante1, "Fundamentos de Programación",  StatusMaterias.aprobada,  4.9, "I"),
            em(estudiante1, "Inglés I",                     StatusMaterias.aprobada,  4.5, "I"),
            em(estudiante1, "Ética Profesional",            StatusMaterias.aprobada,  4.2, "I"),
            # Luis — Nivel II en curso
            em(estudiante1, "Cálculo Integral",             StatusMaterias.encurso,   3.8, "II"),
            em(estudiante1, "Estructura de Datos",          StatusMaterias.encurso,   4.1, "II"),

            # Valentina — buen rendimiento con una materia recuperada
            em(estudiante2, "Cálculo Diferencial",          StatusMaterias.aprobada,  4.0, "I"),
            em(estudiante2, "Álgebra Lineal",               StatusMaterias.aprobada,  4.6, "I"),
            em(estudiante2, "Fundamentos de Programación",  StatusMaterias.aprobada,  3.5, "I"),
            em(estudiante2, "Inglés I",                     StatusMaterias.aprobada,  3.9, "I"),
            em(estudiante2, "Cálculo Integral",             StatusMaterias.reprobada, 2.5, "II"),  # reprobó
            em(estudiante2, "Cálculo Integral",             StatusMaterias.aprobada,  3.8, "II"),  # recuperó → logro Levantándome

            # Andrés (egresado) — hitos completos
            em(estudiante3, "Cálculo Diferencial",          StatusMaterias.aprobada,  3.8, "I"),
            em(estudiante3, "Fundamentos de Programación",  StatusMaterias.aprobada,  4.5, "I"),
            em(estudiante3, "Estructura de Datos",          StatusMaterias.aprobada,  4.3, "II"),
            em(estudiante3, "Base de Datos",                StatusMaterias.aprobada,  4.6, "III"),
            em(estudiante3, "Arquitectura de Software",     StatusMaterias.aprobada,  4.4, "IV"),
            em(estudiante3, "Proyecto de Ingeniería I",     StatusMaterias.aprobada,  4.7, "IX"),
            em(estudiante3, "Proyecto de Ingeniería II",    StatusMaterias.aprobada,  4.8, "X"),
            em(estudiante3, "Práctica Profesional",         StatusMaterias.aprobada,  5.0, "X"),

            # Camila — Nivel I, recién ingresada
            em(estudiante4, "Cálculo Diferencial",          StatusMaterias.encurso,   0.0, "I"),
            em(estudiante4, "Inglés I",                     StatusMaterias.encurso,   0.0, "I"),
            em(estudiante4, "Ética Profesional",            StatusMaterias.aprobada,  4.3, "I"),
        ])
        db.flush()

        # ── 10. Estudiante ↔ Logros ───────────────────────────────────────────
        db.add_all([
            # Luis — semestre perfecto, excelencia, primer código
            EstudianteLogros(staus=StatusLogro.obtenido,   id_estudiante=estudiante1.id_estudiante, id_logromateria=lm_primera.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido,   id_estudiante=estudiante1.id_estudiante, id_logromateria=lm_excelencia.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido,   id_estudiante=estudiante1.id_estudiante, id_logromateria=lm_codigo.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido,   id_estudiante=estudiante1.id_estudiante, id_logromateria=lm_fund_sol.id_logromateria),
            EstudianteLogros(staus=StatusLogro.noobtenido, id_estudiante=estudiante1.id_estudiante, id_logromateria=lm_estructuras.id_logromateria),

            # Valentina — buen desempeño, ciencias básicas
            EstudianteLogros(staus=StatusLogro.obtenido,   id_estudiante=estudiante2.id_estudiante, id_logromateria=lm_primera.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido,   id_estudiante=estudiante2.id_estudiante, id_logromateria=lm_buen.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido,   id_estudiante=estudiante2.id_estudiante, id_logromateria=lm_base_cien.id_logromateria),

            # Andrés — todos los hitos de la malla
            EstudianteLogros(staus=StatusLogro.obtenido, id_estudiante=estudiante3.id_estudiante, id_logromateria=lm_primera.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido, id_estudiante=estudiante3.id_estudiante, id_logromateria=lm_codigo.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido, id_estudiante=estudiante3.id_estudiante, id_logromateria=lm_estructuras.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido, id_estudiante=estudiante3.id_estudiante, id_logromateria=lm_bd.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido, id_estudiante=estudiante3.id_estudiante, id_logromateria=lm_arquitecto.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido, id_estudiante=estudiante3.id_estudiante, id_logromateria=lm_proy_i.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido, id_estudiante=estudiante3.id_estudiante, id_logromateria=lm_proy_ii.id_logromateria),
            EstudianteLogros(staus=StatusLogro.obtenido, id_estudiante=estudiante3.id_estudiante, id_logromateria=lm_practica.id_logromateria),

            # Camila — aún sin logros de materia
            EstudianteLogros(staus=StatusLogro.noobtenido, id_estudiante=estudiante4.id_estudiante, id_logromateria=lm_primera.id_logromateria),
        ])

        db.commit()
        print(" Seed completado con éxito.")
        print(f"   → 3 carreras")
        print(f"   → 4 categorías  (CBAS, CHUM, CHUL, ISCO)")
        print(f"   → {len(MATERIAS_DATA)} materias de la malla Ing. Sistemas UTB")
        print(f"   → {len(LOGROS_DATA)} logros en 7 grupos")
        print(f"   → 4 estudiantes  (T000XXXXX, número > 65000)")


if __name__ == "__main__":
    seed()