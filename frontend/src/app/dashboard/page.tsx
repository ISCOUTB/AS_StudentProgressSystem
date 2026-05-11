"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Info, User, Grid3X3 } from "lucide-react";
import type { Estudiante, EstudianteCarrera, Progreso, EstudianteLogro } from "@/lib/types";

// Mock data for visual testing
const MOCK_MODE = true;

const MOCK_ESTUDIANTE: Estudiante = {
  id_estudiante: "550e8400-e29b-41d4-a716-446655440000",
  nombre: "Juan Sebastian",
  apellido: "Rodriguez Perez",
  correo: "juserpa@utb.edu.co",
  codigo: "T00067000",
};

const MOCK_CARRERAS: EstudianteCarrera[] = [
  {
    id_estudiante: "550e8400-e29b-41d4-a716-446655440000",
    id_carrera: "carrera-isco-001",
    nombre_carrera: "Ingeniería de Sistemas",
    semestre: "VII Nivel",
    fecha_inscripcion: "2022-01-15",
    estado: "Activo",
  },
  {
    id_estudiante: "550e8400-e29b-41d4-a716-446655440000",
    id_carrera: "carrera-cdat-001",
    nombre_carrera: "Transformación Digital",
    semestre: "V Nivel",
    fecha_inscripcion: "2023-06-01",
    estado: "Activo",
  },
];

const MOCK_PROGRESO: Progreso = {
  id_estudiante: "550e8400-e29b-41d4-a716-446655440000",
  nombre_estudiante: "Juan Sebastian Rodriguez Perez",
  id_carrera: "carrera-isco-001",
  nombre_carrera: "Ingeniería de Sistemas",
  total_materias: 56,
  materias_aprobadas: 42,
  materias_en_curso: 4,
  materias_reprobadas: 0,
  materias_pendientes: 14,
  creditos_totales: 160,
  creditos_aprobados: 119,
  porcentaje_avance: 75,
  materias: [],
};

const MOCK_LOGROS: EstudianteLogro[] = [
  {
    id_estudiante: "550e8400-e29b-41d4-a716-446655440000",
    id_logromateria: "logro-cb-001",
    nombre_logro: "Ciencias Básicas",
    descripcion: "Completaste todas las materias de Ciencias Básicas",
    fecha_obtenido: "2024-06-15",
    completado: true,
  },
  {
    id_estudiante: "550e8400-e29b-41d4-a716-446655440000",
    id_logromateria: "logro-chum-001",
    nombre_logro: "CHUM",
    descripcion: "Completaste las materias de Humanidades",
    fecha_obtenido: "2024-08-20",
    completado: true,
  },
  {
    id_estudiante: "550e8400-e29b-41d4-a716-446655440000",
    id_logromateria: "logro-chul-001",
    nombre_logro: "CHUL",
    descripcion: "Completaste las materias de Lenguas",
    fecha_obtenido: "2025-01-10",
    completado: true,
  },
];

// Badge Component
function Badge({ 
  name, 
  variant = "default",
  size = "normal"
}: { 
  name: string; 
  variant?: "utb" | "ubuntu" | "global" | "isco" | "cdat" | "default";
  size?: "normal" | "small";
}) {
  const variants = {
    utb: "bg-white text-[#0B2131] border-2 border-slate-200",
    ubuntu: "bg-[#8B5CF6] text-white",
    global: "bg-[#3B82F6] text-white",
    isco: "bg-white text-[#0B2131] border-2 border-slate-200",
    cdat: "bg-[#8B5CF6] text-white",
    default: "bg-slate-100 text-slate-700",
  };

  const sizeClasses = size === "small" ? "px-3 py-1.5 text-xs" : "px-4 py-2 text-sm";

  return (
    <div className={`rounded-lg font-bold uppercase tracking-wide ${variants[variant]} ${sizeClasses}`}>
      {name}
      <span className="block text-[10px] font-medium opacity-70 tracking-wider">STUDENT</span>
    </div>
  );
}

