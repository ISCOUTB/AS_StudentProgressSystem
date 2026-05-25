"use client";

/**
 * /dashboard/quests — Marathon × UTB Design System
 * Solo cambios visuales. Lógica, hooks y estado sin modificar.
 */

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
  Shield,
  Zap,
  Target,
} from "lucide-react";

// ── Primitives ─────────────────────────────────────────────

function HudSkeleton({ style = {} }: { style?: React.CSSProperties }) {
  return (
    <div
      className="hud-skeleton"
      style={{ height: "1rem", borderRadius: "2px", ...style }}
    />
  );
}

function HudProgress({
  pct,
  color = "var(--utb-cyan)",
  thin = false,
}: {
  pct: number;
  color?: string;
  thin?: boolean;
}) {
  return (
    <div
      className="hud-progress w-full"
      style={{ height: thin ? "2px" : "3px" }}
    >
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

// ── Step list ──────────────────────────────────────────────

function StepList({ steps }: { steps: QuestStep[] }) {
  return (
    <ol className="mt-4 space-y-2">
      {steps.map((s, i) => (
        <li key={s.id} className="flex items-start gap-3">
          <div className="mt-0.5 flex-shrink-0">
            {s.completed ? (
              <CheckCircle2
                className="h-4 w-4"
                style={{ color: "var(--utb-savio)" }}
              />
            ) : (
              <Circle
                className="h-4 w-4"
                style={{ color: "var(--surface-3)" }}
              />
            )}
          </div>
          <div>
            <span
              style={{
                fontFamily: "var(--font-display)",
                fontSize: "0.72rem",
                fontWeight: 600,
                letterSpacing: "0.04em",
                textTransform: "uppercase",
                color: s.completed ? "var(--text-primary)" : "var(--surface-4)",
              }}
            >
              {String(i + 1).padStart(2, "0")}. {s.label}
            </span>
            {s.completed && (
              <p
                style={{
                  fontFamily: "var(--font-body)",
                  fontSize: "0.68rem",
                  color: "var(--text-muted)",
                  marginTop: "2px",
                }}
              >
                {s.description}
              </p>
            )}
          </div>
        </li>
      ))}
    </ol>
  );
}

// ── Main Quest Card ────────────────────────────────────────

const QUEST_ACCENTS: Record<string, { line: string; bar: string }> = {
  "camino-programador": { line: "var(--utb-savio)", bar: "var(--utb-savio)" },
  "ruta-cientifica": { line: "var(--utb-cyan)", bar: "var(--utb-cyan)" },
  "saga-ingeniero": { line: "#7C3AED", bar: "#7C3AED" },
};

function MainQuestCard({ quest }: { quest: Quest }) {
  const [expanded, setExpanded] = useState(false);
  const { line, bar } = QUEST_ACCENTS[quest.id] ?? {
    line: "var(--utb-cyan)",
    bar: "var(--utb-cyan)",
  };

  return (
    <div
      style={{
        position: "relative",
        clipPath: "var(--clip-corner)",
        background: "var(--surface-1)",
        border: `1px solid ${quest.completed ? `${line}50` : "var(--surface-3)"}`,
        overflow: "hidden",
        boxShadow: quest.completed ? `0 0 20px ${line}10` : "none",
      }}
    >
      {/* Top accent */}
      <div
        style={{
          height: "2px",
          background: `linear-gradient(90deg, ${line}, transparent)`,
        }}
      />

      {/* Header strip */}
      <div
        className="flex items-center justify-between px-4 py-3"
        style={{
          background: `${line}08`,
          borderBottom: "1px solid var(--surface-3)",
        }}
      >
        <div className="flex items-center gap-2.5">
          <span style={{ fontSize: "1rem" }}>{quest.icon}</span>
          <div>
            <p className="hud-label" style={{ color: line, fontSize: "9px" }}>
              MAIN QUEST
            </p>
            <h3
              style={{
                fontFamily: "var(--font-display)",
                fontSize: "0.8rem",
                fontWeight: 800,
                letterSpacing: "0.06em",
                textTransform: "uppercase",
                color: "var(--text-primary)",
              }}
            >
              {quest.title}
            </h3>
          </div>
        </div>
        {quest.completed && (
          <div
            className="flex items-center gap-1"
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "9px",
              letterSpacing: "0.12em",
              color: line,
              border: `1px solid ${line}40`,
              clipPath: "var(--clip-corner-sm)",
              padding: "3px 8px",
            }}
          >
            <CheckCircle2 className="h-3 w-3" />
            COMPLETADA
          </div>
        )}
      </div>

      {/* Body */}
      <div className="p-4">
        <p
          style={{
            fontFamily: "var(--font-body)",
            fontSize: "0.75rem",
            color: "var(--text-muted)",
            marginBottom: "0.875rem",
          }}
        >
          {quest.subtitle}
        </p>

        {/* Progress */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-1.5">
            <span className="hud-label" style={{ color: "var(--text-muted)" }}>
              {quest.completedSteps}/{quest.totalSteps} etapas
            </span>
            <span
              style={{
                fontFamily: "var(--font-display)",
                fontSize: "0.85rem",
                fontWeight: 700,
                color: line,
              }}
            >
              {quest.percentComplete}%
            </span>
          </div>
          <HudProgress pct={quest.percentComplete} color={bar} />
        </div>

        {/* Reward title */}
        {quest.rewardTitle && (
          <div
            className="flex items-center gap-2 mb-4"
            style={{
              border: "1px solid var(--surface-3)",
              clipPath: "var(--clip-corner-sm)",
              padding: "0.5rem 0.75rem",
              background: "var(--surface-2)",
            }}
          >
            <Zap
              className="h-3.5 w-3.5 flex-shrink-0"
              style={{ color: "var(--utb-emerald)" }}
            />
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "10px",
                letterSpacing: "0.06em",
                color: "var(--text-secondary)",
              }}
            >
              {quest.completed ? "Título obtenido:" : "Título actual:"}{" "}
              <span style={{ fontWeight: 700, color: "var(--text-primary)" }}>
                "{quest.rewardTitle}"
              </span>
            </span>
          </div>
        )}

        {/* Toggle */}
        <button
          onClick={() => setExpanded(!expanded)}
          className="btn-hud w-full"
          style={{
            justifyContent: "space-between",
            padding: "0.5rem 0.75rem",
            fontSize: "10px",
          }}
        >
          <span>Ver etapas</span>
          {expanded ? (
            <ChevronUp className="h-3.5 w-3.5" />
          ) : (
            <ChevronDown className="h-3.5 w-3.5" />
          )}
        </button>

        {expanded && <StepList steps={quest.steps} />}
      </div>

      {/* Corner brackets */}
      <span
        style={{
          position: "absolute",
          bottom: "6px",
          right: "6px",
          width: "8px",
          height: "8px",
          borderBottom: `1px solid ${line}50`,
          borderRight: `1px solid ${line}50`,
        }}
      />
    </div>
  );
}

