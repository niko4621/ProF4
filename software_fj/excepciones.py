# MODULO: excepciones.py 
# APORTE: Nicolas Chacon Salagado
# Define la jerarquia de excepciones personalizadas del sistema


class ErrorSoftwareFJ(Exception):  #clase base de todas las excepciones propias; hereda de Exception
    """excepcion base del sistema Software FJ""" #docstring: describe la clase

    def __init__(self, mensaje, codigo="FJ-000"):  #recibe un mensaje y un codigo de error
        super().__init__(mensaje)  #llama al constructor de Exception para guardar el mensaje
        self.codigo = codigo  #guarda el codigo para identificar el tipo de error en los logs


class ErrorValidacion(ErrorSoftwareFJ):  #error para datos que no cumplen las reglas de validacion
    """se lanza cuando un dato no cumple las reglas de validacion""" 
    
    def __init__(self, mensaje):  #constructor con solo el mensaje
        super().__init__(mensaje, "FJ-001")  #asigna el codigo FJ-001 a los errores de validacion


class ClienteInvalidoError(ErrorValidacion):  #error especifico para datos de cliente invalidos
    """se lanza cuando los datos de un cliente son invalidos"""
    
    def __init__(self, mensaje):  
        super().__init__(mensaje)  #reutiliza el constructor de ErrorValidacion
        self.codigo = "FJ-002"  #sobrescribe el codigo con el propio de cliente


class ParametroFaltanteError(ErrorValidacion):  #error cuando falta un parametro obligatorio
    """se lanza cuando falta un parametro obligatorio"""
    
    def __init__(self, mensaje):  
        super().__init__(mensaje)  #reutiliza el constructor del padre
        self.codigo = "FJ-003"  #codigo para parametros faltantes


class ServicioNoDisponibleError(ErrorSoftwareFJ):  #error cuando un servicio no se puede usar
    """se lanza cuando se intenta usar un servicio no disponible"""
    
    def __init__(self, mensaje):  
        super().__init__(mensaje, "FJ-004")  #codigo FJ-004: servicio no disponible


class ReservaInvalidaError(ErrorSoftwareFJ):  #error por intentos de reserva incorrectos
    """se lanza cuando una reserva no cumple las condiciones necesarias"""
    
    def __init__(self, mensaje):  
        super().__init__(mensaje, "FJ-005")  #codigo FJ-005: reserva invalida


class OperacionNoPermitidaError(ErrorSoftwareFJ):  #error por operaciones fuera del flujo permitido
    """se lanza cuando se intenta una operacion no permitida en el estado actual"""
    
    def __init__(self, mensaje):  
        super().__init__(mensaje, "FJ-006")  #codigo FJ-006: operacion no permitida


class CalculoInconsistenteError(ErrorSoftwareFJ):  #error cuando un calculo da un resultado absurdo
    """se lanza cuando un calculo produce un resultado inconsistente"""
    
    def __init__(self, mensaje):  
        super().__init__(mensaje, "FJ-007")  #codigo FJ-007: calculo inconsistente