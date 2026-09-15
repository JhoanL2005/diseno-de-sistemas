from singleton import GestorDeConfiguracion, reserva_permitida

def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = True

    assert  reserva_permitida(config) is False

def test_acepta_reserva():
    config = GestorDeConfiguracion.obtener_objeto()

    assert reserva_permitida(config) is True

