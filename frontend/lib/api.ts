import type { 
  Estudiante, 
  EstudianteCarrera, 
  Progreso, 
  EstudianteLogro,
  JWTPayload 
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Decode JWT token payload (without verification)
export function decodeToken(token: string): JWTPayload | null {
  try {
    const base64Payload = token.split(".")[1];
    const payload = JSON.parse(atob(base64Payload));
    return payload as JWTPayload;
  } catch {
    return null;
  }
}

// Check if token is expired
export function isTokenExpired(token: string): boolean {
  const payload = decodeToken(token);
  if (!payload) return true;
  return Date.now() >= payload.exp * 1000;
}

// Get auth headers
function getAuthHeaders(): HeadersInit {
  const token = typeof window !== "undefined" ? localStorage.getItem("sps_token") : null;
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

// API Functions
export async function getEstudianteMe(): Promise<Estudiante> {
  const res = await fetch(`${API_URL}/estudiantes/me`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error("Error al obtener datos del estudiante");
  return res.json();
}

export async function getEstudianteCarreras(idEstudiante: string): Promise<EstudianteCarrera[]> {
  const res = await fetch(`${API_URL}/estudiante-carrera/${idEstudiante}`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error("Error al obtener carreras del estudiante");
  return res.json();
}

export async function getProgreso(idEstudiante: string, idCarrera: string): Promise<Progreso> {
  const res = await fetch(`${API_URL}/progreso/${idEstudiante}/${idCarrera}`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error("Error al obtener progreso");
  return res.json();
}

export async function getEstudianteLogros(idEstudiante: string): Promise<EstudianteLogro[]> {
  const res = await fetch(`${API_URL}/estudiante-logro/${idEstudiante}`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error("Error al obtener logros");
  return res.json();
}

// Logout
export function logout() {
  localStorage.removeItem("sps_token");
  window.location.href = "/";
}
