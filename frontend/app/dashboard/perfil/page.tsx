"use client";

/**
 * /dashboard/perfil — Vista de Perfil Académico
 *
 * Arquitectura:
 *  - ProfileHeader          → nombre, carrera, nivel, avatar hexagonal
 *  - AcademicSummaryBar     → 4 stat-cards horizontales (PGA, créditos, materias, %)
 *  - AchievementsSection    → grid de logros con estado earned/locked + filtros
 *  - TitlesRanksSection     → badges de títulos obtenidos estilo RPG
 *  - NextUnlocksSection     → progreso hacia los 3 logros más cercanos
 *
 * Estado global: todo proviene de useCurrentUser() y useQuestProfile()
 * — sin estado local duplicado, sin prop-drilling.
 *
 * Rendimiento:
 *  - useMemo para derivar listas de logros (earned / locked / near)
 *  - Componentes hoja puros; sin re-renders innecesarios
 */

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  Award,
  Lock,
  ArrowRight,
  Zap,
  Shield,
  Star,
  BookOpen,
  GraduationCap,
  Percent,
  ChevronRight,
  Trophy,
  Flame,
  Target,
} from "lucide-react";
import { useCurrentUser, type ResolvedLogro } from "@/hooks/useCurrentUser";
import { useQuestProfile } from "@/hooks/useQuestProfile";

// ─────────────────────────────────────────────────────────────────────────────
// CONSTANTS
// ─────────────────────────────────────────────────────────────────────────────

/** Mapea nombres de logros a categorías visuales para darles color/rareza */
const LOGRO_RARITY: Record<
  string,
  { tier: "common" | "rare" | "epic" | "legendary"; label: string }
> = {
  "Materia aprobada": { tier: "common", label: "Común" },
  "Primer paso": { tier: "common", label: "Común" },
  "Buen desempeño": { tier: "common", label: "Común" },
  "El código empieza": { tier: "common", label: "Común" },
  "Base científica": { tier: "common", label: "Común" },
  "Fundamentos sólidos": { tier: "common", label: "Común" },
  "Décima superada": { tier: "common", label: "Común" },
  "Arrancando fuerte": { tier: "common", label: "Común" },
  Excelencia: { tier: "rare", label: "Raro" },
  "Cinco con distinción": { tier: "rare", label: "Raro" },
  "Diez con distinción": { tier: "rare", label: "Raro" },
  "Semestre perfecto": { tier: "rare", label: "Raro" },
  "Sin tropiezos": { tier: "rare", label: "Raro" },
  "Estructuras dominadas": { tier: "rare", label: "Raro" },
  "Base de datos lista": { tier: "rare", label: "Raro" },
  "Mitad del camino": { tier: "rare", label: "Raro" },
  "Veinte arriba": { tier: "rare", label: "Raro" },
  "Promedio alto": { tier: "epic", label: "Épico" },
  "Veinte con distinción": { tier: "epic", label: "Épico" },
  "Racha ganadora": { tier: "epic", label: "Épico" },
  Levantándome: { tier: "epic", label: "Épico" },
  "Humanista digital": { tier: "epic", label: "Épico" },
  Políglota: { tier: "epic", label: "Épico" },
  "Científico formado": { tier: "epic", label: "Épico" },
  "Arquitecto de software": { tier: "epic", label: "Épico" },
  "En la recta final": { tier: "epic", label: "Épico" },
  "Treinta y contando": { tier: "epic", label: "Épico" },
  "Matrícula de honor": { tier: "legendary", label: "Legendario" },
  "Ingeniero de sistemas": { tier: "legendary", label: "Legendario" },
  "Programa completo": { tier: "legendary", label: "Legendario" },
  "Progreso perfecto": { tier: "legendary", label: "Legendario" },
  Graduando: { tier: "legendary", label: "Legendario" },
  "Práctica completada": { tier: "legendary", label: "Legendario" },
};

