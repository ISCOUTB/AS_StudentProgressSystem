# AS_StudentProgressSystem

## Documentación inicial de arquitectura basada en arc42

---

# AS_StudentProgressSystem

## Introducción y Metas

Vista de Requerimientos

El sistema AS_StudentProgressSystem es una aplicación web diseñada para
permitir a los estudiantes visualizar y comprender de manera clara su progreso
académico dentro de un programa universitario.

Actualmente, los estudiantes suelen consultar su avance académico mediante
sistemas institucionales que presentan la información de forma poco intuitiva
o difícil de interpretar. En este contexto, el sistema propone una alternativa
que facilite la comprensión del estado académico del estudiante mediante representaciones visuales de la malla curricular, indicadores de progreso y elementos
de visualización que permitan identificar rápidamente las materias aprobadas,
pendientes y el avance general dentro del plan de estudios.

El sistema está orientado principalmente a los estudiantes de la Universidad Tecnológica de Bolívar y está diseñado para soportar múltiples programas académicos,
permitiendo representar diferentes mallas curriculares asociadas a cada carrera.

Adicionalmente, el sistema incorpora elementos de visualización y seguimiento
del progreso académico que buscan mejorar la experiencia del usuario al momento
de consultar su avance dentro del programa de estudios.

## Requerimientos funcionales

• RF1: El sistema debe permitir visualizar la malla curricular completa de
una carrera organizada por semestres.

• RF2: El sistema debe permitir al estudiante identificar las materias que
ya han sido cursadas o aprobadas.

• RF3: El sistema debe permitir marcar o registrar materias como completadas.

• RF4: El sistema debe calcular y mostrar el progreso académico del estudiante en función de las materias aprobadas.

• RF5: El sistema debe permitir gestionar múltiples carreras universitarias,
cada una con su propia estructura curricular.

• RF6: El sistema debe mostrar gráficamente el avance académico mediante
indicadores visuales o dashboards.

• RF7: El sistema debe permitir visualizar materias pendientes dentro del
plan de estudios.

• RF8: El sistema debe permitir mostrar logros o indicadores de avance
asociados al progreso académico del estudiante.

• RF9: El sistema debe permitir asociar un estudiante con una carrera
específica para determinar su plan de estudios.

## Requerimientos no funcionales

• RNF1: El sistema debe proporcionar una interfaz web intuitiva que permita
a los estudiantes comprender su progreso académico de manera clara.

• RNF2: El sistema debe garantizar la seguridad de la información de los
usuarios mediante mecanismos de autenticación y control de acceso.

• RNF3: El sistema debe soportar al menos 100 usuarios concurrentes sin
degradación significativa del rendimiento.

• RNF4: El sistema debe poder desplegarse en diferentes entornos mediante
el uso de contenedores Docker.

• RNF5: La arquitectura del sistema debe permitir su evolución para soportar
nuevas carreras o funcionalidades adicionales.

• RNF6: El sistema debe cumplir con los lineamientos de identidad visual
institucional de la Universidad Tecnológica de Bolívar.

## Metas de Calidad

Las metas de calidad del sistema definen las propiedades no funcionales más
relevantes que deben ser consideradas durante el diseño de la arquitectura.

| Meta de Calidad          | Descripción                                                                 | Prioridad |
|--------------------------|-----------------------------------------------------------------------------|-----------|
| Usabilidad               | El sistema debe presentar la información académica de forma clara e intuitiva para facilitar la comprensión del progreso académico del estudiante. | Alta |
| Mantenibilidad           | La arquitectura debe permitir realizar modificaciones o extensiones del sistema con bajo esfuerzo. | Alta |
| Escalabilidad            | El sistema debe poder soportar un incremento en el número de usuarios o programas académicos sin afectar significativamente su rendimiento. | Media |
| Portabilidad             | El sistema debe poder desplegarse en diferentes entornos utilizando contenedores Docker. | Media |
| Seguridad                | El sistema debe proteger la información de los usuarios mediante mecanismos de autenticación y control de acceso. | Alta |
| Identidad institucional  | La interfaz del sistema debe respetar los lineamientos visuales institucionales de la Universidad Tecnológica de Bolívar. | Alta |

