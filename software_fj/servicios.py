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
    
    
    def _validar_horas(self, horas):  #metodo interno que revisa que las horas sean validas
        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:  #las horas deben ser un numero mayor que cero
            raise ErrorValidacion(f"Las horas '{horas}' deben ser un numero mayor que cero.")  #lanza error si las horas no sirven

    def calcular_costo_total(self, horas, impuesto=0.0, descuento=0.0):  #"sobrecarga": se puede llamar con 1, 2 o 3 datos
        """calcula el costo final aplicando impuesto y descuento opcionales"""
        self._validar_horas(horas)  #revisa las horas antes de calcular
        if not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:  #el impuesto va como porcentaje entre 0 y 1 (0.19 = 19%)
            raise ErrorValidacion(f"El impuesto '{impuesto}' debe estar entre 0 y 1.")  #lanza error si el impuesto no sirve
        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:  #el descuento tambien va entre 0 y 1
            raise ErrorValidacion(f"El descuento '{descuento}' debe estar entre 0 y 1.")  #lanza error si el descuento no sirve
        costo_base = self.calcular_costo(horas)  #llama al calculo propio de cada servicio (polimorfismo)
        total = costo_base * (1 + impuesto) * (1 - descuento)  #suma el impuesto y resta el descuento
        if total <= 0: 
            raise CalculoInconsistenteError(f"El costo calculado ({total}) es inconsistente.")  #lanza error de calculo
        return round(total, 2)  #devuelve el total redondeado a 2 decimales

    def validar_estado(self):  #implementa el metodo abstracto de Entidad
        """revisa que el servicio tenga datos y este disponible"""
        return bool(self._nombre) and self._tarifa_hora > 0 and self.activo  #True solo si todo esta en orden

    def __str__(self):  #define como se muestra el servicio al imprimirlo
        return f"{self._nombre} (${self._tarifa_hora:,.0f}/hora)"  #ejemplo: Sala Andes ($50,000/hora)