# cliente.py
# Clase Cliente con herencia, encapsulacion y validaciones
# Fase 4 - Programacion (UNAD)

import re
from entidad import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError


class Cliente(Entidad):
    """Clase que representa a un cliente de la empresa Software FJ."""

    def __init__(self, id_cliente, nombre, documento, email, telefono):
        # Llamamos al constructor de la clase padre (Entidad)
        super().__init__(id_entidad=id_cliente)

        # Declaramos los atributos privados usando doble guion bajo
        self.__nombre = ""
        self.__documento = ""
        self.__email = ""
        self.__telefono = ""

        # Usamos los setters para que pasen por las validaciones
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    # ==========================================
    # Getters y Setters con validaciones
    # ==========================================

    # --- Nombre ---
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Validar que no sea nulo ni vacio
        if valor is None or not isinstance(valor, str) or valor.strip() == "":
            raise ParametroFaltanteError("El nombre es obligatorio y no puede estar vacio.")

        valor_limpio = valor.strip()

        # Validar que tenga al menos 3 letras
        if len(valor_limpio) < 3:
            raise ClienteInvalidoError(f"El nombre '{valor_limpio}' debe tener al menos 3 letras.")

        # Validar que solo contenga letras y espacios (incluye tildes y ñ)
        patron_letras = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$"
        if not re.match(patron_letras, valor_limpio):
            raise ClienteInvalidoError(f"El nombre '{valor_limpio}' solo puede contener letras y espacios.")

        self.__nombre = valor_limpio

    # --- Documento ---
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        # Si nos pasan un numero entero, lo convertimos a texto
        if isinstance(valor, int):
            valor = str(valor)

        # Validar que no este vacio
        if valor is None or not isinstance(valor, str) or valor.strip() == "":
            raise ParametroFaltanteError("El documento de identificacion es obligatorio.")

        valor_limpio = valor.strip()

        # Validar que sea alfanumerico y tenga entre 5 y 15 caracteres
        if not valor_limpio.isalnum() or len(valor_limpio) < 5 or len(valor_limpio) > 15:
            raise ClienteInvalidoError(
                f"El documento '{valor_limpio}' es invalido. Debe tener entre 5 y 15 letras o numeros."
            )

        self.__documento = valor_limpio

    # --- Correo / Email ---
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        # Validar que no este vacio
        if valor is None or not isinstance(valor, str) or valor.strip() == "":
            raise ParametroFaltanteError("El correo electronico es obligatorio.")

        valor_limpio = valor.strip().lower()

        # Validamos el formato del correo con expresion regular
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
        if not re.match(patron_correo, valor_limpio):
            raise ClienteInvalidoError(f"El correo '{valor_limpio}' no tiene un formato valido (ejemplo: usuario@correo.com).")

        self.__email = valor_limpio

    # --- Telefono ---
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Si nos pasan un numero entero, lo convertimos a texto
        if isinstance(valor, int):
            valor = str(valor)

        # Validar que no este vacio
        if valor is None or not isinstance(valor, str) or valor.strip() == "":
            raise ParametroFaltanteError("El numero de telefono es obligatorio.")

        valor_limpio = valor.strip()

        # Validar que solo tenga numeros y entre 7 y 15 digitos (puede tener + al inicio)
        patron_tel = r"^\+?[0-9]{7,15}$"
        if not re.match(patron_tel, valor_limpio):
            raise ClienteInvalidoError(f"El telefono '{valor_limpio}' es invalido. Debe tener entre 7 y 15 numeros.")

        self.__telefono = valor_limpio

    # ==========================================
    # Metodos obligatorios de la clase abstracta
    # ==========================================

    def obtener_resumen(self):
        """Muestra los datos del cliente en una sola linea."""
        return f"Cliente ID: {self.id} | Nombre: {self.__nombre} | Doc: {self.__documento} | Email: {self.__email} | Tel: {self.__telefono}"

    def validar_estado(self):
        """Revisa que todos los atributos tengan valor y que este activo."""
        if self.__nombre and self.__documento and self.__email and self.__telefono and self.activo:
            return True
        return False

    def __str__(self):
        return f"{self.__nombre} (Doc: {self.__documento})"


# =============================================================================
# Pruebas sencillas para verificar que todo funciona
# =============================================================================
if __name__ == "__main__":
    print("--------------------------------------------------")
    print("      PRUEBAS DE LA CLASE CLIENTE Y ENTIDAD       ")
    print("--------------------------------------------------")

    # Prueba 1: Crear un cliente correcto
    print("\n1. Probando creacion de un cliente valido:")
    try:
        c1 = Cliente("CLI-01", "Carlos Gomez", "1098765432", "carlos@empresa.com", "3001234567")
        print("-> Cliente creado con exito:")
        print("  ", c1.obtener_resumen())
        print("   Fecha de registro:", c1.fecha_creacion)
        print("   Esta activo?:", c1.activo)
    except Exception as e:
        print("Error inesperado:", e)

    # Prueba 2: Correo mal escrito
    print("\n2. Probando validacion de correo sin arroba:")
    try:
        c2 = Cliente("CLI-02", "Mariana Lopez", "1020304050", "correo_sin_arroba.com", "3119876543")
    except ClienteInvalidoError as error:
        print("-> Error capturado correctamente:")
        print("  ", error)

    # Prueba 3: Nombre con numeros
    print("\n3. Probando validacion de nombre con numeros:")
    try:
        c3 = Cliente("CLI-03", "Juan 123", "11223344", "juan@test.com", "3005551234")
    except ClienteInvalidoError as error:
        print("-> Error capturado correctamente:")
        print("  ", error)

    # Prueba 4: Telefono demasiado corto
    print("\n4. Probando validacion de telefono muy corto:")
    try:
        c4 = Cliente("CLI-04", "Pedro Perez", "9876543", "pedro@test.com", "123")
    except ClienteInvalidoError as error:
        print("-> Error capturado correctamente:")
        print("  ", error)

    # Prueba 5: Probar getters y setters
    print("\n5. Probando encapsulacion (getters y setters):")
    print("-> Nombre actual (con getter):", c1.nombre)
    print("-> Modificando nombre con setter a 'Carlos Andres Gomez'...")
    c1.nombre = "Carlos Andres Gomez"
    print("-> Nuevo nombre verificado:", c1.nombre)

    print("\n--------------------------------------------------")
    print("       TODAS LAS PRUEBAS FUNCIONARON BIEN         ")
    print("--------------------------------------------------")