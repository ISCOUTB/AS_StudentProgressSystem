"use client";

import { useState } from "react";
import { useQuestProfile } from "../../../hooks/useQuestProfile";
import type {
  Quest,
  SkillTree,
  SecretQuest,
  QuestStep,
} from "../../../lib/questEngine";
import {
  ChevronDown,
  ChevronUp,
  Lock,
  CheckCircle2,
  Circle,
  Sparkles,
  Shield,
  Zap,
} from "lucide-react";

// ─── Skeleton ────────────────────────────────────────────────────────────────

function Skeleton({ className }: { className: string }) {
  return (
    <div className={`animate-pulse rounded bg-[#1a1a2e]/10 ${className}`} />
  );
}

// ─── Progress bar ─────────────────────────────────────────────────────────────

function ProgressBar({
  pct,
  color,
  thin = false,
}: {
  pct: number;
  color: string;
  thin?: boolean;
}) {
  return (
    <div
      className={`w-full overflow-hidden rounded-full bg-[#1a1a2e]/10 ${thin ? "h-1.5" : "h-2.5"}`}
    >
      <div
        className={`h-full rounded-full transition-all duration-700 ${color}`}
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}

// ─── Step list ────────────────────────────────────────────────────────────────

function StepList({ steps }: { steps: QuestStep[] }) {
  return (
    <ol className="mt-4 space-y-2">
      {steps.map((s, i) => (
        <li key={s.id} className="flex items-start gap-3">
          <div className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center">
            {s.completed ? (
              <CheckCircle2 className="h-5 w-5 text-[#00C853]" />
            ) : (
              <Circle className="h-5 w-5 text-[#1a1a2e]/25" />
            )}
          </div>
          <div>
            <span
              className={`text-sm font-semibold ${
                s.completed ? "text-[#1a1a2e]" : "text-[#1a1a2e]/40"
              }`}
            >
              {i + 1}. {s.label}
            </span>
            {s.completed && (
              <p className="text-xs text-[#1a1a2e]/50">{s.description}</p>
            )}
          </div>
        </li>
      ))}
    </ol>
  );
}

// ─── Main Quest Card ──────────────────────────────────────────────────────────

function MainQuestCard({ quest }: { quest: Quest }) {
  const [expanded, setExpanded] = useState(false);

  const accentBg =
    quest.id === "camino-programador"
      ? "bg-emerald-500"
      : quest.id === "ruta-cientifica"
        ? "bg-blue-500"
        : "bg-purple-600";

  const progressColor =
    quest.id === "camino-programador"
      ? "bg-emerald-400"
      : quest.id === "ruta-cientifica"
        ? "bg-blue-400"
        : "bg-purple-400";

  return (
    <div
      className={`overflow-hidden rounded-2xl border bg-white/90 shadow-sm backdrop-blur-sm transition-all duration-300 ${
        quest.completed
          ? "border-[#00C853]/40 shadow-[#00C853]/10"
          : "border-[#1a1a2e]/10"
      }`}
    >
      {/* Header strip */}
      <div className={`${accentBg} px-5 py-3`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-lg">{quest.icon}</span>
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-white/70">
                Main Quest
              </p>
              <h3 className="font-bold text-white">{quest.title}</h3>
            </div>
          </div>
          {quest.completed && (
            <div className="flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-xs font-bold text-white">
              <CheckCircle2 className="h-3.5 w-3.5" />
              Completada
            </div>
          )}
        </div>
      </div>

      {/* Body */}
      <div className="p-5">
        <p className="mb-3 text-sm text-[#1a1a2e]/60">{quest.subtitle}</p>

        {/* Progress */}
        <div className="mb-4">
          <div className="mb-1.5 flex items-center justify-between">
            <span className="text-xs font-medium text-[#1a1a2e]/50">
              {quest.completedSteps}/{quest.totalSteps} etapas
            </span>
            <span className="text-xs font-bold text-[#1a1a2e]">
              {quest.percentComplete}%
            </span>
          </div>
          <ProgressBar pct={quest.percentComplete} color={progressColor} />
        </div>

        {/* Reward title preview */}
        {quest.rewardTitle && (
          <div className="mb-4 flex items-center gap-2 rounded-xl border border-[#C2F542]/40 bg-[#C2F542]/10 px-3 py-2">
            <Sparkles className="h-4 w-4 shrink-0 text-[#1a1a2e]/60" />
            <span className="text-xs font-semibold text-[#1a1a2e]/70">
              {quest.completed ? "Título obtenido:" : "Título actual:"}{" "}
              <span className="font-bold text-[#1a1a2e]">
                "{quest.rewardTitle}"
              </span>
            </span>
          </div>
        )}

        {/* Expand toggle */}
        <button
          onClick={() => setExpanded(!expanded)}
          className="flex w-full items-center justify-between rounded-xl border border-[#1a1a2e]/10 bg-[#1a1a2e]/5 px-4 py-2.5 text-sm font-medium text-[#1a1a2e]/60 transition-all hover:bg-[#1a1a2e]/10"
        >
          <span>Ver etapas</span>
          {expanded ? (
            <ChevronUp className="h-4 w-4" />
          ) : (
            <ChevronDown className="h-4 w-4" />
          )}
        </button>

        {expanded && <StepList steps={quest.steps} />}
      </div>
    </div>
  );
}

// ─── Skill Tree Card ──────────────────────────────────────────────────────────

function SkillTreeCard({ tree }: { tree: SkillTree }) {
  const [expanded, setExpanded] = useState(false);

  const colorMap: Record<
    string,
    { bar: string; badge: string; border: string }
  > = {
    "bg-cyan-500": {
      bar: "bg-cyan-400",
      badge: "bg-cyan-100 text-cyan-700 border-cyan-200",
      border: "border-cyan-200",
    },
    "bg-violet-500": {
      bar: "bg-violet-400",
      badge: "bg-violet-100 text-violet-700 border-violet-200",
      border: "border-violet-200",
    },
    "bg-orange-500": {
      bar: "bg-orange-400",
      badge: "bg-orange-100 text-orange-700 border-orange-200",
      border: "border-orange-200",
    },
  };

  const colors = colorMap[tree.color] ?? {
    bar: "bg-gray-400",
    badge: "bg-gray-100 text-gray-700 border-gray-200",
    border: "border-gray-200",
  };

  return (
    <div
      className={`overflow-hidden rounded-2xl border bg-white/90 shadow-sm backdrop-blur-sm ${
        tree.completed ? colors.border : "border-[#1a1a2e]/10"
      }`}
    >
      <div className="p-5">
        <div className="mb-3 flex items-start justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="text-xl">{tree.icon}</span>
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-[#1a1a2e]/40">
                Skill Tree
              </p>
              <h3 className="font-bold text-[#1a1a2e]">{tree.title}</h3>
            </div>
          </div>
          {tree.completed && (
            <span
              className={`shrink-0 rounded-full border px-2 py-0.5 text-xs font-bold ${colors.badge}`}
            >
              ✓ {tree.specialty}
            </span>
          )}
        </div>

        {!tree.completed && (
          <p className="mb-3 text-xs text-[#1a1a2e]/50">
            Completa las materias para obtener:{" "}
            <span className="font-semibold">"{tree.specialty}"</span>
          </p>
        )}

        <div className="mb-1.5 flex items-center justify-between">
          <span className="text-xs text-[#1a1a2e]/40">
            {tree.completedSteps}/{tree.totalSteps}
          </span>
          <span className="text-xs font-bold text-[#1a1a2e]">
            {tree.percentComplete}%
          </span>
        </div>
        <ProgressBar pct={tree.percentComplete} color={colors.bar} thin />

        {/* Mini steps */}
        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-3 flex w-full items-center justify-between text-xs text-[#1a1a2e]/40 hover:text-[#1a1a2e]/60"
        >
          <span>Materias del árbol</span>
          {expanded ? (
            <ChevronUp className="h-3.5 w-3.5" />
          ) : (
            <ChevronDown className="h-3.5 w-3.5" />
          )}
        </button>

        {expanded && (
          <ol className="mt-2 space-y-1.5">
            {tree.steps.map((s, i) => (
              <li key={s.id} className="flex items-center gap-2">
                {s.completed ? (
                  <CheckCircle2 className="h-4 w-4 shrink-0 text-[#00C853]" />
                ) : (
                  <Circle className="h-4 w-4 shrink-0 text-[#1a1a2e]/20" />
                )}
                <span
                  className={`text-xs ${
                    s.completed
                      ? "font-medium text-[#1a1a2e]"
                      : "text-[#1a1a2e]/40"
                  }`}
                >
                  {i + 1}. {s.label}
                </span>
              </li>
            ))}
          </ol>
        )}
      </div>
    </div>
  );
}

// ─── Secret Quest Card ────────────────────────────────────────────────────────

function SecretQuestCard({ quest }: { quest: SecretQuest }) {
  const isPending = quest.id === "boss-fight";

  return (
    <div
      className={`overflow-hidden rounded-2xl border bg-white/90 shadow-sm backdrop-blur-sm ${
        quest.completed
          ? "border-[#C2F542]/50"
          : isPending
            ? "border-[#1a1a2e]/5 opacity-50"
            : "border-[#1a1a2e]/10"
      }`}
    >
      <div className="p-5">
        <div className="flex items-start gap-3">
          <div
            className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-2xl ${
              quest.completed ? "bg-[#C2F542]/20" : "bg-[#1a1a2e]/5"
            }`}
          >
            {isPending ? (
              <Lock className="h-5 w-5 text-[#1a1a2e]/20" />
            ) : (
              quest.icon
            )}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h3
                className={`font-bold ${
                  quest.completed ? "text-[#1a1a2e]" : "text-[#1a1a2e]/60"
                }`}
              >
                {quest.completed || !isPending ? quest.title : "???"}
              </h3>
              {quest.completed && (
                <span className="rounded-full bg-[#C2F542]/30 px-2 py-0.5 text-[10px] font-bold text-[#1a1a2e]">
                  COMPLETADO
                </span>
              )}
            </div>
            <p className="mt-1 text-xs text-[#1a1a2e]/50">
              {isPending ? "Próximamente disponible" : quest.description}
            </p>

            {/* Progress for Perfeccionista */}
            {!isPending && quest.progress !== undefined && (
              <div className="mt-3">
                <div className="mb-1 flex justify-between">
                  <span className="text-[10px] text-[#1a1a2e]/40">
                    {quest.progressLabel}
                  </span>
                  <span className="text-[10px] font-bold text-[#1a1a2e]">
                    {quest.progress}%
                  </span>
                </div>
                <ProgressBar
                  pct={quest.progress}
                  color={quest.completed ? "bg-[#C2F542]" : "bg-amber-400"}
                  thin
                />
              </div>
            )}

            {!quest.completed && !isPending && (
              <p className="mt-2 text-[10px] italic text-[#1a1a2e]/30">
                {quest.hint}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Title Badge ──────────────────────────────────────────────────────────────

const TITLE_STYLES: Record<string, string> = {
  Aprendiz: "bg-emerald-100 text-emerald-800 border-emerald-200",
  Desarrollador: "bg-blue-100 text-blue-800 border-blue-200",
  "Arquitecto del Código": "bg-purple-100 text-purple-800 border-purple-200",
  "Científico Formado": "bg-sky-100 text-sky-800 border-sky-200",
  "Ingeniero de Sistemas": "bg-indigo-100 text-indigo-800 border-indigo-200",
  "Network Specialist": "bg-cyan-100 text-cyan-800 border-cyan-200",
  "AI Initiate": "bg-violet-100 text-violet-800 border-violet-200",
  "Backend Engineer": "bg-orange-100 text-orange-800 border-orange-200",
};

function TitleBadge({ title }: { title: string }) {
  const style =
    TITLE_STYLES[title] ?? "bg-gray-100 text-gray-700 border-gray-200";
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full border px-3 py-1 text-xs font-bold ${style}`}
    >
      <Shield className="h-3 w-3" />
      {title}
    </span>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function QuestsPage() {
  const { profile, loading, error } = useQuestProfile();

  if (error) {
    return (
      <div className="flex items-center justify-center py-20">
        <p className="text-sm text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-8">
      {/* ── Header ──────────────────────────────────────────────────────────── */}
      <div>
        <h1 className="text-2xl font-bold uppercase tracking-wide text-[#1a1a2e]">
          Quests
        </h1>
        <p className="text-sm text-[#1a1a2e]/50">
          Tu camino académico como aventura
        </p>
      </div>

      {/* ── Titles strip ─────────────────────────────────────────────────────── */}
      <div className="rounded-2xl border border-[#1a1a2e]/10 bg-white/90 p-5 backdrop-blur-sm">
        <div className="mb-3 flex items-center gap-2">
          <Zap className="h-4 w-4 text-[#1a1a2e]/40" />
          <h2 className="text-xs font-bold uppercase tracking-widest text-[#1a1a2e]/50">
            Títulos obtenidos
          </h2>
        </div>

        {loading ? (
          <div className="flex flex-wrap gap-2">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-7 w-28 rounded-full" />
            ))}
          </div>
        ) : profile && profile.titles.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {profile.titles.map((t) => (
              <TitleBadge key={t} title={t} />
            ))}
          </div>
        ) : (
          <p className="text-sm text-[#1a1a2e]/40">
            Completa etapas de las quests para obtener títulos.
          </p>
        )}
      </div>

      {/* ── Main Quests ───────────────────────────────────────────────────────── */}
      <section>
        <h2 className="mb-4 flex items-center gap-2 text-sm font-bold uppercase tracking-widest text-[#1a1a2e]/60">
          <span className="h-px flex-1 bg-[#1a1a2e]/10" />
          Main Quests
          <span className="h-px flex-1 bg-[#1a1a2e]/10" />
        </h2>

        {loading ? (
          <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-48 w-full rounded-2xl" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
            {profile?.mainQuests.map((q) => (
              <MainQuestCard key={q.id} quest={q} />
            ))}
          </div>
        )}
      </section>

      {/* ── Skill Trees ───────────────────────────────────────────────────────── */}
      <section>
        <h2 className="mb-4 flex items-center gap-2 text-sm font-bold uppercase tracking-widest text-[#1a1a2e]/60">
          <span className="h-px flex-1 bg-[#1a1a2e]/10" />
          Skill Trees
          <span className="h-px flex-1 bg-[#1a1a2e]/10" />
        </h2>

        {loading ? (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-32 w-full rounded-2xl" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {profile?.skillTrees.map((tree) => (
              <SkillTreeCard key={tree.id} tree={tree} />
            ))}
          </div>
        )}
      </section>

      {/* ── Secret Quests ─────────────────────────────────────────────────────── */}
      <section>
        <h2 className="mb-4 flex items-center gap-2 text-sm font-bold uppercase tracking-widest text-[#1a1a2e]/60">
          <span className="h-px flex-1 bg-[#1a1a2e]/10" />
          Quests Secretas
          <span className="h-px flex-1 bg-[#1a1a2e]/10" />
        </h2>

        {loading ? (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {[1, 2].map((i) => (
              <Skeleton key={i} className="h-28 w-full rounded-2xl" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {profile?.secretQuests.map((q) => (
              <SecretQuestCard key={q.id} quest={q} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
