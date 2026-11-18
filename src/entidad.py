"""Clase abstracta base para las entidades del sistema."""
from abc import ABC, abstractmethod


class Entidad(ABC):
    """Representa cualquier entidad general (cliente, servicio, reserva)."""

    _contador = 0  # Contador compartido para generar identificadores únicos

    def __init__(self):
        Entidad._contador += 1          # Incrementa el contador global
        self._id = Entidad._contador    # Asigna un id único a la entidad

    def obtener_id(self):
        """Retorna el identificador único de la entidad."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe describirse a sí misma (polimorfismo)."""
        pass
