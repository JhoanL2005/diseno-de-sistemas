"""PATRÓN SINGLETON: una única instancia de GameConfig (entidad Config del dominio)."""


class GameConfig:
    _instancia = None

    MULTIPLICADORES = {"facil": 0.8, "normal": 1.0, "dificil": 1.25}

    def __new__(cls):
        if cls._instancia is None:
            instancia = super().__new__(cls)
            instancia.dificultad = "normal"
            instancia.numero_maximo_turnos = 15   # num_turnos_max del diagrama
            cls._instancia = instancia
        return cls._instancia

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def multiplicador(cls, dificultad: str) -> float:
        """Cuánto se escala la vida y el ataque del enemigo según la dificultad."""
        return cls.MULTIPLICADORES[dificultad]
