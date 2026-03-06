# AS_StudentProgressSystem

## Documentación inicial de arquitectura basada en arc42

---

## 1. Introducción y Metas

## 1.1 Vista de Requerimientos

El sistema **AS_StudentProgressSystem** tiene como propósito permitir a los estudiantes **visualizar y gestionar su progreso académico a lo largo de su carrera universitaria**.

El sistema representará la **malla curricular por semestres**, permitiendo marcar visualmente las asignaturas que el estudiante ya ha cursado y aprobado. Esto facilita que el estudiante comprenda su avance académico y planifique los semestres futuros.

El sistema está diseñado para ser **multicarrera**, es decir, podrá manejar diferentes programas académicos (Ingeniería, Administración, Medicina, etc.), cada uno con su propia estructura curricular.

### Requerimientos funcionales

- **RF1:** Mostrar la malla curricular completa de una carrera organizada por semestres.
- **RF2:** Permitir al estudiante visualizar las materias que ya ha cursado.
- **RF3:** Permitir marcar materias como completadas.
- **RF4:** Mostrar visualmente el progreso académico del estudiante (materias aprobadas vs pendientes).
- **RF5:** Permitir manejar múltiples carreras con diferentes mallas curriculares.
- **RF6:** Exponer una API REST para gestionar estudiantes, carreras y materias.
- **RF7:** Permitir la comunicación entre frontend y backend mediante HTTP.
- **RF8:** Preparar la arquitectura para integración futura con sistemas académicos institucionales.
### Requerimientos no funcionales

- **RNF1:** Arquitectura modular que facilite futuras extensiones.
- **RNF2:** Separación clara entre frontend y backend.
- **RNF3:** Despliegue reproducible mediante contenedores Docker.
- **RNF4:** Interfaz intuitiva para facilitar la visualización del progreso académico.
- **RNF5:** Capacidad de escalar para soportar múltiples carreras y estudiantes.


# 1.2 Metas de Calidad

Las principales metas de calidad del sistema son:

### Modularidad

Permitir que los diferentes componentes del sistema puedan evolucionar de forma independiente.

### Escalabilidad

La arquitectura debe permitir soportar un crecimiento en el número de estudiantes y carreras registradas.

### Mantenibilidad

El sistema debe ser fácil de mantener y modificar por futuros equipos de desarrollo.

### Portabilidad

El sistema debe poder desplegarse en distintos entornos gracias al uso de contenedores Docker.

### Usabilidad

El sistema debe presentar la información académica de forma clara y comprensible para los estudiantes.

---
---

# 1.3 Stakeholders

| Stakeholder | Descripción | Expectativas |
|--------------|-------------|--------------|
| Estudiantes | Usuarios principales del sistema | Visualizar su avance académico y planificar sus materias |
| Docentes | Pueden consultar progreso de estudiantes | Acceso a información académica organizada |
| Equipo de Desarrollo | Responsables del desarrollo y mantenimiento | Arquitectura clara y extensible |
| Profesor del curso | Evaluador del proyecto | Correcta aplicación de arquitectura de software |


## 2. Restricciones de la Arquitectura

- Uso obligatorio de Docker.
- Separación frontend / backend.
- Backend en Python con FastAPI.
- Frontend en Next.js.
- Proyecto académico con crecimiento incremental.

---

## 3. Alcance y Contexto del Sistema

Dentro del entorno universitario, los estudiantes suelen consultar su progreso académico mediante sistemas institucionales complejos o poco visuales.

El sistema **AS_StudentProgressSystem** propone una herramienta visual que permita:

- Consultar la malla curricular.
- Identificar las materias ya aprobadas.
- Visualizar las materias pendientes.
- Comprender el avance académico por semestre.


### Flujo de interacción

1. El estudiante accede al sistema mediante el navegador.
2. El sistema muestra la malla curricular correspondiente a su carrera.
3. El estudiante puede visualizar las materias aprobadas.
4. El sistema muestra gráficamente el progreso académico.

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