## Partes interesadas (Stakeholders)

| Stakeholder                                      | Expectativas |
|--------------------------------------------------|--------------|
| Estudiantes de la Universidad Tecnológica de Bolívar | Poder visualizar de forma clara su progreso académico, identificar materias aprobadas y pendientes, y planificar su trayectoria académica. |
| Universidad Tecnológica de Bolívar               | Contar con herramientas tecnológicas que mejoren la visualización del progreso académico y que puedan integrarse con sistemas institucionales existentes. |
| Profesor del curso (Jairo Enrique Serrano Castañeda) | Evaluar la correcta aplicación de principios y buenas prácticas de arquitectura de software. |

## Restricciones de la Arquitectura

### Restricciones Técnicas

El sistema debe cumplir con las siguientes restricciones tecnológicas:

• El backend del sistema debe desarrollarse utilizando el framework FastAPI
basado en Python.

• El frontend debe implementarse utilizando el framework Next.js.

• La comunicación entre frontend y backend debe realizarse mediante API
REST utilizando el protocolo HTTP y formato de datos JSON.

• El sistema debe utilizar contenedores Docker para garantizar consistencia en los entornos de desarrollo y despliegue.

### Restricciones de Plataforma

• La primera versión del sistema estará orientada exclusivamente a plataformas web.

• El sistema debe operar bajo el dominio institucional unitecnologica.edu.co.

• La arquitectura debe permitir una futura integración con sistemas académicos institucionales.

## Alcance y Contexto del Sistema

### Contexto de Negocio

Dentro del entorno universitario, los estudiantes consultan su progreso académico
mediante sistemas institucionales que generalmente presentan la información de
forma poco visual. Esto puede dificultar la comprensión del avance dentro del
plan de estudios.

El sistema AS_StudentProgressSystem propone una herramienta que facilite
la visualización del progreso académico mediante una representación gráfica de
la malla curricular y del estado de cada asignatura.

A través del sistema, los estudiantes podrán:

• Consultar la malla curricular correspondiente a su programa académico.

• Identificar las materias que ya han sido aprobadas.

• Visualizar las materias que aún se encuentran pendientes.

• Comprender el progreso académico dentro de su carrera.

• Visualizar indicadores de avance académico dentro del plan de estudios.

El sistema está orientado principalmente a estudiantes de la Universidad Tecnológica de Bolívar y busca mejorar la experiencia de consulta del progreso
académico.

### Flujo de Interacción

El flujo básico de interacción del sistema es el siguiente:

1. El estudiante accede al sistema mediante un navegador web.

2. El usuario se autentica mediante el sistema de autenticación institucional.

3. El sistema identifica la carrera asociada al estudiante.

4. El sistema carga la malla curricular correspondiente al programa académico.

5. El sistema muestra visualmente las materias aprobadas y pendientes.

6. El sistema calcula y presenta el progreso académico del estudiante.

## Contexto Técnico

Desde el punto de vista técnico, el sistema se compone de una arquitectura
cliente-servidor con separación entre la capa de presentación y la lógica de
negocio.

Los principales componentes tecnológicos son:

• Frontend: Aplicación web desarrollada con Next.js encargada de la interfaz
de usuario.

• Backend: API REST desarrollada con FastAPI responsable de la lógica
de negocio y la gestión de los datos.

• Comunicación: Interacción entre frontend y backend mediante HTTP y
formato de datos JSON.

• Contenerización: Uso de Docker para asegurar consistencia en los entornos de desarrollo y despliegue.

La interacción principal del sistema ocurre cuando el frontend realiza solicitudes HTTP a la API del backend para obtener información académica que
posteriormente es presentada al usuario en la interfaz web.

