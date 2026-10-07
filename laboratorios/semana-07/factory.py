"""PATRÓN FACTORY: PersonajeFactory crea personajes según su tipo.

Incluye las entidades Personaje, Jugador y Enemigo del diagrama de dominio.
Solo el Jugador tiene una estrategia de ataque intercambiable; el enemigo
ataca siempre con ataque normal.
"""
from abc import ABC

from strategy import AtaqueNormal


class Personaje(ABC):
    def __init__(self, nombre: str, vida: int, ataque: int):
        self.nombre = nombre
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque

    def recibir_danio(self, danio: int) -> int:
        self.vida = max(0, self.vida - danio)
        return self.vida

    def __str__(self):
        return f"{self.nombre} (vida: {self.vida})"


class Jugador(Personaje):
    """Personaje controlado por el usuario. Contexto del patrón Strategy."""

    def __init__(self, nombre: str, vida: int, ataque: int):
        super().__init__(nombre, vida, ataque)
        self.estrategia = AtaqueNormal()

    def set_estrategia(self, estrategia):
        self.estrategia = estrategia


class Enemigo(Personaje):
    """Personaje controlado por el sistema. Estrategia fija: ataque normal."""

    estrategia = AtaqueNormal()


class Guerrero(Jugador):
    def __init__(self):
        super().__init__("Guerrero", vida=100, ataque=15)


class Soldado(Jugador):
    def __init__(self):
        super().__init__("Soldado", vida=90, ataque=14)


class Dragon(Enemigo):
    def __init__(self):
        super().__init__("Dragón", vida=120, ataque=12)


class Alien(Enemigo):
    def __init__(self):
        super().__init__("Alien", vida=110, ataque=11)


class PersonajeFactory:
    _tipos = {
        "guerrero": Guerrero,
        "soldado": Soldado,
        "dragon": Dragon,
        "alien": Alien,
    }

    @staticmethod
    def crear(tipo: str):
        clase = PersonajeFactory._tipos.get(tipo.lower())
        if clase is None:
            raise ValueError(f"Tipo de personaje desconocido: {tipo}")
        return clase()