"use client";

/**
 * /dashboard/malla —   UTB "Ruta Académica"
 * Solo cambios visuales. Lógica, datos curriculares y hooks sin modificar.
 */

import { Award, BookOpen, Percent, GraduationCap } from "lucide-react";
import { useCurrentUser } from "@/hooks/useCurrentUser";

// ── Category colors ────────────────────────────────────────
const categoryColors: Record<string, string> = {
  humanistico: "#B45309", // amber-700 atenuado
  lenguaExtranjera: "#065F46", // emerald-800
  basico: "#1E40AF", // blue-800
  cienciasIngenieria: "#1E3A8A", // blue-900
  electivo: "#374151", // gray-700
  integrador: "#065F46", // emerald-800
};

const categoryBg: Record<string, string> = {
  humanistico: "rgba(245,158,11,0.75)",
  lenguaExtranjera: "rgba(18,209,145,0.75)",
  basico: "rgba(27,185,235,0.75)",
  cienciasIngenieria: "rgba(9,30,207,0.75)",
  electivo: "rgba(100,116,139,0.75)",
  integrador: "rgba(17,124,74,0.75)",
};

// ── Curriculum data (unchanged) ────────────────────────────
const curriculumData = [
  {
    level: "NIVEL I",
    subjects: [
      {
        code: "CHUM H01A",
        name: "Taller de Comprensión Lectora",
        type: "humanistico",
        credits: 3,
        ht: 0,
        hp: 0,
      },
      {
        code: "CBAS M01A",
        name: "Cálculo Diferencial",
        type: "basico",
        credits: 4,
        ht: 0,
        hp: 18,
      },
      {
        code: "CBAS M02A",
        name: "Matemáticas Básicas",
        type: "basico",
        credits: 2,
        ht: 0,
        hp: 1,
      },
      {
        code: "CBAS C01A",
        name: "Química General",
        type: "basico",
        credits: 3,
        ht: 1,
        hp: 10,
      },
      {
        code: "ECOU U01A",
        name: "Desarrollo Universitario",
        type: "integrador",
        credits: 0,
        ht: 0,
        hp: 0,
      },
      {
        code: "ISCO C01A",
        name: "Sem Ing Sistemas y Computación",
        type: "cienciasIngenieria",
        credits: 1,
        ht: 2,
        hp: 0,
      },
      {
        code: "ISCO C02A",
        name: "Fundamentos de Programación",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 2,
        hp: 1,
      },
    ],
  },
  {
    level: "NIVEL II",
    subjects: [
      {
        code: "CHUL LE1A",
        name: "Lengua Extranjera I",
        type: "lenguaExtranjera",
        credits: 2,
        ht: 0,
        hp: 2,
      },
      {
        code: "CBAS F01A",
        name: "Física Mecánica",
        type: "basico",
        credits: 4,
        ht: 0,
        hp: 18,
      },
      {
        code: "CBAS M03A",
        name: "Cálculo Integral",
        type: "basico",
        credits: 4,
        ht: 0,
        hp: 2,
      },
      {
        code: "CBAS M04A",
        name: "Álgebra Lineal",
        type: "basico",
        credits: 3,
        ht: 1,
        hp: 1,
      },
      {
        code: "ISCO C03A",
        name: "Programación",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 2,
      },
    ],
  },
  {
    level: "NIVEL III",
    subjects: [
      {
        code: "CHUL LE2A",
        name: "Lengua Extranjera II",
        type: "lenguaExtranjera",
        credits: 2,
        ht: 0,
        hp: 3,
      },
      {
        code: "CHUM H02A",
        name: "Taller de Escritura Académica",
        type: "humanistico",
        credits: 3,
        ht: 1,
        hp: 2,
      },
      {
        code: "CBAS F02A",
        name: "Física Electricidad y Magnetis",
        type: "basico",
        credits: 2,
        ht: 0,
        hp: 2,
      },
      {
        code: "CBAS M05A",
        name: "Cálculo Vectorial",
        type: "basico",
        credits: 1,
        ht: 2,
        hp: 2,
      },
      {
        code: "ISCO C04A",
        name: "Programación Orientada a Objet",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 2,
      },
    ],
  },
  {
    level: "NIVEL IV",
    subjects: [
      {
        code: "CHUL LE3A",
        name: "Lengua Extranjera III",
        type: "lenguaExtranjera",
        credits: 2,
        ht: 0,
        hp: 4,
      },
      {
        code: "CBAS F03A",
        name: "Física Calor y Ondas",
        type: "basico",
        credits: 2,
        ht: 0,
        hp: 3,
      },
      {
        code: "CBAS M06A",
        name: "Ecuaciones Dif y Dif.",
        type: "basico",
        credits: 4,
        ht: 0,
        hp: 3,
      },
      {
        code: "ISCU C05A",
        name: "Estructura de Datos",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 3,
        hp: 3,
      },
      {
        code: "ISCO C06A",
        name: "Matemática Discreta",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 2,
      },
      {
        code: "ISCO A03A",
        name: "Algoritmo y Complejidad",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 2,
      },
    ],
  },
  {
    level: "NIVEL V",
    subjects: [
      {
        code: "CHUL LE4A",
        name: "Lengua Extranjera IV",
        type: "lenguaExtranjera",
        credits: 2,
        ht: 0,
        hp: 5,
      },
      {
        code: "CHUM H03A",
        name: "Constitución Política",
        type: "humanistico",
        credits: 2,
        ht: 2,
        hp: 0,
      },
      {
        code: "CBAS E01A",
        name: "Estadística y Probabilidad",
        type: "basico",
        credits: 3,
        ht: 0,
        hp: 3,
      },
      {
        code: "ISCO A01A",
        name: "Base de Datos",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 3,
        hp: 3,
      },
      {
        code: "ISCO A02A",
        name: "Desarrollo de Software",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 2,
      },
      {
        code: "ISCO C08A",
        name: "Comunicaciones y Redes",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 5,
      },
    ],
  },
  {
    level: "NIVEL VI",
    subjects: [
      {
        code: "CHUL LE5A",
        name: "Lengua Extranjera V",
        type: "lenguaExtranjera",
        credits: 2,
        ht: 0,
        hp: 5,
      },
      {
        code: "CBAS E02A",
        name: "Estadística Inferencial",
        type: "basico",
        credits: 3,
        ht: 1,
        hp: 4,
      },
      {
        code: "EMMP G04A",
        name: "Creatividad y Emprendimiento",
        type: "integrador",
        credits: 3,
        ht: 3,
        hp: 3,
      },
      {
        code: "ISCO A04A",
        name: "Arquitectura de Software",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 2,
        hp: 3,
      },
      {
        code: "ISCO C07A",
        name: "Procesamiento Numérico",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 2,
        hp: 4,
      },
      {
        code: "ISCO EC1A",
        name: "Electiva Complementaria I",
        type: "electivo",
        credits: 3,
        ht: 1,
        hp: 2,
      },
    ],
  },
  {
    level: "NIVEL VII",
    subjects: [
      {
        code: "CHUM H05A",
        name: "Ciudadanía Global",
        type: "humanistico",
        credits: 2,
        ht: 2,
        hp: 0,
      },
      {
        code: "ECON M12A",
        name: "Fórmul. y Eval. de Proyectos",
        type: "integrador",
        credits: 3,
        ht: 3,
        hp: 0,
      },
      {
        code: "ISCO A05A",
        name: "Ingeniería de Software",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 9,
      },
      {
        code: "ISCO A06A",
        name: "Arquitectura del Computador",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 2,
      },
      {
        code: "ISCO C09A",
        name: "Sistemas y Modelos",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 5,
      },
      {
        code: "ISCO EC2A",
        name: "Electiva Complementaria II",
        type: "electivo",
        credits: 3,
        ht: 1,
        hp: 2,
      },
    ],
  },
  {
    level: "NIVEL VIII",
    subjects: [
      {
        code: "CHUM H07A",
        name: "Electiva de Humanidades I",
        type: "humanistico",
        credits: 2,
        ht: 2,
        hp: 0,
      },
      {
        code: "ISCO A06A",
        name: "Inteligencia Artificial",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 2,
        hp: 4,
      },
      {
        code: "ISCO A07A",
        name: "Infraestructura para TI",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 6,
      },
      {
        code: "ISCO C11A",
        name: "Sistemas Operativos",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 2,
      },
      {
        code: "ISCO C10A",
        name: "Electiva Complementaria III",
        type: "electivo",
        credits: 3,
        ht: 1,
        hp: 2,
      },
      {
        code: "ISCO P01A",
        name: "Proyecto de Ingeniería I",
        type: "integrador",
        credits: 3,
        ht: 3,
        hp: 0,
      },
    ],
  },
  {
    level: "NIVEL IX",
    subjects: [
      {
        code: "CHUM H08A",
        name: "Electiva de Humanidades II",
        type: "humanistico",
        credits: 2,
        ht: 2,
        hp: 0,
      },
      {
        code: "INDO EE1A",
        name: "Electiva Empresarial",
        type: "electivo",
        credits: 3,
        ht: 3,
        hp: 0,
      },
      {
        code: "ISCO A08A",
        name: "Computación en Paralelo",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 3,
        hp: 6,
      },
      {
        code: "ISCO",
        name: "Tóp Esp Ciencias Computación",
        type: "cienciasIngenieria",
        credits: 3,
        ht: 1,
        hp: 2,
      },
      {
        code: "ISCO P01A",
        name: "Proyecto de Ingeniería II",
        type: "integrador",
        credits: 3,
        ht: 3,
        hp: 0,
      },
    ],
  },
  {
    level: "NIVEL X",
    subjects: [
      {
        code: "CHUM H04A",
        name: "Ética",
        type: "humanistico",
        credits: 2,
        ht: 2,
        hp: 0,
      },
      {
        code: "ISCO EC4A",
        name: "Electiva Complementaria IV",
        type: "electivo",
        credits: 3,
        ht: 1,
        hp: 2,
      },
      {
        code: "ISCO P03A",
        name: "Práctica Profesional",
        type: "integrador",
        credits: 9,
        ht: 0,
        hp: 0,
      },
      {
        code: "ISCO C12A",
        name: "Proyecto de Ingeniería II",
        type: "integrador",
        credits: 3,
        ht: 1,
        hp: 2,
      },
    ],
  },
];

