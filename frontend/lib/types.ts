// Types for the Student Progress System API

export interface Estudiante {
  id_estudiante: string;
  nombre: string;
  apellido: string;
  codigo: string;
  correo: string;
  status: string;
}

export interface EstudianteCarrera {
  id_estudiante: string;
  id_carrera: string;
  semestre: string;
  fecha_admision: string;
}

export interface MateriaProgreso {
  id_materia: string;
  nombre: string;
  creditos: number;
  semestre: number;
  categoria: string;
  estado: "Aprobada" | "En curso" | "Reprobada" | "Pendiente";
  nota?: number;
}

export interface Progreso {
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
  materias: MateriaProgreso[];
}

export interface EstudianteLogro {
  id_estudiante: string;
  id_logromateria: string;
  status: string;
}

export interface Logro {
  id_logro: string;
  nombre: string;
  descripcion: string;
  tipo: string;
}

export interface Carrera {
  id_carrera: string;
  nombre: string;
  codigo: string;
}

// JWT Token payload
export interface JWTPayload {
  sub: string; // email
  id: string;  // id_estudiante
  exp: number;
}
