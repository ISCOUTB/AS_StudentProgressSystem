"use client"

import { useState } from "react"
import { Award, ArrowRight, ArrowLeft, Settings } from "lucide-react"

const badges = [
  { name: "UTB", logo: "UTB", active: true },
  { name: "UBUNTU", logo: "UBUNTU", active: true },
  { name: "GLOBAL", logo: "GLOBAL", active: true },
  { name: "ISCO", logo: "ISCO", active: true }
]

const achievements = [
  {
    title: "CIENCIAS BÁSICAS",
    subtitle: "COMPLETASTE",
    color: "bg-[#9575CD]",
    icon: Award
  },
  {
    title: "ESCUELA DE IDIOMAS",
    subtitle: "COMPLETASTE",
    color: "bg-[#FFB74D]",
    icon: Award
  },
  {
    title: "CIENCIAS Y HUMANIDADES",
    subtitle: "COMPLETASTE",
    color: "bg-[#4CAF50]",
    icon: Award
  }
]

// All achievements data
const allAchievements = [
  { name: "Materia aprobada", description: "Aprobaste tu primera materia" },
  { name: "Buen desempeño", description: "Aprobaste una materia con nota ≥ 4.0" },
  { name: "Excelencia", description: "Aprobaste una materia con nota ≥ 4.5" },
  { name: "Primer paso", description: "Primera materia del programa aprobada" },
  { name: "El código empieza", description: "Aprobaste tu primera materia de programación" },
  { name: "Base científica", description: "Aprobaste tu primera materia de ciencias básicas" },
  { name: "Científico formado", description: "Todas las CBAS completadas (11 materias, 42 créditos)" },
  { name: "Humanista digital", description: "Todas las CHUM completadas (7 materias, 16 créditos)" },
  { name: "Políglota", description: "Todas las CHUL completadas (5 materias, 10 créditos)" },
  { name: "Ingeniero de sistemas", description: "Núcleo ISCO completado (31 materias, 94 créditos)" },
  { name: "Libre elección", description: "Todas las electivas complementarias completadas" },
  { name: "Arrancando fuerte", description: "25% del programa completado (≥ 40 créditos)" },
  { name: "Mitad del camino", description: "50% del programa completado (≥ 81 créditos)" },
  { name: "En la recta final", description: "75% del programa completado (≥ 121 créditos)" },
  { name: "Programa completo", description: "100% del programa completado (162 créditos)" },
  { name: "Décima superada", description: "10 materias aprobadas" },
  { name: "Veinte arriba", description: "20 materias aprobadas" },
  { name: "Treinta y contando", description: "30 materias aprobadas" },
  { name: "Cuarenta logradas", description: "40 materias aprobadas" },
  { name: "Graduando", description: "55 materias aprobadas (programa completo)" },
  { name: "Cinco con distinción", description: "5 materias aprobadas con nota ≥ 4.0" },
  { name: "Diez con distinción", description: "10 materias aprobadas con nota ≥ 4.0" },
  { name: "Veinte con distinción", description: "20 materias aprobadas con nota ≥ 4.0" },
  { name: "Promedio alto", description: "Promedio acumulado ≥ 4.0" },
  { name: "Matrícula de honor", description: "Promedio acumulado ≥ 4.5" },
  { name: "Sin tropiezos", description: "No has reprobado ninguna materia" },
  { name: "Levantándome", description: "Recuperaste una materia que habías reprobado" },
  { name: "Racha ganadora", description: "3 semestres consecutivos sin reprobar" },
  { name: "Semestre perfecto", description: "Aprobaste todas las materias de un semestre" },
  { name: "Nivel I superado", description: "Completaste el primer semestre (16 créditos)" },
  { name: "Fundamentos sólidos", description: "Completaste Fundamentos de Programación" },
  { name: "Estructuras dominadas", description: "Completaste Estructura de Datos" },
  { name: "Base de datos lista", description: "Completaste Base de Datos" },
  { name: "Arquitecto de software", description: "Completaste Arquitectura de Software" },
  { name: "Proyecto iniciado", description: "Completaste Proyecto de Ingeniería I" },
  { name: "Proyecto finalizado", description: "Completaste Proyecto de Ingeniería II" },
  { name: "Práctica completada", description: "Completaste la Práctica Profesional" },
  { name: "Progreso perfecto", description: "Todas las materias cursadas están aprobadas" },
]

