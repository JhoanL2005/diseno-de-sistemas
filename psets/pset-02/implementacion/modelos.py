import threading
import copy
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# ==========================================
# 1. SINGLETON (Configuración Central)
# ==========================================
class Configuracion:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Configuracion, cls).__new__(cls)
            cls._instancia.limite_no_shows = 3
            cls._instancia.dias_suspension = 7
            cls._instancia.ventana_estudiante = timedelta(hours=2)
            cls._instancia.ventana_capitan = timedelta(hours=24)
        return cls._instancia

# ==========================================
# 2. STRATEGY (Prioridades y Cancelaciones)
# ==========================================
class ReglaPrioridad(ABC):
    @abstractmethod
    def tiene_prioridad(self, hora_inicio: datetime) -> bool: pass

class SinPrioridad(ReglaPrioridad):
    def tiene_prioridad(self, hora_inicio: datetime) -> bool: return False

class PrioridadAntesDeLasSeis(ReglaPrioridad):
    def tiene_prioridad(self, hora_inicio: datetime) -> bool: 
        return hora_inicio.hour < 18

class PoliticaCancelacion(ABC):
    @abstractmethod
    def evaluar_penalidad(self, hora_actual: datetime, hora_inicio: datetime) -> str: pass

class CancelacionEstudiante(PoliticaCancelacion):
    def evaluar_penalidad(self, hora_actual: datetime, hora_inicio: datetime) -> str:
        config = Configuracion()
        if (hora_inicio - hora_actual) < config.ventana_estudiante:
            return "No-Show"
        return "Cancelada"

class CancelacionCapitan(PoliticaCancelacion):
    def evaluar_penalidad(self, hora_actual: datetime, hora_inicio: datetime) -> str:
        config = Configuracion()
        if (hora_inicio - hora_actual) < config.ventana_capitan:
            return "No-Show"
        return "Cancelada"

class AnulacionAdministrativa(PoliticaCancelacion):
    def evaluar_penalidad(self, hora_actual: datetime, hora_inicio: datetime) -> str:
        return "Anulada por administración"

# ==========================================
# 3. ENTIDADES DE DOMINIO RICH
# ==========================================
class Usuario(ABC):
    def __init__(self, id_usuario: str, nombre: str, regla_prioridad: ReglaPrioridad):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.regla_prioridad = regla_prioridad
        self.conteo_no_shows = 0
        self.suspendido_hasta = None

    def validar_prioridad(self, hora_inicio: datetime) -> bool:
        return self.regla_prioridad.tiene_prioridad(hora_inicio)

    def esta_suspendido(self, fecha_actual: datetime) -> bool:
        if self.suspendido_hasta and fecha_actual < self.suspendido_hasta:
            return True
        return False

    def registrar_no_show(self, fecha_actual: datetime):
        self.conteo_no_shows += 1
        config = Configuracion()
        if self.conteo_no_shows >= config.limite_no_shows:
            self.suspendido_hasta = fecha_actual + timedelta(days=config.dias_suspension)

class Estudiante(Usuario):
    def __init__(self, id_usuario: str, nombre: str):
        super().__init__(id_usuario, nombre, SinPrioridad())

class Capitan(Usuario):
    def __init__(self, id_usuario: str, nombre: str):
        super().__init__(id_usuario, nombre, PrioridadAntesDeLasSeis())

class Administrador(Usuario):
    def __init__(self, id_usuario: str, nombre: str):
        super().__init__(id_usuario, nombre, SinPrioridad())

class Cancha:
    def __init__(self, codigo: str, sede: str):
        self.codigo = codigo
        self.sede = sede

class Reserva:
    def __init__(self, codigo: str, cancha: Cancha, solicitante: Usuario, fecha_hora: datetime, politica: PoliticaCancelacion, estado="Confirmada"):
        self.codigo = codigo
        self.cancha = cancha
        self.solicitante = solicitante
        self.fecha_hora = fecha_hora
        self.politica = politica
        self.estado = estado

    def procesar_cancelacion(self, hora_actual: datetime) -> str:
        nuevo_estado = self.politica.evaluar_penalidad(hora_actual, self.fecha_hora)
        self.estado = nuevo_estado
        return nuevo_estado

# ==========================================
# 4. ABSTRACT FACTORY (Sedes)
# ==========================================
class ValidadorHorario(ABC):
    @abstractmethod
    def es_valido(self, hora: datetime) -> bool: pass

class Notificador(ABC):
    @abstractmethod
    def notificar(self, mensaje: str): pass

class FabricaSede(ABC):
    @abstractmethod
    def crear_validador(self) -> ValidadorHorario: pass
    @abstractmethod
    def crear_notificador(self) -> Notificador: pass