const TIER_STYLES = {
  common: {
    glow: "shadow-slate-200",
    border: "border-slate-200",
    badge: "bg-slate-100 text-slate-600",
    dot: "bg-slate-400",
    ring: "ring-slate-200",
  },
  rare: {
    glow: "shadow-blue-200",
    border: "border-blue-200",
    badge: "bg-blue-50 text-blue-600",
    dot: "bg-blue-400",
    ring: "ring-blue-200",
  },
  epic: {
    glow: "shadow-purple-200",
    border: "border-purple-200",
    badge: "bg-purple-50 text-purple-600",
    dot: "bg-purple-400",
    ring: "ring-purple-200",
  },
  legendary: {
    glow: "shadow-amber-200",
    border: "border-amber-300",
    badge: "bg-amber-50 text-amber-700",
    dot: "bg-amber-400",
    ring: "ring-amber-300",
  },
};

const TITLE_STYLES: Record<string, string> = {
  Aprendiz: "bg-emerald-50 text-emerald-700 border-emerald-200",
  Desarrollador: "bg-blue-50 text-blue-700 border-blue-200",
  "Arquitecto del Código": "bg-purple-50 text-purple-700 border-purple-200",
  "Científico Formado": "bg-sky-50 text-sky-700 border-sky-200",
  "Ingeniero de Sistemas": "bg-indigo-50 text-indigo-700 border-indigo-200",
  "Network Specialist": "bg-cyan-50 text-cyan-700 border-cyan-200",
  "AI Initiate": "bg-violet-50 text-violet-700 border-violet-200",
  "Backend Engineer": "bg-orange-50 text-orange-700 border-orange-200",
};

type FilterTab = "all" | "earned" | "locked" | "rare" | "legendary";

// ─────────────────────────────────────────────────────────────────────────────
// PRIMITIVES
// ─────────────────────────────────────────────────────────────────────────────

function Skeleton({ className }: { className: string }) {
  return (
    <div className={`animate-pulse rounded-lg bg-slate-100 ${className}`} />
  );
}

