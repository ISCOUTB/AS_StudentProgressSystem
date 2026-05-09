"""
Seed v3 para AS_StudentProgressSystem
Malla: Ingeniería de Sistemas y Computación - UTB (vigente desde 201910)

Arquitectura:
  seed_static() → datos core (categorías, carrera, materias, logros)
                  idempotente, seguro para ejecutar infinitas veces
  seed_demo()   → estudiantes fake + progreso (solo dev/testing)
  seed()        → orquesta ambos según ENABLE_DEMO_SEED
"""
import uuid
import hashlib
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

engine = create_engine(settings.DATABASE_URL, echo=False)

# ── UUIDs FIJOS para datos estáticos ─────────────────────────────────────────
# Generados una sola vez. No cambiar entre ejecuciones.
UUID_CAT = {
    "CBAS": uuid.UUID("10000000-0000-0000-0000-000000000001"),
    "CHUM": uuid.UUID("10000000-0000-0000-0000-000000000002"),
    "CHUL": uuid.UUID("10000000-0000-0000-0000-000000000003"),
    "ISCO": uuid.UUID("10000000-0000-0000-0000-000000000004"),
    "ECOU": uuid.UUID("10000000-0000-0000-0000-000000000005"),
    "AEMP": uuid.UUID("10000000-0000-0000-0000-000000000006"),
    "ECON": uuid.UUID("10000000-0000-0000-0000-000000000007"),
    "IIND": uuid.UUID("10000000-0000-0000-0000-000000000008"),
}

UUID_CARRERA_ISCO = uuid.UUID("20000000-0000-0000-0000-000000000001")

# Materias: el modelo NO tiene campo "codigo", la PK uuid fija ES la clave natural
UUID_MAT = {
    "H01A": uuid.UUID("30000000-0000-0000-0000-000000000001"),
    "M01A": uuid.UUID("30000000-0000-0000-0000-000000000002"),
    "M02A": uuid.UUID("30000000-0000-0000-0000-000000000003"),
    "Q01A": uuid.UUID("30000000-0000-0000-0000-000000000004"),
    "U01A": uuid.UUID("30000000-0000-0000-0000-000000000005"),
    "C01A": uuid.UUID("30000000-0000-0000-0000-000000000006"),
    "C02A": uuid.UUID("30000000-0000-0000-0000-000000000007"),
    "LE1A": uuid.UUID("30000000-0000-0000-0000-000000000008"),
    "F01A": uuid.UUID("30000000-0000-0000-0000-000000000009"),
    "M03A": uuid.UUID("30000000-0000-0000-0000-000000000010"),
    "M04A": uuid.UUID("30000000-0000-0000-0000-000000000011"),
    "C03A": uuid.UUID("30000000-0000-0000-0000-000000000012"),
    "LE2A": uuid.UUID("30000000-0000-0000-0000-000000000013"),
    "H02A": uuid.UUID("30000000-0000-0000-0000-000000000014"),
    "F02A": uuid.UUID("30000000-0000-0000-0000-000000000015"),
    "M05A": uuid.UUID("30000000-0000-0000-0000-000000000016"),
    "C04A": uuid.UUID("30000000-0000-0000-0000-000000000017"),
    "LE3A": uuid.UUID("30000000-0000-0000-0000-000000000018"),
    "F03A": uuid.UUID("30000000-0000-0000-0000-000000000019"),
    "M06A": uuid.UUID("30000000-0000-0000-0000-000000000020"),
    "C05A": uuid.UUID("30000000-0000-0000-0000-000000000021"),
    "C06A": uuid.UUID("30000000-0000-0000-0000-000000000022"),
    "LE4A": uuid.UUID("30000000-0000-0000-0000-000000000023"),
    "H03A": uuid.UUID("30000000-0000-0000-0000-000000000024"),
    "E01A": uuid.UUID("30000000-0000-0000-0000-000000000025"),
    "A01A": uuid.UUID("30000000-0000-0000-0000-000000000026"),
    "A02A": uuid.UUID("30000000-0000-0000-0000-000000000027"),
    "A03A": uuid.UUID("30000000-0000-0000-0000-000000000028"),
    "LE5A": uuid.UUID("30000000-0000-0000-0000-000000000029"),
    "E02A": uuid.UUID("30000000-0000-0000-0000-000000000030"),
    "G04A": uuid.UUID("30000000-0000-0000-0000-000000000031"),
    "A04A": uuid.UUID("30000000-0000-0000-0000-000000000032"),
    "C07A": uuid.UUID("30000000-0000-0000-0000-000000000033"),
    "C08A": uuid.UUID("30000000-0000-0000-0000-000000000034"),
    "H05A": uuid.UUID("30000000-0000-0000-0000-000000000035"),
    "M12A": uuid.UUID("30000000-0000-0000-0000-000000000036"),
    "A05A": uuid.UUID("30000000-0000-0000-0000-000000000037"),
    "C09A": uuid.UUID("30000000-0000-0000-0000-000000000038"),
    "C10A": uuid.UUID("30000000-0000-0000-0000-000000000039"),
    "EC1A": uuid.UUID("30000000-0000-0000-0000-000000000040"),
    "HU1A": uuid.UUID("30000000-0000-0000-0000-000000000041"),
    "A06A": uuid.UUID("30000000-0000-0000-0000-000000000042"),
    "A07A": uuid.UUID("30000000-0000-0000-0000-000000000043"),
    "C11A": uuid.UUID("30000000-0000-0000-0000-000000000044"),
    "EC2A": uuid.UUID("30000000-0000-0000-0000-000000000045"),
    "P01A": uuid.UUID("30000000-0000-0000-0000-000000000046"),
    "HU2A": uuid.UUID("30000000-0000-0000-0000-000000000047"),
    "EE1A": uuid.UUID("30000000-0000-0000-0000-000000000048"),
    "A08A": uuid.UUID("30000000-0000-0000-0000-000000000049"),
    "C12A": uuid.UUID("30000000-0000-0000-0000-000000000050"),
    "EC3A": uuid.UUID("30000000-0000-0000-0000-000000000051"),
    "P02A": uuid.UUID("30000000-0000-0000-0000-000000000052"),
    "H04A": uuid.UUID("30000000-0000-0000-0000-000000000053"),
    "EC4A": uuid.UUID("30000000-0000-0000-0000-000000000054"),
    "P03A": uuid.UUID("30000000-0000-0000-0000-000000000055"),
}

