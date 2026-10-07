# ReservaU: Sistema de Gestión y Reserva de Canchas (PSet 2)

ReservaU es un sistema diseñado para automatizar el ciclo de vida de reservas de instalaciones deportivas universitarias. Esta versión 2.0 soluciona requerimientos complejos como la concurrencia en la solicitud de horarios, prioridades por rol, y reservas recurrentes con verificación atómica. 

El diseño se fundamenta en un modelo de dominio rico y la correcta orquestación mediante controladores (Patrones de Diseño y Reglas ICONIX).

## Arquitectura y Decisiones de Diseño

Para resolver los requerimientos del PSet 2 sin acoplar el código y evitando modelos anémicos, se aplicaron los siguientes 7 patrones de diseño:

| Patrón | Requerimiento que soluciona | Clases Participantes |
| :--- | :--- | :--- |
| **Singleton** | Centralizar las reglas configurables como los 3 No-Shows y las 2h de ventana de estudiante (**RNF-05**). | `Configuracion` |
| **Strategy** | Desacoplar el cálculo de la prioridad (**RF-03**) y las penalidades de cancelación (**RF-04**, **RF-05**) sin usar condicionales `if/else` en las entidades. | `ReglaPrioridad` (y subtipos), `PoliticaCancelacion` (y subtipos), `Reserva` |
| **Factory Method** | Decidir instanciar una reserva de estudiante o una reserva de equipo oficial, asignándoles desde su nacimiento su propia `PoliticaCancelacion` (**RF-13**). | `ReservaCreator` |
| **Abstract Factory** | Combinar validadores de horarios distintos y canales de notificación distintos dependiendo si la cancha es Sede Norte o Sede Sur (**RNF-06**). | `FabricaSede`, `ValidadorHorario`, `Notificador` |
| **Builder** | Permitir configurar reservas recurrentes paso a paso, manejando datos obligatorios (fechas) y opcionales (equipo prestado, notas) sin constructores masivos o *telescópicos* (**RF-10**, **RF-11**). | `ReservaRecurrenteBuilder` |
| **Prototype** | Permitir al Administrador definir una plantilla de bloqueo para eventos o mantenimiento, y clonarla para distintas canchas en distintas fechas sin alterar el original (**RF-18**). | `Bloqueo` (con `copy.deepcopy()`) |
| **Facade** | Proveer un único punto de acceso estructurado para la simulación, coordinando las consultas a las fábricas, los creadores y el calendario subyacente. | `ReservaFacade` |

### Resolución de Concurrencia (RNF-03 y RNF-08)
Para evitar incidentes de **doble reserva** y garantizar que las reservas recurrentes sean atómicas (todo o nada), la clase `ReservaFacade` protege el diccionario `_calendario` utilizando **Locking Pesimista** mediante `threading.RLock()`. Se utilizó `RLock` (Reentrant Lock) en lugar de un `Lock` estándar para permitir que el Administrador cancele reservas de forma segura dentro del mismo bloque crítico cuando aplica bloqueos forzosos.

## Documentación del Proyecto

El repositorio sigue estrictamente la jerarquía solicitada por el syllabus y contiene los siguientes documentos de respaldo:

*   `1_Requerimientos.pdf`: Listado de Requerimientos Funcionales y No Funcionales.
*   `2_Modelo_Dominio.pdf`: Diagrama UML de Clases y trazabilidad.
*   `3_Casos_Uso.pdf`: Diagrama General de los Casos de Uso.
*   `implementacion/4_Flujos_Casos_Uso.pdf`: Diagramas de flujo y actividad detallados.
*   `implementacion/5_Secuencia_Estados.pdf`: Máquinas de estados y secuencias de comportamiento.

## Guía de Ejecución Rápida (Docker)

El proyecto está diseñado para ser portable e independiente del entorno de desarrollo. Sigue estos pasos para ejecutar la simulación de los 7 escenarios descritos en el PSet 2.

### Prerrequisitos
*   Tener **Docker Desktop** (o Docker Engine) instalado y corriendo en tu máquina.

### Pasos de Instalación y Ejecución

1. Clona este repositorio y navega hacia el directorio de implementación:
   ```bash
   cd psets/pset-02/implementacion