"""
Seed v2 para AS_StudentProgressSystem
Malla: Ingeniería de Sistemas y Computación - UTB (vigente desde 201910)
"""
import uuid
from datetime import date
from sqlmodel import Session, create_engine, SQLModel, select
from app.core.config import settings
from app.models import (
    Carreras, Categorias, Materias, CarreraMateria,
    Estudiantes, EstudiantesCarreras, EstudianteMateria,
    Logros, LogroMaterias, EstudianteLogros
)
from app.enums.status_materia import StatusMaterias
from app.enums.status_estudiante import StatusEstudiante
from app.enums.status_logro import StatusLogro
from app.enums.escuela import Escuelas
import hashlib

engine = create_engine(settings.DATABASE_URL, echo=False)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def asignar_logros(session, est, materias_aprobadas, logro_map, logros_materias_map):
    """Evalúa y asigna los logros obtenidos por el estudiante según su progreso real."""

    aprobadas_ids = {em.id_materia for em in materias_aprobadas}
    notas = {em.id_materia: em.nota for em in materias_aprobadas}
    total_aprobadas = len(materias_aprobadas)

    creditos_aprobados = 0
    for em in materias_aprobadas:
        mat = session.get(Materias, em.id_materia)
        if mat:
            creditos_aprobados += mat.creditos

    promedio = (sum(notas.values()) / total_aprobadas) if total_aprobadas > 0 else 0

    def obtener_logro(nombre):
        logro = logro_map.get(nombre)
        if not logro:
            return
        lm = logros_materias_map.get(logro.id_logro)
        if not lm:
            return
        existing = session.exec(
            select(EstudianteLogros)
            .where(EstudianteLogros.id_estudiante == est.id_estudiante)
            .where(EstudianteLogros.id_logromateria == lm.id_logromateria)
        ).first()
        if not existing:
            session.add(EstudianteLogros(
                id_estudiante=est.id_estudiante,
                id_logromateria=lm.id_logromateria,
                status=StatusLogro.obtenido
            ))

    # ── Grupo 1 — Por materia ─────────────────────────────────────────────────
    if total_aprobadas >= 1:
        obtener_logro("Materia aprobada")
        obtener_logro("Primer paso")

    if any(n >= 4.0 for n in notas.values()):
        obtener_logro("Buen desempeño")

    if any(n >= 4.5 for n in notas.values()):
        obtener_logro("Excelencia")

    for em in materias_aprobadas:
        mat = session.get(Materias, em.id_materia)
        if mat and mat.codigo in {"C02A", "C03A"}:
            obtener_logro("El código empieza")
            break

    for em in materias_aprobadas:
        mat = session.get(Materias, em.id_materia)
        if mat:
            cat = session.get(Categorias, mat.id_categoria)
            if cat and cat.codigo == "CBAS":
                obtener_logro("Base científica")
                break

    # ── Grupo 2 — Por categoría ───────────────────────────────────────────────
    def count_cat(code):
        return sum(
            1 for em in materias_aprobadas
            if (m := session.get(Materias, em.id_materia)) and
               (c := session.get(Categorias, m.id_categoria)) and c.codigo == code
        )

    if count_cat("CBAS") >= 11:
        obtener_logro("Científico formado")
    if count_cat("CHUM") >= 7:
        obtener_logro("Humanista digital")
    if count_cat("CHUL") >= 5:
        obtener_logro("Políglota")
    if count_cat("ISCO") >= 31:
        obtener_logro("Ingeniero de sistemas")

    electivas = sum(
        1 for em in materias_aprobadas
        if (m := session.get(Materias, em.id_materia)) and
           m.codigo in {"EC1A", "EC2A", "EC3A", "EC4A"}
    )
    if electivas >= 4:
        obtener_logro("Libre elección")

    # ── Grupo 3 — Por progreso académico ─────────────────────────────────────
    if creditos_aprobados >= 40:
        obtener_logro("Arrancando fuerte")
    if creditos_aprobados >= 81:
        obtener_logro("Mitad del camino")
    if creditos_aprobados >= 121:
        obtener_logro("En la recta final")
    if creditos_aprobados >= 162:
        obtener_logro("Programa completo")
    if total_aprobadas >= 10:
        obtener_logro("Décima superada")
    if total_aprobadas >= 20:
        obtener_logro("Veinte arriba")
    if total_aprobadas >= 30:
        obtener_logro("Treinta y contando")
    if total_aprobadas >= 40:
        obtener_logro("Cuarenta logradas")
    if total_aprobadas >= 55:
        obtener_logro("Graduando")

    # ── Grupo 4 — Rendimiento académico ──────────────────────────────────────
    con_distincion = sum(1 for n in notas.values() if n >= 4.0)
    if con_distincion >= 5:
        obtener_logro("Cinco con distinción")
    if con_distincion >= 10:
        obtener_logro("Diez con distinción")
    if con_distincion >= 20:
        obtener_logro("Veinte con distinción")
    if promedio >= 4.0:
        obtener_logro("Promedio alto")
    if promedio >= 4.5:
        obtener_logro("Matrícula de honor")

    # ── Grupo 5 — Disciplina ──────────────────────────────────────────────────
    if total_aprobadas > 0:
        obtener_logro("Sin tropiezos")
        obtener_logro("Progreso perfecto")

    # ── Grupo 6 — Hitos de la malla ──────────────────────────────────────────
    hitos_check = {
        "Fundamentos sólidos":    "C02A",
        "Estructuras dominadas":  "C05A",
        "Base de datos lista":    "A01A",
        "Arquitecto de software": "A04A",
        "Proyecto iniciado":      "P01A",
        "Proyecto finalizado":    "P02A",
        "Práctica completada":    "P03A",
    }
    for nombre_logro, codigo_mat in hitos_check.items():
        mat_hito = session.exec(
            select(Materias).where(Materias.codigo == codigo_mat)
        ).first()
        if mat_hito and mat_hito.id_materia in aprobadas_ids:
            obtener_logro(nombre_logro)

    session.commit()


