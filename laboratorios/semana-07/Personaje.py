from abc import ABC, abstractmethod
from .StrategyAttack import EstrategiaAtaque, AtaqueNormal

class Personaje(ABC):
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    def recibirDanio(self, danio):
        self.vida = max(0, self.vida - danio)
        return self.vida

    def stadistics(self):
        return f"Nombre: {self.nombre}, Vida: {self.vida}"

class Jugador(Personaje):
    def __init__(self, nombre, vida, ataque):
        super().__init__(nombre, vida, ataque)
        self.estrategia = AtaqueNormal()

    def set_estrategia(self, estrategia):
        self.estrategia = estrategia
class Enemigo(Personaje):

    estrategia = AtaqueNormal() 

class Soldado(Jugador):
    def __init__(self, nombre, vida, ataque):
        super().__init__("Guerrero", 100, 15)
class Guerrero(Jugador):
    def __init__(self, nombre, vida, ataque):
        super().__init__("Guerrero", 100, 20)
class Dragon(Enemigo):
    def __init__(self, nombre, vida, ataque):
        super().__init__("Dragon", 150, 15)
class Alien(Enemigo):
    def __init__(self, nombre, vida, ataque):
        super().__init__("Alien", 100, 10)