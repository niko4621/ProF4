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
    
    
class ReservaSala(Servicio):  #servicio hijo: reserva de salas de reuniones
    """reserva de una sala; cobra recargo si la sala es grande"""

    RECARGO_SALA_GRANDE = 0.20  #recargo del 20% para salas de mas de 20 personas

    def __init__(self, id_servicio, nombre, tarifa_hora, capacidad):  #agrega la capacidad de la sala
        super().__init__(id_servicio, nombre, tarifa_hora)  #reutiliza el constructor de Servicio
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:  #la capacidad debe ser un entero positivo
            raise ErrorValidacion(f"La capacidad '{capacidad}' debe ser un numero entero mayor que cero.")  #lanza error si no sirve
        self._capacidad = capacidad  #guarda la capacidad de personas

    @property 
    def capacidad(self):  #getter de la capacidad
        return self._capacidad  #devuelve la capacidad guardada

    def calcular_costo(self, horas):  #sobrescribe el calculo: tarifa por horas, con recargo si es grande
        self._validar_horas(horas)  #revisa las horas
        costo = self._tarifa_hora * horas  #costo normal: tarifa por cantidad de horas
        if self._capacidad > 20:  #si la sala es para mas de 20 personas
            costo = costo * (1 + self.RECARGO_SALA_GRANDE)  #aplica el recargo del 20%
        return costo  #devuelve el costo base

    def obtener_resumen(self):  #sobrescribe el metodo abstracto de Entidad
        return f"Servicio ID: {self.id} | Sala: {self._nombre} | Capacidad: {self._capacidad} personas | Tarifa: ${self._tarifa_hora:,.0f}/hora"  #resumen en una linea
    
    
class AlquilerEquipo(Servicio):  #servicio hijo: alquiler de equipos
    """alquiler de un equipo; suma un seguro fijo por cada alquiler"""

    def __init__(self, id_servicio, nombre, tarifa_hora, tipo_equipo, seguro=20000):  #agrega el tipo de equipo y el seguro (opcional)
        super().__init__(id_servicio, nombre, tarifa_hora)  #reutiliza el constructor de Servicio
        if tipo_equipo is None or str(tipo_equipo).strip() == "":  #el tipo de equipo es obligatorio
            raise ParametroFaltanteError("El tipo de equipo es obligatorio.")  #lanza error si falta
        if isinstance(seguro, bool) or not isinstance(seguro, (int, float)) or seguro < 0:  #el seguro no puede ser negativo
            raise ErrorValidacion(f"El seguro '{seguro}' debe ser un numero mayor o igual a cero.")  #lanza error si no sirve
        self._tipo_equipo = str(tipo_equipo).strip()  #guarda el tipo de equipo (ej: portatil, proyector)
        self._seguro = float(seguro)  #guarda el valor del seguro

    @property 
    def tipo_equipo(self):  #getter del tipo de equipo
        return self._tipo_equipo  #devuelve el tipo de equipo

    def calcular_costo(self, horas):  #sobrescribe el calculo: tarifa por horas mas el seguro
        self._validar_horas(horas)  #revisa las horas
        return self._tarifa_hora * horas + self._seguro  #costo de las horas mas el seguro fijo

    def obtener_resumen(self):  #sobrescribe el metodo abstracto de Entidad
        return f"Servicio ID: {self.id} | Equipo: {self._nombre} ({self._tipo_equipo}) | Tarifa: ${self._tarifa_hora:,.0f}/hora | Seguro: ${self._seguro:,.0f}"  #resumen en una linea
    
    
