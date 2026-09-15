from singleton import GestorDeConfiguracion, reserva_permitida

def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = True

    assert  reserva_permitida(config) is False

def test_acepta_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = False
    #El problema va cuando el modo de mantenimiento se mantiene con lo de la anterior prueba por lo que cambiamos al modo de mantenimiento a su estado original para hacer pasar la prueba
    assert reserva_permitida(config) is True