## Estrategia de Solución

Para el desarrollo del sistema AS_StudentProgressSystem se adopta una
arquitectura basada en el modelo cliente-servidor, con una clara separación entre
la capa de presentación y la lógica de negocio.

En esta arquitectura, el frontend es responsable de la interacción con el usuario
y la representación visual de la información académica, mientras que el backend
expone una API REST encargada de gestionar la lógica del sistema y proporcionar
los datos necesarios al frontend.

La comunicación entre ambos componentes se realiza mediante solicitudes HTTP
utilizando el formato de datos JSON.

Esta separación de responsabilidades permite que cada componente del sistema
pueda evolucionar de forma independiente, facilitando el mantenimiento y la
escalabilidad de la aplicación.

Adicionalmente, el sistema utiliza contenedores Docker para garantizar la portabilidad y consistencia entre los diferentes entornos de desarrollo y despliegue.

La arquitectura propuesta permite que el sistema evolucione en el futuro hacia
una estructura más compleja que incluya:

• Integración con una base de datos relacional para persistencia de la información académica.

• Implementación de mecanismos de autenticación y autorización basados
en servicios institucionales.

• Integración con sistemas académicos existentes de la universidad.

• Escalamiento de la infraestructura para soportar un mayor número de
usuarios.

Buscando equilibrar simplicidad en la implementación inicial con la capacidad
de evolucionar hacia una arquitectura más robusta conforme el sistema crezca.

## Vista de Bloques

### Sistema General

El sistema AS_StudentProgressSystem se estructura en dos bloques principales que separan la capa de presentación de la lógica de negocio:

• Frontend: responsable de la interfaz de usuario y de la visualización del
progreso académico.

• Backend: encargado de exponer la API REST y gestionar la lógica del
sistema.

La comunicación entre ambos componentes se realiza mediante solicitudes HTTP
utilizando el formato JSON.

### Frontend

**Propósito**

El frontend es responsable de presentar la información académica al usuario
mediante una interfaz web interactiva.

**Tecnología**

El frontend está desarrollado utilizando el framework Next.js.

**Responsabilidades**

• Mostrar la malla curricular de la carrera.

• Visualizar materias aprobadas y pendientes.

• Mostrar indicadores del progreso académico.

• Realizar solicitudes HTTP al backend para obtener información académica.

### Backend

El backend está implementado utilizando FastAPI y expone una API REST
para gestionar la lógica del sistema.

El backend se divide conceptualmente en los siguientes componentes:

**API Layer**

Responsable de exponer los endpoints REST que permiten al frontend interactuar
con el sistema.

**Responsabilidades**

• Definir endpoints para consultar carreras, materias y progreso académico.

• Validar solicitudes provenientes del frontend.

• Formatear respuestas en JSON.

**Service Layer**

Contiene la lógica de negocio del sistema.

**Responsabilidades**

• Calcular el progreso académico del estudiante.

• Determinar materias aprobadas y pendientes.

• Gestionar la información relacionada con carreras y planes de estudio.

**Data Layer**

Encargado de la gestión y persistencia de los datos del sistema.

**Responsabilidades**

• Gestionar el acceso a la base de datos.

• Almacenar información sobre estudiantes, carreras y materias.

• Proveer datos a las capas superiores del sistema.

## Vista de Ejecución

La vista de ejecución describe cómo interactúan los distintos componentes del
sistema durante la ejecución para responder a las solicitudes de los usuarios.

### Escenario: Consulta del progreso académico

Descripción del proceso mediante el cual un estudiante consulta su progreso
académico dentro del sistema.

1. El estudiante accede al sistema utilizando un navegador web.

2. El frontend carga la interfaz principal del sistema.

3. El frontend envía una solicitud HTTP al backend para obtener la información académica del estudiante.

4. El backend recibe la solicitud a través de la capa de API.

5. La capa de servicios procesa la solicitud y calcula el progreso académico
del estudiante.