// Stat Card Component
function StatCard({ 
  label, 
  value, 
  subValue,
  color = "white",
  size = "normal"
}: { 
  label: string; 
  value: string | number; 
  subValue?: string;
  color?: "white" | "green" | "orange" | "purple" | "blue" | "lime";
  size?: "normal" | "large";
}) {
  const colors = {
    white: "bg-white border-2 border-slate-200",
    green: "bg-[#22C55E] text-white",
    orange: "bg-[#F97316] text-white",
    purple: "bg-[#8B5CF6] text-white",
    blue: "bg-[#3B82F6] text-white",
    lime: "bg-[#84CC16] text-white",
  };

  const textColor = color === "white" ? "text-[#0B2131]" : "text-white";
  const labelColor = color === "white" ? "text-slate-500" : "text-white/80";

  return (
    <div className={`rounded-xl p-4 ${colors[color]} ${size === "large" ? "min-h-[120px]" : ""}`}>
      <p className={`text-xs font-bold uppercase tracking-wider mb-2 ${labelColor}`}>{label}</p>
      <div className="flex items-baseline gap-1">
        <span className={`text-4xl font-bold ${textColor}`}>{value}</span>
        {subValue && <span className={`text-lg font-medium ${labelColor}`}>{subValue}</span>}
      </div>
    </div>
  );
}

// Achievement Card Component
function AchievementCard({ 
  name, 
  completed = false,
  color = "green"
}: { 
  name: string; 
  completed?: boolean;
  color?: "green" | "purple" | "blue" | "lime";
}) {
  const colors = {
    green: "bg-[#22C55E]",
    purple: "bg-[#8B5CF6]",
    blue: "bg-[#3B82F6]",
    lime: "bg-[#84CC16]",
  };

  return (
    <div className={`rounded-xl p-3 ${colors[color]} text-white`}>
      <p className="text-[10px] font-medium uppercase tracking-wider opacity-80">
        {completed ? "COMPLETASTE" : "EN PROGRESO"}
      </p>
      <p className="text-sm font-bold uppercase tracking-wide">{name}</p>
    </div>
  );
}

// Logo Badge Component (D icon for achievements)
function LogoBadge({ variant = "purple" }: { variant?: "purple" | "blue" }) {
  const bg = variant === "purple" ? "bg-[#8B5CF6]" : "bg-[#3B82F6]";
  return (
    <div className={`${bg} rounded-xl p-3 flex items-center justify-center aspect-square`}>
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 6H18C23.5228 6 28 10.4772 28 16C28 21.5228 23.5228 26 18 26H8V6Z" stroke="white" strokeWidth="3" fill="none"/>
        <path d="M8 6V26" stroke="white" strokeWidth="3"/>
      </svg>
    </div>
  );
}

