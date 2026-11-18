"""Excepciones personalizadas del sistema Software FJ."""


class SistemaError(Exception):
    """Excepción base: todas las demás heredan de ella."""
    pass


class ClienteError(SistemaError):
    """Se lanza cuando los datos de un cliente son inválidos."""
    pass


class ServicioError(SistemaError):
    """Se lanza cuando los datos de un servicio son inválidos."""
    pass


class ReservaError(SistemaError):
    """Se lanza cuando una reserva no puede crearse o cambiar de estado."""
    pass