# Logros: campo en modelo es "nombre" (no "nombre_logro")
UUID_LOGRO = {
    "Materia aprobada":       uuid.UUID("40000000-0000-0000-0000-000000000001"),
    "Buen desempeño":         uuid.UUID("40000000-0000-0000-0000-000000000002"),
    "Excelencia":             uuid.UUID("40000000-0000-0000-0000-000000000003"),
    "Primer paso":            uuid.UUID("40000000-0000-0000-0000-000000000004"),
    "El código empieza":      uuid.UUID("40000000-0000-0000-0000-000000000005"),
    "Base científica":        uuid.UUID("40000000-0000-0000-0000-000000000006"),
    "Científico formado":     uuid.UUID("40000000-0000-0000-0000-000000000007"),
    "Humanista digital":      uuid.UUID("40000000-0000-0000-0000-000000000008"),
    "Políglota":              uuid.UUID("40000000-0000-0000-0000-000000000009"),
    "Ingeniero de sistemas":  uuid.UUID("40000000-0000-0000-0000-000000000010"),
    "Libre elección":         uuid.UUID("40000000-0000-0000-0000-000000000011"),
    "Arrancando fuerte":      uuid.UUID("40000000-0000-0000-0000-000000000012"),
    "Mitad del camino":       uuid.UUID("40000000-0000-0000-0000-000000000013"),
    "En la recta final":      uuid.UUID("40000000-0000-0000-0000-000000000014"),
    "Programa completo":      uuid.UUID("40000000-0000-0000-0000-000000000015"),
    "Décima superada":        uuid.UUID("40000000-0000-0000-0000-000000000016"),
    "Veinte arriba":          uuid.UUID("40000000-0000-0000-0000-000000000017"),
    "Treinta y contando":     uuid.UUID("40000000-0000-0000-0000-000000000018"),
    "Cuarenta logradas":      uuid.UUID("40000000-0000-0000-0000-000000000019"),
    "Graduando":              uuid.UUID("40000000-0000-0000-0000-000000000020"),
    "Cinco con distinción":   uuid.UUID("40000000-0000-0000-0000-000000000021"),
    "Diez con distinción":    uuid.UUID("40000000-0000-0000-0000-000000000022"),
    "Veinte con distinción":  uuid.UUID("40000000-0000-0000-0000-000000000023"),
    "Promedio alto":          uuid.UUID("40000000-0000-0000-0000-000000000024"),
    "Matrícula de honor":     uuid.UUID("40000000-0000-0000-0000-000000000025"),
    "Sin tropiezos":          uuid.UUID("40000000-0000-0000-0000-000000000026"),
    "Levantándome":           uuid.UUID("40000000-0000-0000-0000-000000000027"),
    "Racha ganadora":         uuid.UUID("40000000-0000-0000-0000-000000000028"),
    "Semestre perfecto":      uuid.UUID("40000000-0000-0000-0000-000000000029"),
    "Nivel I superado":       uuid.UUID("40000000-0000-0000-0000-000000000030"),
    "Fundamentos sólidos":    uuid.UUID("40000000-0000-0000-0000-000000000031"),
    "Estructuras dominadas":  uuid.UUID("40000000-0000-0000-0000-000000000032"),
    "Base de datos lista":    uuid.UUID("40000000-0000-0000-0000-000000000033"),
    "Arquitecto de software": uuid.UUID("40000000-0000-0000-0000-000000000034"),
    "Proyecto iniciado":      uuid.UUID("40000000-0000-0000-0000-000000000035"),
    "Proyecto finalizado":    uuid.UUID("40000000-0000-0000-0000-000000000036"),
    "Práctica completada":    uuid.UUID("40000000-0000-0000-0000-000000000037"),
    "Progreso perfecto":      uuid.UUID("40000000-0000-0000-0000-000000000038"),
}

