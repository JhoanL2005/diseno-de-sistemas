from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# ==========================================
# PATRÓN STRATEGY (Regla de Prioridades)
# ==========================================
class ReglaPrioridad(ABC):
    @abstractmethod
    def tiene_prioridad(self, hora_inicio: datetime) -> bool:
        pass

class PrioridadAntesDeLasSeis(ReglaPrioridad):
    def tiene_prioridad(self, hora_inicio: datetime) -> bool:
        # Prioridad solo si la reserva es antes de las 18:00
        return hora_inicio.hour < 18

class SinPrioridad(ReglaPrioridad):
    def tiene_prioridad(self, hora_inicio: datetime) -> bool:
        # Nunca otorga prioridad
        return False

# ENTIDADES DE DOMINIO
class Usuario:
    def __init__(self, id_usuario: str, nombre: str, regla_prioridad: ReglaPrioridad):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.regla_prioridad = regla_prioridad

    def validar_prioridad(self, hora_inicio: datetime) -> bool:
        # Delega la decisión a la estrategia, sin usar condicionales if/else
        return self.regla_prioridad.tiene_prioridad(hora_inicio)

class Estudiante(Usuario):
    pass

class Capitan(Usuario):
    pass

class Cancha:
    def __init__(self, id_cancha: str, deporte: str):
        self.id_cancha = id_cancha
        self.deporte = deporte
        self.disponible = True

class Reserva:
    def __init__(self, id_reserva: str, cancha: Cancha, solicitante: Usuario, hora_inicio: datetime):
        self.id_reserva = id_reserva
        self.cancha = cancha
        self.solicitante = solicitante
        self.hora_inicio = hora_inicio
        self.estado = "Confirmada"

    def procesar_cancelacion(self, hora_actual: datetime):
        # Responsabilidad autónoma: evalúa la regla de las 2 horas
        tiempo_restante = self.hora_inicio - hora_actual
        
        if tiempo_restante < timedelta(hours=2):
            self.estado = "No-Show"
        else:
            self.estado = "Cancelación Estándar"
            
        self.cancha.disponible = True