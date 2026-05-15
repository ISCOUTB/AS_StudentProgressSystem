"use client";

import { Award, BookOpen, Percent, GraduationCap } from "lucide-react";

// Subject type categories with colors
const categoryColors: Record<string, string> = {
  humanistico: "bg-yellow-400",
  lenguaExtranjera: "bg-green-500",
  basico: "bg-blue-400",
  cienciasIngenieria: "bg-blue-700",
  electivo: "bg-gray-400",
  integrador: "bg-emerald-600",
};

// Curriculum data organized by level
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
        name: "Ecuaciones Dif y Diferencia",
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
        name: "Fórmul. y Evaluación de Proyecto",
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
        name: "Sistemas Modelos",
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
        name: "Tóp Esp de Ciencias Computació",
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
  { label: "Comp. Humanístico", color: "bg-yellow-400" },
  { label: "Comp. Lengua Extranjera", color: "bg-green-500" },
  { label: "Comp. Básico", color: "bg-blue-400" },
  { label: "Comp. Ciencias de la Ingeniería", color: "bg-blue-700" },
  { label: "Comp. Electivo", color: "bg-gray-400" },
  { label: "Comp. Integrador", color: "bg-emerald-600" },
];

export default function MallaPage() {
  return (
    <div className="flex flex-col gap-4">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold uppercase tracking-wide text-[#1a1a2e]">
          Ver Malla
        </h1>
        <p className="text-sm text-[#1a1a2e]/60">Malla Curricular</p>
      </div>

      {/* Top Section: Program Info + Legend + Stats in a Grid */}
      {/* Program Info */}
      <div className="max-w-5xl rounded-xl border border-[#1a1a2e]/10 bg-white/90 p-4 backdrop-blur-sm">
        <div className="mb-3">
          <span className="text-xs font-medium uppercase text-[#1BB9EB]">
            Programa
          </span>
          <p className="text-sm font-semibold text-[#1a1a2e]">
            Ingeniería de Sistemas y Computación
          </p>
        </div>
        <div className="mb-3">
          <span className="text-xs font-medium uppercase text-[#1BB9EB]">
            Facultad
          </span>
          <p className="text-sm font-semibold text-[#1a1a2e]">Ingeniería</p>
        </div>
        <div className="mb-4">
          <hr />
        </div>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div>
            <span className="text-[10px] font-medium uppercase text-[#1a1a2e]/50">
              Código
            </span>
            <p className="font-mono text-[#1a1a2e]">FR-S.GEN 03-004</p>
          </div>
          <div>
            <span className="text-[10px] font-medium uppercase text-[#1a1a2e]/50">
              Versión
            </span>
            <p className="font-mono text-[#1a1a2e]">01</p>
          </div>
          <div>
            <span className="text-[10px] font-medium uppercase text-[#1a1a2e]/50">
              Fecha
            </span>
            <p className="font-mono text-[#1a1a2e]">13-1-2022</p>
          </div>
          <div>
            <span className="text-[10px] font-medium uppercase text-[#1a1a2e]/50">
              Vigente Desde
            </span>
            <p className="font-mono text-[#1a1a2e]">201910</p>
          </div>
        </div>
      </div>

      {/* Curriculum Grid - Only this part scrolls horizontally */}
      <div className="overflow-x-auto rounded-xl border border-[#1a1a2e]/10 bg-white/90 p-4 backdrop-blur-sm">
        <div className="flex min-w-[1400px] gap-2">
          {curriculumData.map((level, levelIndex) => (
            <div
              key={levelIndex}
              className="flex w-[140px] shrink-0 flex-col gap-2"
            >
              {/* Level Header */}
              <div className="rounded-lg bg-[#1BB9EB] px-2 py-2 text-center">
                <span className="text-xs font-bold text-white">
                  {level.level}
                </span>
              </div>

              {/* Subjects */}
              <div className="flex flex-col gap-1.5">
                {level.subjects.map((subject, subjectIndex) => (
                  <div
                    key={subjectIndex}
                    className={`${categoryColors[subject.type]} aspect-square w-full rounded-lg p-1.5 shadow-sm transition-transform hover:scale-105`}
                    title={`${subject.name}\n${subject.code}\nCréditos: ${subject.credits}`}
                  >
                    <div className="flex h-full flex-col justify-between text-white">
                      <div>
                        <div className="flex items-center justify-between text-[7px] opacity-80">
                          <span>
                            {subject.type === "humanistico"
                              ? "Marso"
                              : subject.type === "basico"
                                ? "Cbas"
                                : subject.type === "lenguaExtranjera"
                                  ? "Curso"
                                  : subject.type === "cienciasIngenieria"
                                    ? "Isco"
                                    : "Mat"}
                          </span>
                          <span>Coo C HT HP</span>
                        </div>
                        <div className="mt-0.5 flex items-center justify-between text-[7px] font-medium">
                          <span className="truncate">
                            {subject.code.split(" ")[1]}
                          </span>
                          <span>
                            {subject.credits} {subject.ht} {subject.hp}
                          </span>
                        </div>
                      </div>
                      <div className="mt-1">
                        <p className="line-clamp-3 text-[8px] font-semibold leading-tight">
                          {subject.name.toUpperCase()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="max-w-5xl rounded-xl border border-[#1a1a2e]/10 bg-white/90 p-4 backdrop-blur-sm">
        <span className="mb-3 block text-xs font-medium uppercase text-[#1a1a2e]/50">
          Leyenda de Componentes
        </span>
        <div className="grid grid-cols-2 gap-2">
          {legend.map((item, index) => (
            <div key={index} className="flex items-center gap-2">
              <div className={`h-4 w-4 shrink-0 rounded ${item.color}`} />
              <span className="text-xs text-[#1a1a2e]/70">{item.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Stats with PGA */}
      <div className="max-w-5xl grid grid-cols-2 gap-3">
        <div className="flex items-center gap-3 rounded-xl border border-[#1a1a2e]/10 bg-white/90 p-3 backdrop-blur-sm">
          <GraduationCap className="h-8 w-8 shrink-0 text-[#1BB9EB]" />
          <div>
            <p className="text-[10px] font-medium uppercase text-[#1BB9EB]">
              PGA
            </p>
            <p className="text-2xl font-bold text-[#1a1a2e]">4.69</p>
          </div>
        </div>
        <div className="flex items-center gap-3 rounded-xl border border-[#1a1a2e]/10 bg-white/90 p-3 backdrop-blur-sm">
          <Award className="h-8 w-8 shrink-0 text-[#1a1a2e]/40" />
          <div>
            <p className="text-[10px] font-medium uppercase text-[#1a1a2e]/50">
              Créditos
            </p>
            <p className="text-2xl font-bold text-[#1a1a2e]">119</p>
          </div>
        </div>
        <div className="flex items-center gap-3 rounded-xl border border-[#1a1a2e]/10 bg-white/90 p-3 backdrop-blur-sm">
          <BookOpen className="h-8 w-8 shrink-0 text-[#1a1a2e]/40" />
          <div>
            <p className="text-[10px] font-medium uppercase text-[#1a1a2e]/50">
              Materias
            </p>
            <p className="text-2xl font-bold text-[#1a1a2e]">
              42<span className="text-sm text-[#1a1a2e]/40">/56</span>
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 rounded-xl border border-[#1a1a2e]/10 bg-white/90 p-3 backdrop-blur-sm">
          <Percent className="h-8 w-8 shrink-0 text-[#1a1a2e]/40" />
          <div>
            <p className="text-[10px] font-medium uppercase text-[#1a1a2e]/50">
              Progreso
            </p>
            <p className="text-2xl font-bold text-[#1a1a2e]">75%</p>
          </div>
        </div>
      </div>
    </div>
  );
}
