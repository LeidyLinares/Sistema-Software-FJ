"""Excepciones personalizadas del sistema Software FJ."""


class SistemaError(Exception):
    """Excepción base: todas las demás heredan de ella."""
    pass


class ClienteError(SistemaError):
    """Datos de cliente inválidos, faltantes o duplicados."""
    pass


class ServicioError(SistemaError):
    """Datos de servicio inválidos o faltantes."""
    pass


class ServicioNoDisponibleError(ServicioError):
    """El servicio solicitado no está disponible."""
    pass


class CalculoError(SistemaError):
    """Cálculo inconsistente (impuestos o descuentos fuera de rango)."""
    pass


class ReservaError(SistemaError):
    """La reserva no puede crearse o realizar la operación pedida."""
    pass
