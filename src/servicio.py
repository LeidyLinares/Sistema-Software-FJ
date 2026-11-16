from abc import ABC, abstractmethod

class Servicio(ABC):

    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular_costo(self):
        pass
class ReservaSala(Servicio):

    def __init__(self, nombre, horas):
        super().__init__(nombre)
        self.horas = horas

    def calcular_costo(self):
        return self.horas * 50000
      class AlquilerEquipo(Servicio):

    def __init__(self, nombre, dias):
        super().__init__(nombre)
        self.dias = dias

    def calcular_costo(self):
        return self.dias * 30000
      class AsesoriaEspecializada(Servicio):

    def __init__(self, nombre, horas):
        super().__init__(nombre)
        self.horas = horas

    def calcular_costo(self):
        return self.horas * 80000
