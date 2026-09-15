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
        return "Reserva confirmada para " + self.solicitante
    
class ReservaPrioridad:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante
    
    def confirmar(self):
        return "Reserva con prioridad confirmada para " + self.solicitante
    
def reservar_from_web():
    pass

def reservar_from_hall():
    pass