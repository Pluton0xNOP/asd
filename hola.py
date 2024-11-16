import RPi.GPIO as GPIO
import time
import socket
import threading

# Configuración de pines
RELAY1_PIN = 16
EMISOR1_PIN = 19
RECEPTOR1_PIN = 26
RELAY2_PIN = 12
EMISOR2_PIN = 20
RECEPTOR2_PIN = 21

IP_DESTINO1 = '192.168.101.37'
IP_DESTINO2 = '192.168.101.52'
PUERTO = 12345

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY1_PIN, GPIO.OUT)
GPIO.setup(EMISOR1_PIN, GPIO.OUT)
GPIO.setup(RECEPTOR1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RELAY2_PIN, GPIO.OUT)
GPIO.setup(EMISOR2_PIN, GPIO.OUT)
GPIO.setup(RECEPTOR2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(RELAY1_PIN, GPIO.HIGH)
GPIO.output(EMISOR1_PIN, GPIO.LOW)
GPIO.output(RELAY2_PIN, GPIO.HIGH)
GPIO.output(EMISOR2_PIN, GPIO.LOW)

# Función para enviar mensajes
def enviar_mensaje_linea(mensaje, IP_DESTINO, PUERTO_DESTINO):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(mensaje.encode(), (IP_DESTINO, PUERTO_DESTINO))
        time.sleep(0.5)
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
    finally:
        sock.close()

# Función para activar relé
def activar_rele(pin_rele):
    print(f"Esperando 4 segundos antes de activar el relé en el pin {pin_rele}")
    time.sleep(2.5)
    GPIO.output(pin_rele, GPIO.LOW)
    time.sleep(1.2)
    GPIO.output(pin_rele, GPIO.HIGH)
    print(f"Relé en pin {pin_rele} desactivado")

# Control de relé 1
def controlar_rele1():
    GPIO.output(EMISOR1_PIN, GPIO.HIGH)
    while True:
        if GPIO.input(RECEPTOR1_PIN) == GPIO.HIGH:
            time.sleep(0.05)
            if GPIO.input(RECEPTOR1_PIN) == GPIO.HIGH:
                enviar_mensaje_linea('linea2', IP_DESTINO1, PUERTO)
                activar_rele(RELAY1_PIN)
        time.sleep(0.1)

# Control de relé 2
def controlar_rele2():
    GPIO.output(EMISOR2_PIN, GPIO.HIGH)
    while True:
        if GPIO.input(RECEPTOR2_PIN) == GPIO.HIGH:
            time.sleep(0.05)
            if GPIO.input(RECEPTOR2_PIN) == GPIO.HIGH:
                enviar_mensaje_linea('linea1', IP_DESTINO2, PUERTO)
                activar_rele(RELAY2_PIN)
        time.sleep(0.1)

# Función principal
def main():
    hilo_rele1 = threading.Thread(target=controlar_rele1)
    hilo_rele2 = threading.Thread(target=controlar_rele2)

    hilo_rele1.start()
    hilo_rele2.start()

    hilo_rele1.join()
    hilo_rele2.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupción del usuario. Limpiando GPIO...")
    finally:
        GPIO.cleanup()