function GlowBar({
  pct,
  color = "from-[#1BB9EB] to-[#00C853]",
}: {
  pct: number;
  color?: string;
}) {
  return (
    <div className="relative h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
      <div
        className={`absolute inset-y-0 left-0 rounded-full bg-gradient-to-r ${color} transition-all duration-700`}
        style={{ width: `${Math.min(pct, 100)}%` }}
      />
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PROFILE HEADER
// ─────────────────────────────────────────────────────────────────────────────

interface ProfileHeaderProps {
  loading: boolean;
  fullName: string | null;
  escuela: string | null;
  semesterLabel: string | null;
  porcentaje: number;
  codigo: string | null;
  titlesCount: number;
  earnedCount: number;
}

function ProfileHeader({
  loading,
  fullName,
  escuela,
  semesterLabel,
  porcentaje,
  codigo,
  titlesCount,
  earnedCount,
}: ProfileHeaderProps) {
  /* Derive a visual "rank" from progress */
  const rank =
    porcentaje >= 90
      ? { label: "ÉLITE", color: "text-amber-500", icon: "⚡" }
      : porcentaje >= 70
        ? { label: "AVANZADO", color: "text-purple-500", icon: "🔮" }
        : porcentaje >= 40
          ? { label: "INTERMEDIO", color: "text-blue-500", icon: "🛡️" }
          : { label: "NOVATO", color: "text-emerald-600", icon: "🌱" };

  return (
    <div className="relative overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      {/* Decorative top strip */}
      <div className="h-1.5 w-full bg-gradient-to-r from-[#1BB9EB] via-[#C2F542] to-[#00C853]" />

      {/* Subtle grid background */}
      <div
        className="absolute inset-0 opacity-[0.025]"
        style={{
          backgroundImage:
            "linear-gradient(#1a1a2e 1px, transparent 1px), linear-gradient(90deg, #1a1a2e 1px, transparent 1px)",
          backgroundSize: "24px 24px",
        }}
      />

      <div className="relative flex flex-col gap-6 p-6 sm:flex-row sm:items-center sm:gap-8">
        {/* Hexagonal avatar */}
        <div className="flex shrink-0 flex-col items-center gap-2">
          <div className="relative">
            {/* Hex clip using clip-path */}
            <div
              className="flex h-24 w-24 items-center justify-center bg-gradient-to-br from-[#1BB9EB] to-[#00C853] text-4xl font-black text-white"
              style={{
                clipPath:
                  "polygon(50% 0%, 95% 25%, 95% 75%, 50% 100%, 5% 75%, 5% 25%)",
              }}
            >
              {loading ? "?" : (fullName ?? "?").charAt(0).toUpperCase()}
            </div>
            {/* Rank glow ring */}
            <div
              className="absolute -inset-1 -z-10 opacity-40"
              style={{
                clipPath:
                  "polygon(50% 0%, 95% 25%, 95% 75%, 50% 100%, 5% 75%, 5% 25%)",
                background: "linear-gradient(135deg, #1BB9EB, #C2F542)",
              }}
            />
          </div>
          {/* Rank badge */}
          {!loading && (
            <span
              className={`rounded-full border border-current px-2 py-0.5 text-[10px] font-bold tracking-widest ${rank.color}`}
            >
              {rank.icon} {rank.label}
            </span>
          )}
        </div>

        {/* Info block */}
        <div className="flex-1 min-w-0">
          {loading ? (
            <div className="space-y-2">
              <Skeleton className="h-7 w-48" />
              <Skeleton className="h-4 w-64" />
              <Skeleton className="h-3 w-32" />
            </div>
          ) : (
            <>
              <h1 className="truncate text-2xl font-black tracking-tight text-[#1a1a2e]">
                {fullName ?? "—"}
              </h1>
              <p className="mt-0.5 text-sm text-slate-500">{escuela ?? "—"}</p>
              {semesterLabel && (
                <p className="mt-0.5 text-xs font-medium uppercase tracking-wider text-[#1BB9EB]">
                  {semesterLabel}
                </p>
              )}
              {codigo && (
                <p className="mt-1 font-mono text-xs text-slate-400">
                  ID: {codigo}
                </p>
              )}
            </>
          )}

          {/* Overall progress bar */}
          <div className="mt-4">
            <div className="mb-1.5 flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">
                Progreso del programa
              </span>
              {!loading && (
                <span className="text-xs font-bold text-[#1a1a2e]">
                  {Math.round(porcentaje)}%
                </span>
              )}
            </div>
            {loading ? (
              <Skeleton className="h-1.5 w-full" />
            ) : (
              <GlowBar pct={porcentaje} />
            )}
          </div>
        </div>

        {/* Quick stat pills */}
        {!loading && (
          <div className="flex flex-row gap-3 sm:flex-col">
            <div className="flex items-center gap-1.5 rounded-xl border border-slate-100 bg-slate-50 px-3 py-2">
              <Trophy className="h-4 w-4 text-amber-400" />
              <span className="text-sm font-bold text-[#1a1a2e]">
                {earnedCount}
              </span>
              <span className="text-xs text-slate-400">logros</span>
            </div>
            <div className="flex items-center gap-1.5 rounded-xl border border-slate-100 bg-slate-50 px-3 py-2">
              <Shield className="h-4 w-4 text-[#1BB9EB]" />
              <span className="text-sm font-bold text-[#1a1a2e]">
                {titlesCount}
              </span>
              <span className="text-xs text-slate-400">títulos</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// ACADEMIC SUMMARY BAR
// ─────────────────────────────────────────────────────────────────────────────

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  sub?: string;
  accent?: string;
  loading: boolean;
}

function StatCard({
  icon,
  label,
  value,
  sub,
  accent = "#1BB9EB",
  loading,
}: StatCardProps) {
  return (
    <div className="relative flex flex-1 flex-col gap-1 overflow-hidden rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
      {/* accent strip */}
      <div
        className="absolute left-0 top-0 h-full w-1 rounded-l-2xl"
        style={{ background: accent }}
      />
      <div className="pl-2">
        <div
          className="mb-2 flex items-center gap-1.5"
          style={{ color: accent }}
        >
          {icon}
          <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
            {label}
          </span>
        </div>
        {loading ? (
          <Skeleton className="h-8 w-20" />
        ) : (
          <p className="text-3xl font-black leading-none text-[#1a1a2e]">
            {value}
          </p>
        )}
        {!loading && sub && (
          <p className="mt-1 text-xs text-slate-400">{sub}</p>
        )}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// ACHIEVEMENT CARD
// ─────────────────────────────────────────────────────────────────────────────

function AchievementCard({ logro }: { logro: ResolvedLogro }) {
  const rarity = LOGRO_RARITY[logro.nombre] ?? {
    tier: "common",
    label: "Común",
  };
  const styles = TIER_STYLES[rarity.tier];

  if (!logro.earned) {
    return (
      <div
        className={`relative flex items-start gap-3 rounded-xl border ${styles.border} bg-white/60 p-3 opacity-40 grayscale transition-all hover:opacity-60`}
      >
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-slate-100">
          <Lock className="h-4 w-4 text-slate-300" />
        </div>
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold text-slate-400">
            {logro.nombre}
          </p>
          <p className="mt-0.5 line-clamp-1 text-xs text-slate-300">
            {logro.descripcion}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`group relative flex items-start gap-3 overflow-hidden rounded-xl border ${styles.border} bg-white p-3 shadow-sm ${styles.glow} transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md`}
    >
      {/* Glow effect on hover */}
      <div
        className={`absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100`}
        style={{
          background:
            rarity.tier === "legendary"
              ? "radial-gradient(circle at 50% 0%, rgba(251,191,36,0.08) 0%, transparent 70%)"
              : rarity.tier === "epic"
                ? "radial-gradient(circle at 50% 0%, rgba(168,85,247,0.06) 0%, transparent 70%)"
                : "none",
        }}
      />

      {/* Icon */}
      <div
        className={`relative flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ring-2 ${styles.ring}`}
        style={{
          background:
            rarity.tier === "legendary"
              ? "linear-gradient(135deg, #fef3c7, #fde68a)"
              : rarity.tier === "epic"
                ? "linear-gradient(135deg, #f3e8ff, #e9d5ff)"
                : rarity.tier === "rare"
                  ? "linear-gradient(135deg, #eff6ff, #dbeafe)"
                  : "#f8fafc",
        }}
      >
        <Award
          className={`h-4 w-4 ${
            rarity.tier === "legendary"
              ? "text-amber-500"
              : rarity.tier === "epic"
                ? "text-purple-500"
                : rarity.tier === "rare"
                  ? "text-blue-500"
                  : "text-slate-400"
          }`}
        />
        {/* Sparkle for legendary */}
        {rarity.tier === "legendary" && (
          <span className="absolute -right-0.5 -top-0.5 text-[8px]">✨</span>
        )}
      </div>

      {/* Text */}
      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-1">
          <p className="truncate text-sm font-bold text-[#1a1a2e]">
            {logro.nombre}
          </p>
          <span
            className={`ml-1 shrink-0 rounded-full px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-wide ${styles.badge}`}
          >
            {rarity.label}
          </span>
        </div>
        <p className="mt-0.5 line-clamp-2 text-xs text-slate-500">
          {logro.descripcion}
        </p>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// ACHIEVEMENTS SECTION
// ─────────────────────────────────────────────────────────────────────────────

const FILTER_TABS: { id: FilterTab; label: string }[] = [
  { id: "all", label: "Todos" },
  { id: "earned", label: "Obtenidos" },
  { id: "locked", label: "Bloqueados" },
  { id: "rare", label: "Raros+" },
  { id: "legendary", label: "Legendarios" },
];

interface AchievementsSectionProps {
  logros: ResolvedLogro[];
  loading: boolean;
}

function AchievementsSection({ logros, loading }: AchievementsSectionProps) {
  const [filter, setFilter] = useState<FilterTab>("earned");

  const filtered = useMemo(() => {
    switch (filter) {
      case "earned":
        return logros.filter((l) => l.earned);
      case "locked":
        return logros.filter((l) => !l.earned);
      case "rare":
        return logros.filter((l) => {
          const t = LOGRO_RARITY[l.nombre]?.tier;
          return (
            l.earned && (t === "rare" || t === "epic" || t === "legendary")
          );
        });
      case "legendary":
        return logros.filter(
          (l) => l.earned && LOGRO_RARITY[l.nombre]?.tier === "legendary",
        );
      default:
        return logros;
    }
  }, [logros, filter]);

  const earnedCount = useMemo(
    () => logros.filter((l) => l.earned).length,
    [logros],
  );
  const pct =
    logros.length > 0 ? Math.round((earnedCount / logros.length) * 100) : 0;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
      {/* Section header */}
      <div className="flex flex-col gap-3 border-b border-slate-100 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#1BB9EB]/10">
            <Trophy className="h-4 w-4 text-[#1BB9EB]" />
          </div>
          <div>
            <h2 className="text-sm font-bold uppercase tracking-wider text-[#1a1a2e]">
              Logros
            </h2>
            {!loading && (
              <p className="text-xs text-slate-400">
                {earnedCount} / {logros.length} desbloqueados · {pct}%
              </p>
            )}
          </div>
        </div>

        {/* Compact progress */}
        {!loading && (
          <div className="flex w-32 shrink-0 flex-col gap-1">
            <GlowBar pct={pct} color="from-[#1BB9EB] to-[#C2F542]" />
          </div>
        )}
      </div>

      {/* Filter tabs */}
      <div className="flex gap-1 overflow-x-auto px-5 pt-3 pb-1">
        {FILTER_TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setFilter(tab.id)}
            className={`shrink-0 rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
              filter === tab.id
                ? "bg-[#1a1a2e] text-white"
                : "bg-slate-100 text-slate-500 hover:bg-slate-200"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="p-5">
        {loading ? (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <Skeleton key={i} className="h-20" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-2 py-10 text-center">
            <Star className="h-8 w-8 text-slate-200" />
            <p className="text-sm font-medium text-slate-400">
              Ningún logro en esta categoría
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((logro) => (
              <AchievementCard key={logro.id_logro} logro={logro} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// TITLES / RANKS SECTION
// ─────────────────────────────────────────────────────────────────────────────

function TitlesSection({
  titles,
  loading,
}: {
  titles: string[];
  loading: boolean;
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center gap-2 border-b border-slate-100 px-5 py-4">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-50">
          <Shield className="h-4 w-4 text-amber-500" />
        </div>
        <div>
          <h2 className="text-sm font-bold uppercase tracking-wider text-[#1a1a2e]">
            Títulos y Rangos
          </h2>
          {!loading && (
            <p className="text-xs text-slate-400">
              {titles.length}{" "}
              {titles.length === 1 ? "título obtenido" : "títulos obtenidos"}
            </p>
          )}
        </div>
      </div>

      <div className="p-5">
        {loading ? (
          <div className="flex flex-wrap gap-2">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-8 w-32 rounded-full" />
            ))}
          </div>
        ) : titles.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-2 py-6 text-center">
            <Shield className="h-8 w-8 text-slate-200" />
            <p className="text-sm text-slate-400">
              Completa etapas del programa para obtener títulos
            </p>
          </div>
        ) : (
          <div className="flex flex-wrap gap-2">
            {titles.map((title) => {
              const style =
                TITLE_STYLES[title] ??
                "bg-slate-50 text-slate-700 border-slate-200";
              return (
                <span
                  key={title}
                  className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-bold transition-all hover:scale-105 ${style}`}
                >
                  <Shield className="h-3 w-3" />
                  {title}
                </span>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// NEXT UNLOCKS — "qué puedo desbloquear después"
// ─────────────────────────────────────────────────────────────────────────────

/** Very rough progress estimation for locked achievements */
function estimateProgress(
  logro: ResolvedLogro,
  stats: { materiasAprobadas: number; totalMaterias: number; pga: number },
): number {
  const name = logro.nombre;
  const { materiasAprobadas, totalMaterias, pga } = stats;
  if (name === "Décima superada")
    return Math.min((materiasAprobadas / 10) * 100, 99);
  if (name === "Veinte arriba")
    return Math.min((materiasAprobadas / 20) * 100, 99);
  if (name === "Treinta y contando")
    return Math.min((materiasAprobadas / 30) * 100, 99);
  if (name === "Arrancando fuerte")
    return Math.min((materiasAprobadas / 8) * 100, 99);
  if (name === "Mitad del camino")
    return Math.min((materiasAprobadas / totalMaterias / 0.5) * 100, 99);
  if (name === "Promedio alto") return Math.min((pga / 4.0) * 100, 99);
  if (name === "Matrícula de honor") return Math.min((pga / 4.5) * 100, 99);
  if (name === "Cinco con distinción")
    return Math.min((materiasAprobadas / 5) * 100, 99);
  if (name === "Diez con distinción")
    return Math.min((materiasAprobadas / 10) * 100, 99);
  return Math.min((materiasAprobadas / Math.max(totalMaterias, 1)) * 80, 85);
}

interface NextUnlocksSectionProps {
  logros: ResolvedLogro[];
  loading: boolean;
  materiasAprobadas: number;
  totalMaterias: number;
  pga: number;
}

function NextUnlocksSection({
  logros,
  loading,
  materiasAprobadas,
  totalMaterias,
  pga,
}: NextUnlocksSectionProps) {
  const nextUp = useMemo(() => {
    const stats = { materiasAprobadas, totalMaterias, pga };
    return logros
      .filter((l) => !l.earned)
      .map((l) => ({ ...l, est: estimateProgress(l, stats) }))
      .sort((a, b) => b.est - a.est)
      .slice(0, 3);
  }, [logros, materiasAprobadas, totalMaterias, pga]);

  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-100 px-5 py-4">
          <Skeleton className="h-4 w-40" />
        </div>
        <div className="space-y-3 p-5">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-16" />
          ))}
        </div>
      </div>
    );
  }

  if (nextUp.length === 0) return null;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center gap-2 border-b border-slate-100 px-5 py-4">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#C2F542]/20">
          <Target className="h-4 w-4 text-[#1a1a2e]" />
        </div>
        <div>
          <h2 className="text-sm font-bold uppercase tracking-wider text-[#1a1a2e]">
            Próximos Desbloqueos
          </h2>
          <p className="text-xs text-slate-400">
            Los más cerca de desbloquearse
          </p>
        </div>
      </div>

      <div className="space-y-3 p-5">
        {nextUp.map((logro) => {
          const rarity = LOGRO_RARITY[logro.nombre] ?? {
            tier: "common",
            label: "Común",
          };
          const styles = TIER_STYLES[rarity.tier];
          return (
            <div
              key={logro.id_logro}
              className={`rounded-xl border ${styles.border} bg-white p-3`}
            >
              <div className="mb-2 flex items-center justify-between gap-2">
                <div className="flex items-center gap-2 min-w-0">
                  <div
                    className={`h-2 w-2 shrink-0 rounded-full ${styles.dot}`}
                  />
                  <p className="truncate text-sm font-semibold text-[#1a1a2e]">
                    {logro.nombre}
                  </p>
                </div>
                <span className="shrink-0 text-xs font-bold text-slate-500">
                  {Math.round(logro.est)}%
                </span>
              </div>
              <GlowBar
                pct={logro.est}
                color={
                  rarity.tier === "legendary"
                    ? "from-amber-300 to-amber-500"
                    : rarity.tier === "epic"
                      ? "from-purple-300 to-purple-500"
                      : "from-[#1BB9EB] to-[#00C853]"
                }
              />
              <p className="mt-1.5 text-xs text-slate-400">
                {logro.descripcion}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// ACADEMIC PROGRESS MINI-SECTION (with link to "Ruta Académica")
// ─────────────────────────────────────────────────────────────────────────────

function AcademicProgressSection({
  loading,
  pga,
  creditos,
  materiasAprobadas,
  totalMaterias,
  porcentaje,
}: {
  loading: boolean;
  pga: number;
  creditos: number | null;
  materiasAprobadas: number;
  totalMaterias: number;
  porcentaje: number;
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50">
            <GraduationCap className="h-4 w-4 text-emerald-600" />
          </div>
          <h2 className="text-sm font-bold uppercase tracking-wider text-[#1a1a2e]">
            Progreso Académico
          </h2>
        </div>
        <Link
          href="/dashboard/malla"
          className="flex items-center gap-1 rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-500 transition-all hover:border-[#1BB9EB] hover:text-[#1BB9EB]"
        >
          Ver malla completa
          <ChevronRight className="h-3 w-3" />
        </Link>
      </div>

      <div className="grid grid-cols-2 gap-3 p-5 sm:grid-cols-4">
        <StatCard
          icon={<GraduationCap className="h-3.5 w-3.5" />}
          label="PGA"
          value={loading ? "—" : pga > 0 ? pga.toFixed(2) : "—"}
          accent="#1BB9EB"
          loading={loading}
        />
        <StatCard
          icon={<Award className="h-3.5 w-3.5" />}
          label="Créditos"
          value={loading ? "—" : creditos !== null ? String(creditos) : "—"}
          accent="#00C853"
          loading={loading}
        />
        <StatCard
          icon={<BookOpen className="h-3.5 w-3.5" />}
          label="Materias"
          value={loading ? "—" : String(materiasAprobadas)}
          sub={`de ${totalMaterias}`}
          accent="#C2F542"
          loading={loading}
        />
        <StatCard
          icon={<Percent className="h-3.5 w-3.5" />}
          label="Avance"
          value={loading ? "—" : `${Math.round(porcentaje)}%`}
          accent="#f59e0b"
          loading={loading}
        />
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PAGE ROOT
// ─────────────────────────────────────────────────────────────────────────────

export default function PerfilPage() {
  const { profile, loading } = useCurrentUser();
  const { profile: questProfile, loading: questLoading } = useQuestProfile();

  // ── Derived state (memoised to avoid recalculations on every render) ──────
  const fullName = profile?.fullName ?? null;
  const escuela = profile?.carrera?.escuela ?? null;
  const semesterLabel = profile?.semesterLabel ?? null;
  const codigo = profile?.student?.codigo ?? null;
  const pga = profile?.pga ?? 0;
  const creditos = profile?.progress?.creditos_aprobados ?? null;
  const materiasAprobadas = profile?.materiasAprobadas ?? 0;
  const totalMaterias = profile?.totalMaterias ?? 0;
  const porcentaje = profile?.progress?.porcentaje_avance ?? 0;
  const logros = profile?.logros ?? [];
  const earnedLogros = profile?.earnedLogros ?? [];
  const titles = questProfile?.titles ?? [];

  const isLoading = loading || questLoading;

  return (
    <div className="flex flex-col gap-5 pb-8">
      {/* ── Page title ───────────────────────────────────────────────────── */}
      <div className="flex items-baseline gap-3">
        <h1 className="text-2xl font-black uppercase tracking-tight text-[#1a1a2e]">
          Perfil
        </h1>
        <span className="font-mono text-xs text-slate-400">// dashboard</span>
      </div>

      {/* ── Profile Header ───────────────────────────────────────────────── */}
      <ProfileHeader
        loading={isLoading}
        fullName={fullName}
        escuela={escuela}
        semesterLabel={semesterLabel}
        porcentaje={porcentaje}
        codigo={codigo}
        titlesCount={titles.length}
        earnedCount={earnedLogros.length}
      />

      {/* ── Academic progress ────────────────────────────────────────────── */}
      <AcademicProgressSection
        loading={isLoading}
        pga={pga}
        creditos={creditos}
        materiasAprobadas={materiasAprobadas}
        totalMaterias={totalMaterias}
        porcentaje={porcentaje}
      />

      {/* ── Two-column layout: Achievements + sidebar ─────────────────────── */}
      <div className="flex flex-col gap-5 xl:flex-row">
        {/* Left: Achievements (wider) */}
        <div className="min-w-0 flex-1">
          <AchievementsSection logros={logros} loading={isLoading} />
        </div>

        {/* Right: Titles + Next unlocks */}
        <div className="flex w-full flex-col gap-5 xl:w-80 xl:shrink-0">
          <TitlesSection titles={titles} loading={isLoading} />
          <NextUnlocksSection
            logros={logros}
            loading={isLoading}
            materiasAprobadas={materiasAprobadas}
            totalMaterias={totalMaterias}
            pga={pga}
          />
        </div>
      </div>
    </div>
  );
}
