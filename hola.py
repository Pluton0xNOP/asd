import RPi.GPIO as GPIO
import time
import socket

# Configuración de pines y variables
RELAY_PIN = 10
EMISOR_PIN = 23
RECEPTOR_PIN = 24

IP_SERVIDOR = '192.168.101.30'
PUERTO_SERVIDOR = 12345
MENSAJE = "iniciar_deteccion"

# Configuración inicial de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(EMISOR_PIN, GPIO.OUT)
GPIO.setup(RECEPTOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(RELAY_PIN, GPIO.HIGH)
GPIO.output(EMISOR_PIN, GPIO.LOW)

def enviar_mensaje_persistente(cliente_socket, mensaje):
    """Envía un mensaje al servidor utilizando una conexión persistente."""
    try:
        cliente_socket.sendall(mensaje.encode())
        print(f"Mensaje enviado: {mensaje}")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")

def conectar_servidor():
    """Intenta conectarse al servidor, reintentando en caso de fallo."""
    while True:
        try:
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente_socket.connect((IP_SERVIDOR, PUERTO_SERVIDOR))
            print("Conexión establecida con el servidor.")
            return cliente_socket
        except Exception as e:
            print(f"No se pudo establecer la conexión con el servidor: {e}. Reintentando en 5 segundos...")
            time.sleep(5)

def activar_rele():
    """Activa el relé durante 1 segundo después de esperar 4 segundos."""
    print("Esperando 4 segundos antes de activar el relé")
    time.sleep(4)
    print("Activando relé por 1 segundo")
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(1)
    print("Desactivando relé")
    GPIO.output(RELAY_PIN, GPIO.HIGH)

# Conectar al servidor
cliente_socket = conectar_servidor()

try:
    print("Iniciando el bucle principal del script")
    while True:
        GPIO.output(EMISOR_PIN, GPIO.HIGH)  # Indicador de que está en espera

        # Verificar si se detecta contacto en el pin de receptor
        if GPIO.input(RECEPTOR_PIN) == GPIO.HIGH:
            print("Contacto detectado, enviando mensaje al servidor para iniciar la detección")
            enviar_mensaje_persistente(cliente_socket, MENSAJE)
            activar_rele()  # Llamar a la función para activar el relé
            # Esperar un breve período antes de volver a verificar
            time.sleep(2)
        else:
            print("Esperando contacto...")

        time.sleep(0.1)  # Esperar brevemente antes de la siguiente lectura

except KeyboardInterrupt:
    print("Interrupción del programa. Limpiando configuración GPIO.")
finally:
    cliente_socket.close()
    GPIO.cleanup()
    print("Conexión cerrada y configuración GPIO limpiada.")
