"""Clase abstracta Servicio y tres servicios derivados."""
from abc import abstractmethod
from entidad import Entidad
from excepciones import ServicioError


class Servicio(Entidad):
    """Servicio abstracto que ofrece la empresa."""

    def __init__(self, nombre):
        super().__init__()
        # Validación del nombre del servicio
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioError("El nombre del servicio no puede estar vacío")
        self.nombre = nombre.strip()

    @staticmethod
    def _validar_cantidad(valor, unidad):
        """Valida que la cantidad (horas/días) sea un número mayor que cero."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ServicioError(f"La cantidad de {unidad} debe ser un número")
        if valor <= 0:
            raise ServicioError(f"La cantidad de {unidad} debe ser mayor que cero")
        return valor

    @abstractmethod
    def calcular_costo(self):
        """Cada servicio calcula su costo de forma distinta."""
        pass

    def describir(self):
        """Descripción general del servicio (usa el costo polimórfico)."""
        return f"{self.__class__.__name__} '{self.nombre}' - Costo: ${self.calcular_costo():,.0f}"


class ReservaSala(Servicio):
    """Reserva de salas: $50.000 por hora."""

    def __init__(self, nombre, horas):
        super().__init__(nombre)
        self.horas = self._validar_cantidad(horas, "horas")

    def calcular_costo(self):
        return self.horas * 50000


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: $30.000 por día."""

    def __init__(self, nombre, dias):
        super().__init__(nombre)
        self.dias = self._validar_cantidad(dias, "días")

    def calcular_costo(self):
        return self.dias * 30000


class AsesoriaEspecializada(Servicio):
    """Asesoría especializada: $80.000 por hora."""

    def __init__(self, nombre, horas):
        super().__init__(nombre)
        self.horas = self._validar_cantidad(horas, "horas")

    def calcular_costo(self):
        return self.horas * 80000
