"""PATRÓN FACADE: GameFacade es la única puerta de entrada a la lógica del juego.

Este archivo contiene, en este orden:
  1. Partida (entidad del dominio).
  2. Los 6 controles del diagrama de robustez, que GameFacade compone y oculta.
  3. GameFacade.
  4. La consola (boundaries: Menú de Mundo y Pantalla de Combate) y iniciar(),
     que es lo único que llama main.py. La consola solo habla con GameFacade.
"""
import random
import sys

from abstract_factory import CienciaFiccion, Fantasia
from factory import Jugador
from singleton import GameConfig
from strategy import crear_estrategia

# ======================================================================
# 1. Entidad Partida
# ======================================================================
EN_CURSO = "en_curso"
VICTORIA = "victoria"
DERROTA = "derrota"
EMPATE = "empate"


class Partida:
    def __init__(self, mundo, jugador, enemigo, config: dict):
        self.mundo = mundo
        self.jugador = jugador
        self.enemigo = enemigo
        self.config = config          # reglas: se rige por una Config
        self.estado = EN_CURSO
        self.ganador = None
        self.motivo = None            # "ko" o "limite_turnos"
        self.turno_actual = 0


# ======================================================================
# 2. Controles (diagrama de robustez)
# ======================================================================
class ControlMundo:
    MUNDOS = {"1": Fantasia, "2": CienciaFiccion}

    def solicitar_mundo(self, opcion: str):
        """solicitarMundo(op) -> mundo"""
        if opcion not in self.MUNDOS:
            raise ValueError(f"Mundo desconocido: {opcion}")
        return self.MUNDOS[opcion]()


class ControlPersonajes:
    def crear_personajes(self, mundo):
        """crearPersonajes(mundo) -> (jugador, enemigo), vía Abstract Factory."""
        return mundo.fabrica.crear_jugador(), mundo.fabrica.crear_enemigo()


class ControlConfig:
    def __init__(self):
        self.config = GameConfig.get_instance()   # Singleton

    def configurar(self, dificultad: str, numero_maximo_turnos: int = None):
        if dificultad not in GameConfig.MULTIPLICADORES:
            raise ValueError(f"Dificultad desconocida: {dificultad}")
        self.config.dificultad = dificultad
        if numero_maximo_turnos is not None:
            self.config.numero_maximo_turnos = numero_maximo_turnos

    def obtener_reglas(self) -> dict:
        """getRules() -> num_turnos_max, dificultad"""
        return {
            "numero_maximo_turnos": self.config.numero_maximo_turnos,
            "dificultad": self.config.dificultad,
        }


class ControlPartida:
    """Coordina la preparación de la partida (secuencia 1) y define su estado."""

    def __init__(self, control_mundo: ControlMundo,
                 control_personajes: ControlPersonajes,
                 control_config: ControlConfig):
        self.mundos = control_mundo
        self.personajes = control_personajes
        self.config = control_config

    def iniciar_mundo(self, opcion: str) -> Partida:
        """iniciarMundo(op): solicita mundo, crea personajes, pide reglas y crea la partida."""
        mundo = self.mundos.solicitar_mundo(opcion)
        jugador, enemigo = self.personajes.crear_personajes(mundo)
        reglas = self.config.obtener_reglas()
        return self.crear_partida(mundo, jugador, enemigo, reglas)

    def crear_partida(self, mundo, jugador, enemigo, reglas: dict) -> Partida:
        """crearPartida(mundo, jugador, enemigo, config) -> partida"""
        k = GameConfig.multiplicador(reglas["dificultad"])   # la dificultad escala al enemigo
        enemigo.vida_max = int(enemigo.vida_max * k)
        enemigo.vida = enemigo.vida_max
        enemigo.ataque = int(enemigo.ataque * k)
        return Partida(mundo, jugador, enemigo, reglas)

    def definir_estado(self, partida: Partida) -> str:
        """Define estado: victoria, derrota o continuar."""
        j, e = partida.jugador, partida.enemigo

        if e.vida <= 0:
            partida.estado, partida.ganador, partida.motivo = VICTORIA, j, "ko"
        elif j.vida <= 0:
            partida.estado, partida.ganador, partida.motivo = DERROTA, e, "ko"
        elif partida.turno_actual >= partida.config["numero_maximo_turnos"]:
            partida.motivo = "limite_turnos"
            if j.vida > e.vida:
                partida.estado, partida.ganador = VICTORIA, j
            elif e.vida > j.vida:
                partida.estado, partida.ganador = DERROTA, e
            else:
                partida.estado, partida.ganador = EMPATE, None
        else:
            partida.estado, partida.ganador, partida.motivo = EN_CURSO, None, None
        return partida.estado


