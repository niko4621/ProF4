# MODULO: main.py
# APORTE: Cristian Quiroz Barreto
# Programa principal del sistema Software FJ: integra clientes, servicios, reservas,
# polimorfismo, sobrecarga, manejo avanzado de excepciones y registro en logs.

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import (
    ErrorValidacion,
    ClienteInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
)
from logger import obtener_logger

logger = obtener_logger()


class SistemaSoftwareFJ:
    """Gestor principal en memoria (listas internas, sin base de datos) de Software FJ."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, id_cliente, nombre, documento, email, telefono):
        try:
            nuevo_cliente = Cliente(id_cliente, nombre, documento, email, telefono)
        except (ClienteInvalidoError, ParametroFaltanteError) as error:
            logger.error(f"[{error.codigo}] Error registrando cliente '{nombre}': {error}")
            print(f"   [ERROR {error.codigo}] Registro rechazado: {error}")
            return None
        else:
            self.clientes.append(nuevo_cliente)
            logger.info(f"Cliente registrado exitosamente: {nuevo_cliente.obtener_resumen()}")
            print(f"   [OK] Cliente registrado: {nuevo_cliente}")
            return nuevo_cliente
        finally:
            logger.info(f"Auditoria finalizada para intento de registro de cliente ({id_cliente}).")

    def registrar_servicio(self, servicio):
        if servicio.validar_estado():
            self.servicios.append(servicio)
            logger.info(f"Servicio agregado al catalogo: {servicio.obtener_resumen()}")
            print(f"   [OK] Servicio disponible: {servicio.obtener_resumen()}")
            return servicio
        return None

    def crear_reserva(self, id_reserva, cliente, servicio, horas):
        try:
            nueva_reserva = Reserva(id_reserva, cliente, servicio, horas)
        except (ReservaInvalidaError, ServicioNoDisponibleError) as error:
            logger.error(f"[{error.codigo}] Fallo al crear reserva {id_reserva}: {error}")
            print(f"   [ERROR {error.codigo}] Reserva rechazada: {error}")
            return None
        else:
            self.reservas.append(nueva_reserva)
            print(f"   [OK] Reserva creada en estado '{nueva_reserva.estado}': {nueva_reserva.id}")
            return nueva_reserva

    def mostrar_reporte_general(self):
        print("\n=====================================================================")
        print("            REPORTE CONSOLIDADO EN MEMORIA - SOFTWARE FJ             ")
        print("=====================================================================")
        print(f"\n-> Clientes activos registrados ({len(self.clientes)}):")
        for cli in self.clientes:
            print(f"   • {cli.obtener_resumen()}")

        print(f"\n-> Servicios en catalogo ({len(self.servicios)}):")
        for srv in self.servicios:
            print(f"   • {srv.obtener_resumen()}")

        print(f"\n-> Historial de reservas ({len(self.reservas)}):")
        for res in self.reservas:
            print(f"   • {res.obtener_resumen()}")
        print("=====================================================================\n")


def ejecutar_simulacion():
    print("=====================================================================")
    print("   SISTEMA INTEGRAL DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS     ")
    print("                         EMPRESA SOFTWARE FJ                         ")
    print("=====================================================================")
    logger.info("=== INICIO DE SIMULACION DEL SISTEMA SOFTWARE FJ ===")

    sistema = SistemaSoftwareFJ()

    # -------------------------------------------------------------------------
    # BLOQUE 1: GESTION DE CLIENTES (Operaciones 1 a 4)
    # -------------------------------------------------------------------------
    print("\n--- FASE 1: REGISTRO Y VALIDACION DE CLIENTES ---")

    print("\n[Operacion 1] Registro de cliente valido #1:")
    c1 = sistema.registrar_cliente("CLI-01", "Laura Valentina Mendez", "1020456789", "laura.mendez@correo.com", "3104567890")

    print("\n[Operacion 2] Registro de cliente valido #2:")
    c2 = sistema.registrar_cliente("CLI-02", "Andres Felipe Rojas", "80123456", "andres.rojas@empresa.co", "+573009876543")

    print("\n[Operacion 3] Intento de registro con correo invalido:")
    sistema.registrar_cliente("CLI-03", "Camila Torres", "1098765432", "camila_sin_arroba.com", "3151234567")

    print("\n[Operacion 4] Intento de registro con nombre vacio:")
    sistema.registrar_cliente("CLI-04", "   ", "1055667788", "vacio@test.com", "3201112233")

    # -------------------------------------------------------------------------
    # BLOQUE 2: CREACION DE SERVICIOS Y POLIMORFISMO (Operaciones 5 a 7)
    # -------------------------------------------------------------------------
    print("\n--- FASE 2: CATALOGO DE SERVICIOS, POLIMORFISMO Y SOBRECARGA ---")

    print("\n[Operacion 5] Creacion exitosa de los 3 servicios especializados:")
    s1 = sistema.registrar_servicio(ReservaSala("SRV-01", "Sala Ejecutiva Andes", 60000, 25))
    s2 = sistema.registrar_servicio(AlquilerEquipo("SRV-02", "Workstation Dell Precision", 25000, "Computador Portatil", seguro=30000))
    s3 = sistema.registrar_servicio(AsesoriaEspecializada("SRV-03", "Arquitectura Cloud & Python", 90000, "experto"))

    print("\n[Operacion 6] Demostracion de Polimorfismo y Sobrecarga de costos (4 horas):")
    for servicio in sistema.servicios:
        costo_base = servicio.calcular_costo(4)
        costo_iva = servicio.calcular_costo_total(4, impuesto=0.19)
        costo_promo = servicio.calcular_costo_total(4, impuesto=0.19, descuento=0.15)
        print(f"   • {servicio.nombre}:")
        print(f"     Base (4h): ${costo_base:,.2f} | Con IVA (19%): ${costo_iva:,.2f} | Con IVA + 15% Dcto: ${costo_promo:,.2f}")

    print("\n[Operacion 7] Creacion fallida de servicios con parametros invalidos:")
    intentos_servicios_invalidos = [
        ("Tarifa negativa en sala", lambda: ReservaSala("SRV-ERR1", "Sala Norte", -50000, 10)),
        ("Nivel inexistente en asesoria", lambda: AsesoriaEspecializada("SRV-ERR2", "Asesoria IA", 80000, "guru")),
        ("Tipo de equipo faltante", lambda: AlquilerEquipo("SRV-ERR3", "VideoBeam", 20000, "")),
    ]
    for descripcion, accion in intentos_servicios_invalidos:
        try:
            accion()
        except ErrorValidacion as error:
            logger.error(f"[{error.codigo}] Creacion de servicio fallida ({descripcion}): {error}")
            print(f"   [ERROR {error.codigo}] {descripcion} -> {error}")

    # -------------------------------------------------------------------------
    # BLOQUE 3: CICLO DE VIDA DE RESERVAS Y EXCEPCIONES (Operaciones 8 a 12)
    # -------------------------------------------------------------------------
    print("\n--- FASE 3: GESTION DE RESERVAS, ESTADOS Y EXCEPCIONES ---")

    print("\n[Operacion 8] Reserva exitosa de sala (Crear -> Confirmar -> Procesar con IVA):")
    r1 = sistema.crear_reserva("RES-01", c1, s1, 3)
    if r1:
        r1.confirmar()
        total_r1 = r1.procesar(impuesto=0.19)
        print(f"   -> {r1.obtener_resumen()} (Total cobrado: ${total_r1:,.2f})")

    print("\n[Operacion 9] Reserva exitosa de asesoria experta con descuento (10%):")
    r2 = sistema.crear_reserva("RES-02", c2, s3, 5)
    if r2:
        r2.confirmar()
        total_r2 = r2.procesar(impuesto=0.19, descuento=0.10)
        print(f"   -> {r2.obtener_resumen()} (Total cobrado: ${total_r2:,.2f})")

    print("\n[Operacion 10] Reserva creada y cancelada antes de procesar:")
    r3 = sistema.crear_reserva("RES-03", c1, s2, 2)
    if r3:
        r3.cancelar()
        print(f"   -> {r3.obtener_resumen()}")
        try:
            r3.confirmar()
        except OperacionNoPermitidaError as error:
            logger.warning(f"[{error.codigo}] Intento de operacion invalida sobre {r3.id}: {error}")
            print(f"   [ERROR {error.codigo}] Bloqueo de flujo correcto: {error}")

    print("\n[Operacion 11] Intento de reserva sobre un servicio desactivado:")
    s2.activo = False
    sistema.crear_reserva("RES-04", c2, s2, 4)

    print("\n[Operacion 12] Encadenamiento de excepciones al procesar con descuento > 100%:")
    r5 = sistema.crear_reserva("RES-05", c1, s1, 2)
    if r5:
        r5.confirmar()
        try:
            r5.procesar(impuesto=0.19, descuento=1.50)
        except CalculoInconsistenteError as error:
            print(f"   [ERROR {error.codigo}] Excepcion principal capturada: {error}")
            if error.__cause__:
                print(f"   -> Causa original encadenada (__cause__): {error.__cause__}")

    # -------------------------------------------------------------------------
    # REPORTE FINAL EN MEMORIA
    # -------------------------------------------------------------------------
    sistema.mostrar_reporte_general()
    logger.info("=== FIN DE SIMULACION DEL SISTEMA SOFTWARE FJ (EJECUCION ESTABLE) ===")
    print("Simulacion completada sin interrupciones. Revise el archivo 'logs/software_fj.log'.")


if __name__ == "__main__":
    ejecutar_simulacion()