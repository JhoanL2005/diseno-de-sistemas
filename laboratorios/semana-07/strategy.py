import random
from abc import ABC, abstractmethod


class EstrategiaAtaque(ABC):
    nombre = ""

    @abstractmethod
    def calcular_danio(self, ataque: int) -> int:
        ...


class AtaqueNormal(EstrategiaAtaque):
    nombre = "Ataque normal"

    def calcular_danio(self, ataque):
        return ataque


class AtaqueFuerte(EstrategiaAtaque):
    nombre = "Ataque fuerte"

    def calcular_danio(self, ataque):
        if random.random() < 0.30:
            return 0
        return ataque * 2


_ESTRATEGIAS = {"normal": AtaqueNormal, "fuerte": AtaqueFuerte}


def crear_estrategia(clave: str) -> EstrategiaAtaque:
    try:
        return _ESTRATEGIAS[clave]()
    except KeyError:
        raise ValueError(f"Estrategia desconocida: {clave}")
