class ComportamientoVuelo:
    def vuelo(self):
        raise NotImplementedError

class VuelaConAlas(ComportamientoVuelo):
    def vuelo(self):
        print("Volando con alas ... ")
        
class NoVuela(ComportamientoVuelo):
    def vuelo(self):
        print("No puedo volar ... ")

class ComportamientoGraznar:
    def graznar(self):
        raise NotImplementedError

class GraznidoNormal(ComportamientoGraznar):
    def graznar(self):
        print("Cuack ... ")

class ChirridoGoma(ComportamientoGraznar):
    def graznar(self):
        print("Chirrido de goma ... ")

class Pato:
    def __init__(self, comportamiento_vuelo, comportamiento_graznar):
        self.comportamiento_vuelo = comportamiento_vuelo
        self.comportamiento_graznar = comportamiento_graznar

    def nada(self):
        print("Nadando ... ")
    def graznar(self):
        self.comportamiento_graznar.graznar()
    def vuelo(self):
        self.comportamiento_vuelo.vuelo()

class PatoSalvaje(Pato):
    def __init__(self):
        super().__init__(VuelaConAlas(), GraznidoNormal())

class PatoDeGoma(Pato):
    def __init__(self):
        super().__init__(NoVuela(), ChirridoGoma())

    #def vuelo(self):
    #    print("No puedo volar ... ")  Mala practica

if __name__ == "__main__":
    salvaje = PatoSalvaje()
    salvaje.nada()
    salvaje.graznar()
    salvaje.vuelo()

    print()

    goma = PatoDeGoma()
    goma.nada()
    goma.graznar()
    goma.vuelo()