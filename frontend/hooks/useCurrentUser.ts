"use client";

import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// ── Raw API shapes ─────────────────────────────────────────────────────────────

export interface StudentData {
  id_estudiante: string;
  nombre: string;
  apellido: string;
  codigo: string;
  correo: string;
  status: string;
}

export interface EnrollmentData {
  id_estudiante: string;
  id_carrera: string;
  semestre: string;
  fecha_admision: string;
}

export interface ProgressData {
  id_estudiante: string;
  nombre_estudiante: string;
  id_carrera: string;
  nombre_carrera: string;
  total_materias: number;
  materias_aprobadas: number;
  materias_en_curso: number;
  materias_reprobadas: number;
  materias_pendientes: number;
  creditos_totales: number;
  creditos_aprobados: number;
  porcentaje_avance: number;
  materias: unknown[];
}

export interface CarreraData {
  id_carrera: string;
  nombre: string;
  codigo: string;
  escuela: string;
}

/** Raw row from GET /logros */
export interface LogroData {
  id_logro: string;
  nombre: string;
  descripcion: string;
  icon: string | null;
}

/** Raw row from GET /logro-materia */
export interface LogroMateriaData {
  id_logromateria: string;
  id_logro: string;
  id_materia: string | null;
}

/** Raw row from GET /estudiante-logro/{id} */
export interface EstudianteLogroData {
  id_estudiante: string;
  id_logromateria: string;
  /** "Logro obtenido" | "Logro sin obtener" */
  status: string;
}

/**
 * Fully resolved logro with its earned state.
 * Built by joining the three lists above.
 */
export interface ResolvedLogro {
  id_logro: string;
  id_logromateria: string;
  nombre: string;
  descripcion: string;
  icon: string | null;
  earned: boolean;
}

// ── Composed profile exposed by the hook ──────────────────────────────────────

export interface CurrentUserProfile {
  student: StudentData;
  enrollment: EnrollmentData | null;
  progress: ProgressData | null;
  carrera: CarreraData | null;
  /** All logros in the catalogue, each flagged as earned/not */
  logros: ResolvedLogro[];
  /** Subset of logros where earned === true */
  earnedLogros: ResolvedLogro[];
  displayName: string;
  fullName: string;
  semesterLabel: string | null;
  materiasAprobadas: number;
  totalMaterias: number;
}

// ── Semester label helpers ─────────────────────────────────────────────────────

const ORDINAL_MAP: Record<string, string> = {
  primero: "1",
  primer: "1",
  primera: "1",
  segundo: "2",
  segunda: "2",
  tercero: "3",
  tercer: "3",
  tercera: "3",
  cuarto: "4",
  cuarta: "4",
  quinto: "5",
  quinta: "5",
  sexto: "6",
  sexta: "6",
  séptimo: "7",
  septimo: "7",
  séptima: "7",
  septima: "7",
  octavo: "8",
  octava: "8",
  noveno: "9",
  novena: "9",
  décimo: "10",
  decimo: "10",
  décima: "10",
  decima: "10",
};

const SUFFIX: Record<string, string> = {
  "1": "er",
  "2": "do",
  "3": "er",
  "4": "to",
  "5": "to",
  "6": "to",
  "7": "mo",
  "8": "vo",
  "9": "no",
  "10": "mo",
};

function fromRoman(r: string): number {
  const vals: Record<string, number> = { I: 1, V: 5, X: 10, L: 50, C: 100 };
  let total = 0;
  for (let i = 0; i < r.length; i++) {
    const cur = vals[r[i]] ?? 0;
    const nxt = vals[r[i + 1]] ?? 0;
    total += cur < nxt ? -cur : cur;
  }
  return total;
}

export function parseSemesterLabel(
  semestre: string | null | undefined,
): string | null {
  if (!semestre) return null;
  const s = semestre.trim();

  const nivelRoman = s.match(/nivel\s+([IVXLCDM]+)/i);
  if (nivelRoman) {
    const n = fromRoman(nivelRoman[1].toUpperCase());
    if (n > 0) return `${n}${SUFFIX[String(n)] ?? "mo"} nivel`;
  }

  const nivelDigit = s.match(/nivel\s+(\d+)/i);
  if (nivelDigit) {
    const n = parseInt(nivelDigit[1], 10);
    return `${n}${SUFFIX[String(n)] ?? "mo"} nivel`;
  }

  if (/^\d+\w*\s+nivel$/i.test(s)) return s.toLowerCase();

  for (const w of s.toLowerCase().split(/\s+/)) {
    const digit = ORDINAL_MAP[w];
    if (digit) return `${digit}${SUFFIX[digit] ?? "mo"} nivel`;
  }

  const periodMatch = s.match(/(\w+)\s+periodo\s+(\d{4})/i);
  if (periodMatch) {
    const half = periodMatch[1].toLowerCase() === "primer" ? "1er" : "2do";
    return `${half} período ${periodMatch[2]}`;
  }

  if (/^\d+$/.test(s)) {
    const n = parseInt(s, 10);
    return `${n}${SUFFIX[String(n)] ?? "mo"} nivel`;
  }

  return null;
}

