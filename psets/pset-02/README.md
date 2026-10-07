# ReservaU: Sistema de Gestión y Reserva de Canchas (PSet 2)

ReservaU es una solución orientada a objetos para gestionar reservas de canchas deportivas en una universidad. El sistema modela el ciclo completo de una reserva: validación de horario por sede, prioridad por rol, manejo de conflictos, cancelación con penalidad, suspensión por no-shows, reservas recurrentes, bloqueo administrativo y concurrencia de múltiples solicitudes.

Este proyecto corresponde al PSet 2 de Diseño de Sistemas y se centra en aplicar varios patrones de diseño para resolver requisitos complejos sin acoplar la lógica de negocio a decisiones técnicas.

## Objetivos del sistema

El sistema cubre los siguientes aspectos del problema de negocio:

- Validación de horarios por sede:
  - Norte: 06:00 a 22:00
  - Sur: 07:00 a 23:00
- Priorización según rol:
  - Estudiantes: sin prioridad
  - Capitanes: prioridad antes de las 18:00
- Gestión de conflictos por cancha ocupada
- Diferentes políticas de cancelación:
  - Estudiante
  - Capitán
  - Administración
- Suspensión temporal por reincidencia de no-shows
- Reservas recurrentes por semanas
- Bloqueos masivos por mantenimiento o eventos
- Concurrencia con hilos simultáneos

## Estructura del proyecto

```text
psets/
└── pset-02/
    ├── README.md
    ├── 1. Diagrama_De_Dominio.pdf
    ├── 2. Diagrama_Casos_De_Usos.pdf
    ├── 3. Diagrama_De_Flujo.pdf
    ├── 4. Diagrama_De_Secuencia.pdf
    ├── 5. Diagrama_De_Actividad.pdf
    ├── 6. Maquina_De_Estados.pdf
    ├── Requerimientos.pdf
    └── implementacion/
        ├── Dockerfile
        ├── modelos.py
        ├── simulacion.py
        └── __pycache__/
```

## Patrones de diseño aplicados

| Patrón | Propósito | Clases principales |
| --- | --- | --- |
| Singleton | Centralizar la configuración global del sistema | `Configuracion` |
| Strategy | Separar prioridades y penalidades de cancelación | `ReglaPrioridad`, `PoliticaCancelacion` |
| Factory Method | Crear reservas según el tipo de usuario | `ReservaCreator` |
| Abstract Factory | Definir validadores y notificaciones por sede | `FabricaSede`, `ValidadorHorario`, `Notificador` |
| Builder | Construir reservas recurrentes paso a paso | `ReservaRecurrenteBuilder` |
| Prototype | Clonar plantillas de bloqueo para varias canchas | `Bloqueo` |
| Facade | Agrupar el acceso a calendario, historial y conflictos | `ReservaFacade` |

## Modelo de dominio

El sistema está compuesto por estas entidades principales:

- `Usuario`: base para estudiantes, capitanes y administradores
- `Cancha`: representa una instalación con código y sede
- `Reserva`: encapsula una reserva confirmada o en conflicto
- `Bloqueo`: define una restricción administrativa temporal
- `ReservaFacade`: coordina validaciones, confirmaciones y cancelaciones

## Reglas clave implementadas

### 1. Horario por sede
La validación del horario está desacoplada por sede mediante fábricas abstractas:

- Norte: 06:00 - 22:00
- Sur: 07:00 - 23:00

Si la reserva cae fuera del horario permitido, se rechaza antes de ingresar al calendario.

### 2. Prioridad por rol
Los usuarios tienen una regla de prioridad distinta:

- `Estudiante`: sin prioridad
- `Capitan`: prioridad antes de las 18:00
- `Administrador`: resuelve conflictos y puede anular reservas

Cuando una cancha ya está ocupada, el sistema evalúa si el solicitante tiene prioridad. Si la tiene, la reserva queda en conflicto para ser resuelta por administración.

### 3. Cancelación y no-shows
Cada reserva usa una política de cancelación específica:

- `CancelacionEstudiante`
- `CancelacionCapitan`
- `AnulacionAdministrativa`

Si se detecta un no-show, se incrementa el contador del usuario y, cuando alcanza el límite configurado, queda suspendido temporalmente.

### 4. Concurrencia
El calendario está protegido con `threading.RLock()` para evitar condiciones de carrera y garantizar que las reservas concurrentes no generen inconsistencias.

### 5. Reservas recurrentes
El builder permite crear varias reservas semanales. Si alguna fecha intersecta con una reserva ya ocupada, la operación se aborta por completo, preservando la atomicidad del proceso.

## Escenarios simulados

La simulación incluida en [implementacion/simulacion.py](./implementacion/simulacion.py) cubre 7 escenarios:

1. Reserva por sede y aislamiento de fábricas
2. Validación del horario por sede
3. Reservas recurrentes y choques
4. Resolución de conflictos por prioridad de rol
5. Cancelación con penalidades y límite de suspensión por no-shows
6. Bloqueo con plantilla y clonación masiva
7. Concurrencia con múltiples hilos

## Cómo ejecutar el proyecto

### Opción 1: Python directo

```bash
cd psets/pset-02/implementacion
python simulacion.py
```

### Opción 2: Docker

```bash
cd psets/pset-02/implementacion
docker build -t reservau-pset-02 .
docker run --rm reservau-pset-02
```

El archivo [implementacion/Dockerfile](./implementacion/Dockerfile) ya está preparado para ejecutar la simulación automáticamente.

## Archivos principales

- [implementacion/modelos.py](./implementacion/modelos.py): lógica de dominio, patrones de diseño y fachada
- [implementacion/simulacion.py](./implementacion/simulacion.py): escenarios de prueba y demostración del comportamiento

## Conclusión

El PSet 2 busca demostrar que, al combinar patrones de diseño con un modelo de dominio rico y una capa de coordinación bien definida, se puede resolver un problema realista de gestión de recursos sin perder mantenibilidad ni consistencia. Este proyecto refleja precisamente ese enfoque: una solución modular, extensible y capaz de simular condiciones de negocio complejas.

Los diagramas y documentos anexos del proyecto complementan la implementación y describen el análisis del problema, el modelado del dominio y la evolución de comportamiento esperada del sistema.