def seed():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:

        # ── CATEGORÍAS ────────────────────────────────────────────────────────
        cat_cbas = Categorias(id_categoria=uuid.uuid4(), codigo="CBAS", nombre="Ciencias Básicas")
        cat_chum = Categorias(id_categoria=uuid.uuid4(), codigo="CHUM", nombre="Humanidades")
        cat_chul = Categorias(id_categoria=uuid.uuid4(), codigo="CHUL", nombre="Idiomas")
        cat_isco = Categorias(id_categoria=uuid.uuid4(), codigo="ISCO", nombre="Ingeniería de Sistemas")
        cat_ecou = Categorias(id_categoria=uuid.uuid4(), codigo="ECOU", nombre="Desarrollo Universitario")
        cat_aemp = Categorias(id_categoria=uuid.uuid4(), codigo="AEMP", nombre="Área Empresarial")
        cat_econ = Categorias(id_categoria=uuid.uuid4(), codigo="ECON", nombre="Economía")
        cat_iind = Categorias(id_categoria=uuid.uuid4(), codigo="IIND", nombre="Ingeniería Industrial")
        for cat in [cat_cbas, cat_chum, cat_chul, cat_isco, cat_ecou, cat_aemp, cat_econ, cat_iind]:
            session.add(cat)
        session.commit()

        # ── CARRERA ───────────────────────────────────────────────────────────
        carrera = Carreras(
            id_carrera=uuid.uuid4(),
            nombre="Ingeniería de Sistemas y Computación",
            codigo="ISCO",
            escuela=Escuelas.etd
        )
        session.add(carrera)
        session.commit()

        # ── MATERIAS (malla oficial UTB 201910) ───────────────────────────────
        # NIVEL I
        m_h01a = Materias(id_materia=uuid.uuid4(), nombre="Taller de Comprensión Lectora",    codigo="H01A",  creditos=3, id_categoria=cat_chum.id_categoria)
        m_m01a = Materias(id_materia=uuid.uuid4(), nombre="Cálculo Diferencial",              codigo="M01A",  creditos=4, id_categoria=cat_cbas.id_categoria)
        m_m02a = Materias(id_materia=uuid.uuid4(), nombre="Matemáticas Básicas",              codigo="M02A",  creditos=2, id_categoria=cat_cbas.id_categoria)
        m_q01a = Materias(id_materia=uuid.uuid4(), nombre="Química General",                  codigo="Q01A",  creditos=3, id_categoria=cat_cbas.id_categoria)
        m_u01a = Materias(id_materia=uuid.uuid4(), nombre="Desarrollo Universitario",         codigo="U01A",  creditos=0, id_categoria=cat_ecou.id_categoria)
        m_c01a = Materias(id_materia=uuid.uuid4(), nombre="Sem Ing Sistemas y Computación",   codigo="C01A",  creditos=1, id_categoria=cat_isco.id_categoria)
        m_c02a = Materias(id_materia=uuid.uuid4(), nombre="Fundamentos de Programación",      codigo="C02A",  creditos=3, id_categoria=cat_isco.id_categoria)
        # NIVEL II
        m_le1a = Materias(id_materia=uuid.uuid4(), nombre="Lengua Extranjera I",              codigo="LE1A",  creditos=2, id_categoria=cat_chul.id_categoria)
        m_f01a = Materias(id_materia=uuid.uuid4(), nombre="Física Mecánica",                  codigo="F01A",  creditos=4, id_categoria=cat_cbas.id_categoria)
        m_m03a = Materias(id_materia=uuid.uuid4(), nombre="Cálculo Integral",                 codigo="M03A",  creditos=4, id_categoria=cat_cbas.id_categoria)
        m_m04a = Materias(id_materia=uuid.uuid4(), nombre="Álgebra Lineal",                   codigo="M04A",  creditos=3, id_categoria=cat_cbas.id_categoria)
        m_c03a = Materias(id_materia=uuid.uuid4(), nombre="Programación",                     codigo="C03A",  creditos=3, id_categoria=cat_isco.id_categoria)
        # NIVEL III
        m_le2a = Materias(id_materia=uuid.uuid4(), nombre="Lengua Extranjera II",             codigo="LE2A",  creditos=2, id_categoria=cat_chul.id_categoria)
        m_h02a = Materias(id_materia=uuid.uuid4(), nombre="Taller de Escritura Académica",    codigo="H02A",  creditos=3, id_categoria=cat_chum.id_categoria)
        m_f02a = Materias(id_materia=uuid.uuid4(), nombre="Física Electricidad y Magnetismo", codigo="F02A",  creditos=4, id_categoria=cat_cbas.id_categoria)
        m_m05a = Materias(id_materia=uuid.uuid4(), nombre="Cálculo Vectorial",                codigo="M05A",  creditos=4, id_categoria=cat_cbas.id_categoria)
        m_c04a = Materias(id_materia=uuid.uuid4(), nombre="Programación Orientada a Objetos", codigo="C04A",  creditos=3, id_categoria=cat_isco.id_categoria)
        # NIVEL IV
        m_le3a = Materias(id_materia=uuid.uuid4(), nombre="Lengua Extranjera III",            codigo="LE3A",  creditos=2, id_categoria=cat_chul.id_categoria)
        m_f03a = Materias(id_materia=uuid.uuid4(), nombre="Física Calor y Ondas",             codigo="F03A",  creditos=4, id_categoria=cat_cbas.id_categoria)
        m_m06a = Materias(id_materia=uuid.uuid4(), nombre="Ecuaciones Dif y en Diferencia",   codigo="M06A",  creditos=4, id_categoria=cat_cbas.id_categoria)
        m_c05a = Materias(id_materia=uuid.uuid4(), nombre="Estructura de Datos",              codigo="C05A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_c06a = Materias(id_materia=uuid.uuid4(), nombre="Matemática Discreta",              codigo="C06A",  creditos=3, id_categoria=cat_isco.id_categoria)
        # NIVEL V
        m_le4a = Materias(id_materia=uuid.uuid4(), nombre="Lengua Extranjera IV",             codigo="LE4A",  creditos=2, id_categoria=cat_chul.id_categoria)
        m_h03a = Materias(id_materia=uuid.uuid4(), nombre="Constitución Política",            codigo="H03A",  creditos=2, id_categoria=cat_chum.id_categoria)
        m_e01a = Materias(id_materia=uuid.uuid4(), nombre="Estadística y Probabilidad",       codigo="E01A",  creditos=3, id_categoria=cat_cbas.id_categoria)
        m_a01a = Materias(id_materia=uuid.uuid4(), nombre="Base de Datos",                    codigo="A01A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_a02a = Materias(id_materia=uuid.uuid4(), nombre="Desarrollo de Software",           codigo="A02A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_a03a = Materias(id_materia=uuid.uuid4(), nombre="Algoritmo y Complejidad",          codigo="A03A",  creditos=3, id_categoria=cat_isco.id_categoria)
        # NIVEL VI
        m_le5a = Materias(id_materia=uuid.uuid4(), nombre="Lengua Extranjera V",              codigo="LE5A",  creditos=2, id_categoria=cat_chul.id_categoria)
        m_e02a = Materias(id_materia=uuid.uuid4(), nombre="Estadística Inferencial",          codigo="E02A",  creditos=3, id_categoria=cat_cbas.id_categoria)
        m_g04a = Materias(id_materia=uuid.uuid4(), nombre="Creatividad y Emprendimiento",     codigo="G04A",  creditos=3, id_categoria=cat_aemp.id_categoria)
        m_a04a = Materias(id_materia=uuid.uuid4(), nombre="Arquitectura de Software",         codigo="A04A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_c07a = Materias(id_materia=uuid.uuid4(), nombre="Procesamiento Numérico",           codigo="C07A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_c08a = Materias(id_materia=uuid.uuid4(), nombre="Comunicaciones y Redes",           codigo="C08A",  creditos=3, id_categoria=cat_isco.id_categoria)
        # NIVEL VII
        m_h05a = Materias(id_materia=uuid.uuid4(), nombre="Ciudadanía Global",                codigo="H05A",  creditos=2, id_categoria=cat_chum.id_categoria)
        m_m12a = Materias(id_materia=uuid.uuid4(), nombre="Formul y Evaluación de Proyectos", codigo="M12A",  creditos=3, id_categoria=cat_econ.id_categoria)
        m_a05a = Materias(id_materia=uuid.uuid4(), nombre="Ingeniería de Software",           codigo="A05A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_c09a = Materias(id_materia=uuid.uuid4(), nombre="Arquitectura del Computador",      codigo="C09A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_c10a = Materias(id_materia=uuid.uuid4(), nombre="Sistemas y Modelos",               codigo="C10A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_ec1a = Materias(id_materia=uuid.uuid4(), nombre="Electiva Complementaria I",        codigo="EC1A",  creditos=3, id_categoria=cat_isco.id_categoria)
        # NIVEL VIII
        m_hu1a = Materias(id_materia=uuid.uuid4(), nombre="Electiva de Humanidades I",        codigo="HU1A",  creditos=2, id_categoria=cat_chum.id_categoria)
        m_a06a = Materias(id_materia=uuid.uuid4(), nombre="Inteligencia Artificial",          codigo="A06A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_a07a = Materias(id_materia=uuid.uuid4(), nombre="Infraestructura para TI",          codigo="A07A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_c11a = Materias(id_materia=uuid.uuid4(), nombre="Sistemas Operativos",              codigo="C11A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_ec2a = Materias(id_materia=uuid.uuid4(), nombre="Electiva Complementaria II",       codigo="EC2A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_p01a = Materias(id_materia=uuid.uuid4(), nombre="Proyecto de Ingeniería I",         codigo="P01A",  creditos=3, id_categoria=cat_isco.id_categoria)
        # NIVEL IX
        m_hu2a = Materias(id_materia=uuid.uuid4(), nombre="Electiva de Humanidades II",       codigo="HU2A",  creditos=2, id_categoria=cat_chum.id_categoria)
        m_ee1a = Materias(id_materia=uuid.uuid4(), nombre="Electiva Empresarial",             codigo="EE1A",  creditos=3, id_categoria=cat_iind.id_categoria)
        m_a08a = Materias(id_materia=uuid.uuid4(), nombre="Computación en Paralelo",          codigo="A08A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_c12a = Materias(id_materia=uuid.uuid4(), nombre="Tóp Esp de Ciencias Computación",  codigo="C12A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_ec3a = Materias(id_materia=uuid.uuid4(), nombre="Electiva Complementaria III",      codigo="EC3A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_p02a = Materias(id_materia=uuid.uuid4(), nombre="Proyecto de Ingeniería II",        codigo="P02A",  creditos=3, id_categoria=cat_isco.id_categoria)
        # NIVEL X
        m_h04a = Materias(id_materia=uuid.uuid4(), nombre="Ética",                            codigo="H04A",  creditos=2, id_categoria=cat_chum.id_categoria)
        m_ec4a = Materias(id_materia=uuid.uuid4(), nombre="Electiva Complementaria IV",       codigo="EC4A",  creditos=3, id_categoria=cat_isco.id_categoria)
        m_p03a = Materias(id_materia=uuid.uuid4(), nombre="Práctica Profesional",             codigo="P03A",  creditos=9, id_categoria=cat_isco.id_categoria)

        todas_materias = [
            m_h01a, m_m01a, m_m02a, m_q01a, m_u01a, m_c01a, m_c02a,
            m_le1a, m_f01a, m_m03a, m_m04a, m_c03a,
            m_le2a, m_h02a, m_f02a, m_m05a, m_c04a,
            m_le3a, m_f03a, m_m06a, m_c05a, m_c06a,
            m_le4a, m_h03a, m_e01a, m_a01a, m_a02a, m_a03a,
            m_le5a, m_e02a, m_g04a, m_a04a, m_c07a, m_c08a,
            m_h05a, m_m12a, m_a05a, m_c09a, m_c10a, m_ec1a,
            m_hu1a, m_a06a, m_a07a, m_c11a, m_ec2a, m_p01a,
            m_hu2a, m_ee1a, m_a08a, m_c12a, m_ec3a, m_p02a,
            m_h04a, m_ec4a, m_p03a,
        ]
        for m in todas_materias:
            session.add(m)
        session.commit()

        for m in todas_materias:
            session.add(CarreraMateria(id_carrera=carrera.id_carrera, id_materia=m.id_materia))
        session.commit()

        # ── LOGROS ────────────────────────────────────────────────────────────
        logros_data = [
            ("Materia aprobada",        "Aprobaste tu primera materia"),
            ("Buen desempeño",          "Aprobaste una materia con nota ≥ 4.0"),
            ("Excelencia",              "Aprobaste una materia con nota ≥ 4.5"),
            ("Primer paso",             "Primera materia del programa aprobada"),
            ("El código empieza",       "Aprobaste tu primera materia de programación"),
            ("Base científica",         "Aprobaste tu primera materia de ciencias básicas"),
            ("Científico formado",      "Todas las CBAS completadas (11 materias, 42 créditos)"),
            ("Humanista digital",       "Todas las CHUM completadas (7 materias, 16 créditos)"),
            ("Políglota",               "Todas las CHUL completadas (5 materias, 10 créditos)"),
            ("Ingeniero de sistemas",   "Núcleo ISCO completado (31 materias, 94 créditos)"),
            ("Libre elección",          "Todas las electivas complementarias completadas"),
            ("Arrancando fuerte",       "25% del programa completado (≥ 40 créditos)"),
            ("Mitad del camino",        "50% del programa completado (≥ 81 créditos)"),
            ("En la recta final",       "75% del programa completado (≥ 121 créditos)"),
            ("Programa completo",       "100% del programa completado (162 créditos)"),
            ("Décima superada",         "10 materias aprobadas"),
            ("Veinte arriba",           "20 materias aprobadas"),
            ("Treinta y contando",      "30 materias aprobadas"),
            ("Cuarenta logradas",       "40 materias aprobadas"),
            ("Graduando",               "55 materias aprobadas (programa completo)"),
            ("Cinco con distinción",    "5 materias aprobadas con nota ≥ 4.0"),
            ("Diez con distinción",     "10 materias aprobadas con nota ≥ 4.0"),
            ("Veinte con distinción",   "20 materias aprobadas con nota ≥ 4.0"),
            ("Promedio alto",           "Promedio acumulado ≥ 4.0"),
            ("Matrícula de honor",      "Promedio acumulado ≥ 4.5"),
            ("Sin tropiezos",           "No has reprobado ninguna materia"),
            ("Levantándome",            "Recuperaste una materia que habías reprobado"),
            ("Racha ganadora",          "3 semestres consecutivos sin reprobar"),
            ("Semestre perfecto",       "Aprobaste todas las materias de un semestre"),
            ("Nivel I superado",        "Completaste el primer semestre (16 créditos)"),
            ("Fundamentos sólidos",     "Completaste Fundamentos de Programación"),
            ("Estructuras dominadas",   "Completaste Estructura de Datos"),
            ("Base de datos lista",     "Completaste Base de Datos"),
            ("Arquitecto de software",  "Completaste Arquitectura de Software"),
            ("Proyecto iniciado",       "Completaste Proyecto de Ingeniería I"),
            ("Proyecto finalizado",     "Completaste Proyecto de Ingeniería II"),
            ("Práctica completada",     "Completaste la Práctica Profesional"),
            ("Progreso perfecto",       "Todas las materias cursadas están aprobadas"),
        ]

        logros = []
        for nombre, desc, icon in logros_data:
            l = Logros(id_logro=uuid.uuid4(), nombre_logro=nombre, descripcion=desc)
            session.add(l)
            logros.append(l)
        session.commit()

        logro_map = {l.nombre_logro: l for l in logros}

        hitos = {
            "Fundamentos sólidos":    m_c02a,
            "Estructuras dominadas":  m_c05a,
            "Base de datos lista":    m_a01a,
            "Arquitecto de software": m_a04a,
            "Proyecto iniciado":      m_p01a,
            "Proyecto finalizado":    m_p02a,
            "Práctica completada":    m_p03a,
        }

        logros_materias_list = []
        for l in logros:
            lm = LogroMaterias(
                id_logromateria=uuid.uuid4(),
                id_logro=l.id_logro,
                id_materia=hitos[l.nombre_logro].id_materia if l.nombre_logro in hitos else None
            )
            session.add(lm)
            logros_materias_list.append(lm)
        session.commit()

        logros_materias_map = {lm.id_logro: lm for lm in logros_materias_list}

        # ── ESTUDIANTES SIMULADOS ─────────────────────────────────────────────
        nivel_1 = [m_h01a, m_m01a, m_m02a, m_q01a, m_u01a, m_c01a, m_c02a]
        nivel_2 = [m_le1a, m_f01a, m_m03a, m_m04a, m_c03a]
        nivel_3 = [m_le2a, m_h02a, m_f02a, m_m05a, m_c04a]
        nivel_4 = [m_le3a, m_f03a, m_m06a, m_c05a, m_c06a]
        nivel_5 = [m_le4a, m_h03a, m_e01a, m_a01a, m_a02a, m_a03a]
        nivel_6 = [m_le5a, m_e02a, m_g04a, m_a04a, m_c07a, m_c08a]
        nivel_7 = [m_h05a, m_m12a, m_a05a, m_c09a, m_c10a, m_ec1a]
        nivel_8 = [m_hu1a, m_a06a, m_a07a, m_c11a, m_ec2a, m_p01a]
        nivel_9 = [m_hu2a, m_ee1a, m_a08a, m_c12a, m_ec3a, m_p02a]

        perfiles = {
            "nuevo": {
                "aprobadas": [],
                "en_curso": nivel_1,
                "semestre": "Nivel I",
                "fecha": date(2026, 1, 15),
                "hist": ["PRIMER PERIODO 2026 PREGRADO"],
                "notas": [],
            },
            "intermedio": {
                "aprobadas": nivel_1 + nivel_2,
                "en_curso": nivel_3,
                "semestre": "Nivel III",
                "fecha": date(2024, 1, 15),
                "hist": ["PRIMER PERIODO 2024 PREGRADO", "SEGUNDO PERIODO 2024 PREGRADO"],
                "notas": [3.5, 4.0, 3.8, 3.2, 4.5, 4.2, 3.9, 3.7, 4.1, 3.6, 4.3, 3.5],
            },
            "avanzado": {
                "aprobadas": nivel_1 + nivel_2 + nivel_3 + nivel_4,
                "en_curso": nivel_5,
                "semestre": "Nivel V",
                "fecha": date(2023, 1, 15),
                "hist": ["PRIMER PERIODO 2023 PREGRADO", "SEGUNDO PERIODO 2023 PREGRADO",
                         "PRIMER PERIODO 2024 PREGRADO", "SEGUNDO PERIODO 2024 PREGRADO"],
                "notas": [4.0, 4.2, 3.8, 4.5, 4.1, 3.9, 4.3, 4.0, 3.7, 4.2, 4.4, 3.8,
                          4.1, 3.9, 4.0, 4.3, 3.8],
            },
            "senior": {
                "aprobadas": nivel_1 + nivel_2 + nivel_3 + nivel_4 + nivel_5 + nivel_6,
                "en_curso": nivel_7,
                "semestre": "Nivel VII",
                "fecha": date(2022, 1, 15),
                "hist": ["PRIMER PERIODO 2022 PREGRADO", "SEGUNDO PERIODO 2022 PREGRADO",
                         "PRIMER PERIODO 2023 PREGRADO", "SEGUNDO PERIODO 2023 PREGRADO",
                         "PRIMER PERIODO 2024 PREGRADO", "SEGUNDO PERIODO 2024 PREGRADO"],
                "notas": [4.2, 4.0, 3.9, 4.5, 4.3, 4.1, 3.8, 4.2, 4.0, 4.4, 3.9, 4.1,
                          4.3, 4.0, 3.8, 4.2, 4.5, 4.1, 3.9, 4.0, 4.2, 4.3, 3.8, 4.1,
                          4.0, 4.2, 3.9, 4.3],
            },
            "casi_graduado": {
                "aprobadas": nivel_1 + nivel_2 + nivel_3 + nivel_4 + nivel_5 +
                             nivel_6 + nivel_7 + nivel_8,
                "en_curso": nivel_9,
                "semestre": "Nivel IX",
                "fecha": date(2021, 1, 15),
                "hist": ["PRIMER PERIODO 2021 PREGRADO", "SEGUNDO PERIODO 2021 PREGRADO",
                         "PRIMER PERIODO 2022 PREGRADO", "SEGUNDO PERIODO 2022 PREGRADO",
                         "PRIMER PERIODO 2023 PREGRADO", "SEGUNDO PERIODO 2023 PREGRADO",
                         "PRIMER PERIODO 2024 PREGRADO", "SEGUNDO PERIODO 2024 PREGRADO"],
                "notas": [4.5, 4.3, 4.0, 4.8, 4.2, 4.5, 4.1, 4.3, 4.6, 4.2, 4.4, 4.0,
                          4.3, 4.5, 4.2, 4.6, 4.1, 4.3, 4.5, 4.0, 4.2, 4.4, 4.3, 4.5,
                          4.1, 4.2, 4.5, 4.3, 4.6, 4.2, 4.4, 4.5, 4.1, 4.3, 4.2, 4.5,
                          4.3, 4.6, 4.2, 4.4, 4.5, 4.3, 4.1, 4.5],
            },
        }

        estudiantes_data = [
            ("Ana",     "García",    "T00065001", "anagarcia@utb.edu.co",      "avanzado"),
            ("Carlos",  "Martínez",  "T00065002", "carlosmartinez@utb.edu.co", "intermedio"),
            ("Laura",   "Rodríguez", "T00065003", "laurarodriguez@utb.edu.co", "senior"),
            ("Miguel",  "López",     "T00065004", "miguellopez@utb.edu.co",    "nuevo"),
            ("Valeria", "Torres",    "T00065005", "valeriatorres@utb.edu.co",  "casi_graduado"),
        ]

        for nombre, apellido, codigo, correo, perfil in estudiantes_data:
            p = perfiles[perfil]

            est = Estudiantes(
                id_estudiante=uuid.uuid4(),
                nombre=nombre,
                apellido=apellido,
                codigo=codigo,
                correo=correo,
                status=StatusEstudiante.activo,
                hash_password=hash_password("Password123!")
            )
            session.add(est)
            session.commit()

            session.add(EstudiantesCarreras(
                id_estudiante=est.id_estudiante,
                id_carrera=carrera.id_carrera,
                semestre=p["semestre"],
                fecha_admision=p["fecha"]
            ))

            # Materias aprobadas
            materias_aprobadas_obj = []
            for i, mat in enumerate(p["aprobadas"]):
                nota = p["notas"][i] if i < len(p["notas"]) else 3.5
                sem_idx = min(i // 6, len(p["hist"]) - 1)
                em = EstudianteMateria(
                    id_estudiante=est.id_estudiante,
                    id_materia=mat.id_materia,
                    status=StatusMaterias.aprobada,
                    nota=nota,
                    semestre=p["hist"][sem_idx]
                )
                session.add(em)
                materias_aprobadas_obj.append(em)

            # Materias en curso
            for mat in p["en_curso"]:
                session.add(EstudianteMateria(
                    id_estudiante=est.id_estudiante,
                    id_materia=mat.id_materia,
                    status=StatusMaterias.encurso,
                    nota=0.0,
                    semestre="PRIMER PERIODO 2026 PREGRADO"
                ))

            session.commit()

            # Asignar logros obtenidos
            asignar_logros(session, est, materias_aprobadas_obj, logro_map, logros_materias_map)

        print("Seed completado exitosamente.")
        print("   - 1 carrera | 8 categorías | 55 materias | 38 logros | 5 estudiantes")
        print()
        print("   Logros asignados por perfil:")
        print("   • Miguel  (nuevo)         →  0 logros  | 0 materias aprobadas")
        print("   • Carlos  (intermedio)    → ~8 logros  | 12 materias aprobadas (niveles I-II)")
        print("   • Ana     (avanzado)      → ~14 logros | 17 materias aprobadas (niveles I-IV)")
        print("   • Laura   (senior)        → ~22 logros | 28 materias aprobadas (niveles I-VI)")
        print("   • Valeria (casi_graduado) → ~30 logros | 44 materias aprobadas (niveles I-VIII)")


if __name__ == "__main__":
    seed()