UUID_LM = {nombre: uuid.UUID(f"50000000-0000-0000-0000-{str(i+1).zfill(12)}")
           for i, nombre in enumerate(UUID_LOGRO)}

# ── Constantes de hitos y semestres ──────────────────────────────────────────
HITO_FUNDAMENTOS  = "Fundamentos sólidos"
HITO_ESTRUCTURAS  = "Estructuras dominadas"
HITO_BASE_DATOS   = "Base de datos lista"
HITO_ARQUITECTURA = "Arquitecto de software"
HITO_PROYECTO_I   = "Proyecto iniciado"
HITO_PROYECTO_II  = "Proyecto finalizado"
HITO_PRACTICA     = "Práctica completada"

P_2021 = "PRIMER PERIODO 2021 PREGRADO"
S_2021 = "SEGUNDO PERIODO 2021 PREGRADO"
P_2022 = "PRIMER PERIODO 2022 PREGRADO"
S_2022 = "SEGUNDO PERIODO 2022 PREGRADO"
P_2023 = "PRIMER PERIODO 2023 PREGRADO"
S_2023 = "SEGUNDO PERIODO 2023 PREGRADO"
P_2024 = "PRIMER PERIODO 2024 PREGRADO"
S_2024 = "SEGUNDO PERIODO 2024 PREGRADO"
P_2026 = "PRIMER PERIODO 2026 PREGRADO"

# Mapa codigo → uuid para lookup en lógica de logros (no es columna del modelo)
CODIGO_MAT = {codigo: uid for codigo, uid in UUID_MAT.items()}


# ── Helpers ───────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_or_create(session, model, defaults: dict = None, **kwargs):
    """
    Busca por kwargs usando where() compatible con SQLModel/SQLAlchemy.
    Si existe lo retorna. Si no, lo crea con kwargs + defaults y hace flush.
    Idempotente: seguro de llamar múltiples veces.
    """
    stmt = select(model)
    for key, value in kwargs.items():
        stmt = stmt.where(getattr(model, key) == value)
    instance = session.exec(stmt).first()
    if instance:
        return instance
    params = {**kwargs, **(defaults or {})}
    instance = model(**params)
    session.add(instance)
    session.flush()
    return instance


# ── Lógica de logros ──────────────────────────────────────────────────────────

def _calcular_creditos(materias_aprobadas, materias_map):
    """Usa caché en memoria en vez de queries N+1."""
    return sum(
        materias_map[em.id_materia].creditos
        for em in materias_aprobadas
        if em.id_materia in materias_map
    )


def _asignar_logros_por_materia(obtener_logro, materias_aprobadas, notas,
                                 materias_map, categorias_map):
    total = len(materias_aprobadas)
    if total >= 1:
        obtener_logro("Materia aprobada")
        obtener_logro("Primer paso")
    if any(n >= 4.0 for n in notas.values()):
        obtener_logro("Buen desempeño")
    if any(n >= 4.5 for n in notas.values()):
        obtener_logro("Excelencia")

    # "El código empieza": aprobó C02A o C03A
    prog_ids = {CODIGO_MAT["C02A"], CODIGO_MAT["C03A"]}
    if any(em.id_materia in prog_ids for em in materias_aprobadas):
        obtener_logro("El código empieza")

    # "Base científica": aprobó alguna materia de CBAS
    for em in materias_aprobadas:
        mat = materias_map.get(em.id_materia)
        if mat:
            cat = categorias_map.get(mat.id_categoria)
            if cat and cat.codigo == "CBAS":
                obtener_logro("Base científica")
                break


