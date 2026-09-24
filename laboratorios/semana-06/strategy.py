from abc import ABC, abstractmethod

class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar(self, precio_base):
        pass

class sinDescuento(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base
class descuentoVIP(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.80
class descuentoEstudiante(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.95
class descuentoEmpleado(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.75

class Compra:
    def __init__(self, estrategiaDescuento):
        self.estrategiaDescuento = estrategiaDescuento

    def calcular_total(self , precio):
        return self.estrategiaDescuento.aplicar(precio)


def main():

    sin_descuento = sinDescuento()
    vip_descuento = descuentoVIP()
    estud_descuento = descuentoEstudiante()
    empleado_descuento = descuentoEmpleado()

    compra_1 = Compra(sin_descuento)
    print(compra_1.calcular_total(100))
    compra_2 = Compra(vip_descuento)
    print(compra_2.calcular_total(1000))
    compra_3 = Compra(estud_descuento)
    print(compra_3.calcular_total(550))
    compra_4 = Compra(empleado_descuento)
    print(compra_4.calcular_total(300))

main()

        
