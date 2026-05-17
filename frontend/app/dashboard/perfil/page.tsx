"use client";

import { useState } from "react";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { Settings } from "lucide-react";

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

function capitalise(s: string) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function Skeleton({ className }: { className: string }) {
  return (
    <div className={`animate-pulse rounded bg-[#1a1a2e]/10 ${className}`} />
  );
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

export default function ProfilePage() {
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
    <div className="mx-auto max-w-2xl">
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
  );
}