6. La capa de datos obtiene la información necesaria sobre materias, carrera
y estado académico del estudiante.

7. El backend genera una respuesta en formato JSON con la información
solicitada.

8. El frontend recibe la respuesta del backend.

9. El frontend procesa la información recibida y renderiza visualmente el
progreso académico del estudiante en la interfaz.

Este flujo representa la interacción principal entre el frontend y el backend
durante la consulta del progreso académico del usuario.

## Vista de Despliegue

El sistema AS_StudentProgressSystem utiliza contenedores Docker para
garantizar consistencia entre los entornos de desarrollo, pruebas y despliegue.

### Infraestructura Inicial

La arquitectura de despliegue inicial se compone de los siguientes elementos:

• Un contenedor Docker que ejecuta el Frontend desarrollado con Next.js.

• Un contenedor Docker que ejecuta el Backend desarrollado con FastAPI.

• Comunicación entre ambos contenedores mediante solicitudes HTTP.

### Distribución de Componentes

• **Frontend Container**  
  Ejecuta la aplicación web encargada de la interfaz de usuario y la visualización del progreso académico.

• **Backend Container**  
  Ejecuta la API REST responsable de procesar las solicitudes del frontend
y gestionar la lógica del sistema.

### Evolución de la Infraestructura

La arquitectura está diseñada para permitir la incorporación futura de componentes adicionales, tales como:

• Un servidor de base de datos relacional (por ejemplo PostgreSQL) para
persistencia de datos.

• Servicios de autenticación institucional.

• Infraestructura de despliegue en la nube o servidores institucionales.

El uso de contenedores Docker facilita la portabilidad del sistema y permite
replicar fácilmente el entorno de ejecución en diferentes plataformas.

## Conceptos Transversales

Esta sección describe principios y mecanismos arquitectónicos que son utilizados
de manera transversal en diferentes componentes del sistema.

### Separación de Responsabilidades

La arquitectura del sistema sigue el principio de separación de responsabilidades,
en el cual cada componente del sistema tiene una función específica dentro de la
arquitectura.

El frontend se encarga exclusivamente de la presentación de la información y la
interacción con el usuario, mientras que el backend gestiona la lógica de negocio
y el acceso a los datos.

Esta separación facilita el mantenimiento, la evolución del sistema y el desarrollo
independiente de cada componente.

### Comunicación mediante API REST

La comunicación entre los componentes del sistema se realiza mediante una API
REST expuesta por el backend.

Las solicitudes se realizan utilizando el protocolo HTTP y las respuestas se
envían en formato JSON. Este enfoque permite una integración sencilla entre el
frontend y el backend y facilita la futura integración con otros sistemas.

### Autenticación

El sistema contempla la implementación de mecanismos de autenticación para
garantizar que solo usuarios autorizados puedan acceder a la información
académica.

Se prevé la integración con sistemas de autenticación institucional basados en
servicios de identidad utilizados por la universidad.

### Manejo de Errores

El sistema implementa un manejo estandarizado de errores en la API REST.

Las respuestas del backend incluirán códigos de estado HTTP adecuados y
mensajes descriptivos que permitan al frontend interpretar correctamente las
fallas y presentar información clara al usuario.

### Contenerización

El sistema utiliza contenedores Docker para empaquetar los componentes del
frontend y backend junto con sus dependencias.

Esto permite asegurar que la aplicación se ejecute de forma consistente en
diferentes entornos, facilitando el despliegue y la portabilidad del sistema.

## Decisiones de Diseño

Esta sección describe las principales decisiones arquitectónicas tomadas durante
el diseño del sistema y las razones que justifican su elección.

### Uso de arquitectura cliente-servidor

**Decisión**  
Adoptar una arquitectura cliente-servidor que separe la interfaz de usuario de la
lógica de negocio.

**Motivación**  
Esta arquitectura permite separar claramente las responsabilidades del sistema,
facilitando el desarrollo independiente del frontend y del backend.

