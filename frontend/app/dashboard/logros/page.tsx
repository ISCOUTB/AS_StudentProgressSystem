"use client";

import { useState } from "react";
import { Award, ArrowRight, ArrowLeft, Settings, Lock } from "lucide-react";
import { useCurrentUser, type ResolvedLogro } from "@/hooks/useCurrentUser";

// ── UTB logo SVG path (reused in badge) ───────────────────────────────────────

function UtbLogoPath() {
  return (
    <svg width="40" height="20" viewBox="0 0 874 428" fill="currentColor">
      <path d="M833.88 213.77C833.179 213.888 833.179 214.901 833.88 215.02C856.599 218.78 874 239.166 874 263.747V395.12C874 413.336 859.744 428 842.179 428H560.536V235.865H743.317V193.568H518.901V428H356.283V193.568H313.311V395.12C313.311 413.283 299.068 428 281.49 428H31.8213C14.2559 428 0 413.322 0 395.12V32.8796C0 14.73 14.2559 0 31.8213 0H135.367V287H178.352V0H842.166C859.744 0 873.987 14.73 873.987 32.8796V165.082C873.987 189.663 856.6 210.008 833.867 213.757" />
    </svg>
  );
}

// ── Featured card config ───────────────────────────────────────────────────────
// Maps specific logro names to the big coloured highlight cards.
// Order determines display priority; only earned ones are shown.

interface FeaturedConfig {
  logroName: string;
  label: string;
  color: string;
}

const FEATURED_CONFIG: FeaturedConfig[] = [
  {
    logroName: "Científico formado",
    label: "CIENCIAS BÁSICAS",
    color: "bg-[#9575CD]",
  },
  {
    logroName: "Políglota",
    label: "ESCUELA DE IDIOMAS",
    color: "bg-[#FFB74D]",
  },
  {
    logroName: "Humanista digital",
    label: "CIENCIAS Y HUMANIDADES",
    color: "bg-[#4CAF50]",
  },
  {
    logroName: "Ingeniero de sistemas",
    label: "INGENIERÍA ISCO",
    color: "bg-[#1BB9EB]",
  },
  { logroName: "Libre elección", label: "ELECTIVAS", color: "bg-[#EF5350]" },
  {
    logroName: "Programa completo",
    label: "PROGRAMA COMPLETO",
    color: "bg-[#26A69A]",
  },
  {
    logroName: "Matrícula de honor",
    label: "MATRÍCULA DE HONOR",
    color: "bg-[#AB47BC]",
  },
  { logroName: "Graduando", label: "GRADUANDO", color: "bg-[#FF7043]" },
];

// Badge labels — static, represent memberships/institutions
const BADGES = [
  { logo: "UTB", label: "UTB" },
  { logo: "UBUNTU", label: "UBUNTU" },
  { logo: "GLOBAL", label: "GLOBAL" },
  { logo: "ISCO", label: "ISCO" },
];

// ── Helpers ────────────────────────────────────────────────────────────────────

function capitalise(s: string) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

// ── Skeleton ───────────────────────────────────────────────────────────────────

function Skeleton({ className }: { className: string }) {
  return (
    <div className={`animate-pulse rounded bg-[#1a1a2e]/10 ${className}`} />
  );
}

// ── Personal info panel (shared between mobile + desktop) ─────────────────────

interface InfoPanelProps {
  loading: boolean;
  fullName: string | null;
  escuela: string | null;
  semesterLabel: string | null;
  materiasAprobadas: number;
  totalMaterias: number;
  earnedCount: number;
  totalLogros: number;
}