def _asignar_logros_por_categoria(obtener_logro, materias_aprobadas,
                                   materias_map, categorias_map):
    def count_cat(code):
        return sum(
            1 for em in materias_aprobadas
            if (m := materias_map.get(em.id_materia)) and
               (c := categorias_map.get(m.id_categoria)) and c.codigo == code
        )

    if count_cat("CBAS") >= 11:
        obtener_logro("Científico formado")
    if count_cat("CHUM") >= 7:
        obtener_logro("Humanista digital")
    if count_cat("CHUL") >= 5:
        obtener_logro("Políglota")
    if count_cat("ISCO") >= 31:
        obtener_logro("Ingeniero de sistemas")

    electivas_ids = {CODIGO_MAT[c] for c in ["EC1A", "EC2A", "EC3A", "EC4A"]}
    if sum(1 for em in materias_aprobadas if em.id_materia in electivas_ids) >= 4:
        obtener_logro("Libre elección")


def _asignar_logros_por_progreso(obtener_logro, total_aprobadas, creditos_aprobados):
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


def _asignar_logros_por_rendimiento(obtener_logro, notas, promedio):
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


def _asignar_logros_por_hitos(obtener_logro, aprobadas_ids):
    hitos_check = {
        HITO_FUNDAMENTOS:  CODIGO_MAT["C02A"],
        HITO_ESTRUCTURAS:  CODIGO_MAT["C05A"],
        HITO_BASE_DATOS:   CODIGO_MAT["A01A"],
        HITO_ARQUITECTURA: CODIGO_MAT["A04A"],
        HITO_PROYECTO_I:   CODIGO_MAT["P01A"],
        HITO_PROYECTO_II:  CODIGO_MAT["P02A"],
        HITO_PRACTICA:     CODIGO_MAT["P03A"],
    }
    for nombre_logro, mat_uuid in hitos_check.items():
        if mat_uuid in aprobadas_ids:
            obtener_logro(nombre_logro)


def asignar_logros(session, est, materias_aprobadas, logro_map,
                   logros_materias_map, materias_map, categorias_map):
    aprobadas_ids      = {em.id_materia for em in materias_aprobadas}
    notas              = {em.id_materia: em.nota for em in materias_aprobadas}
    total_aprobadas    = len(materias_aprobadas)
    creditos_aprobados = _calcular_creditos(materias_aprobadas, materias_map)
    promedio = (sum(notas.values()) / total_aprobadas) if total_aprobadas > 0 else 0

    # Precargar logros ya asignados — evita queries en el loop
    logros_ya_asignados = {
        row.id_logromateria
        for row in session.exec(
            select(EstudianteLogros).where(
                EstudianteLogros.id_estudiante == est.id_estudiante
            )
        ).all()
    }

    def obtener_logro(nombre):
        logro = logro_map.get(nombre)
        if not logro:
            return
        lm = logros_materias_map.get(logro.id_logro)
        if not lm:
            return
        if lm.id_logromateria not in logros_ya_asignados:
            session.add(EstudianteLogros(
                id_estudiante=est.id_estudiante,
                id_logromateria=lm.id_logromateria,
                status=StatusLogro.obtenido
            ))
            logros_ya_asignados.add(lm.id_logromateria)

    _asignar_logros_por_materia(obtener_logro, materias_aprobadas, notas,
                                 materias_map, categorias_map)
    _asignar_logros_por_categoria(obtener_logro, materias_aprobadas,
                                   materias_map, categorias_map)
    _asignar_logros_por_progreso(obtener_logro, total_aprobadas, creditos_aprobados)
    _asignar_logros_por_rendimiento(obtener_logro, notas, promedio)

    if total_aprobadas > 0:
        obtener_logro("Sin tropiezos")
        obtener_logro("Progreso perfecto")

    _asignar_logros_por_hitos(obtener_logro, aprobadas_ids)


# ── SEED ESTÁTICO ─────────────────────────────────────────────────────────────
# Idempotente. Seguro para correr siempre (restart, rebuild, CI, prod).