**Consecuencias**  
Permite mejorar la mantenibilidad del sistema y facilita la futura integración
con otros servicios o aplicaciones.

### Uso de FastAPI para el backend

**Decisión**  
Implementar el backend utilizando el framework FastAPI basado en Python.

**Motivación**  
FastAPI ofrece alto rendimiento, facilidad para desarrollar APIs REST y soporte
para validación automática de datos.

**Consecuencias**  
Permite desarrollar servicios web de manera rápida y eficiente, manteniendo una
estructura clara para la implementación de la lógica de negocio.

### Uso de Next.js para el frontend

**Decisión**  
Desarrollar el frontend utilizando el framework Next.js basado en React.

**Motivación**  
Next.js permite crear interfaces web modernas y ofrece características como
renderizado del lado del servidor y optimización de rendimiento.

**Consecuencias**  
Facilita la construcción de una interfaz interactiva y escalable para la visualización
del progreso académico.

### Uso de contenedores Docker

**Decisión**  
Utilizar contenedores Docker para empaquetar y ejecutar los componentes del
sistema.

**Motivación**  
Docker permite garantizar consistencia entre los entornos de desarrollo, pruebas
y despliegue.

**Consecuencias**  
Facilita la portabilidad del sistema y simplifica el proceso de despliegue.

### Arquitectura modular

**Decisión**  
Diseñar el backend siguiendo una estructura modular con diferentes capas (API,
servicios y acceso a datos).

**Motivación**  
La modularidad permite organizar mejor el código y facilita la evolución del
sistema a medida que se agregan nuevas funcionalidades.

**Consecuencias**  
Permite mantener una arquitectura más mantenible y escalable a largo plazo.

## Requerimientos de Calidad

A continuación se presentan algunos escenarios de calidad relevantes para el
sistema.

### Usabilidad

**Escenario**  
• Contexto: Un estudiante accede al sistema para consultar su progreso
académico.  
• Estímulo: El usuario navega por la interfaz para identificar materias
aprobadas y pendientes.  
• Respuesta esperada: La interfaz presenta la información académica de
forma clara, visual y fácil de interpretar.

### Rendimiento

**Escenario**  
• Contexto: Varios estudiantes acceden simultáneamente al sistema.  
• Estímulo: Los usuarios realizan consultas sobre su progreso académico.  
• Respuesta esperada: El sistema responde a las solicitudes en un tiempo
razonable sin degradación significativa del servicio.

### Escalabilidad

**Escenario**  
• Contexto: El número de estudiantes que utilizan el sistema aumenta.  
• Estímulo: Se incrementa la cantidad de solicitudes al backend.  
• Respuesta esperada: La arquitectura permite escalar los servicios para
soportar mayor carga de usuarios.

### Seguridad

**Escenario**  
• Contexto: Un usuario intenta acceder al sistema.  
• Estímulo: El usuario introduce sus credenciales de autenticación.  
• Respuesta esperada: El sistema valida la identidad del usuario y solo
permite el acceso a usuarios autorizados.

### Portabilidad

**Escenario**  
• Contexto: El sistema necesita ser desplegado en un nuevo entorno de
ejecución.  
• Estímulo: Se despliega la aplicación utilizando contenedores Docker.  
• Respuesta esperada: El sistema se ejecuta correctamente sin necesidad
de realizar configuraciones adicionales en el entorno.

## Riesgos y Deuda Técnica

El sistema se encuentra en fase de diseño arquitectónico y planificación. Por
esta razón, existen algunos riesgos y aspectos técnicos que deberán abordarse en
las siguientes iteraciones del desarrollo.

### Persistencia de datos aún no implementada

Actualmente la arquitectura contempla la futura integración de una base de datos
para almacenar información relacionada con estudiantes, carreras y materias.

**Impacto**  
La ausencia de persistencia limita la capacidad del sistema para manejar información académica real durante las primeras etapas de desarrollo.