// ── Hook ──────────────────────────────────────────────────────────────────────

interface UseCurrentUserResult {
  profile: CurrentUserProfile | null;
  loading: boolean;
  error: string | null;
  /** Backward-compat aliases used by layout.tsx */
  user: StudentData | null;
  displayName: string | null;
}

export function useCurrentUser(): UseCurrentUserResult {
  const [profile, setProfile] = useState<CurrentUserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token =
      typeof window !== "undefined" ? localStorage.getItem("sps_token") : null;

    if (!token) {
      setLoading(false);
      return;
    }

    const headers = { Authorization: `Bearer ${token}` };

    // ── Step 1: authenticated student ──────────────────────────────────────
    fetch(`${API_URL}/estudiantes/me`, { headers })
      .then((r) => {
        if (!r.ok) throw new Error("Unauthorized");
        return r.json() as Promise<StudentData>;
      })
      .then(async (student) => {
        let enrollment: EnrollmentData | null = null;
        let progress: ProgressData | null = null;
        let carrera: CarreraData | null = null;

        // ── Step 2: enrollment (non-fatal) ─────────────────────────────────
        try {
          const res = await fetch(
            `${API_URL}/estudiante-carrera/${student.id_estudiante}`,
            { headers },
          );
          if (res.ok) {
            const list: EnrollmentData[] = await res.json();
            enrollment = list[0] ?? null;
          }
        } catch {
          /* non-fatal */
        }

        // ── Step 3: progress + carrera + logro catalogue in parallel ───────
        const [
          fetchedProgress,
          fetchedCarrera,
          allLogros,
          allLogrosMateria,
          estudianteLogros,
        ] = await Promise.all([
          // progress (needs enrollment)
          enrollment
            ? fetch(
                `${API_URL}/progreso/${student.id_estudiante}/${enrollment.id_carrera}`,
                { headers },
              )
                .then((r) =>
                  r.ok ? (r.json() as Promise<ProgressData>) : null,
                )
                .catch((): null => null)
            : Promise.resolve(null),

          // carrera details (needs enrollment)
          enrollment
            ? fetch(`${API_URL}/carreras/${enrollment.id_carrera}`, { headers })
                .then((r) => (r.ok ? (r.json() as Promise<CarreraData>) : null))
                .catch((): null => null)
            : Promise.resolve(null),

          // full logros catalogue
          fetch(`${API_URL}/logros`, { headers })
            .then((r) => (r.ok ? (r.json() as Promise<LogroData[]>) : []))
            .catch((): LogroData[] => []),

          // logromateria join table
          fetch(`${API_URL}/logro-materia`, { headers })
            .then((r) =>
              r.ok ? (r.json() as Promise<LogroMateriaData[]>) : [],
            )
            .catch((): LogroMateriaData[] => []),

          // student's earned logros
          fetch(`${API_URL}/estudiante-logro/${student.id_estudiante}`, {
            headers,
          })
            .then((r) =>
              r.ok ? (r.json() as Promise<EstudianteLogroData[]>) : [],
            )
            .catch((): EstudianteLogroData[] => []),
        ]);

        progress = fetchedProgress;
        carrera = fetchedCarrera;

        // ── Step 4: join logros ─────────────────────────────────────────────
        //
        // Index: logromateria_id → earned status
        const earnedSet = new Set<string>(
          (estudianteLogros ?? [])
            .filter((el) => el.status === "Logro obtenido")
            .map((el) => el.id_logromateria),
        );

        // Index: logro_id → first logromateria record for that logro
        const lmByLogro = new Map<string, LogroMateriaData>();
        for (const lm of allLogrosMateria ?? []) {
          if (!lmByLogro.has(lm.id_logro)) lmByLogro.set(lm.id_logro, lm);
        }

        const logros: ResolvedLogro[] = (allLogros ?? []).map((logro) => {
          const lm = lmByLogro.get(logro.id_logro);
          const earned = lm ? earnedSet.has(lm.id_logromateria) : false;
          return {
            id_logro: logro.id_logro,
            id_logromateria: lm?.id_logromateria ?? "",
            nombre: logro.nombre,
            descripcion: logro.descripcion,
            icon: logro.icon,
            earned,
          };
        });

        const earnedLogros = logros.filter((l) => l.earned);

        setProfile({
          student,
          enrollment,
          progress,
          carrera,
          logros,
          earnedLogros,
          displayName: student.correo.split("@")[0].toUpperCase(),
          fullName: `${student.nombre} ${student.apellido}`,
          semesterLabel: parseSemesterLabel(enrollment?.semestre ?? null),
          materiasAprobadas: progress?.materias_aprobadas ?? 0,
          totalMaterias: progress?.total_materias ?? 0,
        });
      })
      .catch((err) => setError((err as Error).message ?? "Error"))
      .finally(() => setLoading(false));
  }, []);

  return {
    profile,
    loading,
    error,
    user: profile?.student ?? null,
    displayName: profile?.displayName ?? null,
  };
}
