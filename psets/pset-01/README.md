# PSET 01 - Sistema de reservas de canchas

## Descripción general

Este proyecto implementa una simulación de un sistema de reservas de canchas deportivas, centrado en la lógica de prioridad de usuarios y la gestión de cancelaciones. El objetivo es modelar un flujo realista de reserva, validación de prioridad y clasificación de cancelaciones según el tiempo restante antes del evento.

La solución está desarrollada en Python y hace uso del patrón de diseño Strategy para encapsular la regla de prioridad de cada usuario de manera flexible y extensible.

## Objetivo del sistema

El sistema permite:

- Registrar usuarios con diferentes reglas de prioridad.
- Validar si un usuario tiene prioridad para reservar una cancha.
- Confirmar reservas asociadas a una cancha específica.
- Evaluar cancelaciones según el tiempo restante antes del inicio de la reserva.
- Liberar la cancha cuando la reserva se cancela o se considera no-show.

## Funcionalidades principales

### 1. Priorización por tipo de usuario

Se define una estrategia base llamada `ReglaPrioridad`, con implementaciones concretas como:

- `PrioridadAntesDeLasSeis`: otorga prioridad si la reserva inicia antes de las 18:00.
- `SinPrioridad`: no otorga prioridad.

Cada usuario posee una regla de prioridad y delega la decisión al objeto estrategia mediante el método `validar_prioridad()`.

### 2. Entidades del dominio

El sistema cuenta con las siguientes clases principales:

- `Usuario`: representa a cualquier solicitante.
- `Estudiante`: subclase de `Usuario`.
- `Capitan`: subclase de `Usuario`.
- `Cancha`: representa una cancha deportiva disponible o ocupada.
- `Reserva`: registra la reserva asociada a una cancha, un usuario y una hora de inicio.

### 3. Manejo de cancelaciones

La clase `Reserva` incluye la lógica de cancelación:

- Si faltan más de 2 horas para el inicio, la reserva se clasifica como "Cancelación Estándar".
- Si faltan menos de 2 horas, se clasifica como "No-Show".
- En ambos casos la cancha vuelve a quedar disponible.

## Estructura del proyecto

```text
pset-01/
├── README.md
├── 1_Requerimientos.pdf
├── 2_Modelo_de_uso.pdf
├── 3_Diagrama_de_casos.pdf
├── 4_1_Diagrama_de_flujo.pdf
├── 4_2_Diagrama_de_flujo.pdf
└── implementacion/
    ├── modelos.py
    ├── simulacion.py
    └── Dockerfile
```

## Archivos relevantes

### `implementacion/modelos.py`

Contiene la lógica del dominio y las entidades del sistema. Aquí se definen:

- Las reglas de prioridad.
- La jerarquía de usuarios.
- Las clases `Cancha` y `Reserva`.
- La lógica de cancelación.

### `implementacion/simulacion.py`

Ejecuta una demostración del sistema con distintos escenarios:

- reserva con prioridad.
- cancelación estándar con más de 2 horas de anticipación.
- detección de no-show con menos de 2 horas.

## Patrón de diseño aplicado

### Strategy

El patrón Strategy se usa para encapsular el comportamiento asociado a la prioridad del usuario. Esto permite variar la regla de prioridad sin modificar la lógica principal del sistema.

Esto se logra porque:

- `Usuario` no tiene lógica condicional interna.
- La decisión se delega a la estrategia configurada.
- Cada tipo de prioridad puede cambiarse sin afectar al resto del sistema.

## Cómo ejecutar la simulación

Desde la carpeta del proyecto:

```bash
cd implementacion
python simulacion.py
```

Si se usa Docker, también se puede construir y ejecutar el contenedor definido en `Dockerfile`.

## Resultado esperado

Al ejecutar la simulación, el programa imprime una secuencia de mensajes que muestran:

1. La validación de prioridad de un capitán.
2. La confirmación de una reserva exitosa.
3. La clasificación de una cancelación estándar.
4. La detección de un no-show cuando falta menos de dos horas.

## Conclusión

Este ejercicio permite comprender cómo aplicar principios de diseño orientado a objetos en un caso práctico de gestión de reservas, además de mostrar cómo la composición de comportamiento mediante estrategias mejora la extensibilidad del sistema.

## Autoría

Proyecto desarrollado para el curso de Diseño de Sistemas.
