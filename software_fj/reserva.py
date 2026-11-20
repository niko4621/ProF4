# MODULO: reserva.py
# APORTE: Nicolas Chacon Salgado
# Define la clase Reserva, une un cliente con un servicio y controla su ciclo de vida


from entidad import Entidad  #clase abstracta base del sistema
from cliente import Cliente  #clase Cliente 
from servicios import Servicio  #clase abstracta de servicios
from excepciones import (  #excepciones propias que usa este modulo
    ErrorValidacion,  #errores de datos invalidos
    ReservaInvalidaError,  #reserva creada con datos incorrectos
    ServicioNoDisponibleError,  #servicio inactivo
    OperacionNoPermitidaError,  #accion que no corresponde al estado actual
    CalculoInconsistenteError,  #fallo al calcular el costo
)
from logger import obtener_logger  #funcion que entrega el logger configurado

logger = obtener_logger()  #logger compartido para registrar los eventos de las reservas


class Reserva(Entidad):  #hereda de Entidad: tiene id, fecha de creacion y estado activo
    """reserva de un servicio hecha por un cliente; pasa por estados en orden"""

    ESTADOS = ("pendiente", "confirmada", "cancelada", "procesada")  #estados posibles de una reserva

    def __init__(self, id_reserva, cliente, servicio, horas):  #recibe id, cliente, servicio y horas
        super().__init__(id_entidad=id_reserva)  #el padre asigna el id, la fecha y el estado activo
        if not isinstance(cliente, Cliente):  #el cliente debe ser un objeto Cliente
            raise ReservaInvalidaError("La reserva necesita un cliente valido.")  #lanza error si no lo es
        if not isinstance(servicio, Servicio):  #el servicio debe ser un objeto Servicio (o hijo)
            raise ReservaInvalidaError("La reserva necesita un servicio valido.")  #lanza error si no lo es
        if not servicio.activo:  #no se puede reservar un servicio desactivado
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no esta disponible.")  #lanza error de disponibilidad
        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:  #las horas deben ser un numero positivo
            raise ReservaInvalidaError(f"Las horas '{horas}' deben ser un numero mayor que cero.")  #lanza error si no sirven
        self._cliente = cliente  #guarda el cliente de la reserva
        self._servicio = servicio  #guarda el servicio reservado
        self._horas = horas  #guarda la cantidad de horas
        self._estado = "pendiente"  #toda reserva nueva empieza pendiente
        self._costo_final = None  #el costo se calcula solo al procesar
        logger.info(f"Reserva {self.id} creada: {cliente.nombre} - {servicio.nombre} - {horas} h")  #registra la creacion en el log

    @property  #atributo de solo lectura
    def cliente(self):  #getter del cliente
        return self._cliente  #devuelve el cliente

    @property  
    def servicio(self):  #getter del servicio
        return self._servicio  #devuelve el servicio

    @property 
    def horas(self):  #getter de las horas
        return self._horas  #devuelve las horas

    @property  
    def estado(self):  #getter del estado
        return self._estado  #devuelve el estado actual

    @property  
    def costo_final(self):  #getter del costo final
        return self._costo_final  #devuelve el costo (None si aun no se procesa)

    def obtener_resumen(self):  #implementa el metodo abstracto de Entidad
        costo = f"${self._costo_final:,.2f}" if self._costo_final is not None else "sin calcular"  #texto del costo segun si ya se proceso
        return f"Reserva ID: {self.id} | Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | Horas: {self._horas} | Estado: {self._estado} | Costo: {costo}"  #resumen en una linea

    def validar_estado(self):  #implementa el metodo abstracto de Entidad
        """revisa que la reserva, su cliente y su servicio esten en orden"""
        return self._estado in self.ESTADOS and self._cliente.validar_estado() and self._servicio.validar_estado()  #True solo si todo esta bien

    def __str__(self):  #define como se muestra la reserva al imprimirla
        return f"Reserva {self.id} ({self._estado})"  #ejemplo: Reserva RES-01 (confirmada)
    
    
    def confirmar(self):  #pasa la reserva de pendiente a confirmada
        if self._estado != "pendiente":  #solo se confirma una reserva pendiente
            raise OperacionNoPermitidaError(f"No se puede confirmar la reserva {self.id}: esta '{self._estado}'.")  #lanza error si no corresponde
        if not self._servicio.activo:  #el servicio pudo desactivarse despues de crear la reserva
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' ya no esta disponible.")  #lanza error de disponibilidad
        self._estado = "confirmada"  #cambia el estado
        logger.info(f"Reserva {self.id} confirmada")  #registra el cambio en el log

    def cancelar(self):  #cancela la reserva si aun no se ha procesado
        if self._estado in ("cancelada", "procesada"):  #no se cancela algo ya cancelado o ya cobrado
            raise OperacionNoPermitidaError(f"No se puede cancelar la reserva {self.id}: esta '{self._estado}'.")  #lanza error si no corresponde
        self._estado = "cancelada"  #cambia el estado
        logger.info(f"Reserva {self.id} cancelada")  #registra el cambio en el log
        
        
    def procesar(self, impuesto=0.19, descuento=0.0):  #calcula el costo final y cierra la reserva
        if self._estado != "confirmada":  #solo se procesa una reserva confirmada
            raise OperacionNoPermitidaError(f"No se puede procesar la reserva {self.id}: esta '{self._estado}'.")  #lanza error si no corresponde
        try:  #intenta calcular el costo
            total = self._servicio.calcular_costo_total(self._horas, impuesto, descuento)  #el servicio calcula su total (polimorfismo)
        except (ErrorValidacion, CalculoInconsistenteError) as e:  #si el calculo falla por datos o por resultado absurdo
            logger.error(f"Fallo el calculo de la reserva {self.id}: {e}")  #registra el error original en el log
            raise CalculoInconsistenteError(f"No se pudo procesar la reserva {self.id}.") from e  #encadena: lanza un error nuevo que guarda el original
        else:  #solo se ejecuta si el try no tuvo errores
            self._costo_final = total  #guarda el costo calculado
            self._estado = "procesada"  #cambia el estado
            logger.info(f"Reserva {self.id} procesada. Total: ${total:,.2f}")  #registra el exito en el log
            return total  #devuelve el total cobrado
        finally:  #se ejecuta siempre, haya error o no
            logger.info(f"Fin del intento de procesar la reserva {self.id}")  #deja constancia de que termino el intento
            
            
 
