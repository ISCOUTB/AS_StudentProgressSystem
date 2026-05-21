// ─────────────────────────────────────────────────────────────────────────────
// Quest Engine
// All UUIDs match seed.py UUID_MAT constants exactly.
// ─────────────────────────────────────────────────────────────────────────────

export interface Materia {
  id_materia: string;
  nombre: string;
  creditos: number;
  status: "Aprobada" | "Reprobada" | "En Curso";
  nota?: number;
}

export interface QuestStep {
  id: string;
  label: string;
  description: string;
  completed: boolean;
}

export interface Quest {
  id: string;
  title: string;
  subtitle: string;
  color: string; // tailwind bg class
  accentColor: string; // tailwind text/border class
  icon: string; // emoji
  steps: QuestStep[];
  completedSteps: number;
  totalSteps: number;
  percentComplete: number;
  rewardTitle?: string; // título otorgado al completar
  completed: boolean;
}

export interface SkillTree {
  id: string;
  title: string;
  specialty: string; // reward title
  color: string;
  icon: string;
  steps: QuestStep[];
  completedSteps: number;
  totalSteps: number;
  percentComplete: number;
  completed: boolean;
}

export interface SecretQuest {
  id: string;
  title: string;
  description: string;
  icon: string;
  hint: string;
  completed: boolean;
  progress?: number; // 0-100 optional visual progress
  progressLabel?: string;
}

export interface QuestProfile {
  mainQuests: Quest[];
  skillTrees: SkillTree[];
  secretQuests: SecretQuest[];
  titles: string[]; // all earned titles, no hierarchy
  creditosAprobados: number;
  materiasAprobadasCount: number;
}

// ─── UUID maps (match seed.py UUID_MAT exactly) ───────────────────────────────

const MAT: Record<string, string> = {
  // Nivel I
  C01A: "30000000-0000-0000-0000-000000000006",
  C02A: "30000000-0000-0000-0000-000000000007", // Fundamentos de Programación
  // Nivel II
  C03A: "30000000-0000-0000-0000-000000000012", // Programación
  F01A: "30000000-0000-0000-0000-000000000009", // Física Mecánica
  M03A: "30000000-0000-0000-0000-000000000010",
  M04A: "30000000-0000-0000-0000-000000000011",
  // Nivel III
  C04A: "30000000-0000-0000-0000-000000000017", // POO
  F02A: "30000000-0000-0000-0000-000000000015", // Física E&M
  M05A: "30000000-0000-0000-0000-000000000016", // Cálculo Vectorial
  // Nivel IV
  C05A: "30000000-0000-0000-0000-000000000021", // Estructura de Datos
  F03A: "30000000-0000-0000-0000-000000000019", // Física Calor y Ondas
  // Nivel V
  A01A: "30000000-0000-0000-0000-000000000026", // Base de Datos
  A02A: "30000000-0000-0000-0000-000000000027",
  A03A: "30000000-0000-0000-0000-000000000028", // Algoritmos y Complejidad
  // Nivel VI
  A04A: "30000000-0000-0000-0000-000000000032", // Arquitectura de Software
  C07A: "30000000-0000-0000-0000-000000000033",
  C08A: "30000000-0000-0000-0000-000000000034", // Comunicaciones y Redes
  E02A: "30000000-0000-0000-0000-000000000030", // Estadística Inferencial
  // Nivel VII
  A05A: "30000000-0000-0000-0000-000000000037", // Ingeniería de Software
  C09A: "30000000-0000-0000-0000-000000000038", // Arquitectura del Computador
  C10A: "30000000-0000-0000-0000-000000000039", // Sistemas y Modelos
  // Nivel VIII
  A06A: "30000000-0000-0000-0000-000000000042", // Inteligencia Artificial
  A07A: "30000000-0000-0000-0000-000000000043", // Infraestructura para TI
  C11A: "30000000-0000-0000-0000-000000000044", // Sistemas Operativos
  // Nivel IX
  A08A: "30000000-0000-0000-0000-000000000049",
  C12A: "30000000-0000-0000-0000-000000000050",
  // Nivel X
  P01A: "30000000-0000-0000-0000-000000000046", // Proyecto I
  P02A: "30000000-0000-0000-0000-000000000052", // Proyecto II
  P03A: "30000000-0000-0000-0000-000000000055", // Práctica
  // Stats
  E01A: "30000000-0000-0000-0000-000000000025", // Estadística y Probabilidad
  // CBAS set (all 11 basic science subjects)
  H01A: "30000000-0000-0000-0000-000000000001",
  M01A: "30000000-0000-0000-0000-000000000002",
  M02A: "30000000-0000-0000-0000-000000000003",
  Q01A: "30000000-0000-0000-0000-000000000004",
  M06A: "30000000-0000-0000-0000-000000000020",
};