export default function LogrosPage() {
  const [showAllAchievements, setShowAllAchievements] = useState(false)

  if (showAllAchievements) {
    return (
      <div className="flex flex-col gap-6">
        {/* Header with back button */}
        <div className="flex items-center gap-4">
          <button
            onClick={() => setShowAllAchievements(false)}
            className="flex items-center gap-2 rounded-lg border border-[#1a1a2e]/20 bg-white px-4 py-2 font-medium text-[#1a1a2e] transition-all hover:bg-[#1a1a2e] hover:text-white"
          >
            <ArrowLeft className="h-4 w-4" />
            Volver
          </button>
          <h1 className="text-2xl font-bold uppercase tracking-wide text-[#1a1a2e]">
            Todos los Logros
          </h1>
        </div>

        {/* All achievements list */}
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {allAchievements.map((achievement, index) => (
            <div
              key={index}
              className="overflow-hidden rounded-xl border border-[#1a1a2e]/10 bg-white/90 p-4 shadow-sm backdrop-blur-sm transition-all hover:shadow-md"
            >
              <div className="flex items-start gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#C2F542]/20">
                  <Award className="h-5 w-5 text-[#00C853]" />
                </div>
                <div>
                  <h3 className="font-bold text-[#1a1a2e]">{achievement.name}</h3>
                  <p className="mt-1 text-sm text-[#1a1a2e]/60">{achievement.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Personal Info - Shows at top on smaller screens */}
      <div className="w-full xl:hidden">
        <div className="overflow-hidden rounded-2xl border border-[#00C853] bg-white/90 shadow-sm backdrop-blur-sm">
          {/* Header */}
          <div className="border-b border-[#00C853]/20 bg-[#00C853] px-4 py-3">
            <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-white">
              <Settings className="h-4 w-4" />
              <span>Información Personal</span>
            </div>
          </div>
          
          {/* Content */}
          <div className="p-4">
            <h3 className="mb-2 text-lg font-bold uppercase tracking-wide text-[#1a1a2e]">
              Nombre Completo
            </h3>
            <p className="mb-4 text-sm leading-relaxed text-[#1a1a2e]/70">
              Escuela de Transformación Digital. 7mo nivel.
            </p>
            <div className="border-t border-[#1a1a2e]/10 pt-4">
              <h4 className="mb-2 text-sm font-medium text-[#1a1a2e]/60">
                Materias Cursadas
              </h4>
              <div className="flex items-baseline gap-1">
                <span className="text-2xl font-bold text-[#1a1a2e]">42</span>
                <span className="text-lg text-[#1a1a2e]/40">/56</span>
              </div>
              <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-gray-200">
                <div 
                  className="h-full rounded-full bg-[#00C853]"
                  style={{ width: '75%' }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex flex-col-reverse gap-6 xl:flex-row">
        {/* Main Content */}
        <div className="min-w-0 flex-1 space-y-6">
          {/* Badges Row - All highlighted with border */}
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {badges.map((badge, index) => (
              <div
                key={index}
                className="flex flex-col items-center justify-center rounded-xl border-2 border-[#1a1a2e] bg-white p-4 transition-all"
              >
                <div className="mb-2 text-2xl font-black text-[#1a1a2e]">
                  {badge.logo === "UTB" ? (
                    <svg width="40" height="20" viewBox="0 0 874 428" fill="currentColor">
                      <path d="M833.88 213.77C833.179 213.888 833.179 214.901 833.88 215.02C856.599 218.78 874 239.166 874 263.747V395.12C874 413.336 859.744 428 842.179 428H560.536V235.865H743.317V193.568H518.901V428H356.283V193.568H313.311V395.12C313.311 413.283 299.068 428 281.49 428H31.8213C14.2559 428 0 413.322 0 395.12V32.8796C0 14.73 14.2559 0 31.8213 0H135.367V287H178.352V0H842.166C859.744 0 873.987 14.73 873.987 32.8796V165.082C873.987 189.663 856.6 210.008 833.867 213.757" />
                    </svg>
                  ) : badge.logo}
                </div>
                <span className="text-xs font-medium tracking-wide text-[#1a1a2e]">
                  STUDENT
                </span>
              </div>
            ))}
          </div>

          {/* Achievements Grid */}
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {achievements.map((achievement, index) => {
              const Icon = achievement.icon
              return (
                <div
                  key={index}
                  className={`relative overflow-hidden rounded-2xl ${achievement.color} p-6 text-white shadow-lg`}
                >
                  <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider opacity-90">
                    <Icon className="h-4 w-4" />
                    <span>{achievement.subtitle}</span>
                  </div>
                  <h3 className="mt-2 text-xl font-bold uppercase tracking-wide">
                    {achievement.title}
                  </h3>
                </div>
              )
            })}
          </div>
          
          {/* View All Achievements Button */}
          <button
            onClick={() => setShowAllAchievements(true)}
            className="flex w-full items-center justify-between rounded-2xl border-2 border-[#1a1a2e]/20 bg-white/80 p-4 transition-all hover:border-[#1a1a2e]/40 hover:bg-white"
          >
            <div className="flex items-center gap-3 text-[#1a1a2e]/70">
              <Award className="h-5 w-5" />
              <span className="font-medium uppercase tracking-wide">Ver todos los logros</span>
            </div>
            <ArrowRight className="h-5 w-5 text-[#1a1a2e]/70" />
          </button>
        </div>

        {/* Personal Info Sidebar - Hidden on small screens, shown on xl+ */}
        <div className="hidden w-64 shrink-0 xl:block 2xl:w-72">
          <div className="sticky top-8 overflow-hidden rounded-2xl border border-[#00C853] bg-white/90 shadow-sm backdrop-blur-sm">
            {/* Header */}
            <div className="border-b border-[#00C853]/20 bg-[#00C853] px-4 py-3">
              <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-white">
                <Settings className="h-4 w-4" />
                <span>Información Personal</span>
              </div>
            </div>
            
            {/* Content */}
            <div className="p-4 xl:p-6">
              <h3 className="mb-3 text-base font-bold uppercase tracking-wide text-[#1a1a2e] xl:mb-4 xl:text-lg">
                Nombre Completo
              </h3>
              
              <p className="mb-4 text-sm leading-relaxed text-[#1a1a2e]/70 xl:mb-6">
                Escuela de Transformación Digital. 7mo nivel.
              </p>
              
              <div className="border-t border-[#1a1a2e]/10 pt-4 xl:pt-6">
                <h4 className="mb-2 text-sm font-medium text-[#1a1a2e]/60">
                  Materias Cursadas
                </h4>
                <div className="flex items-baseline gap-1">
                  <span className="text-xl font-bold text-[#1a1a2e] xl:text-2xl">42</span>
                  <span className="text-base text-[#1a1a2e]/40 xl:text-lg">/56</span>
                </div>
                <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-gray-200">
                  <div 
                    className="h-full rounded-full bg-[#00C853]"
                    style={{ width: '75%' }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
