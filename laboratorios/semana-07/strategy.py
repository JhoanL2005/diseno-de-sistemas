"""PATRÓN STRATEGY: EstrategiaAtaque con ataqueNormal y ataqueFuerte intercambiables."""
import random
from abc import ABC, abstractmethod


class EstrategiaAtaque(ABC):
    nombre = ""

    @abstractmethod
    def calcular_danio(self, ataque: int) -> int:
        ...


class AtaqueNormal(EstrategiaAtaque):
    """Daño igual al ataque base. Siempre acierta."""
    nombre = "Ataque normal"

    def calcular_danio(self, ataque):
        return ataque


class AtaqueFuerte(EstrategiaAtaque):
    """Doble de daño, pero con 30% de probabilidad de fallar."""
    nombre = "Ataque fuerte"

    def calcular_danio(self, ataque):
        if random.random() < 0.30:
            return 0
        return ataque * 2


_ESTRATEGIAS = {"normal": AtaqueNormal, "fuerte": AtaqueFuerte}


def crear_estrategia(clave: str) -> EstrategiaAtaque:
    """Equivale a cambiarEstrategia("fuerte") del diagrama de secuencia."""
    try:
        return _ESTRATEGIAS[clave]()
    except KeyError:
        raise ValueError(f"Estrategia desconocida: {clave}")
