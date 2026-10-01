"""PATRÓN ABSTRACT FACTORY: familias completas de personajes según el mundo.

FantasyFactory -> Guerrero + Dragón
SciFiFactory   -> Soldado + Alien

Incluye la entidad Mundo (Fantasía, Ciencia Ficción) del diagrama de dominio.
"""
from abc import ABC, abstractmethod

from factory import PersonajeFactory


class MundoFactory(ABC):
    @abstractmethod
    def crear_jugador(self):
        ...

    @abstractmethod
    def crear_enemigo(self):
        ...


class FantasyFactory(MundoFactory):
    def crear_jugador(self):
        return PersonajeFactory.crear("guerrero")

    def crear_enemigo(self):
        return PersonajeFactory.crear("dragon")


class SciFiFactory(MundoFactory):
    def crear_jugador(self):
        return PersonajeFactory.crear("soldado")

    def crear_enemigo(self):
        return PersonajeFactory.crear("alien")


class Mundo:
    nombre = ""

    def __init__(self, fabrica: MundoFactory):
        self.fabrica = fabrica   # cada mundo "tiene" su familia de personajes


class Fantasia(Mundo):
    nombre = "Fantasía"

    def __init__(self):
        super().__init__(FantasyFactory())


class CienciaFiccion(Mundo):
    nombre = "Ciencia ficción"

    def __init__(self):
        super().__init__(SciFiFactory())
