import RPi.GPIO as GPIO
import time
import socket

# Configuración de pines y variables
RELAY_PIN = 10
EMISOR_PIN = 23
RECEPTOR_PIN = 24

IP_SERVIDOR = '192.168.101.30'
PUERTO_SERVIDOR = 12345
MENSAJE = "linea6"

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

def activar_rele():
    """Activa el relé durante 1 segundo después de esperar 4 segundos."""
    print("Esperando 4 segundos antes de activar el relé")
    time.sleep(4)
    print("Activando relé por 1 segundo")
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(1)
    print("Desactivando relé")
    GPIO.output(RELAY_PIN, GPIO.HIGH)

# Crear una conexión persistente
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cliente_socket.connect((IP_SERVIDOR, PUERTO_SERVIDOR))
    print("Conexión establecida con el servidor.")

    while True:
        try:
            # Reiniciar los pines a su estado inicial
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            GPIO.output(EMISOR_PIN, GPIO.LOW)

            print("Iniciando el bucle principal del script")
            while True:
                # Activar el emisor
                GPIO.output(EMISOR_PIN, GPIO.HIGH)

                # Comprobar si el receptor detecta un contacto de manera constante
                if GPIO.input(RECEPTOR_PIN) == GPIO.HIGH:
                    # Esperar un breve momento para evitar falsos positivos
                    time.sleep(0.05)
                    # Verificar nuevamente si el estado sigue siendo alto
                    if GPIO.input(RECEPTOR_PIN) == GPIO.HIGH:
                        print("Contacto detectado, enviando mensaje y activando temporizador")
                        enviar_mensaje_persistente(cliente_socket, MENSAJE)  # Enviar el mensaje primero
                        activar_rele()  # Luego activar el relé
                else:
                    print("Esperando contacto....")

                # Reducir el tiempo de espera para detectar más rápidamente
                time.sleep(0.1)

        except Exception as e:
            print(f"Error detectado: {e}. Reiniciando el bucle...")
            cliente_socket.close()
            break

except Exception as e:
    print(f"No se pudo establecer la conexión inicial con el servidor: {e}")
finally:
    cliente_socket.close()
    GPIO.cleanup()
    print("Conexión cerrada y configuración GPIO limpiada.")