def seed_static(session: Session):
    # ── CATEGORÍAS ────────────────────────────────────────────────────────────
    cats_data = [
        ("CBAS", "Ciencias Básicas"),
        ("CHUM", "Humanidades"),
        ("CHUL", "Idiomas"),
        ("ISCO", "Ingeniería de Sistemas"),
        ("ECOU", "Desarrollo Universitario"),
        ("AEMP", "Área Empresarial"),
        ("ECON", "Economía"),
        ("IIND", "Ingeniería Industrial"),
    ]
    cats = {}
    for codigo, nombre in cats_data:
        cat = get_or_create(
            session, Categorias,
            id_categoria=UUID_CAT[codigo],
            defaults={"nombre": nombre, "codigo": codigo},
        )
        cats[codigo] = cat

    # ── CARRERA ───────────────────────────────────────────────────────────────
    carrera = get_or_create(
        session, Carreras,
        id_carrera=UUID_CARRERA_ISCO,
        defaults={
            "nombre": "Ingeniería de Sistemas y Computación",
            "codigo": "ISCO",
            "escuela": Escuelas.etd,
        },
    )

    # ── MATERIAS ──────────────────────────────────────────────────────────────
    # El modelo Materias NO tiene campo "codigo".
    # La búsqueda idempotente se hace por id_materia (UUID fijo).
    # U01A tiene 0 créditos — se almacena como 0 aunque el modelo tenga ge=1,
    # si eso lanza error actualiza la constraint a ge=0 en materia.py.
    materias_data = [
        # (codigo_interno, nombre, creditos, cat_codigo)
        # NIVEL I
        ("H01A", "Taller de Comprensión Lectora",    3, "CHUM"),
        ("M01A", "Cálculo Diferencial",              4, "CBAS"),
        ("M02A", "Matemáticas Básicas",              2, "CBAS"),
        ("Q01A", "Química General",                  3, "CBAS"),
        ("U01A", "Desarrollo Universitario",         0, "ECOU"),
        ("C01A", "Sem Ing Sistemas y Computación",   1, "ISCO"),
        ("C02A", "Fundamentos de Programación",      3, "ISCO"),
        # NIVEL II
        ("LE1A", "Lengua Extranjera I",              2, "CHUL"),
        ("F01A", "Física Mecánica",                  4, "CBAS"),
        ("M03A", "Cálculo Integral",                 4, "CBAS"),
        ("M04A", "Álgebra Lineal",                   3, "CBAS"),
        ("C03A", "Programación",                     3, "ISCO"),
        # NIVEL III
        ("LE2A", "Lengua Extranjera II",             2, "CHUL"),
        ("H02A", "Taller de Escritura Académica",    3, "CHUM"),
        ("F02A", "Física Electricidad y Magnetismo", 4, "CBAS"),
        ("M05A", "Cálculo Vectorial",                4, "CBAS"),
        ("C04A", "Programación Orientada a Objetos", 3, "ISCO"),
        # NIVEL IV
        ("LE3A", "Lengua Extranjera III",            2, "CHUL"),
        ("F03A", "Física Calor y Ondas",             4, "CBAS"),
        ("M06A", "Ecuaciones Dif y en Diferencia",   4, "CBAS"),
        ("C05A", "Estructura de Datos",              3, "ISCO"),
        ("C06A", "Matemática Discreta",              3, "ISCO"),
        # NIVEL V
        ("LE4A", "Lengua Extranjera IV",             2, "CHUL"),
        ("H03A", "Constitución Política",            2, "CHUM"),
        ("E01A", "Estadística y Probabilidad",       3, "CBAS"),
        ("A01A", "Base de Datos",                    3, "ISCO"),
        ("A02A", "Desarrollo de Software",           3, "ISCO"),
        ("A03A", "Algoritmo y Complejidad",          3, "ISCO"),
        # NIVEL VI
        ("LE5A", "Lengua Extranjera V",              2, "CHUL"),
        ("E02A", "Estadística Inferencial",          3, "CBAS"),
        ("G04A", "Creatividad y Emprendimiento",     3, "AEMP"),
        ("A04A", "Arquitectura de Software",         3, "ISCO"),
        ("C07A", "Procesamiento Numérico",           3, "ISCO"),
        ("C08A", "Comunicaciones y Redes",           3, "ISCO"),
        # NIVEL VII
        ("H05A", "Ciudadanía Global",                2, "CHUM"),
        ("M12A", "Formul y Evaluación de Proyectos", 3, "ECON"),
        ("A05A", "Ingeniería de Software",           3, "ISCO"),
        ("C09A", "Arquitectura del Computador",      3, "ISCO"),
        ("C10A", "Sistemas y Modelos",               3, "ISCO"),
        ("EC1A", "Electiva Complementaria I",        3, "ISCO"),
        # NIVEL VIII
        ("HU1A", "Electiva de Humanidades I",        2, "CHUM"),
        ("A06A", "Inteligencia Artificial",          3, "ISCO"),
        ("A07A", "Infraestructura para TI",          3, "ISCO"),
        ("C11A", "Sistemas Operativos",              3, "ISCO"),
        ("EC2A", "Electiva Complementaria II",       3, "ISCO"),
        ("P01A", "Proyecto de Ingeniería I",         3, "ISCO"),
        # NIVEL IX
        ("HU2A", "Electiva de Humanidades II",       2, "CHUM"),
        ("EE1A", "Electiva Empresarial",             3, "IIND"),
        ("A08A", "Computación en Paralelo",          3, "ISCO"),
        ("C12A", "Tóp Esp de Ciencias Computación",  3, "ISCO"),
        ("EC3A", "Electiva Complementaria III",      3, "ISCO"),
        ("P02A", "Proyecto de Ingeniería II",        3, "ISCO"),
        # NIVEL X
        ("H04A", "Ética",                            2, "CHUM"),
        ("EC4A", "Electiva Complementaria IV",       3, "ISCO"),
        ("P03A", "Práctica Profesional",             9, "ISCO"),
    ]

    mats = {}
    for codigo, nombre, creditos, cat_codigo in materias_data:
        # Busca por id_materia (UUID fijo) — único campo identificador disponible en el modelo
        m = get_or_create(
            session, Materias,
            id_materia=UUID_MAT[codigo],
            defaults={
                "nombre": nombre,
                "creditos": creditos,
                "id_categoria": cats[cat_codigo].id_categoria,
            },
        )
        mats[codigo] = m

    # ── CARRERA-MATERIA ───────────────────────────────────────────────────────
    for m in mats.values():
        get_or_create(
            session, CarreraMateria,
            id_carrera=carrera.id_carrera,
            id_materia=m.id_materia,
        )

    # ── LOGROS ────────────────────────────────────────────────────────────────
    # El modelo Logros tiene campo "nombre" (no "nombre_logro") y tiene "icon" opcional.
    logros_data = [
        ("Materia aprobada",       "Aprobaste tu primera materia"),
        ("Buen desempeño",         "Aprobaste una materia con nota ≥ 4.0"),
        ("Excelencia",             "Aprobaste una materia con nota ≥ 4.5"),
        ("Primer paso",            "Primera materia del programa aprobada"),
        ("El código empieza",      "Aprobaste tu primera materia de programación"),
        ("Base científica",        "Aprobaste tu primera materia de ciencias básicas"),
        ("Científico formado",     "Todas las CBAS completadas (11 materias, 42 créditos)"),
        ("Humanista digital",      "Todas las CHUM completadas (7 materias, 16 créditos)"),
        ("Políglota",              "Todas las CHUL completadas (5 materias, 10 créditos)"),
        ("Ingeniero de sistemas",  "Núcleo ISCO completado (31 materias, 94 créditos)"),
        ("Libre elección",         "Todas las electivas complementarias completadas"),
        ("Arrancando fuerte",      "25% del programa completado (≥ 40 créditos)"),
        ("Mitad del camino",       "50% del programa completado (≥ 81 créditos)"),
        ("En la recta final",      "75% del programa completado (≥ 121 créditos)"),
        ("Programa completo",      "100% del programa completado (162 créditos)"),
        ("Décima superada",        "10 materias aprobadas"),
        ("Veinte arriba",          "20 materias aprobadas"),
        ("Treinta y contando",     "30 materias aprobadas"),
        ("Cuarenta logradas",      "40 materias aprobadas"),
        ("Graduando",              "55 materias aprobadas (programa completo)"),
        ("Cinco con distinción",   "5 materias aprobadas con nota ≥ 4.0"),
        ("Diez con distinción",    "10 materias aprobadas con nota ≥ 4.0"),
        ("Veinte con distinción",  "20 materias aprobadas con nota ≥ 4.0"),
        ("Promedio alto",          "Promedio acumulado ≥ 4.0"),
        ("Matrícula de honor",     "Promedio acumulado ≥ 4.5"),
        ("Sin tropiezos",          "No has reprobado ninguna materia"),
        ("Levantándome",           "Recuperaste una materia que habías reprobado"),
        ("Racha ganadora",         "3 semestres consecutivos sin reprobar"),
        ("Semestre perfecto",      "Aprobaste todas las materias de un semestre"),
        ("Nivel I superado",       "Completaste el primer semestre (16 créditos)"),
        ("Fundamentos sólidos",    "Completaste Fundamentos de Programación"),
        ("Estructuras dominadas",  "Completaste Estructura de Datos"),
        ("Base de datos lista",    "Completaste Base de Datos"),
        ("Arquitecto de software", "Completaste Arquitectura de Software"),
        ("Proyecto iniciado",      "Completaste Proyecto de Ingeniería I"),
        ("Proyecto finalizado",    "Completaste Proyecto de Ingeniería II"),
        ("Práctica completada",    "Completaste la Práctica Profesional"),
        ("Progreso perfecto",      "Todas las materias cursadas están aprobadas"),
    ]

    hitos_mat = {
        HITO_FUNDAMENTOS:  mats["C02A"],
        HITO_ESTRUCTURAS:  mats["C05A"],
        HITO_BASE_DATOS:   mats["A01A"],
        HITO_ARQUITECTURA: mats["A04A"],
        HITO_PROYECTO_I:   mats["P01A"],
        HITO_PROYECTO_II:  mats["P02A"],
        HITO_PRACTICA:     mats["P03A"],
    }

    logros = {}
    for nombre, desc in logros_data:
        # Campo en modelo: "nombre" (no "nombre_logro"). "icon" es opcional → default None.
        l = get_or_create(
            session, Logros,
            id_logro=UUID_LOGRO[nombre],
            defaults={"descripcion": desc},
            nombre=nombre,
        )
        logros[nombre] = l

    logros_materias = {}
    for nombre, l in logros.items():
        mat_hito = hitos_mat.get(nombre)
        lm = get_or_create(
            session, LogroMaterias,
            id_logromateria=UUID_LM[nombre],
            defaults={"id_materia": mat_hito.id_materia if mat_hito else None},
            id_logro=l.id_logro,
        )
        logros_materias[l.id_logro] = lm

    # Un único commit atómico para todo el seed estático
    session.commit()

    return carrera, mats, cats, logros, logros_materias