function InfoPanel({
  loading,
  fullName,
  escuela,
  semesterLabel,
  materiasAprobadas,
  totalMaterias,
  earnedCount,
  totalLogros,
}: InfoPanelProps) {
  const subjectPct =
    totalMaterias > 0
      ? Math.round((materiasAprobadas / totalMaterias) * 100)
      : 0;
  const logroPct =
    totalLogros > 0 ? Math.round((earnedCount / totalLogros) * 100) : 0;

  if (loading) {
    return (
      <div className="space-y-3 p-4">
        <Skeleton className="h-4 w-36" />
        <Skeleton className="h-3 w-48" />
        <Skeleton className="h-3 w-28" />
        <div className="mt-4 space-y-2 border-t border-[#1a1a2e]/10 pt-4">
          <Skeleton className="h-3 w-24" />
          <Skeleton className="h-6 w-16" />
          <Skeleton className="h-2 w-full rounded-full" />
        </div>
      </div>
    );
  }

  return (
    <div className="p-4">
      <h3 className="mb-2 text-lg font-bold uppercase tracking-wide text-[#1a1a2e]">
        {fullName ?? "—"}
      </h3>
      <p className="mb-4 text-sm leading-relaxed text-[#1a1a2e]/70">
        {escuela ?? "—"}
      </p>
      <p className="mb-4 text-sm leading-relaxed text-[#1a1a2e]/70">
        {semesterLabel ? `. ${capitalise(semesterLabel)}.` : "."}
      </p>
      {/* Subjects */}
      <div className="border-t border-[#1a1a2e]/10 pt-4">
        <h4 className="mb-2 text-sm font-medium text-[#1a1a2e]/60">
          Materias Cursadas
        </h4>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold text-[#1a1a2e]">
            {materiasAprobadas}
          </span>
          <span className="text-lg text-[#1a1a2e]/40">
            /{totalMaterias || "—"}
          </span>
        </div>
        <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-gray-200">
          <div
            className="h-full rounded-full bg-[#00C853] transition-all duration-700"
            style={{ width: `${subjectPct}%` }}
          />
        </div>
      </div>

      {/* Logros */}
      <div className="mt-4 border-t border-[#1a1a2e]/10 pt-4">
        <h4 className="mb-2 text-sm font-medium text-[#1a1a2e]/60">
          Logros Obtenidos
        </h4>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold text-[#1a1a2e]">
            {earnedCount}
          </span>
          <span className="text-lg text-[#1a1a2e]/40">
            /{totalLogros || "—"}
          </span>
        </div>
        <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-gray-200">
          <div
            className="h-full rounded-full bg-[#1BB9EB] transition-all duration-700"
            style={{ width: `${logroPct}%` }}
          />
        </div>
      </div>
    </div>
  );
}

// ── "Ver todos los logros" sub-view ───────────────────────────────────────────

interface AllLogrosViewProps {
  logros: ResolvedLogro[];
  loading: boolean;
  onBack: () => void;
}

function AllLogrosView({ logros, loading, onBack }: AllLogrosViewProps) {
  const earned = logros.filter((l) => l.earned);
  const locked = logros.filter((l) => !l.earned);

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={onBack}
          className="flex items-center gap-2 rounded-lg border border-[#1a1a2e]/20 bg-white px-4 py-2 font-medium text-[#1a1a2e] transition-all hover:bg-[#1a1a2e] hover:text-white"
        >
          <ArrowLeft className="h-4 w-4" />
          Volver
        </button>
        <div>
          <h1 className="text-2xl font-bold uppercase tracking-wide text-[#1a1a2e]">
            Todos los Logros
          </h1>
          {!loading && (
            <p className="text-sm text-[#1a1a2e]/50">
              {earned.length} obtenidos · {locked.length} pendientes
            </p>
          )}
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 9 }).map((_, i) => (
            <div
              key={i}
              className="rounded-xl border border-[#1a1a2e]/10 bg-white/90 p-4"
            >
              <div className="flex items-start gap-3">
                <Skeleton className="h-10 w-10 shrink-0 rounded-full" />
                <div className="flex-1 space-y-2">
                  <Skeleton className="h-4 w-32" />
                  <Skeleton className="h-3 w-full" />
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <>
          {/* ── Earned ─────────────────────────────────────────────────── */}
          {earned.length > 0 && (
            <section>
              <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-widest text-[#00C853]">
                <Award className="h-4 w-4" />
                Obtenidos ({earned.length})
              </h2>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                {earned.map((logro) => (
                  <div
                    key={logro.id_logro}
                    className="overflow-hidden rounded-xl border border-[#00C853]/30 bg-white/90 p-4 shadow-sm backdrop-blur-sm transition-all hover:shadow-md"
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#C2F542]/20">
                        <Award className="h-5 w-5 text-[#00C853]" />
                      </div>
                      <div>
                        <h3 className="font-bold text-[#1a1a2e]">
                          {logro.nombre}
                        </h3>
                        <p className="mt-1 text-sm text-[#1a1a2e]/60">
                          {logro.descripcion}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* ── Locked ─────────────────────────────────────────────────── */}
          {locked.length > 0 && (
            <section>
              <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-widest text-[#1a1a2e]/40">
                <Lock className="h-4 w-4" />
                Pendientes ({locked.length})
              </h2>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                {locked.map((logro) => (
                  <div
                    key={logro.id_logro}
                    className="overflow-hidden rounded-xl border border-[#1a1a2e]/10 bg-white/60 p-4 opacity-50 backdrop-blur-sm"
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-100">
                        <Lock className="h-5 w-5 text-[#1a1a2e]/30" />
                      </div>
                      <div>
                        <h3 className="font-bold text-[#1a1a2e]/60">
                          {logro.nombre}
                        </h3>
                        <p className="mt-1 text-sm text-[#1a1a2e]/40">
                          {logro.descripcion}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {logros.length === 0 && (
            <p className="text-center text-sm text-[#1a1a2e]/50">
              No hay logros disponibles.
            </p>
          )}
        </>
      )}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function LogrosPage() {
  const [showAll, setShowAll] = useState(false);
  const { profile, loading } = useCurrentUser();

  // ── Derived values ────────────────────────────────────────────────────────
  const fullName = profile?.fullName ?? null;
  const escuela = profile?.carrera?.escuela ?? null;
  const semesterLabel = profile?.semesterLabel ?? null;
  const materiasAprobadas = profile?.materiasAprobadas ?? 0;
  const totalMaterias = profile?.totalMaterias ?? 0;
  const logros = profile?.logros ?? [];
  const earnedLogros = profile?.earnedLogros ?? [];
  const earnedNames = new Set(earnedLogros.map((l) => l.nombre));

  // Featured cards: earned entries from FEATURED_CONFIG, max 3 shown in main view
  const featuredCards = FEATURED_CONFIG.filter((cfg) =>
    earnedNames.has(cfg.logroName),
  ).slice(0, 6); // show up to 6 so grid stays balanced

  // ── "All achievements" sub-view ───────────────────────────────────────────
  if (showAll) {
    return (
      <AllLogrosView
        logros={logros}
        loading={loading}
        onBack={() => setShowAll(false)}
      />
    );
  }

  // ── Main view ─────────────────────────────────────────────────────────────
  const infoPanelProps: InfoPanelProps = {
    loading,
    fullName,
    escuela,
    semesterLabel,
    materiasAprobadas,
    totalMaterias,
    earnedCount: earnedLogros.length,
    totalLogros: logros.length,
  };

  return (
    <div className="flex flex-col gap-6">
      {/* ── Personal Info (mobile, hidden on xl+) ────────────────────────── */}
      <div className="w-full xl:hidden">
        <div className="overflow-hidden rounded-2xl border border-[#00C853] bg-white/90 shadow-sm backdrop-blur-sm">
          <div className="border-b border-[#00C853]/20 bg-[#00C853] px-4 py-3">
            <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-white">
              <Settings className="h-4 w-4" />
              <span>Información Personal</span>
            </div>
          </div>
          <InfoPanel {...infoPanelProps} />
        </div>
      </div>

      {/* ── Main content + sidebar ────────────────────────────────────────── */}
      <div className="flex flex-col-reverse gap-6 xl:flex-row">
        {/* Left column */}
        <div className="min-w-0 flex-1 space-y-6">
          {/* Badges row */}
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {BADGES.map((badge) => (
              <div
                key={badge.logo}
                className="flex flex-col items-center justify-center rounded-xl border-2 border-[#1a1a2e] bg-white p-4 transition-all"
              >
                <div className="mb-2 text-2xl font-black text-[#1a1a2e]">
                  {badge.logo === "UTB" ? <UtbLogoPath /> : badge.logo}
                </div>
                <span className="text-xs font-medium tracking-wide text-[#1a1a2e]">
                  STUDENT
                </span>
              </div>
            ))}
          </div>

          {/* Featured achievement cards */}
          {loading ? (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-28 w-full rounded-2xl" />
              ))}
            </div>
          ) : featuredCards.length > 0 ? (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {featuredCards.map((cfg) => (
                <div
                  key={cfg.logroName}
                  className={`relative overflow-hidden rounded-2xl ${cfg.color} p-6 text-white shadow-lg`}
                >
                  <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider opacity-90">
                    <Award className="h-4 w-4" />
                    <span>COMPLETASTE</span>
                  </div>
                  <h3 className="mt-2 text-xl font-bold uppercase tracking-wide">
                    {cfg.label}
                  </h3>
                </div>
              ))}
            </div>
          ) : (
            /* No featured achievements yet — show a motivational placeholder */
            <div className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-[#1a1a2e]/15 bg-white/60 px-6 py-10 text-center">
              <Award className="mb-3 h-10 w-10 text-[#1a1a2e]/20" />
              <p className="font-semibold text-[#1a1a2e]/50">
                Aún no tienes logros destacados
              </p>
              <p className="mt-1 text-sm text-[#1a1a2e]/35">
                Completa áreas del programa para desbloquear tus primeras
                medallas.
              </p>
            </div>
          )}

          {/* Counter strip */}
          {!loading && logros.length > 0 && (
            <div className="flex items-center gap-3 rounded-2xl border border-[#1a1a2e]/10 bg-white/80 px-5 py-3">
              <Award className="h-5 w-5 shrink-0 text-[#00C853]" />
              <span className="text-sm font-medium text-[#1a1a2e]/70">
                <span className="font-bold text-[#1a1a2e]">
                  {earnedLogros.length}
                </span>{" "}
                de{" "}
                <span className="font-bold text-[#1a1a2e]">
                  {logros.length}
                </span>{" "}
                logros obtenidos
              </span>
              <div className="ml-auto h-2 w-32 overflow-hidden rounded-full bg-gray-200">
                <div
                  className="h-full rounded-full bg-[#00C853] transition-all duration-700"
                  style={{
                    width:
                      logros.length > 0
                        ? `${Math.round((earnedLogros.length / logros.length) * 100)}%`
                        : "0%",
                  }}
                />
              </div>
            </div>
          )}

          {/* View all button */}
          <button
            onClick={() => setShowAll(true)}
            className="flex w-full items-center justify-between rounded-2xl border-2 border-[#1a1a2e]/20 bg-white/80 p-4 transition-all hover:border-[#1a1a2e]/40 hover:bg-white"
          >
            <div className="flex items-center gap-3 text-[#1a1a2e]/70">
              <Award className="h-5 w-5" />
              <span className="font-medium uppercase tracking-wide">
                Ver todos los logros
              </span>
            </div>
            <ArrowRight className="h-5 w-5 text-[#1a1a2e]/70" />
          </button>
        </div>

        {/* ── Personal Info sidebar (xl+) ──────────────────────────────────── */}
        <div className="hidden w-64 shrink-0 xl:block 2xl:w-72">
          <div className="sticky top-8 overflow-hidden rounded-2xl border border-[#00C853] bg-white/90 shadow-sm backdrop-blur-sm">
            <div className="border-b border-[#00C853]/20 bg-[#00C853] px-4 py-3">
              <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-white">
                <Settings className="h-4 w-4" />
                <span>Información Personal</span>
              </div>
            </div>
            <div className="p-4 xl:p-6">
              <InfoPanel {...infoPanelProps} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
