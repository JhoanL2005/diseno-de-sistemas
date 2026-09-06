from modelos import (
    Estudiante, Capitan, Cancha, Reserva,
    PrioridadAntesDeLasSeis, SinPrioridad
)
from datetime import datetime

def ejecutar_simulacion():
    print("=== INICIANDO SIMULACIÓN RESERVAU ===")
    
    # Configuración inicial
    cancha1 = Cancha("C-01", "Fútbol")
    estudiante = Estudiante("E01", "Jhoan", SinPrioridad())
    capitan = Capitan("C01", "María", PrioridadAntesDeLasSeis())
    
    # ---------------------------------------------------------
    print("\n--- FLUJO 1: Reservar Cancha (Con prioridad) ---")
    hora_reserva = datetime(2026, 9, 10, 16, 0) # 16:00 hrs
    
    print("1. El solicitante indica al sistema su intención de reservar.")
    print("2. El sistema verifica la disponibilidad de las canchas.")
    if cancha1.disponible:
        print("3. El sistema evalúa la regla de prioridad asociada al solicitante.")
        tiene_prio = capitan.validar_prioridad(hora_reserva)
        print(f"   [!] Evaluación: ¿Capitán tiene prioridad a las 16:00? -> {tiene_prio}")
        
        reserva1 = Reserva("R-001", cancha1, capitan, hora_reserva)
        cancha1.disponible = False
        print("4. El sistema registra la reserva en estado 'Confirmada'.")
        print("5. El sistema confirma al solicitante que la reserva fue exitosa.")

    # ---------------------------------------------------------
    print("\n--- FLUJO 2: Cancelación Estándar (>= 2 horas) ---")
    hora_actual_temprano = datetime(2026, 9, 10, 12, 0) # 12:00 hrs (Faltan 4h)
    
    print("1. El usuario solicita revocar de forma voluntaria su reserva.")
    print("2. Un daemon evalúa el tiempo restante entre la cancelación y el evento.")
    reserva1.procesar_cancelacion(hora_actual_temprano)
    print("3. El sistema determina que faltan 2 horas o más para el evento.")
    print(f"4. El sistema etiqueta la reserva como: '{reserva1.estado}'.")
    print("5. El sistema libera el bloque horario.")

    # ---------------------------------------------------------
    print("\n--- FLUJO 3: Detección de No-Show (< 2 horas) ---")
    # Creamos una nueva reserva para probar el No-Show
    hora_reserva_noche = datetime(2026, 9, 10, 19, 0) # 19:00 hrs
    reserva2 = Reserva("R-002", cancha1, estudiante, hora_reserva_noche)
    hora_actual_tarde = datetime(2026, 9, 10, 18, 0) # 18:00 hrs (Falta 1h)
    
    print("1. El usuario solicita revocar de forma voluntaria su reserva.")
    print("2. Un daemon evalúa el tiempo restante entre la cancelación y el evento.")
    reserva2.procesar_cancelacion(hora_actual_tarde)
    print("3a1. El daemon determina que faltan menos de 2 horas para el inicio.")
    print(f"3a2. El daemon clasifica automáticamente como: '{reserva2.estado}'.")
    print("5. El sistema libera el bloque horario y actualiza historial.")

if __name__ == "__main__":
    ejecutar_simulacion()