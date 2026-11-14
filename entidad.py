# entidad.py
# Clase abstracta para las entidades del sistema Software FJ
# Fase 4 - Programacion (UNAD)

from abc import ABC, abstractmethod
from datetime import datetime
import uuid


class Entidad(ABC):
    """Clase abstracta base para las entidades del sistema."""

    def __init__(self, id_entidad=None):
        # Si no nos pasan un id, generamos uno automatico
        if id_entidad is not None and str(id_entidad).strip() != "":
            self._id = str(id_entidad).strip()
        else:
            self._id = str(uuid.uuid4())[:8].upper()

        # Guardamos la fecha de creacion y estado activo
        self._fecha_creacion = datetime.now()
        self._activo = True

    # Getter para el id (solo lectura para que no lo cambien)
    @property
    def id(self):
        return self._id

    # Getter para la fecha de creacion
    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    # Getter para el estado activo
    @property
    def activo(self):
        return self._activo

    # Setter para cambiar el estado activo
    @activo.setter
    def activo(self, valor):
        # Validamos que sea booleano (True o False)
        if not isinstance(valor, bool):
            raise TypeError("El valor de activo debe ser True o False.")
        self._activo = valor

    # Metodos abstractos obligatorios para las clases hijas
    @abstractmethod
    def obtener_resumen(self):
        """Metodo abstracto: cada clase hija debe implementarlo con su propio formato."""
        pass

    @abstractmethod
    def validar_estado(self):
        """Metodo abstracto: cada clase hija debe implementarlo para verificar sus datos."""
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self._id} activo={self._activo}>"


# Alias de compatibilidad por si se importa como EntidadBase
EntidadBase = Entidad


# =============================================================================
# Demostracion y pruebas de la clase abstracta
# =============================================================================
if __name__ == "__main__":
    print("--------------------------------------------------")
    print("         PRUEBAS DE LA CLASE ENTIDAD (POO)        ")
    print("--------------------------------------------------")

    # 1. Demostrar el Principio de Abstraccion:
    # Verificamos que sea abstracta consultando sus metodos abstractos (sin instanciarla directamente)
    print("\n1. Verificando principio de Abstraccion:")
    if Entidad.__abstractmethods__:
        print("-> Correcto: La clase es abstracta y define los metodos obligatorios:")
        for metodo in sorted(Entidad.__abstractmethods__):
            print(f"   • {metodo}()")

    # 2. Demostrar el funcionamiento completo a traves de una clase hija (como Cliente):
    print("\n2. Demostrando funcionamiento completo mediante una clase hija:")
    class EntidadEjemplo(Entidad):
        def obtener_resumen(self):
            return f"Entidad de prueba con ID: {self.id}"

        def validar_estado(self):
            return self.activo

    # Creamos un objeto usando la clase hija
    obj = EntidadEjemplo("ENT-001")
    print("-> Objeto creado y funcionando al 100%:")
    print("   • ID de la entidad:", obj.id)
    print("   • Fecha de creacion:", obj.fecha_creacion)
    print("   • Estado activo:", obj.activo)
    print("   • Resumen:", obj.obtener_resumen())
    print("   • Validacion de estado:", obj.validar_estado())

    # 3. Probar el setter de activo:
    print("\n3. Probando setter de estado activo:")
    obj.activo = False
    print("   • Nuevo estado activo:", obj.activo)
    print("   • Validacion tras desactivar:", obj.validar_estado())

    print("\n--------------------------------------------------")
    print("      CLASE ENTIDAD 100% FUNCIONAL Y VERIFICADA   ")
    print("--------------------------------------------------")
