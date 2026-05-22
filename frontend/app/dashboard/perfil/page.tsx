"use client";

/**
 * /dashboard/perfil — Marathon × UTB Design System
 * Rediseño visual completo. Lógica, hooks y estado sin cambios.
 */

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  Award,
  Lock,
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
  ArrowUpRight,
} from "lucide-react";
import { useCurrentUser, type ResolvedLogro } from "@/hooks/useCurrentUser";
import { useQuestProfile } from "@/hooks/useQuestProfile";

// ─────────────────────────────────────────────────────────────────────────────
// DESIGN TOKENS (mismo mapa de rareza que antes)
// ─────────────────────────────────────────────────────────────────────────────

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

const TITLE_STYLES: Record<
  string,
  { bg: string; color: string; border: string }
> = {
  Aprendiz: {
    bg: "rgba(18,209,145,0.08)",
    color: "var(--utb-savio)",
    border: "rgba(18,209,145,0.30)",
  },
  Desarrollador: {
    bg: "rgba(27,185,235,0.08)",
    color: "var(--utb-cyan)",
    border: "rgba(27,185,235,0.30)",
  },
  "Arquitecto del Código": {
    bg: "rgba(124,58,237,0.08)",
    color: "#7C3AED",
    border: "rgba(124,58,237,0.30)",
  },
  "Científico Formado": {
    bg: "rgba(0,163,161,0.08)",
    color: "var(--utb-aqua)",
    border: "rgba(0,163,161,0.30)",
  },
  "Ingeniero de Sistemas": {
    bg: "rgba(9,30,207,0.08)",
    color: "var(--utb-blue)",
    border: "rgba(9,30,207,0.30)",
  },
  "Network Specialist": {
    bg: "rgba(27,185,235,0.08)",
    color: "var(--utb-cyan)",
    border: "rgba(27,185,235,0.30)",
  },
  "AI Initiate": {
    bg: "rgba(124,58,237,0.08)",
    color: "#7C3AED",
    border: "rgba(124,58,237,0.30)",
  },
  "Backend Engineer": {
    bg: "rgba(100,237,42,0.08)",
    color: "var(--utb-emerald)",
    border: "rgba(100,237,42,0.30)",
  },
};

type FilterTab = "all" | "earned" | "locked" | "rare" | "legendary";

// ─────────────────────────────────────────────────────────────────────────────
// PRIMITIVES
// ─────────────────────────────────────────────────────────────────────────────

function HudSkeleton({ className = "" }: { className?: string }) {
  return (
    <div className={`hud-skeleton ${className}`} style={{ height: "1rem" }} />
  );
}

function HudProgress({
  pct,
  color = "var(--utb-cyan)",
}: {
  pct: number;
  color?: string;
}) {
  return (
    <div className="hud-progress w-full">
      <div
        className="hud-progress-fill"
        style={{
          width: `${Math.min(pct, 100)}%`,
          background: `linear-gradient(90deg, ${color}, var(--utb-emerald))`,
        }}
      />
    </div>
  );
}

