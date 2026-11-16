from excepciones import ClienteError

class Cliente:

    def __init__(self, nombre, documento):

        if nombre == "":
            raise ClienteError("El nombre no puede estar vacío")

        if len(documento) < 5:
            raise ClienteError("Documento inválido")

        self.__nombre = nombre
        self.__documento = documento

    def obtener_nombre(self):
        return self.__nombre

    def obtener_documento(self):
        return self.__documento
