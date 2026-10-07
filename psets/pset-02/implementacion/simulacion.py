import threading
from datetime import datetime, timedelta
from modelos import (
    ReservaFacade, Estudiante, Capitan, Administrador,
    Cancha, ReservaRecurrenteBuilder, Bloqueo
)

def ejecutar_simulacion():
    print("=======================================")
    print(" INICIANDO SIMULACIÓN RESERVAU PSET 2")
    print("=======================================\n")
    
    facade = ReservaFacade()
    norte = Cancha("CN-01", "Norte")
    sur = Cancha("CS-01", "Sur")
    
    est_normal = Estudiante("E1", "Carlos (Estudiante)")
    capitan = Capitan("C1", "Laura (Capitana)")
    admin = Administrador("A1", "Admin Central")
    
    hora_base = datetime(2026, 10, 10, 15, 0)
    
    print("ESCENARIO 1: Reserva por Sede (Aislamiento de fábricas)")
    facade.reservar_cancha("R1-Norte", norte, est_normal, hora_base) 
    facade.reservar_cancha("R2-Sur", sur, capitan, hora_base) 
    
    print("\nESCENARIO 2: Validaciones fuera de horario por Sede")
    hora_tarde = datetime(2026, 10, 10, 22, 30)
    print(">> Sede Norte a las 22:30:")
    facade.reservar_cancha("R3-Rechazada", norte, est_normal, hora_tarde)
    print(">> Sede Sur a las 22:30:")
    facade.reservar_cancha("R4-Aceptada", sur, capitan, hora_tarde)

    print("\nESCENARIO 3: Reservas Recurrentes y Choques")
    builder_exito = ReservaRecurrenteBuilder(sur, capitan, datetime(2026, 11, 1, 10, 0)).set_semanas(3)
    facade.reservar_recurrente(builder_exito)
    
    print("\n>> Evaluando conflicto atómico en recurrente:")
    facade.reservar_cancha("R-Obstaculo", norte, est_normal, datetime(2026, 12, 8, 10, 0))
    builder_falla = ReservaRecurrenteBuilder(norte, capitan, datetime(2026, 12, 1, 10, 0)).set_semanas(4)
    facade.reservar_recurrente(builder_falla) 

    print("\n>> Evaluando conflicto de Prioridad de Rol:")
    hora_prio = datetime(2026, 10, 15, 16, 0)
    facade.reservar_cancha("R-Est", norte, est_normal, hora_prio)
    facade.reservar_cancha("R-Cap", norte, capitan, hora_prio) 
    facade.resolver_conflictos(admin) 

    print("\nESCENARIO 4: Tres resoluciones de cancelación (Diferencias por rol)")
    res_est = facade._calendario[(norte.codigo, hora_base)]
    res_cap = facade._calendario[(sur.codigo, hora_base)]
    
    facade.cancelar_reserva(res_est, hora_base - timedelta(hours=4))
    facade.cancelar_reserva(res_cap, hora_base - timedelta(hours=4))
    res_nocturna = facade._calendario[(sur.codigo, hora_tarde)]
    facade.cancelar_reserva(res_nocturna, hora_tarde - timedelta(minutes=10), es_admin=True)

    print("\nESCENARIO 5: Límite de Suspensión por Reincidencia (3 No-Shows)")
    est_malo = Estudiante("E2", "Pedro Infractor")
    hora_test = datetime(2026, 10, 20, 12, 0)
    for i in range(3):
        facade.reservar_cancha(f"R-Infraccion-{i}", norte, est_malo, hora_test + timedelta(days=i))
        r_inf = facade._calendario[(norte.codigo, hora_test + timedelta(days=i))]
        facade.cancelar_reserva(r_inf, hora_test + timedelta(days=i)) 
    
    print(">> Nuevo intento de reserva de Pedro:")
    facade.reservar_cancha("R-Denegada", norte, est_malo, datetime.now())

    print("\nESCENARIO 6: Plantilla de Bloqueo y Clonación Masiva")
    hora_evento = datetime(2026, 11, 20, 14, 0)
    facade.reservar_cancha("R-Victima", norte, est_normal, hora_evento)
    plantilla = Bloqueo("Torneo Regional", "Redes Oficiales")
    facade.aplicar_bloqueo(plantilla, [norte, sur], hora_evento, admin)

    print("\nESCENARIO 7: Concurrencia mediante Múltiples Hilos")
    hora_pico = datetime(2026, 12, 31, 20, 0)
    
    def intento_reserva(nombre_hilo, usuario):
        res = facade.reservar_cancha(nombre_hilo, norte, usuario, hora_pico)
        if res: print(f"{nombre_hilo} obtuvo éxito en la condición de carrera.")

    t1 = threading.Thread(target=intento_reserva, args=("Hilo-A (Estudiante)", est_normal))
    t2 = threading.Thread(target=intento_reserva, args=("Hilo-B (Capitán)", capitan))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    facade.consultar_historial(est_normal)

if __name__ == "__main__":
    ejecutar_simulacion()