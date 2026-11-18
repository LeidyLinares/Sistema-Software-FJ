"""Clase Cliente con encapsulación y validaciones."""
from entidad import Entidad
from excepciones import ClienteError


class Cliente(Entidad):
    """Cliente de la empresa Software FJ."""

    def __init__(self, nombre, documento):
        super().__init__()  # Genera el id único de la entidad

        # Validación del nombre: debe ser texto no vacío
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteError("El nombre no puede estar vacío")

        # Validación del documento: solo dígitos y mínimo 5 caracteres
        documento = str(documento).strip()
        if not documento.isdigit() or len(documento) < 5:
            raise ClienteError("Documento inválido: mínimo 5 dígitos numéricos")

        self.__nombre = nombre.strip()  # Atributo privado (encapsulación)
        self.__documento = documento    # Atributo privado (encapsulación)

    def obtener_nombre(self):
        """Getter del nombre."""
        return self.__nombre

    def obtener_documento(self):
        """Getter del documento."""
        return self.__documento

    def describir(self):
        """Descripción del cliente."""
        return f"Cliente #{self._id}: {self.__nombre} (Doc: {self.__documento})"
