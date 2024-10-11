import RPi.GPIO as GPIO
import time
import socket

# Configuración de pines y variables
RECEPTOR_PIN = 24

IP_SERVIDOR = '192.168.1.255'  # Dirección de broadcast para enviar a toda la red local
PUERTO_SERVIDOR = 12345
MENSAJE = "linea6"

# Configuración inicial de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEPTOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def enviar_mensaje_broadcast(mensaje):
    """Envía un mensaje a toda la red local utilizando un socket UDP en modo broadcast."""
    try:
        # Crear un socket UDP
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cliente_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Enviar el mensaje al puerto especificado
        cliente_socket.sendto(mensaje.encode(), (IP_SERVIDOR, PUERTO_SERVIDOR))
        print(f"Mensaje enviado a la red local: {mensaje}")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
    finally:
        cliente_socket.close()

try:
    print("Iniciando el bucle principal del script")
    while True:
        # Comprobar si el receptor detecta un contacto
        if GPIO.input(RECEPTOR_PIN) == GPIO.HIGH:
            print("Contacto detectado, enviando mensaje a la red local")
            enviar_mensaje_broadcast(MENSAJE)
        else:
            print("Esperando contacto...")

        # Reducir el tiempo de espera para detectar más rápidamente
        time.sleep(0.1)

except Exception as e:
    print(f"Error detectado: {e}")
finally:
    GPIO.cleanup()
    print("Configuración GPIO limpiada.")
