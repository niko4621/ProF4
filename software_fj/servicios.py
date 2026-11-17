# MODULO: servicios.py
# APORTE: Nicolas Chacon Salgado
# Define la clase abstracta Servicio y los tres servicios que ofrece Software FJ


from abc import abstractmethod  #permite declarar metodos abstractos que las hijas deben implementar
from entidad import Entidad  #clase abstracta base del sistema
from excepciones import ErrorValidacion, ParametroFaltanteError, CalculoInconsistenteError  #excepciones propias del sistema


class Servicio(Entidad):  #clase abstracta: hereda de Entidad y agrega lo comun a todos los servicios
    """servicio general que ofrece Software FJ; no se puede crear directamente"""

    def __init__(self, id_servicio, nombre, tarifa_hora):  #constructor: recibe id, nombre y tarifa por hora
        super().__init__(id_entidad=id_servicio)  #el padre asigna el id (o lo genera), la fecha y el estado activo
        if nombre is None or str(nombre).strip() == "":  #valida que el nombre no venga vacio
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")  #lanza error si falta el nombre
        if isinstance(tarifa_hora, bool) or not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:  #la tarifa debe ser un numero positivo
            raise ErrorValidacion(f"La tarifa por hora '{tarifa_hora}' debe ser un numero mayor que cero.")  #lanza error si la tarifa no sirve
        self._nombre = str(nombre).strip()  #guarda el nombre sin espacios sobrantes (atributo protegido)
        self._tarifa_hora = float(tarifa_hora)  #guarda la tarifa como numero decimal

    @property  #convierte el metodo en un atributo de solo lectura
    def nombre(self):  #getter del nombre del servicio
        return self._nombre  #devuelve el nombre guardado

    @property 
    def tarifa_hora(self):  #getter de la tarifa por hora
        return self._tarifa_hora  #devuelve la tarifa guardada

    @abstractmethod  #obliga a cada servicio hijo a definir su propio calculo
    def calcular_costo(self, horas):  #calcula el costo base segun las horas (polimorfismo)
        """cada servicio calcula su costo base de forma distinta"""
        pass  #no tiene cuerpo aqui, lo implementan las clases hijas