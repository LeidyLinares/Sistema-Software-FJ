"""Clase Reserva que relaciona un cliente con un servicio."""
from entidad import Entidad
from cliente import Cliente
from servicio import Servicio
from excepciones import ReservaError


class Reserva(Entidad):
    """Reserva con control de estados: Pendiente, Confirmada, Cancelada."""

    def __init__(self, cliente, servicio):
        super().__init__()
        # Valida que los objetos recibidos sean del tipo correcto
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva requiere un cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva requiere un servicio válido")
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"  # Estado inicial

    def confirmar(self):
        """Confirma la reserva solo si está pendiente."""
        if self.estado != "Pendiente":
            raise ReservaError(f"No se puede confirmar una reserva {self.estado}")
        self.estado = "Confirmada"

    def cancelar(self):
        """Cancela la reserva si no está cancelada."""
        if self.estado == "Cancelada":
            raise ReservaError("La reserva ya estaba cancelada")
        self.estado = "Cancelada"

    def describir(self):
        return (f"Reserva #{self._id} | {self.cliente.obtener_nombre()} | "
                f"{self.servicio.nombre} | ${self.servicio.calcular_costo():,.0f} | {self.estado}")