class AsesoriaEspecializada(Servicio):  #servicio hijo: asesorias con un experto
    """asesoria cuyo precio cambia segun el nivel del asesor"""

    FACTORES_NIVEL = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  #multiplicador de la tarifa segun el nivel

    def __init__(self, id_servicio, nombre, tarifa_hora, nivel):  #agrega el nivel del asesor
        super().__init__(id_servicio, nombre, tarifa_hora)  #reutiliza el constructor de Servicio
        nivel_limpio = str(nivel).strip().lower() if nivel is not None else ""  #pasa el nivel a minusculas para compararlo
        if nivel_limpio not in self.FACTORES_NIVEL:  #el nivel debe ser junior, senior o experto
            raise ErrorValidacion(f"El nivel '{nivel}' no es valido. Use: junior, senior o experto.")  #lanza error si no existe
        self._nivel = nivel_limpio  #guarda el nivel del asesor

    @property 
    def nivel(self):  #getter del nivel
        return self._nivel  #devuelve el nivel guardado

    def calcular_costo(self, horas):  #sobrescribe el calculo: tarifa por horas por el factor del nivel
        self._validar_horas(horas)  #revisa las horas
        return self._tarifa_hora * horas * self.FACTORES_NIVEL[self._nivel]  #un experto cobra el doble que un junior

    def obtener_resumen(self):  #sobrescribe el metodo abstracto de Entidad
        return f"Servicio ID: {self.id} | Asesoria: {self._nombre} | Nivel: {self._nivel} | Tarifa: ${self._tarifa_hora:,.0f}/hora"  #resumen en una linea
    
    
# Pruebas del modulo (solo se ejecutan al correr: python servicios.py)
if __name__ == "__main__":  #este bloque solo corre si se ejecuta este archivo directamente
    print("--------------------------------------------------")  
    print("          PRUEBAS DE LA CLASE SERVICIOS           ")  
    print("--------------------------------------------------")  

    print("\n1. Creando los tres servicios y calculando su costo por 3 horas:")  #prueba de polimorfismo
    sala = ReservaSala("SRV-01", "Sala Andes", 50000, 25)  #sala grande: tendra recargo
    equipo = AlquilerEquipo("SRV-02", "Portatil Lenovo", 15000, "portatil")  #equipo con seguro de 20.000
    asesoria = AsesoriaEspecializada("SRV-03", "Asesoria en Python", 80000, "senior")  #asesor senior: factor 1.5
    for servicio in [sala, equipo, asesoria]:  #recorre los tres servicios con el mismo codigo
        print("  ", servicio.obtener_resumen())  #cada uno muestra su propio resumen (sobrescritura)
        print("   Costo base 3 h: $", f"{servicio.calcular_costo(3):,.0f}")  #cada uno calcula distinto (polimorfismo)

    print("\n2. Probando la 'sobrecarga' de calcular_costo_total:")  #mismo metodo con distintos parametros
    print("   Solo horas:              $", f"{asesoria.calcular_costo_total(2):,.0f}")  #sin impuesto ni descuento
    print("   Con IVA 19%:             $", f"{asesoria.calcular_costo_total(2, 0.19):,.0f}")  #con impuesto
    print("   Con IVA y 10% descuento: $", f"{asesoria.calcular_costo_total(2, 0.19, 0.10):,.0f}")  #con impuesto y descuento

    print("\n3. Probando validaciones (deben salir errores controlados):")  #pruebas de datos invalidos
    pruebas = [  #lista de intentos que deben fallar
        lambda: ReservaSala("SRV-04", "", 50000, 10),  #nombre vacio
        lambda: AlquilerEquipo("SRV-05", "Proyector", -100, "proyector"),  #tarifa negativa
        lambda: AsesoriaEspecializada("SRV-06", "Asesoria Java", 70000, "maestro"),  #nivel que no existe
        lambda: sala.calcular_costo_total(0),  #cero horas
    ]
    for prueba in pruebas:  #ejecuta cada intento
        try:  #intenta ejecutar la operacion
            prueba()  #llama a la prueba
        except ErrorValidacion as error:  #captura los errores de validacion propios
            print(f"   -> [{error.codigo}] {error}")  #muestra el codigo y el mensaje del error

    print("\n--------------------------------------------------") 
    print("       TODAS LAS PRUEBAS FUNCIONARON BIEN         ") 
    print("--------------------------------------------------")  