"""Gestor del sistema: administra las listas internas (sin base de datos)."""
from cliente import Cliente
from servicio import Servicio
from reserva import Reserva
from excepciones import ClienteError, ServicioError


class GestorFJ:
    """Guarda clientes, servicios y reservas en listas internas."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    def registrar_cliente(self, nombre=None, documento=None):
        """Crea y registra un cliente; no permite documentos repetidos."""
        try:
            cliente = Cliente(nombre, documento)
        except ClienteError as e:
            raise ClienteError(f"No se pudo registrar el cliente: {e}") from e
        if any(c.obtener_documento() == cliente.obtener_documento() for c in self._clientes):
            raise ClienteError(f"Ya existe un cliente con el documento {cliente.obtener_documento()}")
        self._clientes.append(cliente)
        return cliente

    def registrar_servicio(self, servicio):
        """Registra un servicio ya creado."""
        if not isinstance(servicio, Servicio):
            raise ServicioError("Solo se pueden registrar objetos de tipo Servicio")
        self._servicios.append(servicio)
        return servicio

    def crear_reserva(self, cliente=None, servicio=None):
        """Crea y registra una reserva."""
        reserva = Reserva(cliente, servicio)
        self._reservas.append(reserva)
        return reserva

    def obtener_reserva(self, indice):
        """Devuelve una reserva por posición (puede lanzar IndexError)."""
        return self._reservas[indice]

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)