const legend = [
  { label: "Comp. Humanístico", color: "humanistico" },
  { label: "Comp. Lengua Extranjera", color: "lenguaExtranjera" },
  { label: "Comp. Básico", color: "basico" },
  { label: "Comp. Ciencias Ingeniería", color: "cienciasIngenieria" },
  { label: "Comp. Electivo", color: "electivo" },
  { label: "Comp. Integrador", color: "integrador" },
];

// ── Stat skeleton ──────────────────────────────────────────
function StatSkeleton() {
  return (
    <div className="stat-card flex items-center gap-3" style={{ opacity: 0.6 }}>
      <div
        className="stat-accent-strip"
        style={{ background: "var(--surface-3)" }}
      />
      <div
        className="hud-skeleton h-8 w-8 rounded-full flex-shrink-0"
        style={{ height: "32px", width: "32px", borderRadius: "50%" }}
      />
      <div className="space-y-1.5 pl-1">
        <div
          className="hud-skeleton"
          style={{ height: "10px", width: "48px" }}
        />
        <div
          className="hud-skeleton"
          style={{ height: "20px", width: "64px" }}
        />
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────
export default function MallaPage() {
  const { profile, loading } = useCurrentUser();

  const pga = profile?.pga ?? null;
  const creditos = profile?.progress?.creditos_aprobados ?? null;
  const aprobadas = profile?.materiasAprobadas ?? null;
  const total = profile?.totalMaterias ?? null;
  const progreso = profile?.progress?.porcentaje_avance ?? null;

  const pgaLabel = pga !== null && pga > 0 ? pga.toFixed(2) : "—";
  const progresoLabel = progreso !== null ? `${Math.round(progreso)}%` : "—";

  return (
    <div className="flex flex-col gap-5">
      {/* Page heading */}
      <div className="flex items-baseline gap-3">
        <h1
          style={{
            fontFamily: "var(--font-display)",
            fontSize: "1.5rem",
            fontWeight: 900,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--text-primary)",
          }}
        >
          Ruta Académica
        </h1>
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "10px",
            letterSpacing: "0.12em",
            color: "var(--text-muted)",
          }}
        >
          // malla · curricular
        </span>
      </div>

      {/* Program info panel */}
      <div className="hud-panel" style={{ padding: "0", maxWidth: "860px" }}>
        <div
          className="flex items-center gap-2 px-4 py-3"
          style={{ borderBottom: "1px solid var(--surface-3)" }}
        >
          <div
            className="h-4 w-[2px]"
            style={{ background: "var(--utb-cyan)" }}
          />
          <h2
            style={{
              fontFamily: "var(--font-display)",
              fontSize: "0.7rem",
              fontWeight: 700,
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              color: "var(--text-primary)",
            }}
          >
            Información del Programa
          </h2>
        </div>
        <div
          className="grid grid-cols-2 gap-px sm:grid-cols-4"
          style={{ background: "var(--surface-3)" }}
        >
          {[
            { label: "Programa", value: "Ing. de Sistemas y Computación" },
            { label: "Facultad", value: "Ingeniería" },
            { label: "Código", value: "FR-S.GEN 03-004" },
            { label: "Vigente desde", value: "201910" },
          ].map((item) => (
            <div
              key={item.label}
              className="px-4 py-3"
              style={{ background: "var(--surface-1)" }}
            >
              <p
                className="hud-label"
                style={{ color: "var(--utb-cyan)", marginBottom: "3px" }}
              >
                {item.label}
              </p>
              <p
                style={{
                  fontFamily: "var(--font-body)",
                  fontSize: "0.78rem",
                  fontWeight: 600,
                  color: "var(--text-primary)",
                }}
              >
                {item.value}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Curriculum grid */}
      <div className="hud-panel" style={{ padding: "0", overflow: "hidden" }}>
        <div
          className="flex items-center gap-2 px-4 py-3"
          style={{ borderBottom: "1px solid var(--surface-3)" }}
        >
          <div
            className="h-4 w-[2px]"
            style={{ background: "var(--utb-emerald)" }}
          />
          <h2
            style={{
              fontFamily: "var(--font-display)",
              fontSize: "0.7rem",
              fontWeight: 700,
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              color: "var(--text-primary)",
            }}
          >
            Malla Curricular
          </h2>
        </div>
        <div className="overflow-x-auto p-4">
          <div className="flex gap-2" style={{ minWidth: "1400px" }}>
            {curriculumData.map((level, li) => (
              <div
                key={li}
                className="flex flex-col gap-2"
                style={{ width: "138px", flexShrink: 0 }}
              >
                {/* Level header */}
                <div
                  style={{
                    clipPath: "var(--clip-corner-sm)",
                    background: "var(--utb-cyan)",
                    padding: "6px",
                    textAlign: "center",
                  }}
                >
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "9px",
                      fontWeight: 700,
                      letterSpacing: "0.12em",
                      color: "var(--utb-black)",
                      textTransform: "uppercase",
                    }}
                  >
                    {level.level}
                  </span>
                </div>

                {/* Subject tiles */}
                <div className="flex flex-col gap-1.5">
                  {level.subjects.map((s, si) => (
                    <div
                      key={si}
                      title={`${s.name}\n${s.code}\nCréditos: ${s.credits}`}
                      style={{
                        width: "100%",
                        aspectRatio: "1/1",
                        background:
                          categoryBg[s.type] ?? "rgba(100,116,139,0.75)",
                        clipPath: "var(--clip-corner-sm)",
                        padding: "6px",
                        cursor: "default",
                        transition:
                          "transform 0.15s ease, box-shadow 0.15s ease",
                        position: "relative",
                        overflow: "hidden",
                      }}
                      onMouseEnter={(e) => {
                        (e.currentTarget as HTMLElement).style.transform =
                          "scale(1.04)";
                        (e.currentTarget as HTMLElement).style.zIndex = "10";
                      }}
                      onMouseLeave={(e) => {
                        (e.currentTarget as HTMLElement).style.transform =
                          "scale(1)";
                        (e.currentTarget as HTMLElement).style.zIndex = "1";
                      }}
                    >
                      {/* Inner content */}
                      <div
                        style={{
                          height: "100%",
                          display: "flex",
                          flexDirection: "column",
                          justifyContent: "space-between",
                          color: "white",
                        }}
                      >
                        <div>
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              alignItems: "center",
                              fontSize: "6px",
                              opacity: 0.75,
                              letterSpacing: "0.05em",
                              fontFamily: "var(--font-mono)",
                            }}
                          >
                            <span>{s.code.split(" ")[0]}</span>
                            <span>C·HT·HP</span>
                          </div>
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              fontSize: "7px",
                              fontWeight: 700,
                              fontFamily: "var(--font-mono)",
                              marginTop: "2px",
                            }}
                          >
                            <span
                              style={{
                                overflow: "hidden",
                                textOverflow: "ellipsis",
                                whiteSpace: "nowrap",
                                maxWidth: "70%",
                              }}
                            >
                              {s.code.split(" ")[1] ?? s.code}
                            </span>
                            <span>
                              {s.credits}·{s.ht}·{s.hp}
                            </span>
                          </div>
                        </div>
                        <p
                          style={{
                            fontSize: "7.5px",
                            fontWeight: 600,
                            lineHeight: 1.25,
                            fontFamily: "var(--font-display)",
                            letterSpacing: "0.02em",
                            textTransform: "uppercase",
                            display: "-webkit-box",
                            WebkitLineClamp: 3,
                            WebkitBoxOrient: "vertical",
                            overflow: "hidden",
                          }}
                        >
                          {s.name}
                        </p>
                      </div>
                      {/* Corner accent */}
                      <div
                        style={{
                          position: "absolute",
                          bottom: "3px",
                          right: "3px",
                          width: "5px",
                          height: "5px",
                          borderBottom: "1px solid rgba(255,255,255,0.4)",
                          borderRight: "1px solid rgba(255,255,255,0.4)",
                        }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="hud-panel" style={{ padding: "0", maxWidth: "860px" }}>
        <div
          className="flex items-center gap-2 px-4 py-3"
          style={{ borderBottom: "1px solid var(--surface-3)" }}
        >
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "9px",
              letterSpacing: "0.18em",
              textTransform: "uppercase",
              color: "var(--text-muted)",
            }}
          >
            Leyenda de Componentes
          </span>
        </div>
        <div className="grid grid-cols-2 gap-2 p-4 sm:grid-cols-3">
          {legend.map((item) => (
            <div key={item.label} className="flex items-center gap-2">
              <div
                style={{
                  width: "14px",
                  height: "14px",
                  flexShrink: 0,
                  clipPath: "var(--clip-corner-sm)",
                  background: categoryBg[item.color],
                }}
              />
              <span
                style={{
                  fontFamily: "var(--font-body)",
                  fontSize: "0.72rem",
                  color: "var(--text-secondary)",
                }}
              >
                {item.label}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Stat cards */}
      <div
        className="grid grid-cols-2 gap-3 sm:grid-cols-4"
        style={{ maxWidth: "860px" }}
      >
        {loading ? (
          [1, 2, 3, 4].map((i) => <StatSkeleton key={i} />)
        ) : (
          <>
            <div className="stat-card flex items-center gap-3">
              <div
                className="stat-accent-strip"
                style={{ background: "var(--utb-cyan)" }}
              />
              <GraduationCap
                className="h-7 w-7 flex-shrink-0"
                style={{ color: "var(--utb-cyan)" }}
              />
              <div className="pl-1">
                <p className="hud-label" style={{ color: "var(--utb-cyan)" }}>
                  PGA
                </p>
                <p className="hud-value" style={{ fontSize: "1.5rem" }}>
                  {pgaLabel}
                </p>
              </div>
            </div>

            <div className="stat-card flex items-center gap-3">
              <div
                className="stat-accent-strip"
                style={{ background: "var(--utb-savio)" }}
              />
              <Award
                className="h-7 w-7 flex-shrink-0"
                style={{ color: "var(--utb-savio)" }}
              />
              <div className="pl-1">
                <p className="hud-label" style={{ color: "var(--utb-savio)" }}>
                  Créditos
                </p>
                <p className="hud-value" style={{ fontSize: "1.5rem" }}>
                  {creditos !== null ? creditos : "—"}
                </p>
              </div>
            </div>

            <div className="stat-card flex items-center gap-3">
              <div
                className="stat-accent-strip"
                style={{ background: "var(--utb-emerald)" }}
              />
              <BookOpen
                className="h-7 w-7 flex-shrink-0"
                style={{ color: "var(--utb-emerald)" }}
              />
              <div className="pl-1">
                <p
                  className="hud-label"
                  style={{ color: "var(--utb-emerald)" }}
                >
                  Materias
                </p>
                <p className="hud-value" style={{ fontSize: "1.5rem" }}>
                  {aprobadas !== null ? aprobadas : "—"}
                  <span
                    style={{
                      fontSize: "0.9rem",
                      color: "var(--text-muted)",
                      fontWeight: 400,
                    }}
                  >
                    /{total !== null ? total : "—"}
                  </span>
                </p>
              </div>
            </div>

            <div className="stat-card flex items-center gap-3">
              <div
                className="stat-accent-strip"
                style={{ background: "var(--utb-aqua)" }}
              />
              <Percent
                className="h-7 w-7 flex-shrink-0"
                style={{ color: "var(--utb-aqua)" }}
              />
              <div className="pl-1">
                <p className="hud-label" style={{ color: "var(--utb-aqua)" }}>
                  Progreso
                </p>
                <p className="hud-value" style={{ fontSize: "1.5rem" }}>
                  {progresoLabel}
                </p>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
