class Inventario:
    def verificar(self, producto):
        print(f"Verificando el stock de: {producto}")
        return True 

class Pago:
    def procesar(self, monto):
        print(f"Procesando pago: {monto}")
        return True

class Envio:
    def crear_envio(self, producto):
        print(f"Preparando el envio de: {producto}")
        return True

class TiendaFacade:
    def __init__(self):
        self.inventario = Inventario()
        self.pago = Pago()
        self.envio = Envio()

    def comprar(self, producto, precio):
        if not self.inventario.verificar(producto):
            print("No hay stock")
            return

        if not self.pago.procesar(precio):
            print("Fallo el pago")
            return

        self.envio.crear_envio(producto)
        print("Compra completada")

    
def main():
    tienda = TiendaFacade()
    tienda.comprar("Laptop", 1500)

main()