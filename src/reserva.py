"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidad import Entidad
from cliente import Cliente
from servicio import Servicio
from excepciones import ReservaError, ServicioNoDisponibleError, CalculoError
from logger_config import logger


class Reserva(Entidad):
    """Estados posibles: Pendiente, Confirmada, Procesada y Cancelada."""

    def __init__(self, cliente=None, servicio=None):
        super().__init__()
        if cliente is None or servicio is None:
            raise ReservaError("Faltan parámetros: la reserva requiere cliente y servicio")
        if not isinstance(cliente, Cliente):
            raise ReservaError("El cliente de la reserva no es válido")
        if not isinstance(servicio, Servicio):
            raise ReservaError("El servicio de la reserva no es válido")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = servicio.duracion   # Duración tomada del servicio
        self.unidad = servicio.unidad
        self.estado = "Pendiente"
        self.costo_final = None

    def confirmar(self):
        """Confirma la reserva si está pendiente y el servicio está disponible."""
        if self.estado != "Pendiente":
            raise ReservaError(f"No se puede confirmar una reserva {self.estado}")
        try:
            self.servicio.verificar_disponibilidad()
        except ServicioNoDisponibleError as e:
            # Encadenamiento de excepciones: se conserva la causa original
            raise ReservaError("No se pudo confirmar la reserva") from e
        self.estado = "Confirmada"

    def cancelar(self):
        """Cancela la reserva si no está cancelada ni procesada."""
        if self.estado in ("Cancelada", "Procesada"):
            raise ReservaError(f"No se puede cancelar una reserva {self.estado}")
        self.estado = "Cancelada"

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Procesa una reserva confirmada y calcula su costo final.
        Método sobrecargado: procesar(), procesar(0.19) o procesar(0.19, 0.10)."""
        if self.estado != "Confirmada":
            raise ReservaError(f"Solo se puede procesar una reserva confirmada (estado actual: {self.estado})")
        try:
            costo = self.servicio.calcular_costo(impuesto, descuento)
        except CalculoError as e:
            raise ReservaError("No se pudo procesar la reserva por un error de cálculo") from e
        else:
            self.costo_final = costo
            self.estado = "Procesada"
            logger.info(f"Reserva #{self._id} procesada. Costo final: ${costo:,.0f}")
            return costo
        finally:
            logger.info(f"Procesamiento de la reserva #{self._id} finalizado")

    def describir(self):
        texto = (f"Reserva #{self._id} | {self.cliente.obtener_nombre()} | {self.servicio.nombre} | "
                 f"{self.duracion} {self.unidad} | {self.estado}")
        if self.costo_final is not None:
            texto += f" | Costo final: ${self.costo_final:,.0f}"
        return texto
