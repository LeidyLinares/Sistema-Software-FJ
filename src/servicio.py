"""Clase abstracta Servicio y tres servicios especializados."""
from abc import abstractmethod
from entidad import Entidad
from excepciones import ServicioError, ServicioNoDisponibleError, CalculoError


class Servicio(Entidad):
    """Servicio abstracto que ofrece la empresa Software FJ."""

    unidad = "unidades"  # Unidad de la duración (se sobrescribe en cada servicio)

    def __init__(self, nombre=None):
        super().__init__()
        if nombre is None:
            raise ServicioError("Falta el parámetro: nombre del servicio")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioError("El nombre del servicio no puede estar vacío")
        self.nombre = nombre.strip()
        self.disponible = True   # Estado de disponibilidad
        self.duracion = None     # Se asigna en cada servicio derivado

    # ----- Disponibilidad -----
    def marcar_no_disponible(self):
        """Marca el servicio como no disponible."""
        self.disponible = False

    def verificar_disponibilidad(self):
        """Lanza ServicioNoDisponibleError si el servicio no está disponible."""
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible")

    # ----- Validaciones y cálculos -----
    @staticmethod
    def _validar_cantidad(valor, nombre_param, maximo):
        """Valida que la duración exista, sea numérica, positiva y no exceda el máximo."""
        if valor is None:
            raise ServicioError(f"Falta el parámetro: {nombre_param}")
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ServicioError(f"La cantidad de {nombre_param} debe ser un número")
        if valor <= 0:
            raise ServicioError(f"La cantidad de {nombre_param} debe ser mayor que cero")
        if valor > maximo:
            raise ServicioError(f"La cantidad de {nombre_param} no puede superar {maximo}")
        return valor

    @staticmethod
    def _aplicar_ajustes(base, impuesto, descuento):
        """Aplica descuento e impuesto (fracciones entre 0 y 1) al costo base."""
        for nombre, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise CalculoError(f"El {nombre} debe ser un número")
            if not 0 <= valor <= 1:
                raise CalculoError(f"El {nombre} debe estar entre 0 y 1 (0% y 100%)")
        return base * (1 - descuento) * (1 + impuesto)

    @abstractmethod
    def validar_parametros(self):
        """Cada servicio valida sus propios parámetros."""
        pass

    @abstractmethod
    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """Costo del servicio. Método sobrecargado mediante parámetros opcionales:
        calcular_costo(), calcular_costo(0.19) o calcular_costo(0.19, 0.10)."""
        pass


class ReservaSala(Servicio):
    """Reserva de salas: $50.000 por hora (máximo 12 horas)."""

    unidad = "horas"

    def __init__(self, nombre=None, horas=None):
        super().__init__(nombre)
        self.duracion = horas
        self.validar_parametros()

    def validar_parametros(self):
        self.duracion = self._validar_cantidad(self.duracion, "horas", 12)

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        return self._aplicar_ajustes(self.duracion * 50000, impuesto, descuento)

    def describir(self):
        return f"Reserva de sala '{self.nombre}' por {self.duracion} horas ($50.000 por hora)"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: $30.000 por día (máximo 30 días)."""

    unidad = "días"

    def __init__(self, nombre=None, dias=None):
        super().__init__(nombre)
        self.duracion = dias
        self.validar_parametros()

    def validar_parametros(self):
        self.duracion = self._validar_cantidad(self.duracion, "días", 30)

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        return self._aplicar_ajustes(self.duracion * 30000, impuesto, descuento)

    def describir(self):
        return f"Alquiler del equipo '{self.nombre}' por {self.duracion} días ($30.000 por día)"


class AsesoriaEspecializada(Servicio):
    """Asesoría especializada: $80.000 por hora (máximo 8 horas)."""

    unidad = "horas"

    def __init__(self, nombre=None, horas=None):
        super().__init__(nombre)
        self.duracion = horas
        self.validar_parametros()

    def validar_parametros(self):
        self.duracion = self._validar_cantidad(self.duracion, "horas", 8)

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        return self._aplicar_ajustes(self.duracion * 80000, impuesto, descuento)

    def describir(self):
        return f"Asesoría especializada '{self.nombre}' por {self.duracion} horas ($80.000 por hora)"
