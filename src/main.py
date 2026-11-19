"""Simulación de operaciones con manejo de errores sin detener el programa."""
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorFJ
from excepciones import SistemaError
from logger_config import logger

contador = 0
estadisticas = {"exitosas": 0, "con_error": 0}


def ejecutar(descripcion, operacion):
    """Ejecuta una operación capturando cualquier error para no detener el programa."""
    global contador
    contador += 1
    numero = contador
    print(f"\n[{numero}] {descripcion}")
    try:
        resultado = operacion()  # Intenta ejecutar la operación
    except SistemaError as e:
        # Error controlado del sistema (validaciones de negocio)
        print(f"   ERROR controlado: {e}")
        if e.__cause__ is not None:  # Encadenamiento: muestra la causa original
            print(f"   Causa original: {type(e.__cause__).__name__}: {e.__cause__}")
        logger.error(f"Operación {numero} ({descripcion}): {e} | causa: {e.__cause__!r}")
        estadisticas["con_error"] += 1
        return None
    except Exception as e:
        # Error inesperado: también se registra y el programa continúa
        print(f"   ERROR inesperado ({type(e).__name__}): {e}")
        logger.critical(f"Operación {numero} ({descripcion}) inesperado: {type(e).__name__}: {e}")
        estadisticas["con_error"] += 1
        return None
    else:
        # Solo se ejecuta si no hubo excepción
        texto = resultado.describir() if hasattr(resultado, "describir") else resultado
        print(f"   OK: {texto}")
        logger.info(f"Operación {numero} ({descripcion}) exitosa")
        estadisticas["exitosas"] += 1
        return resultado
    finally:
        # Siempre se ejecuta, haya o no error
        logger.info(f"Operación {numero} finalizada")


def main():
    logger.info("=== Inicio de la simulación ===")
    gestor = GestorFJ()

    # ---- Clientes ----
    cliente1 = ejecutar("Registrar cliente válido", lambda: gestor.registrar_cliente("Leidy Linares", "123456"))
    cliente2 = ejecutar("Registrar segundo cliente válido", lambda: gestor.registrar_cliente("Dary Ramírez", "987654"))
    ejecutar("Registrar cliente con nombre vacío", lambda: gestor.registrar_cliente("", "555555"))
    ejecutar("Registrar cliente con documento inválido", lambda: gestor.registrar_cliente("Ana Pérez", "12a"))
    ejecutar("Registrar cliente con documento duplicado", lambda: gestor.registrar_cliente("Otro Cliente", "123456"))
    ejecutar("Registrar cliente sin documento (parámetro faltante)", lambda: gestor.registrar_cliente("Pedro Gómez"))

    # ---- Servicios ----
    sala = ejecutar("Crear reserva de sala (3 horas)", lambda: gestor.registrar_servicio(ReservaSala("Sala Principal", 3)))
    ejecutar("Crear sala con horas negativas", lambda: gestor.registrar_servicio(ReservaSala("Sala B", -2)))
    ejecutar("Crear sala de 20 horas (supera el máximo)", lambda: gestor.registrar_servicio(ReservaSala("Sala C", 20)))
    equipo = ejecutar("Crear alquiler de equipo (2 días)", lambda: gestor.registrar_servicio(AlquilerEquipo("Portátil", 2)))
    asesoria = ejecutar("Crear asesoría especializada (4 horas)", lambda: gestor.registrar_servicio(AsesoriaEspecializada("Asesoría Python", 4)))
    ejecutar("Crear asesoría sin indicar las horas (parámetro faltante)", lambda: gestor.registrar_servicio(AsesoriaEspecializada("Asesoría X")))

    # ---- Reservas ----
    def flujo_completo():
        reserva = gestor.crear_reserva(cliente1, sala)
        reserva.confirmar()
        reserva.procesar(impuesto=0.19, descuento=0.10)  # Costo con IVA 19% y descuento 10%
        return reserva

    ejecutar("Reserva exitosa: crear, confirmar y procesar con IVA y descuento", flujo_completo)
    ejecutar("Crear reserva sin cliente (parámetro faltante)", lambda: gestor.crear_reserva(None, equipo))

    reserva2 = ejecutar("Crear reserva de asesoría", lambda: gestor.crear_reserva(cliente2, asesoria))

    def confirmar_dos_veces():
        reserva2.confirmar()   # Primera confirmación: correcta
        reserva2.confirmar()   # Segunda: lanza ReservaError
        return reserva2

    ejecutar("Confirmar dos veces la misma reserva", confirmar_dos_veces)
    ejecutar("Procesar con descuento de 150% (cálculo inconsistente)", lambda: reserva2.procesar(descuento=1.5))
    ejecutar("Procesar la reserva con descuento válido", lambda: (reserva2.procesar(descuento=0.05), reserva2)[1])

    def reserva_servicio_no_disponible():
        equipo.marcar_no_disponible()
        reserva = gestor.crear_reserva(cliente2, equipo)
        reserva.confirmar()    # Falla: el servicio no está disponible
        return reserva

    ejecutar("Confirmar reserva de un servicio no disponible", reserva_servicio_no_disponible)
    ejecutar("Procesar una reserva que sigue pendiente", lambda: gestor.crear_reserva(cliente1, asesoria).procesar())

    def cancelar_dos_veces():
        reserva = gestor.crear_reserva(cliente2, sala)
        reserva.cancelar()     # Primera cancelación: correcta
        reserva.cancelar()     # Segunda: lanza ReservaError
        return reserva

    ejecutar("Cancelar dos veces la misma reserva", cancelar_dos_veces)
    ejecutar("Error inesperado: consultar una reserva inexistente", lambda: gestor.obtener_reserva(99))

    # ---- Polimorfismo y métodos sobrecargados ----
    print("\n--- Polimorfismo: descripción y costo de cada servicio ---")
    for servicio in gestor.servicios:
        print(f"{servicio.describir()} -> ${servicio.calcular_costo():,.0f}")

    print("\n--- Método sobrecargado calcular_costo() en la sala ---")
    print(f"Sin extras:                ${sala.calcular_costo():,.0f}")
    print(f"Con IVA 19%:               ${sala.calcular_costo(0.19):,.0f}")
    print(f"Con IVA 19% y descuento 10%: ${sala.calcular_costo(0.19, 0.10):,.0f}")

    print("\n--- Resumen del sistema (listas internas) ---")
    print(f"Clientes: {len(gestor.clientes)} | Servicios: {len(gestor.servicios)} | Reservas: {len(gestor.reservas)}")
    for reserva in gestor.reservas:
        print(reserva.describir())

    print(f"\nOperaciones: {contador} | Exitosas: {estadisticas['exitosas']} | Con error controlado: {estadisticas['con_error']}")
    logger.info("=== Fin de la simulación (el programa no se detuvo) ===")
    print("Simulación terminada. Revise logs/sistema.log")


if __name__ == "__main__":
    main()