class FabricaNorte(FabricaSede):
    class ValidadorNorte(ValidadorHorario):
        def es_valido(self, hora: datetime): return 6 <= hora.hour < 22
    class NotificadorNorte(Notificador):
        def notificar(self, msj): print(f"[Correo Institucional - Norte] {msj}")
        
    def crear_validador(self): return self.ValidadorNorte()
    def crear_notificador(self): return self.NotificadorNorte()

class FabricaSur(FabricaSede):
    class ValidadorSur(ValidadorHorario):
        def es_valido(self, hora: datetime): return 7 <= hora.hour < 23
    class NotificadorSur(Notificador):
        def notificar(self, msj): print(f"[SMS - Sur] {msj}")
        
    def crear_validador(self): return self.ValidadorSur()
    def crear_notificador(self): return self.NotificadorSur()

# ==========================================
# 5. FACTORY METHOD
# ==========================================
class ReservaCreator:
    @staticmethod
    def crear_reserva(codigo: str, cancha: Cancha, solicitante: Usuario, fecha_hora: datetime, estado="Confirmada") -> Reserva:
        if isinstance(solicitante, Capitan):
            return Reserva(codigo, cancha, solicitante, fecha_hora, CancelacionCapitan(), estado)
        elif isinstance(solicitante, Administrador):
            return Reserva(codigo, cancha, solicitante, fecha_hora, AnulacionAdministrativa(), estado)
        else:
            return Reserva(codigo, cancha, solicitante, fecha_hora, CancelacionEstudiante(), estado)

# ==========================================
# 6. BUILDER & PROTOTYPE 
# ==========================================
class ReservaRecurrenteBuilder:
    def __init__(self, cancha: Cancha, solicitante: Usuario, fecha_inicio: datetime):
        self.cancha = cancha
        self.solicitante = solicitante
        self.fecha_inicio = fecha_inicio
        self.semanas = 2
        self.equipo = None
        self.notas = None

    def set_semanas(self, n: int):
        if 2 <= n <= 8: self.semanas = n
        return self

    def set_equipo_prestado(self, equipo: str):
        self.equipo = equipo
        return self

    def build_fechas(self):
        return [self.fecha_inicio + timedelta(weeks=i) for i in range(self.semanas)]

class Bloqueo:
    def __init__(self, motivo: str, equipo_montaje: str):
        self.motivo = motivo
        self.equipo_montaje = equipo_montaje
        self.cancha = None
        self.fecha_hora = None
        self.codigo = f"BLOQUEO-{motivo.lower().replace(' ', '-')[:20]}"
        self.solicitante = Administrador("ADMIN-BLOQUEO", "Sistema")
        self.politica = AnulacionAdministrativa()
        self.estado = "Bloqueado"

    def clone(self):
        return copy.deepcopy(self)

    def procesar_cancelacion(self, hora_actual: datetime) -> str:
        self.estado = "Bloqueo levantado"
        return self.estado