# ── SEED DEMO ─────────────────────────────────────────────────────────────────
# Solo para desarrollo/testing. NO ejecutar en producción.

def seed_demo(session: Session, carrera, mats, cats, logros, logros_materias):
    # Cachés en memoria para evitar N+1 queries
    materias_map   = {m.id_materia: m for m in mats.values()}
    categorias_map = {c.id_categoria: c for c in cats.values()}
    logro_map      = {nombre: l for nombre, l in logros.items()}
    logros_mat_map = logros_materias  # {id_logro: lm}

    nivel_1 = [mats[c] for c in ["H01A","M01A","M02A","Q01A","U01A","C01A","C02A"]]
    nivel_2 = [mats[c] for c in ["LE1A","F01A","M03A","M04A","C03A"]]
    nivel_3 = [mats[c] for c in ["LE2A","H02A","F02A","M05A","C04A"]]
    nivel_4 = [mats[c] for c in ["LE3A","F03A","M06A","C05A","C06A"]]
    nivel_5 = [mats[c] for c in ["LE4A","H03A","E01A","A01A","A02A","A03A"]]
    nivel_6 = [mats[c] for c in ["LE5A","E02A","G04A","A04A","C07A","C08A"]]
    nivel_7 = [mats[c] for c in ["H05A","M12A","A05A","C09A","C10A","EC1A"]]
    nivel_8 = [mats[c] for c in ["HU1A","A06A","A07A","C11A","EC2A","P01A"]]
    nivel_9 = [mats[c] for c in ["HU2A","EE1A","A08A","C12A","EC3A","P02A"]]

    perfiles = {
        "nuevo": {
            "aprobadas": [],
            "en_curso":  nivel_1,
            "semestre":  "Nivel I",
            "fecha":     date(2026, 1, 15),
            "hist":      [P_2026],
            "notas":     [],
        },
        "intermedio": {
            "aprobadas": nivel_1 + nivel_2,
            "en_curso":  nivel_3,
            "semestre":  "Nivel III",
            "fecha":     date(2024, 1, 15),
            "hist":      [P_2024, S_2024],
            "notas":     [3.5, 4.0, 3.8, 3.2, 4.5, 4.2, 3.9, 3.7, 4.1, 3.6, 4.3, 3.5],
        },
        "avanzado": {
            "aprobadas": nivel_1 + nivel_2 + nivel_3 + nivel_4,
            "en_curso":  nivel_5,
            "semestre":  "Nivel V",
            "fecha":     date(2023, 1, 15),
            "hist":      [P_2023, S_2023, P_2024, S_2024],
            "notas":     [4.0, 4.2, 3.8, 4.5, 4.1, 3.9, 4.3, 4.0, 3.7, 4.2, 4.4, 3.8,
                          4.1, 3.9, 4.0, 4.3, 3.8],
        },
        "senior": {
            "aprobadas": nivel_1 + nivel_2 + nivel_3 + nivel_4 + nivel_5 + nivel_6,
            "en_curso":  nivel_7,
            "semestre":  "Nivel VII",
            "fecha":     date(2022, 1, 15),
            "hist":      [P_2022, S_2022, P_2023, S_2023, P_2024, S_2024],
            "notas":     [4.2, 4.0, 3.9, 4.5, 4.3, 4.1, 3.8, 4.2, 4.0, 4.4, 3.9, 4.1,
                          4.3, 4.0, 3.8, 4.2, 4.5, 4.1, 3.9, 4.0, 4.2, 4.3, 3.8, 4.1,
                          4.0, 4.2, 3.9, 4.3],
        },
        "casi_graduado": {
            "aprobadas": nivel_1 + nivel_2 + nivel_3 + nivel_4 + nivel_5 +
                         nivel_6 + nivel_7 + nivel_8,
            "en_curso":  nivel_9,
            "semestre":  "Nivel IX",
            "fecha":     date(2021, 1, 15),
            "hist":      [P_2021, S_2021, P_2022, S_2022, P_2023, S_2023, P_2024, S_2024],
            "notas":     [4.5, 4.3, 4.0, 4.8, 4.2, 4.5, 4.1, 4.3, 4.6, 4.2, 4.4, 4.0,
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
        est = get_or_create(
            session, Estudiantes,
            codigo=codigo,
            defaults={
                "nombre": nombre,
                "apellido": apellido,
                "correo": correo,
                "status": StatusEstudiante.activo,
                "hash_password": hash_password("Password123!"),
            },
        )

        p = perfiles[perfil]

        get_or_create(
            session, EstudiantesCarreras,
            id_estudiante=est.id_estudiante,
            id_carrera=carrera.id_carrera,
            defaults={"semestre": p["semestre"], "fecha_admision": p["fecha"]},
        )

        materias_aprobadas_obj = []
        for i, mat in enumerate(p["aprobadas"]):
            nota    = p["notas"][i] if i < len(p["notas"]) else 3.5
            sem_idx = min(i // 6, len(p["hist"]) - 1)
            em = get_or_create(
                session, EstudianteMateria,
                id_estudiante=est.id_estudiante,
                id_materia=mat.id_materia,
                defaults={
                    "status": StatusMaterias.aprobada,
                    "nota": nota,
                    "semestre": p["hist"][sem_idx],
                },
            )
            materias_aprobadas_obj.append(em)

        for mat in p["en_curso"]:
            get_or_create(
                session, EstudianteMateria,
                id_estudiante=est.id_estudiante,
                id_materia=mat.id_materia,
                defaults={
                    "status": StatusMaterias.encurso,
                    "nota": 0.0,
                    "semestre": P_2026,
                },
            )

        session.flush()

        asignar_logros(
            session, est, materias_aprobadas_obj,
            logro_map, logros_mat_map,
            materias_map, categorias_map,
        )

    session.commit()


# ── ENTRYPOINT ────────────────────────────────────────────────────────────────

def seed():
    """
    Punto de entrada principal.
    Ejecutar manualmente:
        docker compose exec backend python -m app.db.seed
    NO llamar desde on_startup() en producción.
    """
    try:
        with Session(engine) as session:
            print("→ Ejecutando seed estático...")
            carrera, mats, cats, logros, logros_materias = seed_static(session)
            print("  ✓ Categorías, carrera, materias y logros listos.")

            enable_demo = getattr(settings, "ENABLE_DEMO_SEED", False)
            if enable_demo:
                print("→ Ejecutando seed de demo (ENABLE_DEMO_SEED=true)...")
                seed_demo(session, carrera, mats, cats, logros, logros_materias)
                print("  ✓ Estudiantes y progreso demo listos.")
            else:
                print("  (seed demo omitido — activa ENABLE_DEMO_SEED=true para datos fake)")

        print()
        print("Seed completado exitosamente.")
        print("   - 1 carrera | 8 categorías | 55 materias | 38 logros")
        if getattr(settings, "ENABLE_DEMO_SEED", False):
            print("   - 5 estudiantes demo con progreso y logros asignados")
            print()
            print("   Logros asignados por perfil:")
            print("   • Miguel  (nuevo)         →  0 logros  | 0 materias aprobadas")
            print("   • Carlos  (intermedio)    → ~8 logros  | 12 materias aprobadas (niveles I-II)")
            print("   • Ana     (avanzado)      → ~14 logros | 17 materias aprobadas (niveles I-IV)")
            print("   • Laura   (senior)        → ~22 logros | 28 materias aprobadas (niveles I-VI)")
            print("   • Valeria (casi_graduado) → ~30 logros | 44 materias aprobadas (niveles I-VIII)")
    except Exception as e:
        print(f"✗ Error en seed: {e}")
        raise


if __name__ == "__main__":
    seed()