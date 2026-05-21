"use client";

import { useState, useEffect } from "react";
import {
  computeQuestProfile,
  type QuestProfile,
  type Materia,
} from "../lib/questEngine";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("sps_token");
}

interface UseQuestProfileResult {
  profile: QuestProfile | null;
  loading: boolean;
  error: string | null;
}

export function useQuestProfile(): UseQuestProfileResult {
  const [profile, setProfile] = useState<QuestProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      const token = getToken();
      if (!token) {
        setError("No autenticado");
        setLoading(false);
        return;
      }

      try {
        // 1. Get current user ID
        const meRes = await fetch(`${API_URL}/estudiantes/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!meRes.ok) throw new Error("No se pudo obtener el usuario");
        const me = await meRes.json();

        // 2. Get all materias for this student
        const matRes = await fetch(
          `${API_URL}/estudiante-materia/${me.id_estudiante}`,
          { headers: { Authorization: `Bearer ${token}` } },
        );
        if (!matRes.ok) throw new Error("No se pudieron obtener las materias");
        const rawMaterias = await matRes.json();

        // 3. Get full materia info (names + credits) from malla
        // We need to enrich the EstudianteMateria records with nombre + creditos
        // The materia details come from /materias/{id}
        // To avoid N+1, get all from /materias/ and build a map
        const allMatRes = await fetch(`${API_URL}/materias/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!allMatRes.ok) throw new Error("No se pudo obtener el catálogo");
        const allMaterias: Array<{
          id_materia: string;
          nombre: string;
          creditos: number;
          id_categoria: string;
        }> = await allMatRes.json();

        const materiaMap = new Map(allMaterias.map((m) => [m.id_materia, m]));

        // 4. Merge: enrich each EstudianteMateria with nombre + creditos
        const materias: Materia[] = rawMaterias
          .map(
            (em: {
              id_materia: string;
              status: string;
              nota: number;
              semestre: string;
            }) => {
              const info = materiaMap.get(em.id_materia);
              if (!info) return null;
              return {
                id_materia: em.id_materia,
                nombre: info.nombre,
                creditos: info.creditos,
                status: em.status as Materia["status"],
                nota: em.nota,
              };
            },
          )
          .filter(Boolean) as Materia[];

        // 5. Run quest engine
        setProfile(computeQuestProfile(materias));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error desconocido");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return { profile, loading, error };
}
