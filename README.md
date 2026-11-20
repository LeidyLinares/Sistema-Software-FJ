# Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto desarrollado para el curso de Programación (213023) - UNAD.

## Objetivos

Desarrollar un sistema orientado a objetos para gestionar clientes, servicios y reservas de la empresa Software FJ, aplicando manejo de excepciones para garantizar estabilidad y robustez.

## Tecnologías

- Python 3
- Programación Orientada a Objetos (abstracción, herencia, polimorfismo y encapsulación)

## Integrantes

- Leidy Liliana Linares Parra
- Dary Ramírez Marín

## Funcionalidades

- Gestión de clientes con validación de datos.
- Gestión de servicios: reserva de salas, alquiler de equipos y asesorías especializadas, con validación de parámetros y control de disponibilidad.
- Gestión de reservas con duración y estados (Pendiente, Confirmada, Procesada, Cancelada).
- Cálculo de costos sobrecargado: con impuestos y descuentos opcionales.
- Listas internas para clientes, servicios y reservas (sin base de datos).
- Manejo de excepciones personalizadas (`ClienteError`, `ServicioError`, `ServicioNoDisponibleError`, `CalculoError`, `ReservaError`) y encadenamiento de excepciones (`raise ... from`).
- Registro de eventos y errores en `logs/sistema.log`.
- Simulación de 22 operaciones sin que el programa se detenga ante errores.

## Estructura

```
src/
├── excepciones.py     # Excepciones personalizadas
├── entidad.py         # Clase abstracta Entidad
├── cliente.py         # Clase Cliente
├── servicio.py        # Servicio (abstracta) y servicios derivados
├── reserva.py         # Clase Reserva
├── gestor.py          # Listas internas del sistema
├── logger_config.py   # Configuración de logs
└── main.py            # Simulación de operaciones
```

## Ejecución

```bash
python src/main.py
```
```

## Ejecución

```bash
python src/main.py
