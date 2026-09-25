class Envio:
    def enviar(self, paquete):
        print(f"Enviando paquete: {paquete}")
        return True

class Notificacion:
    def enviar(self, mensaje):
        print(f"Enviando notificacion: {mensaje}")
        return True

class SistemaEnvio:
    def __init__(self):
        self.envio = Envio()
        self.notificacion = Notificacion()

    def procesar_envio(self, paquete):
        if not self.envio.enviar(paquete):
            print("Fallo el envio")
            return

        if not self.notificacion.enviar(f"El paquete {paquete} ha sido enviado"):
            print("Fallo la notificacion")
            return
        
        print("Envio completado")

def main():
    sistema_envio = SistemaEnvio()
    sistema_envio.procesar_envio("Paquete 1")

main()