# Pruebas del modulo (solo se ejecutan al correr: python reserva.py)
if __name__ == "__main__":  #este bloque solo corre si se ejecuta este archivo directamente
    from servicios import ReservaSala, AsesoriaEspecializada  #servicios concretos para las pruebas
    from excepciones import ErrorSoftwareFJ  #clase base para capturar cualquier error propio

    print("--------------------------------------------------")  
    print("           PRUEBAS DE LA CLASE RESERVA            ")  #titulo de las pruebas
    print("--------------------------------------------------")  

    cliente = Cliente("CLI-01", "Carlos Gomez", "1098765432", "carlos@empresa.com", "3001234567")  #cliente valido (5 datos)
    sala = ReservaSala("SRV-01", "Sala Andes", 50000, 25)  #sala grande
    asesoria = AsesoriaEspecializada("SRV-03", "Asesoria en Python", 80000, "experto")  #asesoria experta

    print("\n1. Flujo correcto: crear -> confirmar -> procesar")  #prueba del camino normal
    r1 = Reserva("RES-01", cliente, sala, 3)  #crea la reserva
    r1.confirmar()  #la confirma
    r1.procesar()  #la procesa con IVA del 19% por defecto
    print("  ", r1.obtener_resumen())  #muestra el resultado

    print("\n2. Errores controlados (el programa no se detiene):")  #pruebas de operaciones invalidas
    r2 = Reserva("RES-02", cliente, asesoria, 2)  #reserva para probar el flujo de estados
    pruebas = [  #lista de intentos que deben fallar
        ("Procesar sin confirmar", lambda: r2.procesar()),  #todavia esta pendiente
        ("Cancelar ya procesada", lambda: r1.cancelar()),  #r1 ya fue procesada
        ("Reservar 0 horas", lambda: Reserva("RES-03", cliente, sala, 0)),  #horas invalidas
        ("Cliente que no es Cliente", lambda: Reserva("RES-04", "Carlos", sala, 2)),  #se pasa un texto
        ("Descuento mayor a 100%", lambda: (r2.confirmar(), r2.procesar(0.19, 1.5))),  #provoca error encadenado
    ]
    for nombre, prueba in pruebas:  #ejecuta cada intento
        try:  #intenta la operacion
            prueba()  #llama a la prueba
        except ErrorSoftwareFJ as error:  #captura cualquier error propio del sistema
            causa = f" | causa: {error.__cause__}" if error.__cause__ else ""  #muestra el error original si fue encadenado
            print(f"   {nombre}: [{error.codigo}] {error}{causa}")  #muestra el codigo y el mensaje

    print("\n3. Servicio no disponible:")  #prueba de disponibilidad
    sala.activo = False  #se desactiva la sala
    try:  #intenta reservarla
        Reserva("RES-05", cliente, sala, 1)  #debe fallar
    except ServicioNoDisponibleError as error:  #captura el error de disponibilidad
        print(f"   [{error.codigo}] {error}")  #muestra el error

    print("\n--------------------------------------------------")  
    print("       TODAS LAS PRUEBAS FUNCIONARON BIEN         ")  #mensaje final
    print("--------------------------------------------------")  