class ControlEstadisticas:
    @staticmethod
    def _ficha(p) -> dict:
        return {
            "nombre": p.nombre,
            "vida": p.vida,
            "vida_max": p.vida_max,
            "ataque": p.ataque,
            "estrategia": p.estrategia.nombre,
        }

    def obtener_estadisticas(self, jugador, enemigo) -> dict:
        """obtenerEstadisticas() -> vida, ataque de ambos personajes"""
        return {"jugador": self._ficha(jugador), "enemigo": self._ficha(enemigo)}

    def recibir_danio(self, personaje, danio: int) -> int:
        """recibirDanio(personaje, danio) -> vida restante"""
        return personaje.recibir_danio(danio)


class ControlAtaque:
    def __init__(self, control_estadisticas: ControlEstadisticas):
        self.estadisticas = control_estadisticas

    def cambiar_estrategia(self, jugador: Jugador, clave: str):
        """cambiarEstrategia("fuerte"): solo el Jugador tiene estrategia intercambiable."""
        if not isinstance(jugador, Jugador):
            raise TypeError("Solo el Jugador puede cambiar de estrategia")
        estrategia = crear_estrategia(clave)
        jugador.set_estrategia(estrategia)
        return estrategia

    def atacar(self, atacante, objetivo) -> dict:
        """ataque(jugador): calcularDanio() y luego recibirDanio()"""
        danio = atacante.estrategia.calcular_danio(atacante.ataque)   # Strategy
        vida = self.estadisticas.recibir_danio(objetivo, danio)
        return {
            "atacante": atacante.nombre,
            "objetivo": objetivo.nombre,
            "danio": danio,
            "vida_objetivo": vida,
            "vida_max_objetivo": objetivo.vida_max,
        }

    def turno_enemigo(self, enemigo, jugador) -> dict:
        """turnoEnemigo()"""
        return self.atacar(enemigo, jugador)


# ======================================================================
# 3. GameFacade
# ======================================================================
class GameFacade:
    def __init__(self):
        self._config = ControlConfig()
        self._estadisticas = ControlEstadisticas()
        self._ataque = ControlAtaque(self._estadisticas)
        self._partida_ctl = ControlPartida(ControlMundo(), ControlPersonajes(), self._config)
        self._partida = None

    # --- Configuración (Singleton) ---
    def configurar(self, dificultad: str, numero_maximo_turnos: int = None):
        self._config.configurar(dificultad, numero_maximo_turnos)

    # --- Secuencia 1: preparación de la partida ---
    def iniciar_partida(self, opcion_mundo: str) -> dict:
        self._partida = self._partida_ctl.iniciar_mundo(opcion_mundo)
        return {
            "mundo": self._partida.mundo.nombre,
            "dificultad": self._partida.config["dificultad"],
            "numero_maximo_turnos": self._partida.config["numero_maximo_turnos"],
        }

    # --- Secuencia 2: turno de combate ---
    def obtener_estadisticas(self) -> dict:
        p = self._partida
        stats = self._estadisticas.obtener_estadisticas(p.jugador, p.enemigo)
        stats["turno"] = p.turno_actual + 1
        return stats

    def cambiar_estrategia(self, clave: str) -> str:
        return self._ataque.cambiar_estrategia(self._partida.jugador, clave).nombre

    def jugador_ataca(self) -> dict:
        p = self._partida
        return self._ataque.atacar(p.jugador, p.enemigo)

    def turno_enemigo(self) -> dict:
        p = self._partida
        return self._ataque.turno_enemigo(p.enemigo, p.jugador)

    def ejecutar_turno(self) -> list:
        """Jugador ataca; si el enemigo sigue en pie, responde."""
        eventos = [self.jugador_ataca()]
        if self._partida_ctl.definir_estado(self._partida) == EN_CURSO:
            eventos.append(self.turno_enemigo())
        self._partida.turno_actual += 1
        self._partida_ctl.definir_estado(self._partida)
        return eventos

    # --- Resultado ---
    @property
    def terminada(self) -> bool:
        return self._partida_ctl.definir_estado(self._partida) != EN_CURSO

    def resultado(self) -> str:
        p = self._partida
        self._partida_ctl.definir_estado(p)
        prefijo = "Límite de turnos alcanzado. " if p.motivo == "limite_turnos" else ""
        if p.estado == EMPATE:
            return prefijo + "¡Empate!"
        if p.ganador is p.jugador:
            return prefijo + f"¡Gana {p.jugador.nombre}!"
        return prefijo + f"Gana {p.enemigo.nombre}. Has sido derrotado."


