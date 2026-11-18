"""Configuración del archivo de logs del sistema."""
import logging
import os

# Carpeta logs/ en la raíz del proyecto (un nivel arriba de src/)
RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(RUTA_LOGS, exist_ok=True)  # La crea si no existe

# Logger único para todo el sistema
logger = logging.getLogger("sistema_fj")
logger.setLevel(logging.INFO)

# Evita duplicar manejadores si el módulo se importa varias veces
if not logger.handlers:
    manejador = logging.FileHandler(
        os.path.join(RUTA_LOGS, "sistema.log"), mode="w", encoding="utf-8"
    )
    manejador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logger.addHandler(manejador)
