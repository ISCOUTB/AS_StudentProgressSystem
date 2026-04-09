from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum


# ─── Enums (espejo de los usados en los modelos) ─────────────────────────────
class StatusEstudianteSchema(str, Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    egresado = "Egresado"


# ─── Schema base (campos compartidos) ────────────────────────────────────────
class StudentBase(BaseModel):
    nombre: str
    apellido: str
    codigo: str
    correo: EmailStr
    status: StatusEstudianteSchema = StatusEstudianteSchema.activo


# ─── Schema de creación (recibe contraseña en texto plano) ───────────────────
class StudentCreate(StudentBase):
    password: str  # se hasheará antes de guardar


# ─── Schema de respuesta pública (sin datos sensibles) ───────────────────────
class StudentResponse(StudentBase):
    id_estudiante: UUID

    class Config:
        from_attributes = True  # compatible con SQLModel / ORM


# ─── Schema simplificado (mantiene compatibilidad con la ruta existente) ─────
class Student(BaseModel):
    """Schema ligero usado en /students para listados rápidos."""
    id: int
    name: str
    average: float

    class Config:
        from_attributes = True