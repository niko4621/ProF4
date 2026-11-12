# MODULO: logger.py  |  APORTE: Nicolas Chacon Salgado
# Configura el archivo de logs donde se registran errores y eventos


import logging  #modulo estandar de Python para registrar mensajes
import os  #modulo para trabajar con carpetas y rutas

CARPETA_LOGS = "logs"  #nombre de la carpeta donde se guardara el archivo de logs
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")  #ruta completa del archivo de logs


def obtener_logger(nombre="SoftwareFJ"):  #funcion que entrega un logger ya configurado
    os.makedirs(CARPETA_LOGS, exist_ok=True)  #crea la carpeta de logs si no existe
    logger = logging.getLogger(nombre)  #obtiene o crea el logger con ese nombre
    if not logger.handlers:  #rvita duplicar manejadores si ya se configuro antes
        logger.setLevel(logging.INFO)  #registra mensajes desde nivel INFO hacia arriba
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")  #formato: fecha | nivel | mensaje
        archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  #manejador que escribe en el archivo
        archivo.setFormatter(formato)  #aplica el formato al archivo
        logger.addHandler(archivo)  #conecta el manejador de archivo al logger
        consola = logging.StreamHandler()  #manejador que tambien muestra los mensajes en pantalla
        consola.setFormatter(formato)  #aplica el mismo formato a la consola
        logger.addHandler(consola)  #conecta el manejador de consola al logger
    return logger  #devuelve el logger listo para usar