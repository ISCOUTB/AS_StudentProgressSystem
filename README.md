# AS_StudentProgressSystem

## Documentación inicial de arquitectura basada en arc42

---

## 1. Introducción y Metas

## 1.1 Vista de Requerimientos

La aplicación Student Progress System es una app de visualización gamificada que busca ofrecer al estudiante una mejor experiencia al momento de consultar su progreso académico. Para ello, presenta un dashboard de fácil lectura junto con un sistema de logros categóricos y seguimiento del progreso global.

Su objetivo es transformar la forma tradicional (poco cómoda y poco intuitiva) en la que actualmente los estudiantes de la Universidad Tecnológica visualizan su avance académico, brindando una interfaz más clara, dinámica y motivadora.

El sistema está diseñado para ser **multicarrera**, es decir, podrá manejar diferentes programas académicos (Ingeniería, Administración, etc.), cada uno con su propia estructura curricular.

### Requerimientos funcionales

- **RF1:** Mostrar la malla curricular completa de una carrera organizada por semestres.
- **RF2:** Permitir al estudiante visualizar las materias que ya ha cursado.
- **RF3:** El sistema debe contar con autenticación proporcionada por Microsoft authenticator
- **RF4:** Mostrar visualmente el progreso académico del estudiante (materias aprobadas vs pendientes).
- **RF5:** Permitir manejar múltiples carreras con diferentes mallas curriculares.
- **RF6:** Exponer una API REST para gestionar estudiantes, carreras y materias.
- **RF7:** La aplicación debe operar bajo el dominio unitecnológica
- **RF8:** Preparar la arquitectura para integración futura con sistemas académicos institucionales.  
### Requerimientos no funcionales

- **RNF1:** Arquitectura modular que facilite futuras extensiones.
- **RNF2:** Separación clara entre frontend y backend.
- **RNF3:** Despliegue reproducible mediante contenedores Docker.
- **RNF4:** Interfaz intuitiva para facilitar la visualización del progreso académico.
- **RNF5:** El sistema debe soportar alto tráfico de usuarios


# 1.2 Metas de Calidad

Las principales metas de calidad del sistema son:

### Identidad institucional
El sistema debe cumplir con los estándares de uso de imágenes y colores corporativos de la Universidad Tecnológica.

### Seguridad de la información

El sistema debe estar en capacidad de proteger y mantener seguros los datos de sus usuarios.

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

# 1.3 Stakeholder

| Stakeholder | Descripción | Expectativas |
|--------------|-------------|--------------|
| Profesor del curso | Evaluador del proyecto | Correcta aplicación de arquitectura de software |


## 2. Restricciones de la Arquitectura

- Uso obligatorio de Docker.
- Separación frontend / backend.
- Backend en Python con FastAPI.
- Frontend en Next.js.
- Proyecto académico con crecimiento incremental.
- Seguridad y autenticación.
- Una frase temprana de la aplicación solo será para plataformas web

---

## 3. Alcance y Contexto del Sistema

### Contexto de negocio

Dentro del entorno universitario, los estudiantes suelen consultar su progreso académico mediante sistemas institucionales complejos o poco visuales.

El sistema **AS_StudentProgressSystem** propone una herramienta visual que permita:

- Consultar la malla curricular.
- Identificar las materias ya aprobadas.
- Visualizar las materias pendientes.
- Comprender el avance académico por semestre.
- La obtención de logros
  



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
Mostrar la interfaz de usuario.

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
|--------|------------|
| Contenerización | Técnica que permite empaquetar una aplicación junto con todas sus dependencias dentro de un contenedor, garantizando que el software pueda ejecutarse de manera consistente en diferentes entornos. |
| Gamificación | Estrategia que consiste en aplicar elementos propios de los videojuegos, como logros, niveles o recompensas, en contextos no lúdicos con el objetivo de aumentar la motivación y la participación del usuario. |
| FastAPI | Framework de desarrollo web para Python que permite construir APIs REST de forma rápida, eficiente y con alto rendimiento. |
| Next.js | Framework de desarrollo web basado en React que permite crear aplicaciones web modernas con renderizado del lado del servidor y generación de páginas optimizadas. |
| PostgreSQL | Sistema de gestión de bases de datos relacional de código abierto utilizado para almacenar y administrar la información del sistema. |
| SAVIO | Plataforma académica utilizada por la Universidad Tecnológica de Bolívar. |
| Banner | Sistema de gestión académica utilizado por la Universidad Tecnológica de Bolívar para administrar procesos relacionados con estudiantes, matrículas, cursos y registros académicos. |
| Dashboard | Interfaz visual que muestra información relevante mediante gráficos, indicadores y métricas, facilitando la comprensión rápida del estado o progreso de un sistema. |

## prototipo
![8d79857c-2607-494b-af99-07a0e5f02ad3](https://github.com/user-attachments/assets/70954a0f-d9b6-4d25-a197-bb4726ede099)

