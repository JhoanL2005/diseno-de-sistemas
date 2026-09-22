class Computadora:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.disco = None
        self.gpu = None
        self.wifi = None

    def mostrar_configuracion(self):
        print(f"CPU: {self.cpu}")
        print(f"RAM: {self.ram}")
        print(f"Disco: {self.disco}")
        print(f"GPU: {self.gpu}")
        print(f"WiFi: {self.wifi}")

class ComputadoraBuilder:
    def __init__(self):
        self.computadora = Computadora()
    def add_cpu(self, cpu):
        self.computadora.cpu = cpu
        return self

    def add_ram(self, ram):
        self.computadora.ram = ram
        return self

    def add_disco(self, disco):
        self.computadora.disco = disco
        return self

    def add_gpu(self, gpu):
        self.computadora.gpu = gpu
        return self

    def add_wifi(self, wifi: bool):
        self.computadora.wifi = wifi
        return self

    def build(self):
        return self.computadora

def main():
    pc_builder = ComputadoraBuilder()

    # aqui hay mas codigo

    pc_builder = pc_builder.add_ram(4).add_gpu(18)
    pc_builder = pc_builder.add_disco(1).add_cpu(20).add_wifi(True)

    pc_gaming = pc_builder.build()
    pc_gaming.mostrar_configuracion()

main()