# ==========================================
# 7. FACADE Y CONCURRENCIA
# ==========================================
class ReservaFacade:
    def __init__(self):
        self._calendario = {}  
        self._historial = []
        self._conflictos = []
        self._lock = threading.RLock()

    def _obtener_fabrica_sede(self, cancha: Cancha) -> FabricaSede:
        return FabricaNorte() if cancha.sede == "Norte" else FabricaSur()

    def reservar_cancha(self, codigo_reserva: str, cancha: Cancha, solicitante: Usuario, fecha_hora: datetime) -> bool:
        if solicitante.esta_suspendido(datetime.now()):
            print(f"Rechazo: El solicitante {solicitante.nombre} está suspendido.")
            return False

        fabrica = self._obtener_fabrica_sede(cancha)
        if not fabrica.crear_validador().es_valido(fecha_hora):
            print(f"Rechazo: {fecha_hora.strftime('%H:%M')} fuera del horario de Sede {cancha.sede}.")
            return False

        with self._lock:
            clave = (cancha.codigo, fecha_hora)
            if clave in self._calendario:
                if solicitante.validar_prioridad(fecha_hora):
                    nueva_reserva = ReservaCreator.crear_reserva(codigo_reserva, cancha, solicitante, fecha_hora, estado="Conflicto")
                    self._conflictos.append(nueva_reserva)
                    self._historial.append(nueva_reserva)
                    print(f"Conflicto: Cancha ocupada, pero {solicitante.nombre} tiene prioridad oficial. Requiere intervención.")
                    return True
                else:
                    print(f"Rechazo: La cancha {cancha.codigo} ya está ocupada.")
                    return False
            
            nueva_reserva = ReservaCreator.crear_reserva(codigo_reserva, cancha, solicitante, fecha_hora)
            self._calendario[clave] = nueva_reserva
            self._historial.append(nueva_reserva)
            
        fabrica.crear_notificador().notificar(f"Reserva {codigo_reserva} confirmada para {solicitante.nombre}.")
        return True

    def cancelar_reserva(self, reserva: Reserva, hora_actual: datetime, es_admin=False):
        if not isinstance(reserva, (Reserva, Bloqueo)):
            print("Cancelación rechazada: el elemento no es una reserva ni un bloqueo válido.")
            return

        if es_admin and hasattr(reserva, 'politica'):
            reserva.politica = AnulacionAdministrativa()

        resultado = reserva.procesar_cancelacion(hora_actual)

        with self._lock:
            clave = (reserva.cancha.codigo, reserva.fecha_hora)
            if clave in self._calendario and self._calendario[clave] == reserva:
                del self._calendario[clave]

        if isinstance(reserva, Reserva):
            if resultado == "No-Show":
                reserva.solicitante.registrar_no_show(hora_actual)
                print(f"No-Show: Falta registrada a {reserva.solicitante.nombre}. Total mes: {reserva.solicitante.conteo_no_shows}")
            else:
                print(f"Cancelación exitosa: Estado -> {resultado}")
        else:
            print(f"Bloqueo levantado: Estado -> {resultado}")

    def reservar_recurrente(self, builder: ReservaRecurrenteBuilder) -> bool:
        if not isinstance(builder.solicitante, Capitan):
            print("Rechazo: Solo capitanes reservan de forma recurrente.")
            return False

        fechas = builder.build_fechas()
        fabrica = self._obtener_fabrica_sede(builder.cancha)

        with self._lock:
            for f in fechas:
                if (builder.cancha.codigo, f) in self._calendario:
                    print(f"Rechazo Recurrente: Choque detectado en {f.strftime('%Y-%m-%d')}. Se aborta solicitud completa.")
                    return False
            
            for i, f in enumerate(fechas):
                res = ReservaCreator.crear_reserva(f"REC-{i}", builder.cancha, builder.solicitante, f)
                self._calendario[(builder.cancha.codigo, f)] = res
                self._historial.append(res)
                
        fabrica.crear_notificador().notificar(f"Reserva recurrente confirmada ({builder.semanas} semanas).")
        return True

    def aplicar_bloqueo(self, plantilla: Bloqueo, canchas: list, fecha_hora: datetime, admin: Administrador):
        for c in canchas:
            fabrica = self._obtener_fabrica_sede(c)
            clon = plantilla.clone()
            clon.cancha = c
            clon.fecha_hora = fecha_hora

            with self._lock:
                clave = (c.codigo, fecha_hora)
                if clave in self._calendario:
                    res_afectada = self._calendario[clave]
                    if isinstance(res_afectada, Reserva):
                        self.cancelar_reserva(res_afectada, datetime.now(), es_admin=True)
                        fabrica.crear_notificador().notificar(f"Tu reserva {res_afectada.codigo} fue anulada por mantenimiento administrativo.")
                self._calendario[clave] = clon
            print(f"Bloqueo aplicado con éxito en la cancha {c.codigo}.")

    def consultar_historial(self, usuario: Usuario):
        print(f"\n--- Historial de {usuario.nombre} ---")
        mias = [r for r in self._historial if isinstance(r, Reserva) and r.solicitante == usuario]
        if not mias:
            print("El historial está vacío.")
            return
        for r in mias:
            print(f"[{r.estado}] {r.codigo} - {r.fecha_hora.strftime('%Y-%m-%d %H:%M')}")

    def resolver_conflictos(self, admin: Administrador):
        print("\n--- Resolución de Conflictos (Administrador) ---")
        if not self._conflictos:
            print("No hay conflictos pendientes.")
            return

        for conf in self._conflictos:
            clave = (conf.cancha.codigo, conf.fecha_hora)
            res_anterior = self._calendario.get(clave)

            if isinstance(res_anterior, Reserva):
                print(f"Resolviendo sobrecupo en {conf.cancha.codigo}. Anulando reserva estándar a favor del Equipo Oficial.")
                self.cancelar_reserva(res_anterior, datetime.now(), es_admin=True)
            else:
                print(f"Resolviendo sobrecupo en {conf.cancha.codigo}. No había reserva estándar vigente; se mantiene la prioridad del equipo oficial.")

            conf.estado = "Confirmada"
            self._calendario[clave] = conf
        self._conflictos.clear()