// All 11 CBAS UUIDs
const CBAS_IDS = new Set([
  MAT.M01A,
  MAT.M02A,
  MAT.Q01A,
  MAT.F01A,
  MAT.M03A,
  MAT.M04A,
  MAT.F02A,
  MAT.M05A,
  MAT.F03A,
  MAT.M06A,
  MAT.E01A,
]);

const FISICAS = [MAT.F01A, MAT.F02A, MAT.F03A];

// Nivel I materias (7)
const NIVEL_I_IDS = new Set([
  MAT.H01A,
  "30000000-0000-0000-0000-000000000002", // M01A
  "30000000-0000-0000-0000-000000000003", // M02A
  "30000000-0000-0000-0000-000000000004", // Q01A
  "30000000-0000-0000-0000-000000000005", // U01A
  MAT.C01A,
  MAT.C02A,
]);

// ─── Helpers ──────────────────────────────────────────────────────────────────

function approved(materias: Materia[], uuid: string): boolean {
  return materias.some((m) => m.id_materia === uuid && m.status === "Aprobada");
}

function countApproved(materias: Materia[]): number {
  return materias.filter((m) => m.status === "Aprobada").length;
}

function totalCredits(materias: Materia[]): number {
  return materias
    .filter((m) => m.status === "Aprobada")
    .reduce((sum, m) => sum + m.creditos, 0);
}

function step(
  id: string,
  label: string,
  description: string,
  completed: boolean,
): QuestStep {
  return { id, label, description, completed };
}

function questMeta(steps: QuestStep[]) {
  const completedSteps = steps.filter((s) => s.completed).length;
  const totalSteps = steps.length;
  const percentComplete =
    totalSteps > 0 ? Math.round((completedSteps / totalSteps) * 100) : 0;
  const completed = completedSteps === totalSteps;
  return { completedSteps, totalSteps, percentComplete, completed };
}

// ─── MAIN QUESTS ─────────────────────────────────────────────────────────────

function buildCaminoProgramador(materias: Materia[]): Quest {
  const steps: QuestStep[] = [
    step(
      "C02A",
      "Fundamentos de Programación",
      "Tu primer encuentro con el código. Todo comienza aquí.",
      approved(materias, MAT.C02A),
    ),
    step(
      "C03A",
      "Programación",
      "Consolida las bases. El código empieza a tomar forma.",
      approved(materias, MAT.C03A),
    ),
    step(
      "C04A",
      "Programación Orientada a Objetos",
      "Piensa en objetos. El mundo real en código.",
      approved(materias, MAT.C04A),
    ),
    step(
      "C05A",
      "Estructura de Datos",
      "Domina cómo se organiza la información.",
      approved(materias, MAT.C05A),
    ),
    step(
      "A03A",
      "Algoritmos y Complejidad",
      "El arte de resolver problemas eficientemente.",
      approved(materias, MAT.A03A),
    ),
  ];

  // Title earned based on progress
  const completedCount = steps.filter((s) => s.completed).length;
  let rewardTitle: string | undefined;
  if (completedCount >= 5) rewardTitle = "Arquitecto del Código";
  else if (completedCount >= 3) rewardTitle = "Desarrollador";
  else if (completedCount >= 1) rewardTitle = "Aprendiz";

  return {
    id: "camino-programador",
    title: "Camino del Programador",
    subtitle: "Domina el arte de escribir código",
    color: "bg-emerald-500",
    accentColor: "text-emerald-400",
    icon: "🟢",
    steps,
    rewardTitle,
    ...questMeta(steps),
  };
}

