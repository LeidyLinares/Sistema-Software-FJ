"""Simulación de 12 operaciones con manejo de errores sin detener el programa."""
from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import SistemaError
from logger_config import logger


def ejecutar(numero, descripcion, operacion):
    """Ejecuta una operación capturando cualquier error para no detener el programa."""
    print(f"\n[{numero}] {descripcion}")
    try:
        resultado = operacion()  # Intenta ejecutar la operación
    except SistemaError as e:
        # Errores propios del sistema (validaciones de negocio)
        print(f"   ERROR controlado: {e}")
        logger.error(f"Operación {numero} ({descripcion}): {e}")
        return None
    except Exception as e:
        # Cualquier error inesperado también se registra y el programa continúa
        print(f"   ERROR inesperado: {e}")
        logger.critical(f"Operación {numero} ({descripcion}) inesperado: {e}")
        return None
    else:
        # Solo se ejecuta si no hubo excepción
        print(f"   OK: {resultado.describir() if hasattr(resultado, 'describir') else resultado}")
        logger.info(f"Operación {numero} ({descripcion}) exitosa")
        return resultado
    finally:
        # Siempre se ejecuta, haya o no error
        logger.info(f"Operación {numero} finalizada")


def main():
    logger.info("=== Inicio de la simulación ===")

    # 1-3: Creación de clientes (1 válido y 2 inválidos)
    cliente1 = ejecutar(1, "Crear cliente válido", lambda: Cliente("Leidy Linares", "123456"))
    ejecutar(2, "Crear cliente con nombre vacío", lambda: Cliente("", "123456"))
    ejecutar(3, "Crear cliente con documento inválido", lambda: Cliente("Ana Pérez", "12a"))

    # 4-8: Creación de servicios (3 válidos y 2 inválidos)
    sala = ejecutar(4, "Crear reserva de sala (3 horas)", lambda: ReservaSala("Sala Principal", 3))
    ejecutar(5, "Crear reserva de sala con horas negativas", lambda: ReservaSala("Sala B", -2))
    equipo = ejecutar(6, "Crear alquiler de equipo (2 días)", lambda: AlquilerEquipo("Portátil", 2))
    asesoria = ejecutar(7, "Crear asesoría especializada (4 horas)", lambda: AsesoriaEspecializada("Asesoría Python", 4))
    ejecutar(8, "Crear asesoría con horas como texto", lambda: AsesoriaEspecializada("Asesoría X", "cuatro"))

    # 9-12: Operaciones sobre reservas
    reserva1 = ejecutar(9, "Crear reserva válida", lambda: Reserva(cliente1, sala))
    ejecutar(10, "Crear reserva sin cliente", lambda: Reserva(None, equipo))

    def confirmar_dos_veces():
        reserva1.confirmar()   # Primera confirmación: correcta
        reserva1.confirmar()   # Segunda: lanza ReservaError
        return reserva1

    ejecutar(11, "Confirmar la misma reserva dos veces", confirmar_dos_veces)

    reserva2 = Reserva(cliente1, asesoria)  # Reserva adicional para cancelar

    def cancelar_dos_veces():
        reserva2.cancelar()    # Primera cancelación: correcta
        reserva2.cancelar()    # Segunda: lanza ReservaError
        return reserva2

    ejecutar(12, "Cancelar la misma reserva dos veces", cancelar_dos_veces)

    # Demostración de polimorfismo: cada servicio calcula su costo distinto
    print("\n--- Polimorfismo: costos de los servicios ---")
    for servicio in (sala, equipo, asesoria):
        print(servicio.describir())

    logger.info("=== Fin de la simulación (el programa no se detuvo) ===")
    print("\nSimulación terminada. Revise logs/sistema.log")


if __name__ == "__main__":
    main()