# ======================================================================
# 4. Consola (boundaries del diagrama de robustez)
# ======================================================================
DIFICULTADES = {"1": "facil", "2": "normal", "3": "dificil"}
ESTRATEGIAS = {"1": "normal", "2": "fuerte"}


def _pedir(texto, validas, automatico):
    if automatico:
        eleccion = random.choice(validas)
        print(f"{texto}{eleccion}  (automático)")
        return eleccion
    while True:
        eleccion = input(texto).strip()
        if eleccion in validas:
            return eleccion
        print("  Opción no válida.")


def _barra(vida, vida_max, ancho=20):
    llenos = round(ancho * vida / vida_max) if vida_max else 0
    return f"[{'#' * llenos}{'-' * (ancho - llenos)}] {vida}/{vida_max}"


class MenuMundo:
    def __init__(self, juego: GameFacade, automatico: bool):
        self.juego = juego
        self.automatico = automatico

    def mostrar(self):
        mundo = _pedir("Mundo [1] Fantasía  [2] Ciencia ficción: ", ["1", "2"], self.automatico)
        dif = _pedir("Dificultad [1] fácil  [2] normal  [3] difícil: ", list(DIFICULTADES), self.automatico)
        self.juego.configurar(DIFICULTADES[dif])
        info = self.juego.iniciar_partida(mundo)
        print(f"\nMundo: {info['mundo']}  |  Dificultad: {info['dificultad']}  |  "
              f"Turnos máximos: {info['numero_maximo_turnos']}")


class PantallaCombate:
    def __init__(self, juego: GameFacade, automatico: bool):
        self.juego = juego
        self.automatico = automatico

    @staticmethod
    def _mostrar_estadisticas(s):
        j, e = s["jugador"], s["enemigo"]
        print(f"\n--- Turno {s['turno']} ---")
        print(f"{j['nombre']:<9} (ATQ {j['ataque']:>2}) {_barra(j['vida'], j['vida_max'])}")
        print(f"{e['nombre']:<9} (ATQ {e['ataque']:>2}) {_barra(e['vida'], e['vida_max'])}")

    @staticmethod
    def _mostrar_evento(ev):
        if ev["danio"] == 0:
            print(f"  {ev['atacante']} ataca a {ev['objetivo']} y FALLA.")
        else:
            print(f"  {ev['atacante']} ataca a {ev['objetivo']} y causa {ev['danio']} de daño.")

    def jugar(self):
        while True:
            self._mostrar_estadisticas(self.juego.obtener_estadisticas())
            if self.juego.terminada:
                break
            op = _pedir("Estrategia [1] Normal  [2] Fuerte: ", list(ESTRATEGIAS), self.automatico)
            print(f"Usas: {self.juego.cambiar_estrategia(ESTRATEGIAS[op])}")
            for evento in self.juego.ejecutar_turno():
                self._mostrar_evento(evento)

        print("\n" + "=" * 44)
        print(self.juego.resultado())
        print("=" * 44)


def iniciar():
    """Punto de entrada del juego. Es lo único que invoca main.py."""
    # Sin terminal interactiva (docker run sin -it) el juego corre en modo demo
    automatico = not sys.stdin.isatty()

    print("=" * 44)
    print("   VIDEOJUEGO POR TURNOS - PATRONES DE DISEÑO")
    print("=" * 44)
    if automatico:
        print("(Modo demo: sin entrada interactiva, elige al azar.)")
        print("(Para jugar tú: docker run -it --rm game-patterns)\n")

    juego = GameFacade()
    MenuMundo(juego, automatico).mostrar()
    PantallaCombate(juego, automatico).jugar()