# AS_StudentProgressSystem

## Documentación inicial de arquitectura basada en arc42

---

## 1. Introducción y Metas

### 1.1 Vista de Requerimientos

El sistema **AS_StudentProgressSystem** tiene como objetivo permitir la gestión y visualización del progreso académico de estudiantes.

#### Requerimientos funcionales iniciales

- RF1: Exponer una API REST para gestión de estudiantes.
- RF2: Permitir comunicación entre frontend y backend.
- RF3: Preparar la estructura para autenticación futura.
- RF4: Contenerizar el sistema con Docker.

#### Requerimientos no funcionales

- RNF1: Arquitectura modular y escalable.
- RNF2: Separación clara entre frontend y backend.
- RNF3: Despliegue reproducible mediante contenedores.

---

### 1.2 Metas de Calidad

En esta fase inicial las metas principales son:

- Modularidad  
- Escalabilidad  
- Mantenibilidad  
- Portabilidad  

---

### 1.3 Stakeholders

| Rol | Expectativa |
|------|------------|
| Estudiante | Visualizar su progreso académico |
| Docente | Consultar información de estudiantes |
| Equipo de Desarrollo | Construir una arquitectura limpia y escalable |
| Profesor del curso | Evaluar aplicación correcta de principios arquitectónicos |

---

## 2. Restricciones de la Arquitectura

- Uso obligatorio de Docker.
- Separación frontend / backend.
- Backend en Python con FastAPI.
- Frontend en Next.js.
- Proyecto académico con crecimiento incremental.

---

## 3. Alcance y Contexto del Sistema

### 3.1 Contexto de Negocio

El sistema permitirá gestionar y consultar información académica dentro de un entorno universitario.

Flujo general:
Usuario → Frontend → Backend API → (Base de datos futura)

En esta fase aún no se implementa base de datos.

---

### 3.2 Contexto Técnico

Arquitectura técnica inicial:

- Frontend: Next.js
- Backend: FastAPI
- Contenedores: Docker
- Comunicación: HTTP REST (JSON)

Interacción:
Frontend → HTTP → Backend


---

## 4. Estrategia de Solución

Se adopta una arquitectura cliente-servidor con separación clara de responsabilidades:

- El **Frontend** gestiona la interfaz de usuario.
- El **Backend** expone la API REST y contendrá la lógica de negocio.
- Docker asegura portabilidad y consistencia del entorno.

La arquitectura está preparada para evolucionar hacia:

- Integración de base de datos relacional.
- Implementación de autenticación.
- Escalamiento futuro.

---

## 5. Vista de Bloques

### 5.1 Sistema General

Bloques principales:

- Frontend
- Backend

Comunicación mediante API REST sobre HTTP.

---

### Frontend

**Propósito:**  
Mostrar la interfaz de usuario y consumir la API.

**Ubicación:**  
`/frontend`

**Interfaz:**  
HTTP REST hacia el backend.

---

### Backend

**Propósito:**  
Exponer API REST y manejar lógica de negocio futura.

**Ubicación:**  
`/backend/app`

**Interfaz:**  
Endpoints REST (FastAPI).

---

## 6. Vista de Ejecución

### Escenario: Consulta básica

1. Usuario accede desde navegador.
2. Frontend carga interfaz.
3. Frontend realiza petición HTTP al backend.
4. Backend responde en formato JSON.
5. Frontend renderiza la información.

---

## 7. Vista de Despliegue

Infraestructura inicial:

- Contenedor Docker para Frontend.
- Contenedor Docker para Backend.

Mapeo:

- Frontend → Contenedor Node.
- Backend → Contenedor Python.

Motivación:  
Permitir despliegue uniforme y reproducible.

---

## 8. Conceptos Transversales

### Contenerización

Uso de Docker para garantizar consistencia entre entornos de desarrollo y despliegue.

### Separación de Responsabilidades

Frontend y backend desacoplados para facilitar mantenimiento y escalabilidad.

---

## 9. Decisiones de Diseño

- Uso de FastAPI por simplicidad y rendimiento.
- Uso de Next.js como framework frontend moderno.
- Uso de Docker desde la fase inicial.
- Arquitectura monolítica modular (evolutiva).

---

## 10. Requerimientos de Calidad

Prioridad actual:

- Mantenibilidad
- Escalabilidad
- Portabilidad
- Rendimiento

---

## 11. Riesgos y Deuda Técnica

- No hay base de datos implementada.
- No existe autenticación.
- No hay pruebas automatizadas.
- No existe integración continua (CI/CD).

---

## 12. Glosario

| Término | Definición |
|----------|------------|
| API REST | Interfaz HTTP para comunicación entre sistemas |
| Contenedor | Entorno aislado de ejecución (Docker) |
| FastAPI | Framework backend en Python |
| Next.js | Framework frontend basado en React |




