# Vehiculo -> mueva -> mover

# Auto -> se mueve por carretera -> Conduciendo por carretera
# Bote -> se mueve por mar -> Navegando por agua
# Avion -> se mueve por cielo -> Volando por aire

class ComportamientoVuelo:
    def mover(self):
        raise NotImplementedError
class MuevePorCarretera(ComportamientoVuelo):
    def mover(self):
        print("Conduciendo por carretera")
class MuevePorMar(ComportamientoVuelo):
    def mover(self):
        print("Navegando por agua")
class MuevePorCielo(ComportamientoVuelo):
    def mover(self):
        print("Volando por aire")

class Vehiculo:
    def __init__(self, comportamiento_vuelo):
        self.comportamiento_vuelo = comportamiento_vuelo
    def mover(self):
        self.comportamiento_vuelo.mover()

class Auto(Vehiculo):
    def __init__(self):
        super().__init__(MuevePorCarretera())

class Bote(Vehiculo):
    def __init__(self):
        super().__init__(MuevePorMar())

class Avion(Vehiculo):
    def __init__(self):
        super().__init__(MuevePorCielo())

if __name__ == "__main__":
    print("Auto")
    auto = Auto()
    auto.mover()

    print("Bote")
    bote = Bote()
    bote.mover()

    print("Avion")
    avion = Avion()
    avion.mover()