// ── Skill Tree Card ────────────────────────────────────────

const TREE_ACCENTS: Record<string, string> = {
  "bg-cyan-500": "var(--utb-cyan)",
  "bg-violet-500": "#7C3AED",
  "bg-orange-500": "var(--utb-aqua)",
};

function SkillTreeCard({ tree }: { tree: SkillTree }) {
  const [expanded, setExpanded] = useState(false);
  const accent = TREE_ACCENTS[tree.color] ?? "var(--utb-cyan)";

  return (
    <div
      style={{
        position: "relative",
        clipPath: "var(--clip-corner-sm)",
        background: "var(--surface-1)",
        border: `1px solid ${tree.completed ? `${accent}45` : "var(--surface-3)"}`,
        overflow: "hidden",
      }}
    >
      {/* Accent top */}
      <div
        style={{
          height: "2px",
          background: `linear-gradient(90deg, ${accent}, transparent)`,
        }}
      />

      <div className="p-4">
        <div className="flex items-start justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <span style={{ fontSize: "1.1rem" }}>{tree.icon}</span>
            <div>
              <p
                className="hud-label"
                style={{ color: "var(--text-muted)", fontSize: "9px" }}
              >
                SKILL TREE
              </p>
              <h3
                style={{
                  fontFamily: "var(--font-display)",
                  fontSize: "0.75rem",
                  fontWeight: 800,
                  letterSpacing: "0.05em",
                  textTransform: "uppercase",
                  color: "var(--text-primary)",
                }}
              >
                {tree.title}
              </h3>
            </div>
          </div>
          {tree.completed && (
            <span
              className="tier-badge"
              style={{
                background: `${accent}12`,
                color: accent,
                borderColor: `${accent}35`,
                flexShrink: 0,
              }}
            >
              ✓ {tree.specialty}
            </span>
          )}
        </div>

        {!tree.completed && (
          <p
            style={{
              fontFamily: "var(--font-body)",
              fontSize: "0.7rem",
              color: "var(--text-muted)",
              marginBottom: "0.75rem",
            }}
          >
            Obtén:{" "}
            <span style={{ fontWeight: 600, color: "var(--text-secondary)" }}>
              "{tree.specialty}"
            </span>
          </p>
        )}

        <div className="flex items-center justify-between mb-1.5">
          <span className="hud-label" style={{ color: "var(--text-muted)" }}>
            {tree.completedSteps}/{tree.totalSteps}
          </span>
          <span
            style={{
              fontFamily: "var(--font-display)",
              fontSize: "0.8rem",
              fontWeight: 700,
              color: accent,
            }}
          >
            {tree.percentComplete}%
          </span>
        </div>
        <HudProgress pct={tree.percentComplete} color={accent} thin />

        <button
          onClick={() => setExpanded(!expanded)}
          className="flex w-full items-center justify-between mt-3"
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "10px",
            letterSpacing: "0.08em",
            color: "var(--text-muted)",
            background: "none",
            border: "none",
            cursor: "pointer",
          }}
        >
          <span>Materias del árbol</span>
          {expanded ? (
            <ChevronUp className="h-3 w-3" />
          ) : (
            <ChevronDown className="h-3 w-3" />
          )}
        </button>

        {expanded && (
          <ol className="mt-2 space-y-1.5">
            {tree.steps.map((s, i) => (
              <li key={s.id} className="flex items-center gap-2">
                {s.completed ? (
                  <CheckCircle2
                    className="h-3.5 w-3.5 flex-shrink-0"
                    style={{ color: "var(--utb-savio)" }}
                  />
                ) : (
                  <Circle
                    className="h-3.5 w-3.5 flex-shrink-0"
                    style={{ color: "var(--surface-3)" }}
                  />
                )}
                <span
                  style={{
                    fontFamily: "var(--font-body)",
                    fontSize: "0.68rem",
                    color: s.completed
                      ? "var(--text-primary)"
                      : "var(--surface-4)",
                  }}
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

// ── Secret Quest Card ──────────────────────────────────────

function SecretQuestCard({ quest }: { quest: SecretQuest }) {
  const isPending = quest.id === "boss-fight";

  return (
    <div
      style={{
        position: "relative",
        clipPath: "var(--clip-corner-sm)",
        background: "var(--surface-1)",
        border: quest.completed
          ? "1px solid rgba(100,237,42,0.40)"
          : isPending
            ? "1px solid var(--surface-2)"
            : "1px solid var(--surface-3)",
        opacity: isPending ? 0.5 : 1,
        overflow: "hidden",
      }}
    >
      {quest.completed && (
        <div
          style={{
            height: "2px",
            background:
              "linear-gradient(90deg, var(--utb-emerald), transparent)",
          }}
        />
      )}

      <div className="p-4">
        <div className="flex items-start gap-3">
          <div
            style={{
              flexShrink: 0,
              width: "40px",
              height: "40px",
              clipPath: "var(--clip-corner-sm)",
              background: quest.completed
                ? "rgba(100,237,42,0.10)"
                : "var(--surface-2)",
              border: quest.completed
                ? "1px solid rgba(100,237,42,0.25)"
                : "1px solid var(--surface-3)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "1.1rem",
            }}
          >
            {isPending ? (
              <Lock className="h-4 w-4" style={{ color: "var(--surface-4)" }} />
            ) : (
              quest.icon
            )}
          </div>

          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <h3
                style={{
                  fontFamily: "var(--font-display)",
                  fontSize: "0.75rem",
                  fontWeight: 700,
                  letterSpacing: "0.06em",
                  textTransform: "uppercase",
                  color: quest.completed
                    ? "var(--text-primary)"
                    : "var(--text-secondary)",
                }}
              >
                {quest.completed || !isPending ? quest.title : "???"}
              </h3>
              {quest.completed && (
                <span
                  className="tier-badge"
                  style={{
                    background: "rgba(100,237,42,0.10)",
                    color: "var(--utb-emerald)",
                    borderColor: "rgba(100,237,42,0.30)",
                  }}
                >
                  COMPLETADO
                </span>
              )}
            </div>
            <p
              style={{
                fontFamily: "var(--font-body)",
                fontSize: "0.7rem",
                color: "var(--text-muted)",
                marginTop: "3px",
              }}
            >
              {isPending ? "Próximamente disponible" : quest.description}
            </p>

            {!isPending && quest.progress !== undefined && (
              <div className="mt-3">
                <div className="flex justify-between mb-1">
                  <span
                    className="hud-label"
                    style={{ color: "var(--text-muted)" }}
                  >
                    {quest.progressLabel}
                  </span>
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "10px",
                      fontWeight: 700,
                      color: "var(--text-secondary)",
                    }}
                  >
                    {quest.progress}%
                  </span>
                </div>
                <HudProgress
                  pct={quest.progress}
                  color={
                    quest.completed ? "var(--utb-emerald)" : "var(--utb-aqua)"
                  }
                  thin
                />
              </div>
            )}

            {!quest.completed && !isPending && (
              <p
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "9px",
                  letterSpacing: "0.08em",
                  color: "var(--surface-4)",
                  marginTop: "0.5rem",
                  fontStyle: "italic",
                }}
              >
                {quest.hint}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Title Badge ────────────────────────────────────────────

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

function TitleBadge({ title }: { title: string }) {
  const s = TITLE_STYLES[title] ?? {
    bg: "rgba(122,139,168,0.08)",
    color: "var(--text-muted)",
    border: "rgba(122,139,168,0.25)",
  };
  return (
    <span
      className="title-badge"
      style={{ background: s.bg, color: s.color, borderColor: s.border }}
    >
      <Shield className="h-2.5 w-2.5" />
      {title}
    </span>
  );
}

// ── Section divider ────────────────────────────────────────

function SectionDivider({ label }: { label: string }) {
  return (
    <div className="hud-divider my-1">
      <div
        className="hud-divider-line"
        style={{
          background: "linear-gradient(270deg, var(--utb-cyan), transparent)",
        }}
      />
      <span className="hud-divider-label">{label}</span>
      <div
        className="hud-divider-line"
        style={{
          background: "linear-gradient(90deg, var(--utb-cyan), transparent)",
        }}
      />
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────

export default function QuestsPage() {
  const { profile, loading, error } = useQuestProfile();

  if (error) {
    return (
      <div className="flex items-center justify-center py-20">
        <div
          style={{
            border: "1px solid rgba(220,38,38,0.35)",
            clipPath: "var(--clip-corner-sm)",
            padding: "1rem 1.5rem",
            background: "rgba(220,38,38,0.05)",
          }}
        >
          <p
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "11px",
              color: "#DC2626",
            }}
          >
            ERROR · {error}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
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
          Quests
        </h1>
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "10px",
            letterSpacing: "0.12em",
            color: "var(--text-muted)",
          }}
        >
          // academic · adventure
        </span>
      </div>

      {/* Titles strip */}
      <div className="hud-panel" style={{ padding: 0 }}>
        <div
          className="flex items-center gap-2 px-4 py-3"
          style={{ borderBottom: "1px solid var(--surface-3)" }}
        >
          <Zap
            className="h-3.5 w-3.5"
            style={{ color: "var(--utb-emerald)" }}
          />
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "9px",
              letterSpacing: "0.18em",
              textTransform: "uppercase",
              color: "var(--utb-emerald)",
            }}
          >
            Títulos Obtenidos
          </span>
        </div>
        <div className="p-4">
          {loading ? (
            <div className="flex flex-wrap gap-2">
              {[1, 2, 3].map((i) => (
                <HudSkeleton
                  key={i}
                  style={{ height: "24px", width: "100px" }}
                />
              ))}
            </div>
          ) : profile && profile.titles.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {profile.titles.map((t) => (
                <TitleBadge key={t} title={t} />
              ))}
            </div>
          ) : (
            <p className="hud-label" style={{ color: "var(--text-muted)" }}>
              Completa etapas de las quests para obtener títulos.
            </p>
          )}
        </div>
      </div>

      {/* Main Quests */}
      <section>
        <SectionDivider label="Main Quests" />
        <div className="mt-4">
          {loading ? (
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
              {[1, 2, 3].map((i) => (
                <HudSkeleton key={i} style={{ height: "200px" }} />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
              {profile?.mainQuests.map((q) => (
                <MainQuestCard key={q.id} quest={q} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Skill Trees */}
      <section>
        <SectionDivider label="Skill Trees" />
        <div className="mt-4">
          {loading ? (
            <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
              {[1, 2, 3].map((i) => (
                <HudSkeleton key={i} style={{ height: "140px" }} />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
              {profile?.skillTrees.map((tree) => (
                <SkillTreeCard key={tree.id} tree={tree} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Secret Quests */}
      <section>
        <SectionDivider label="Quests Secretas" />
        <div className="mt-4">
          {loading ? (
            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
              {[1, 2].map((i) => (
                <HudSkeleton key={i} style={{ height: "110px" }} />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
              {profile?.secretQuests.map((q) => (
                <SecretQuestCard key={q.id} quest={q} />
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
