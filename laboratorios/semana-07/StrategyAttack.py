import random
from abc import ABC, abstractmethod

class EstrategiaAtaque(ABC):
    @abstractmethod
    def calcularDanio(self, ataque):
        pass

class AtaqueNormal(EstrategiaAtaque):
    def calcularDanio(self, ataque):
        return ataque

class AtaqueFuerte(EstrategiaAtaque):
    def calcularDanio(self, ataque):
        if random.random() < 0.25:
            return 0
        return ataque * 1.5

class Estrategia:
    def __init__(self, estrategiaAtaque):
        self.estrategiaAtaque = estrategiaAtaque

    def calcular_danio(self, ataque):
        return self.estrategiaAtaque.calcularDanio(ataque)