// Progress Bar Component
function ProgressBar({ current, total }: { current: number; total: number }) {
  const percentage = Math.round((current / total) * 100);
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-slate-600">Materias Cursadas</span>
      </div>
      <div className="h-6 bg-slate-200 rounded overflow-hidden relative">
        <div 
          className="h-full bg-[#166534] rounded transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
        <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-white">
          {current}/{total}
        </span>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [estudiante, setEstudiante] = useState<Estudiante | null>(null);
  const [carreras, setCarreras] = useState<EstudianteCarrera[]>([]);
  const [selectedCarrera, setSelectedCarrera] = useState<string | null>(null);
  const [progreso, setProgreso] = useState<Progreso | null>(null);
  const [logros, setLogros] = useState<EstudianteLogro[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Extract username from email (part before @)
  const username = estudiante?.correo?.split("@")[0]?.toUpperCase() || "USUARIO";

  // Calculate PGA (average grade from approved subjects)
  const calcularPGA = useCallback(() => {
    if (!progreso?.materias) return 0;
    const aprobadas = progreso.materias.filter(m => m.estado === "Aprobada" && m.nota);
    if (aprobadas.length === 0) return 0;
    const sum = aprobadas.reduce((acc, m) => acc + (m.nota || 0), 0);
    return (sum / aprobadas.length).toFixed(2);
  }, [progreso]);

  // Load data on mount
  useEffect(() => {
    async function loadData() {
      if (MOCK_MODE) {
        // Use mock data for visual testing
        setEstudiante(MOCK_ESTUDIANTE);
        setCarreras(MOCK_CARRERAS);
        setSelectedCarrera(MOCK_CARRERAS[0].id_carrera);
        setProgreso(MOCK_PROGRESO);
        setLogros(MOCK_LOGROS);
        setLoading(false);
        return;
      }

      // Real API calls (disabled in mock mode)
      try {
        const { decodeToken, isTokenExpired, getEstudianteMe, getEstudianteCarreras, getEstudianteLogros } = await import("@/lib/api");
        
        const token = localStorage.getItem("sps_token");
        if (!token || isTokenExpired(token)) {
          router.push("/");
          return;
        }

        const payload = decodeToken(token);
        if (!payload?.id) {
          throw new Error("Token inválido");
        }

        const estudianteData = await getEstudianteMe();
        setEstudiante(estudianteData);

        const carrerasData = await getEstudianteCarreras(payload.id);
        setCarreras(carrerasData);

        if (carrerasData.length > 0) {
          setSelectedCarrera(carrerasData[0].id_carrera);
        }

        const logrosData = await getEstudianteLogros(payload.id);
        setLogros(logrosData);

      } catch (err) {
        setError(err instanceof Error ? err.message : "Error al cargar datos");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [router]);

  // Load progress when career changes
  useEffect(() => {
    async function loadProgreso() {
      if (MOCK_MODE) return; // Skip in mock mode
      if (!selectedCarrera || !estudiante) return;

      try {
        const { decodeToken, getProgreso } = await import("@/lib/api");
        const token = localStorage.getItem("sps_token");
        const payload = decodeToken(token || "");
        if (!payload?.id) return;

        const progresoData = await getProgreso(payload.id, selectedCarrera);
        setProgreso(progresoData);
      } catch (err) {
        console.error("Error loading progress:", err);
      }
    }

    loadProgreso();
  }, [selectedCarrera, estudiante]);

  // Get career codes for tabs
  const getCarreraCode = (nombre: string) => {
    if (nombre.toLowerCase().includes("sistema")) return "ISCO";
    if (nombre.toLowerCase().includes("digital") || nombre.toLowerCase().includes("transformación")) return "CDAT";
    return nombre.substring(0, 4).toUpperCase();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-[#0ea5e9] border-t-transparent rounded-full animate-spin" />
          <p className="text-slate-600 font-medium">Cargando dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="bg-white rounded-2xl p-8 shadow-lg text-center max-w-md">
          <p className="text-red-500 font-medium mb-4">{error}</p>
          <button 
            onClick={() => router.push("/")}
            className="px-6 py-2 bg-[#0ea5e9] text-white rounded-lg font-medium hover:bg-[#0284c7] transition-colors"
          >
            Volver al inicio
          </button>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="min-h-screen w-full bg-cover bg-center bg-no-repeat"
      style={{ backgroundImage: "url('/dashboard-bg.png')" }}
    >
      <div className="min-h-screen p-6 lg:p-8">
        <div className="max-w-7xl mx-auto">
          {/* Main Grid Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-6">
            
            {/* Left Section */}
            <div className="space-y-6">
              {/* User Header */}
              <div className="flex items-start gap-4">
                <div>
                  <h1 className="text-3xl font-black text-[#0B2131] tracking-tight">{username}</h1>
                  <p className="text-slate-500 text-sm font-mono">ID {estudiante?.codigo || "T000XXXXX"}</p>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {/* PGA */}
                <StatCard 
                  label="PGA" 
                  value={calcularPGA()} 
                  color="white"
                />

                {/* Materias Cursadas */}
                <StatCard 
                  label="MATERIAS CURSADAS" 
                  value={progreso?.materias_aprobadas || 0} 
                  color="green"
                />

                {/* Materias Faltantes */}
                <StatCard 
                  label="MATERIAS FALTANTES" 
                  value={progreso?.materias_pendientes || 0} 
                  color="orange"
                />
              </div>

              {/* Second Row */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {/* Materias Progress */}
                <div className="bg-white rounded-xl p-4 border-2 border-slate-200">
                  <p className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">MATERIAS</p>
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-bold text-[#0B2131]">{progreso?.materias_aprobadas || 0}</span>
                    <span className="text-lg text-slate-400">/{progreso?.total_materias || 0}</span>
                  </div>
                </div>

                {/* Achievements Column */}
                <div className="col-span-1 md:col-span-2 space-y-2">
                  <AchievementCard name="CIENCIAS BÁSICAS" completed={true} color="green" />
                  <div className="grid grid-cols-2 gap-2">
                    <AchievementCard name="CHUM" completed={true} color="lime" />
                    <AchievementCard name="CHUL" completed={true} color="lime" />
                  </div>
                </div>
              </div>

              {/* Third Row - Badges and Credits */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {/* UTB Badge */}
                <div className="bg-white rounded-xl p-4 border-2 border-slate-200 flex items-center justify-center">
                  <div className="text-center">
                    <img 
                      src="/logo-utb.png" 
                      alt="UTB" 
                      className="w-12 h-auto mx-auto mb-1"
                      style={{
                        filter: "brightness(0) saturate(100%) invert(10%) sepia(30%) saturate(1500%) hue-rotate(180deg) brightness(95%) contrast(95%)"
                      }}
                    />
                    <span className="text-[10px] font-bold text-[#0B2131] uppercase tracking-wider">STUDENT</span>
                  </div>
                </div>

                {/* Credits */}
                <div className="bg-[#22C55E] rounded-xl p-4 text-white">
                  <p className="text-[10px] font-bold uppercase tracking-wider opacity-80 mb-1">CRÉDITOS TOTALES</p>
                  <span className="text-4xl font-bold">{progreso?.creditos_aprobados || 0}</span>
                </div>

                {/* Logo Badges */}
                <div className="grid grid-cols-2 gap-2">
                  <LogoBadge variant="purple" />
                  <LogoBadge variant="purple" />
                  <LogoBadge variant="purple" />
                  <LogoBadge variant="purple" />
                </div>

                {/* Progress */}
                <div className="bg-white rounded-xl p-4 border-2 border-slate-200">
                  <p className="text-xs font-bold uppercase tracking-wider text-[#22C55E] mb-2">PROGRESO</p>
                  <div className="flex items-baseline">
                    <span className="text-4xl font-bold text-[#0B2131]">{progreso?.porcentaje_avance || 0}</span>
                    <span className="text-xl text-slate-400">%</span>
                  </div>
                </div>
              </div>

              {/* Fourth Row - More Badges */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <Badge name="UBUNTU" variant="ubuntu" />
                <Badge name="GLOBAL" variant="global" />
                <Badge name="ISCO" variant="isco" />
                <Badge name="CDAT" variant="cdat" />
              </div>
            </div>

            {/* Right Sidebar */}
            <div className="space-y-4">
              {/* Career Tabs */}
              <div className="bg-white rounded-xl p-1 border-2 border-slate-200 flex">
                {carreras.map((carrera) => {
                  const code = getCarreraCode(progreso?.nombre_carrera || carrera.id_carrera);
                  const isSelected = carrera.id_carrera === selectedCarrera;
                  return (
                    <button
                      key={carrera.id_carrera}
                      onClick={() => setSelectedCarrera(carrera.id_carrera)}
                      className={`flex-1 py-2 px-4 rounded-lg text-sm font-bold uppercase tracking-wider transition-colors ${
                        isSelected 
                          ? "bg-[#22C55E] text-white" 
                          : "text-slate-600 hover:bg-slate-100"
                      }`}
                    >
                      {code}
                    </button>
                  );
                })}
                {carreras.length === 1 && (
                  <button
                    className="flex-1 py-2 px-4 rounded-lg text-sm font-bold uppercase tracking-wider bg-[#8B5CF6] text-white"
                  >
                    CDAT
                  </button>
                )}
              </div>

              {/* Action Buttons */}
              <button className="w-full bg-white rounded-xl p-4 border-2 border-slate-200 text-left font-bold text-[#0B2131] uppercase tracking-wide hover:bg-slate-50 transition-colors flex items-center gap-3">
                <User className="w-5 h-5" />
                EDITAR PERFIL
              </button>

              <button 
                onClick={() => router.push("/malla")}
                className="w-full bg-white rounded-xl p-4 border-2 border-slate-200 text-left font-bold text-[#0B2131] uppercase tracking-wide hover:bg-slate-50 transition-colors flex items-center gap-3"
              >
                <Grid3X3 className="w-5 h-5" />
                VER MALLA
              </button>

              {/* Personal Info Card */}
              <div className="bg-white rounded-xl border-2 border-slate-200 overflow-hidden">
                <div className="bg-slate-100 px-4 py-2 flex items-center gap-2 border-b border-slate-200">
                  <Info className="w-4 h-4 text-slate-500" />
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
                    INFORMACIÓN PERSONAL
                  </span>
                </div>
                <div className="p-4 space-y-4">
                  <div>
                    <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Nombre Completo</p>
                    <p className="font-bold text-[#0B2131] text-lg">
                      {estudiante?.nombre} {estudiante?.apellido}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-400 mb-1">
                      Escuela de<br />
                      <span className="font-semibold text-[#0B2131]">Transformación Digital.</span>{" "}
                      <span className="text-slate-600">
                        {carreras.find(c => c.id_carrera === selectedCarrera)?.semestre || "Nivel I"}.
                      </span>
                    </p>
                  </div>
                  <ProgressBar 
                    current={progreso?.materias_aprobadas || 0} 
                    total={progreso?.total_materias || 1} 
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