function buildRutaCientifica(materias: Materia[]): Quest {
  const cbas = materias.filter(
    (m) => CBAS_IDS.has(m.id_materia) && m.status === "Aprobada",
  );
  const cbas3 = cbas.length >= 3;
  const todasFisicas = FISICAS.every((id) => approved(materias, id));
  const calcVectorial = approved(materias, MAT.M05A);
  const todasCBAS = cbas.length >= 11;

  const steps: QuestStep[] = [
    step(
      "cbas-3",
      "3 materias de Ciencias Básicas",
      `Aprobadas: ${cbas.length}/3. Da tus primeros pasos científicos.`,
      cbas3,
    ),
    step(
      "fisicas",
      "Las 3 Físicas",
      "Mecánica, Electricidad y Calor. La trinidad física.",
      todasFisicas,
    ),
    step(
      "M05A",
      "Cálculo Vectorial",
      "El lenguaje del universo en múltiples dimensiones.",
      calcVectorial,
    ),
    step(
      "cbas-all",
      "Completar todas las CBAS",
      `${cbas.length}/11 materias científicas. La formación completa.`,
      todasCBAS,
    ),
  ];

  return {
    id: "ruta-cientifica",
    title: "Ruta Científica",
    subtitle: "Construye tu base en ciencias exactas",
    color: "bg-blue-500",
    accentColor: "text-blue-400",
    icon: "🔵",
    steps,
    rewardTitle: todasCBAS ? "Científico Formado" : undefined,
    ...questMeta(steps),
  };
}

function buildSagaIngeniero(materias: Materia[]): Quest {
  const creditos = totalCredits(materias);
  const totalAprobadas = countApproved(materias);

  const nivel1Done = Array.from(NIVEL_I_IDS).every((id) =>
    approved(materias, id),
  );

  const steps: QuestStep[] = [
    step(
      "nivel1",
      "Nivel I Completado",
      "Siete materias. El comienzo de la saga.",
      nivel1Done,
    ),
    step(
      "mitad",
      "Mitad del Camino",
      `${creditos}/81 créditos. La mitad de la historia.`,
      creditos >= 81,
    ),
    step(
      "A04A",
      "Arquitectura Dominada",
      "Aprueba Arquitectura de Software.",
      approved(materias, MAT.A04A),
    ),
    step(
      "P01A",
      "Proyecto I Iniciado",
      "La primera gran creación.",
      approved(materias, MAT.P01A),
    ),
    step(
      "P02A",
      "Proyecto II Finalizado",
      "La obra se completa.",
      approved(materias, MAT.P02A),
    ),
    step(
      "P03A",
      "Práctica Profesional",
      "El mundo real te espera.",
      approved(materias, MAT.P03A),
    ),
    step(
      "graduando",
      "Graduando",
      `${totalAprobadas}/55 materias. El final del camino.`,
      totalAprobadas >= 55,
    ),
  ];

  return {
    id: "saga-ingeniero",
    title: "Saga del Ingeniero",
    subtitle: "La gran aventura que dura toda la carrera",
    color: "bg-purple-600",
    accentColor: "text-purple-400",
    icon: "🟣",
    steps,
    rewardTitle: totalAprobadas >= 55 ? "Ingeniero de Sistemas" : undefined,
    ...questMeta(steps),
  };
}

// ─── SKILL TREES ─────────────────────────────────────────────────────────────

function buildSkillTree(
  id: string,
  title: string,
  specialty: string,
  color: string,
  icon: string,
  stepDefs: Array<{ key: string; uuid: string; label: string; desc: string }>,
  materias: Materia[],
): SkillTree {
  const steps = stepDefs.map((s) =>
    step(s.key, s.label, s.desc, approved(materias, s.uuid)),
  );
  return { id, title, specialty, color, icon, steps, ...questMeta(steps) };
}

function buildNetworkSpecialist(materias: Materia[]): SkillTree {
  return buildSkillTree(
    "network",
    "Árbol de Redes",
    "Network Specialist",
    "bg-cyan-500",
    "🌐",
    [
      {
        key: "C08A",
        uuid: MAT.C08A,
        label: "Comunicaciones y Redes",
        desc: "Los cimientos de la conectividad.",
      },
      {
        key: "A07A",
        uuid: MAT.A07A,
        label: "Infraestructura para TI",
        desc: "Construye la infraestructura que soporta todo.",
      },
      {
        key: "C11A",
        uuid: MAT.C11A,
        label: "Sistemas Operativos",
        desc: "El cerebro de la máquina.",
      },
    ],
    materias,
  );
}