**Mitigación**  
En fases posteriores del proyecto se integrará un sistema de base de datos
relacional, como PostgreSQL, para gestionar la información del sistema.

### Mecanismo de autenticación aún no integrado

Aunque la arquitectura contempla el uso de autenticación institucional, este
mecanismo aún no ha sido implementado en la versión inicial del sistema.

**Impacto**  
Durante las primeras iteraciones el acceso al sistema podrá ser limitado o simulado
mediante mecanismos temporales.

**Mitigación**  
En futuras versiones se integrará un sistema de autenticación basado en servicios
institucionales.

### Falta de integración con sistemas académicos institucionales

El sistema está diseñado para permitir una futura integración con plataformas
académicas de la universidad, como SAVIO o Banner. Sin embargo, dicha
integración aún no ha sido definida ni implementada.

**Impacto**  
La información académica utilizada en las primeras etapas del proyecto podrá
ser simulada o cargada manualmente.

**Mitigación**  
En futuras iteraciones se evaluarán mecanismos de integración con sistemas
institucionales.

### Ausencia inicial de pruebas automatizadas

Debido a que el desarrollo del sistema apenas inicia, aún no se han implementado
pruebas automatizadas.

**Impacto**  
Esto podría aumentar el riesgo de introducir errores durante las primeras fases
del desarrollo.

**Mitigación**  
Se prevé incorporar pruebas unitarias y pruebas de integración conforme avance
el desarrollo del sistema.

## Glosario

| Término                  | Definición |
|--------------------------|----------|
| Malla curricular         | Estructura que organiza las asignaturas que conforman un programa académico. Generalmente se distribuye por semestres y define el recorrido académico que debe seguir el estudiante para completar su carrera. |
| Asignatura / Materia     | Unidad académica dentro de un programa de estudios que el estudiante debe cursar y aprobar para avanzar en su carrera. |
| Créditos académicos      | Unidad utilizada por las universidades para medir la carga académica de una asignatura dentro del plan de estudios. |
| Progreso académico       | Nivel de avance de un estudiante dentro de su programa académico, determinado por las materias aprobadas y pendientes. |
| Materia aprobada         | Asignatura que el estudiante ha completado satisfactoriamente cumpliendo los requisitos académicos establecidos por la universidad. |
| Materia pendiente        | Asignatura que el estudiante aún no ha cursado o no ha aprobado dentro de su plan de estudios. |
| Gamificación             | Estrategia que consiste en aplicar elementos propios de los videojuegos, como logros, niveles o recompensas, en contextos no lúdicos con el objetivo de aumentar la motivación y la participación del usuario. |
| API REST                 | Estilo de arquitectura para el desarrollo de servicios web que permite la comunicación entre sistemas mediante solicitudes HTTP y el intercambio de datos estructurados. |
| FastAPI                  | Framework de desarrollo web para Python que permite construir APIs REST de forma rápida y eficiente. |
| Next.js                  | Framework basado en React utilizado para desarrollar aplicaciones web modernas con soporte para renderizado del lado del servidor. |
| Docker                   | Plataforma que permite crear, desplegar y ejecutar aplicaciones dentro de contenedores que incluyen todas sus dependencias necesarias para funcionar. |
| SAVIO                    | Plataforma académica utilizada por la Universidad Tecnológica de Bolívar para la gestión de procesos académicos relacionados con estudiantes y cursos. |
| Banner                   | Sistema de gestión académica utilizado por la Universidad Tecnológica de Bolívar para administrar información académica como matrículas, cursos y registros estudiantiles. |
| Dashboard                | Interfaz visual que presenta información mediante gráficos, indicadores y métricas que facilitan la comprensión rápida de un estado o progreso. |
## Planteamiento inicial.
![8d79857c-2607-494b-af99-07a0e5f02ad3](https://github.com/user-attachments/assets/70954a0f-d9b6-4d25-a197-bb4726ede099)