// Número de secuencia técnico estilo HUD
function SeqNumber({ n }: { n: number }) {
  return (
    <span
      className="font-mono absolute"
      style={{
        fontFamily: "var(--font-mono)",
        fontSize: "8px",
        color: "var(--surface-3)",
        top: "6px",
        right: "8px",
        letterSpacing: "0.1em",
      }}
    >
      {String(n).padStart(3, "0")}
    </span>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PROFILE HEADER
// ─────────────────────────────────────────────────────────────────────────────

function ProfileHeader({
  loading,
  fullName,
  escuela,
  semesterLabel,
  porcentaje,
  codigo,
  titlesCount,
  earnedCount,
}: {
  loading: boolean;
  fullName: string | null;
  escuela: string | null;
  semesterLabel: string | null;
  porcentaje: number;
  codigo: string | null;
  titlesCount: number;
  earnedCount: number;
}) {
  const rank =
    porcentaje >= 90
      ? { label: "ÉLITE", color: "var(--utb-emerald)", code: "S-TIER" }
      : porcentaje >= 70
        ? { label: "AVANZADO", color: "var(--utb-cyan)", code: "A-TIER" }
        : porcentaje >= 40
          ? { label: "INTERMEDIO", color: "var(--utb-savio)", code: "B-TIER" }
          : { label: "NOVATO", color: "var(--utb-aqua)", code: "C-TIER" };

  return (
    <div
      className="hud-panel-lg relative overflow-hidden hud-grid-bg"
      style={{ padding: "1.5rem", marginBottom: "0" }}
    >
      {/* Corner brackets */}
      <span className="hud-bracket tl" />
      <span className="hud-bracket tr" />
      <span className="hud-bracket bl" />
      <span className="hud-bracket br" />

      <div className="relative z-10 flex flex-col gap-5 sm:flex-row sm:items-center sm:gap-8">
        {/* Hexagonal avatar + rank */}
        <div className="flex flex-col items-center gap-2 flex-shrink-0">
          <div className="relative">
            <div
              className="hex-avatar"
              style={{ width: "76px", height: "76px", fontSize: "2rem" }}
            >
              {loading ? "?" : (fullName ?? "?").charAt(0).toUpperCase()}
            </div>
            {/* outer glow ring */}
            <div
              className="absolute inset-0 -z-10"
              style={{
                clipPath:
                  "polygon(50% 0%, 93% 25%, 93% 75%, 50% 100%, 7% 75%, 7% 25%)",
                background:
                  "linear-gradient(135deg, var(--utb-cyan), var(--utb-emerald))",
                transform: "scale(1.1)",
                opacity: 0.25,
              }}
            />
          </div>
          {!loading && (
            <span
              className="rank-pill"
              style={{
                color: rank.color,
                borderColor: rank.color,
                fontSize: "8px",
              }}
            >
              {rank.code}
            </span>
          )}
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          {loading ? (
            <div className="space-y-2">
              <HudSkeleton className="h-6 w-48" />
              <HudSkeleton className="h-3 w-64" />
              <HudSkeleton className="h-2 w-32" />
            </div>
          ) : (
            <>
              <div className="flex items-center gap-2 flex-wrap">
                <h1
                  className="truncate"
                  style={{
                    fontFamily: "var(--font-display)",
                    fontSize: "1.5rem",
                    fontWeight: 800,
                    letterSpacing: "0.04em",
                    textTransform: "uppercase",
                    color: "var(--text-primary)",
                  }}
                >
                  {fullName ?? "—"}
                </h1>
                <span
                  className="rank-pill"
                  style={{
                    color: rank.color,
                    borderColor: rank.color,
                    fontSize: "9px",
                  }}
                >
                  {rank.label}
                </span>
              </div>
              <p
                style={{
                  fontFamily: "var(--font-body)",
                  fontSize: "0.8rem",
                  color: "var(--text-muted)",
                  marginTop: "2px",
                }}
              >
                {escuela ?? "—"}
              </p>
              {semesterLabel && (
                <p
                  className="hud-label mt-1"
                  style={{ color: "var(--utb-cyan)" }}
                >
                  {semesterLabel}
                </p>
              )}
              {codigo && (
                <p
                  className="hud-label mt-0.5"
                  style={{
                    fontFamily: "var(--font-mono)",
                    color: "var(--surface-4)",
                  }}
                >
                  ID · {codigo}
                </p>
              )}
            </>
          )}

          {/* Progress bar */}
          <div className="mt-4 space-y-1.5">
            <div className="flex items-center justify-between">
              <span
                className="hud-label"
                style={{ color: "var(--text-muted)" }}
              >
                Progreso del programa
              </span>
              {!loading && (
                <span
                  style={{
                    fontFamily: "var(--font-display)",
                    fontSize: "0.9rem",
                    fontWeight: 700,
                    color: "var(--utb-cyan)",
                  }}
                >
                  {Math.round(porcentaje)}%
                </span>
              )}
            </div>
            {loading ? (
              <HudSkeleton className="h-1" />
            ) : (
              <HudProgress pct={porcentaje} />
            )}
          </div>
        </div>

        {/* Quick stats */}
        {!loading && (
          <div className="flex flex-row gap-2 sm:flex-col">
            {[
              {
                icon: Trophy,
                value: earnedCount,
                label: "logros",
                color: "var(--utb-emerald)",
              },
              {
                icon: Shield,
                value: titlesCount,
                label: "títulos",
                color: "var(--utb-cyan)",
              },
            ].map(({ icon: Icon, value, label, color }) => (
              <div
                key={label}
                className="stat-card flex items-center gap-2"
                style={{ padding: "0.5rem 0.875rem", minWidth: "90px" }}
              >
                <div
                  className="stat-accent-strip"
                  style={{ background: color }}
                />
                <Icon className="h-3.5 w-3.5 flex-shrink-0" style={{ color }} />
                <div className="pl-1">
                  <p className="hud-value" style={{ fontSize: "1.1rem" }}>
                    {value}
                  </p>
                  <p className="hud-label">{label}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// ACADEMIC PROGRESS SECTION
// ─────────────────────────────────────────────────────────────────────────────

function StatCard({
  icon: Icon,
  label,
  value,
  sub,
  accentColor,
  loading,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  sub?: string;
  accentColor: string;
  loading: boolean;
}) {
  return (
    <div className="stat-card flex-1" style={{ minWidth: "0" }}>
      <div className="stat-accent-strip" style={{ background: accentColor }} />
      <div className="pl-3">
        <div
          className="flex items-center gap-1.5 mb-2"
          style={{ color: accentColor }}
        >
          <Icon className="h-3 w-3" />
          <span className="hud-label">{label}</span>
        </div>
        {loading ? (
          <HudSkeleton className="h-8 w-16" />
        ) : (
          <p className="hud-value" style={{ fontSize: "1.75rem" }}>
            {value}
          </p>
        )}
        {!loading && sub && (
          <p className="hud-label mt-1" style={{ color: "var(--text-muted)" }}>
            {sub}
          </p>
        )}
      </div>
    </div>
  );
}

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
    <div
      className="hud-panel relative overflow-hidden"
      style={{ padding: "0" }}
    >
      {/* Header */}
      <div
        className="flex items-center justify-between px-4 py-3"
        style={{ borderBottom: "1px solid var(--surface-3)" }}
      >
        <div className="flex items-center gap-2">
          <div
            className="h-4 w-[2px]"
            style={{ background: "var(--utb-savio)" }}
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
            Progreso Académico
          </h2>
        </div>
        <Link
          href="/dashboard/malla"
          className="btn-hud"
          style={{ fontSize: "9px", padding: "3px 10px" }}
        >
          Ver malla completa
          <ArrowUpRight className="h-2.5 w-2.5" />
        </Link>
      </div>

      {/* Stats */}
      <div
        className="grid grid-cols-2 gap-px sm:grid-cols-4"
        style={{ background: "var(--surface-3)" }}
      >
        <StatCard
          icon={GraduationCap}
          label="PGA"
          value={loading ? "—" : pga > 0 ? pga.toFixed(2) : "—"}
          accentColor="var(--utb-cyan)"
          loading={loading}
        />
        <StatCard
          icon={Award}
          label="Créditos"
          value={loading ? "—" : creditos !== null ? String(creditos) : "—"}
          accentColor="var(--utb-savio)"
          loading={loading}
        />
        <StatCard
          icon={BookOpen}
          label="Materias"
          value={loading ? "—" : String(materiasAprobadas)}
          sub={`de ${totalMaterias}`}
          accentColor="var(--utb-emerald)"
          loading={loading}
        />
        <StatCard
          icon={Percent}
          label="Avance"
          value={loading ? "—" : `${Math.round(porcentaje)}%`}
          accentColor="var(--utb-aqua)"
          loading={loading}
        />
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// ACHIEVEMENT CARD — Marathon geometric style
// ─────────────────────────────────────────────────────────────────────────────

function AchievementCard({
  logro,
  idx,
}: {
  logro: ResolvedLogro;
  idx: number;
}) {
  const rarity = LOGRO_RARITY[logro.nombre] ?? {
    tier: "common" as const,
    label: "Común",
  };

  const tierColors = {
    common: { accent: "var(--tier-common)", line: "rgba(122,139,168,0.3)" },
    rare: { accent: "var(--utb-cyan)", line: "rgba(27,185,235,0.35)" },
    epic: { accent: "#7C3AED", line: "rgba(124,58,237,0.35)" },
    legendary: { accent: "var(--utb-emerald)", line: "rgba(245,158,11,0.40)" },
  }[rarity.tier];

  if (!logro.earned) {
    return (
      <div className="achievement-card locked" style={{ position: "relative" }}>
        <SeqNumber n={idx + 1} />
        <div className="flex items-start gap-2.5">
          <div
            className="flex h-8 w-8 shrink-0 items-center justify-center"
            style={{
              clipPath: "var(--clip-corner-sm)",
              background: "var(--surface-2)",
              border: "1px solid var(--surface-3)",
            }}
          >
            <Lock
              className="h-3.5 w-3.5"
              style={{ color: "var(--surface-4)" }}
            />
          </div>
          <div className="min-w-0 flex-1">
            <p
              className="truncate"
              style={{
                fontFamily: "var(--font-display)",
                fontSize: "0.75rem",
                fontWeight: 600,
                letterSpacing: "0.04em",
                textTransform: "uppercase",
                color: "var(--surface-4)",
              }}
            >
              {logro.nombre}
            </p>
            <p
              style={{
                fontFamily: "var(--font-body)",
                fontSize: "0.7rem",
                color: "var(--surface-4)",
                marginTop: "2px",
              }}
            >
              {logro.descripcion}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`achievement-card ${rarity.tier === "legendary" ? "legendary" : ""}`}
      style={{
        position: "relative",
        borderColor: rarity.tier !== "common" ? tierColors.line : undefined,
      }}
    >
      <SeqNumber n={idx + 1} />

      {/* Left accent line */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          bottom: 0,
          width: "2px",
          background: tierColors.accent,
          opacity: 0.7,
        }}
      />

      <div className="flex items-start gap-2.5 pl-2">
        {/* Icon */}
        <div
          className="flex h-8 w-8 shrink-0 items-center justify-center"
          style={{
            clipPath: "var(--clip-corner-sm)",
            background: `${tierColors.accent}15`,
            border: `1px solid ${tierColors.accent}40`,
            position: "relative",
          }}
        >
          <Award className="h-3.5 w-3.5" style={{ color: tierColors.accent }} />
          {rarity.tier === "legendary" && (
            <span
              style={{
                position: "absolute",
                top: "-2px",
                right: "-2px",
                fontSize: "7px",
              }}
            >
              ✦
            </span>
          )}
        </div>

        {/* Text */}
        <div className="min-w-0 flex-1 pr-6">
          <div className="flex items-start justify-between gap-1 flex-wrap">
            <p
              className="truncate"
              style={{
                fontFamily: "var(--font-display)",
                fontSize: "0.72rem",
                fontWeight: 700,
                letterSpacing: "0.05em",
                textTransform: "uppercase",
                color: "var(--text-primary)",
              }}
            >
              {logro.nombre}
            </p>
          </div>
          <p
            style={{
              fontFamily: "var(--font-body)",
              fontSize: "0.68rem",
              color: "var(--text-muted)",
              marginTop: "2px",
              lineHeight: 1.4,
            }}
          >
            {logro.descripcion}
          </p>
          {/* Tier badge */}
          <div className="mt-1.5">
            <span className={`tier-badge tier-${rarity.tier}`}>
              {rarity.label}
            </span>
          </div>
        </div>
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

function AchievementsSection({
  logros,
  loading,
}: {
  logros: ResolvedLogro[];
  loading: boolean;
}) {
  const [filter, setFilter] = useState<FilterTab>("earned");

  const filtered = useMemo(() => {
    switch (filter) {
      case "earned":
        return logros.filter((l) => l.earned);
      case "locked":
        return logros.filter((l) => !l.earned);
      case "rare":
        return logros.filter(
          (l) =>
            l.earned &&
            ["rare", "epic", "legendary"].includes(
              LOGRO_RARITY[l.nombre]?.tier ?? "",
            ),
        );
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
    <div className="hud-panel" style={{ padding: 0 }}>
      {/* Header */}
      <div
        className="flex flex-col gap-3 px-4 py-3 sm:flex-row sm:items-center sm:justify-between"
        style={{ borderBottom: "1px solid var(--surface-3)" }}
      >
        <div className="flex items-center gap-3">
          <div
            className="h-4 w-[2px]"
            style={{ background: "var(--utb-cyan)" }}
          />
          <div>
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
              Logros
            </h2>
            {!loading && (
              <p
                className="hud-label"
                style={{ color: "var(--text-muted)", marginTop: "1px" }}
              >
                {earnedCount}/{logros.length} desbloqueados · {pct}%
              </p>
            )}
          </div>
        </div>
        {!loading && (
          <div style={{ width: "6rem" }}>
            <HudProgress pct={pct} color="var(--utb-cyan)" />
          </div>
        )}
      </div>

      {/* Filters */}
      <div
        className="flex gap-1.5 overflow-x-auto px-4 py-2.5"
        style={{ borderBottom: "1px solid var(--surface-3)" }}
      >
        {FILTER_TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setFilter(tab.id)}
            className={`filter-tab ${filter === tab.id ? "active" : ""}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="p-4">
        {loading ? (
          <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <HudSkeleton key={i} className="h-20" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-2 py-10 text-center">
            <Star className="h-7 w-7" style={{ color: "var(--surface-3)" }} />
            <p className="hud-label" style={{ color: "var(--text-muted)" }}>
              Ningún logro en esta categoría
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((logro, i) => (
              <AchievementCard key={logro.id_logro} logro={logro} idx={i} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// TITLES SECTION
// ─────────────────────────────────────────────────────────────────────────────

function TitlesSection({
  titles,
  loading,
}: {
  titles: string[];
  loading: boolean;
}) {
  return (
    <div className="hud-panel" style={{ padding: 0 }}>
      <div
        className="flex items-center gap-2 px-4 py-3"
        style={{ borderBottom: "1px solid var(--surface-3)" }}
      >
        <div
          className="h-4 w-[2px]"
          style={{ background: "var(--utb-emerald)" }}
        />
        <div>
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
            Títulos y Rangos
          </h2>
          {!loading && (
            <p
              className="hud-label"
              style={{ color: "var(--text-muted)", marginTop: "1px" }}
            >
              {titles.length}{" "}
              {titles.length === 1 ? "título obtenido" : "títulos obtenidos"}
            </p>
          )}
        </div>
      </div>
      <div className="p-4">
        {loading ? (
          <div className="flex flex-wrap gap-2">
            {[1, 2, 3].map((i) => (
              <HudSkeleton key={i} className="h-6 w-28" />
            ))}
          </div>
        ) : titles.length === 0 ? (
          <div className="flex flex-col items-center gap-2 py-5 text-center">
            <Shield className="h-6 w-6" style={{ color: "var(--surface-3)" }} />
            <p className="hud-label" style={{ color: "var(--text-muted)" }}>
              Completa etapas del programa para obtener títulos
            </p>
          </div>
        ) : (
          <div className="flex flex-wrap gap-2">
            {titles.map((title) => {
              const s = TITLE_STYLES[title] ?? {
                bg: "rgba(122,139,168,0.08)",
                color: "var(--text-muted)",
                border: "rgba(122,139,168,0.25)",
              };
              return (
                <span
                  key={title}
                  className="title-badge"
                  style={{
                    background: s.bg,
                    color: s.color,
                    borderColor: s.border,
                  }}
                >
                  <Shield className="h-2.5 w-2.5" />
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
// NEXT UNLOCKS
// ─────────────────────────────────────────────────────────────────────────────

function estimateProgress(
  logro: ResolvedLogro,
  stats: { materiasAprobadas: number; totalMaterias: number; pga: number },
): number {
  const { materiasAprobadas, totalMaterias, pga } = stats;
  const n = logro.nombre;
  if (n === "Décima superada")
    return Math.min((materiasAprobadas / 10) * 100, 99);
  if (n === "Veinte arriba")
    return Math.min((materiasAprobadas / 20) * 100, 99);
  if (n === "Treinta y contando")
    return Math.min((materiasAprobadas / 30) * 100, 99);
  if (n === "Arrancando fuerte")
    return Math.min((materiasAprobadas / 8) * 100, 99);
  if (n === "Mitad del camino")
    return Math.min((materiasAprobadas / totalMaterias / 0.5) * 100, 99);
  if (n === "Promedio alto") return Math.min((pga / 4.0) * 100, 99);
  if (n === "Matrícula de honor") return Math.min((pga / 4.5) * 100, 99);
  if (n === "Cinco con distinción")
    return Math.min((materiasAprobadas / 5) * 100, 99);
  if (n === "Diez con distinción")
    return Math.min((materiasAprobadas / 10) * 100, 99);
  return Math.min((materiasAprobadas / Math.max(totalMaterias, 1)) * 80, 85);
}

function NextUnlocksSection({
  logros,
  loading,
  materiasAprobadas,
  totalMaterias,
  pga,
}: {
  logros: ResolvedLogro[];
  loading: boolean;
  materiasAprobadas: number;
  totalMaterias: number;
  pga: number;
}) {
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
      <div className="hud-panel" style={{ padding: 0 }}>
        <div
          className="px-4 py-3"
          style={{ borderBottom: "1px solid var(--surface-3)" }}
        >
          <HudSkeleton className="h-4 w-40" />
        </div>
        <div className="space-y-2 p-4">
          {[1, 2, 3].map((i) => (
            <HudSkeleton key={i} className="h-16" />
          ))}
        </div>
      </div>
    );
  }

  if (nextUp.length === 0) return null;

  return (
    <div className="hud-panel" style={{ padding: 0 }}>
      <div
        className="flex items-center gap-2 px-4 py-3"
        style={{ borderBottom: "1px solid var(--surface-3)" }}
      >
        <div
          className="h-4 w-[2px]"
          style={{ background: "var(--utb-aqua)" }}
        />
        <div>
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
            Próximos Desbloqueos
          </h2>
          <p
            className="hud-label"
            style={{ color: "var(--text-muted)", marginTop: "1px" }}
          >
            Los más cercanos a desbloquearse
          </p>
        </div>
      </div>
      <div className="space-y-2 p-4">
        {nextUp.map((logro, i) => {
          const rarity = LOGRO_RARITY[logro.nombre] ?? {
            tier: "common" as const,
          };
          const accentColor =
            rarity.tier === "legendary"
              ? "var(--utb-emerald)"
              : rarity.tier === "epic"
                ? "#7C3AED"
                : rarity.tier === "rare"
                  ? "var(--utb-cyan)"
                  : "var(--text-muted)";
          return (
            <div
              key={logro.id_logro}
              className="unlock-row"
              style={{ borderColor: `${accentColor}30` }}
            >
              <div className="flex items-center justify-between gap-2 mb-2">
                <div className="flex items-center gap-2 min-w-0">
                  <div
                    className="h-1.5 w-1.5 shrink-0"
                    style={{
                      background: accentColor,
                      clipPath: "var(--clip-corner-sm)",
                    }}
                  />
                  <p
                    className="truncate"
                    style={{
                      fontFamily: "var(--font-display)",
                      fontSize: "0.7rem",
                      fontWeight: 700,
                      letterSpacing: "0.05em",
                      textTransform: "uppercase",
                      color: "var(--text-primary)",
                    }}
                  >
                    {logro.nombre}
                  </p>
                </div>
                <span
                  className="shrink-0"
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "10px",
                    color: accentColor,
                    fontWeight: 700,
                  }}
                >
                  {Math.round(logro.est)}%
                </span>
              </div>
              <HudProgress pct={logro.est} color={accentColor} />
              <p
                className="mt-1.5"
                style={{
                  fontFamily: "var(--font-body)",
                  fontSize: "0.67rem",
                  color: "var(--text-muted)",
                }}
              >
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
// ACTIVITY RIBBON
// ─────────────────────────────────────────────────────────────────────────────

function ActivityRibbon({
  earnedCount,
  pga,
  loading,
}: {
  earnedCount: number;
  pga: number;
  loading: boolean;
}) {
  if (loading) return null;
  const alerts = [];
  if (pga >= 4.5)
    alerts.push({
      icon: Flame,
      text: `PGA ${pga.toFixed(2)} — Matrícula de Honor`,
      color: "var(--utb-emerald)",
    });
  else if (pga >= 4.0)
    alerts.push({
      icon: Flame,
      text: `PGA ${pga.toFixed(2)} — Promedio Alto`,
      color: "var(--utb-savio)",
    });
  if (earnedCount >= 10)
    alerts.push({
      icon: Zap,
      text: `${earnedCount} logros desbloqueados`,
      color: "var(--utb-cyan)",
    });
  if (alerts.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2">
      {alerts.map((a, i) => (
        <div
          key={i}
          className="flex items-center gap-2"
          style={{
            border: `1px solid ${a.color}40`,
            background: `${a.color}08`,
            padding: "0.4rem 0.875rem",
            clipPath: "var(--clip-corner-sm)",
          }}
        >
          <a.icon className="h-3.5 w-3.5" style={{ color: a.color }} />
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "10px",
              letterSpacing: "0.08em",
              color: a.color,
              fontWeight: 700,
            }}
          >
            {a.text}
          </span>
        </div>
      ))}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PAGE ROOT
// ─────────────────────────────────────────────────────────────────────────────

export default function PerfilPage() {
  const { profile, loading } = useCurrentUser();
  const { profile: questProfile, loading: questLoading } = useQuestProfile();

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
    <div className="flex flex-col gap-4 pb-8">
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
          Perfil
        </h1>
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "10px",
            letterSpacing: "0.12em",
            color: "var(--text-muted)",
          }}
        >
          // dashboard · student-profile
        </span>
      </div>

      {/* Header panel */}
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

      {/* Activity alerts */}
      <ActivityRibbon
        earnedCount={earnedLogros.length}
        pga={pga}
        loading={isLoading}
      />

      {/* Academic stats */}
      <AcademicProgressSection
        loading={isLoading}
        pga={pga}
        creditos={creditos}
        materiasAprobadas={materiasAprobadas}
        totalMaterias={totalMaterias}
        porcentaje={porcentaje}
      />

      {/* Main: Achievements + sidebar */}
      <div className="flex flex-col gap-4 xl:flex-row">
        <div className="min-w-0 flex-1">
          <AchievementsSection logros={logros} loading={isLoading} />
        </div>
        <div className="flex w-full flex-col gap-4 xl:w-72 xl:shrink-0">
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
