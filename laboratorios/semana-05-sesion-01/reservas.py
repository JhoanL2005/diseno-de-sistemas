class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre

class EquipoOficial:
    def __init__(self, nombre):
        self.nombre = nombre

class ReservaRegular:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante
    
    def confirmar(self):
        print ("Reserva confirmada para " + self.solicitante.nombre)
    
class ReservaPrioridad:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante
    
    def confirmar(self):
        print("Reserva con prioridad confirmada para " + self.solicitante.nombre)
    
def reservar_from_web(cancha, fecha, hora_inicio, hora_fin, solicitante):

    creador = FabricaDeReservas.elegir_creador(solicitante)
    reserva = creador.crear_reserva(
        cancha,
        fecha,
        hora_inicio,
        hora_fin,
        solicitante
    )

    return reserva



class CreadorDeReserva():
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        raise NotImplementedError

class CreadorDeReservaRegular(CreadorDeReserva):
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaRegular(
            cancha,
            fecha,
            hora_inicio,
            hora_fin,
            solicitante
        )

class CreadorDeReservaPrioritaria(CreadorDeReserva):
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaPrioridad(
            cancha,
            fecha,
            hora_inicio,
            hora_fin,
            solicitante
        )

class FabricaDeReservas():
    @staticmethod
    def elegir_creador(solicitante):
        if isinstance(solicitante, Estudiante):
            return CreadorDeReservaRegular()
        elif isinstance(solicitante,EquipoOficial):
            return CreadorDeReservaPrioritaria


def main():
    reserva_1 = reservar_from_web(
        'Cancha de Futbol',
        '2026-09-17',
        '18:00',
        '19:30',
        Estudiante('Erick')
    )
    reserva_1.confirmar()

if __name__ == "__main__":
    main()