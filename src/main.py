print("Sistema Software FJ")
from cliente import Cliente
from servicio import ReservaSala
from reserva import Reserva

cliente1 = Cliente("Leidy Linares", "123456")

servicio1 = ReservaSala("Sala Principal", 3)

reserva1 = Reserva(cliente1, servicio1)

reserva1.confirmar()

print("Cliente:", cliente1.obtener_nombre())
print("Costo:", servicio1.calcular_costo())
print("Estado:", reserva1.estado)