function buildAiInitiate(materias: Materia[]): SkillTree {
  return buildSkillTree(
    "ai",
    "Árbol de IA",
    "AI Initiate",
    "bg-violet-500",
    "🤖",
    [
      {
        key: "E01A",
        uuid: MAT.E01A,
        label: "Estadística y Probabilidad",
        desc: "El lenguaje matemático de la incertidumbre.",
      },
      {
        key: "E02A",
        uuid: MAT.E02A,
        label: "Estadística Inferencial",
        desc: "Deduce el todo a partir de la parte.",
      },
      {
        key: "A06A",
        uuid: MAT.A06A,
        label: "Inteligencia Artificial",
        desc: "Máquinas que aprenden. El futuro.",
      },
      {
        key: "C10A",
        uuid: MAT.C10A,
        label: "Sistemas y Modelos",
        desc: "Modela la realidad computacionalmente.",
      },
    ],
    materias,
  );
}

function buildBackendEngineer(materias: Materia[]): SkillTree {
  return buildSkillTree(
    "backend",
    "Backend Path",
    "Backend Engineer",
    "bg-orange-500",
    "🛠️",
    [
      {
        key: "A01A",
        uuid: MAT.A01A,
        label: "Base de Datos",
        desc: "Donde vive toda la información.",
      },
      {
        key: "A04A",
        uuid: MAT.A04A,
        label: "Arquitectura de Software",
        desc: "El arte de diseñar sistemas que escalan.",
      },
      {
        key: "A05A",
        uuid: MAT.A05A,
        label: "Ingeniería de Software",
        desc: "Construye software de calidad profesional.",
      },
    ],
    materias,
  );
}

// ─── SECRET QUESTS ───────────────────────────────────────────────────────────

function buildSecretQuests(materias: Materia[]): SecretQuest[] {
  // Perfeccionista: any 5 approved materias with nota >= 4.5
  const highGrades = materias.filter(
    (m) => m.status === "Aprobada" && (m.nota ?? 0) >= 4.5,
  );
  const perfProgress = Math.min(highGrades.length, 5);
  const perfCompleted = highGrades.length >= 5;

  return [
    {
      id: "perfeccionista",
      title: "Perfeccionista",
      description: "Aprueba 5 materias con nota mayor o igual a 4.5",
      icon: "🧩",
      hint: "La excelencia no es un accidente.",
      completed: perfCompleted,
      progress: Math.round((perfProgress / 5) * 100),
      progressLabel: `${perfProgress}/5 materias con ≥4.5`,
    },
    {
      id: "boss-fight",
      title: "Boss Fight",
      description: "Aprueba una materia con alto índice de pérdida",
      icon: "💀",
      hint: "Algunos jefes son más difíciles que otros. ¿Te atreves?",
      completed: false, // needs tasa_perdida field — pending backend
      progress: 0,
      progressLabel: "Próximamente disponible",
    },
  ];
}

// ─── TITLES ───────────────────────────────────────────────────────────────────

function computeTitles(mainQuests: Quest[], skillTrees: SkillTree[]): string[] {
  const titles: string[] = [];

  // From Camino del Programador — all intermediate titles earned
  const prog = mainQuests.find((q) => q.id === "camino-programador");
  if (prog) {
    const done = prog.steps.filter((s) => s.completed).length;
    if (done >= 1) titles.push("Aprendiz");
    if (done >= 3) titles.push("Desarrollador");
    if (done >= 5) titles.push("Arquitecto del Código");
  }

  // From Ruta Científica
  const cient = mainQuests.find((q) => q.id === "ruta-cientifica");
  if (cient?.completed) titles.push("Científico Formado");

  // From Saga del Ingeniero
  const saga = mainQuests.find((q) => q.id === "saga-ingeniero");
  if (saga?.completed) titles.push("Ingeniero de Sistemas");

  // From Skill Trees
  skillTrees.forEach((tree) => {
    if (tree.completed) titles.push(tree.specialty);
  });

  return titles;
}

// ─── PUBLIC ENTRY POINT ──────────────────────────────────────────────────────

export function computeQuestProfile(materias: Materia[]): QuestProfile {
  const mainQuests = [
    buildCaminoProgramador(materias),
    buildRutaCientifica(materias),
    buildSagaIngeniero(materias),
  ];

  const skillTrees = [
    buildNetworkSpecialist(materias),
    buildAiInitiate(materias),
    buildBackendEngineer(materias),
  ];

  const secretQuests = buildSecretQuests(materias);
  const titles = computeTitles(mainQuests, skillTrees);

  return {
    mainQuests,
    skillTrees,
    secretQuests,
    titles,
    creditosAprobados: totalCredits(materias),
    materiasAprobadasCount: countApproved(materias),
  };
}
