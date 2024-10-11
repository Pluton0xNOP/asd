import RPi.GPIO as GPIO
import time
import requests

# Pines GPIO
RELAY_PIN = 10
EMISOR_PIN = 23
RECEPTOR_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(EMISOR_PIN, GPIO.OUT)
GPIO.setup(RECEPTOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(RELAY_PIN, GPIO.HIGH)
GPIO.output(EMISOR_PIN, GPIO.LOW)

def activar_rele():
    print("Esperando 4 segundos antes de activar el rele")
    time.sleep(4)
    print("Activando relé por 1 segundo")
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(1)
    print("Desactivando relé")
    GPIO.output(RELAY_PIN, GPIO.HIGH)

def enviar_get_request():
    try:
        # URL del archivo PHP
        url = 'http://localhost/linea6/linea6.php?status=true'  # Reemplaza con la URL correcta
        response = requests.get(url)
        if response.status_code == 200:
            print("Solicitud GET exitosa")
        else:
            print(f"Error en la solicitud GET: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar la solicitud GET: {e}")

while True:
    try:
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        GPIO.output(EMISOR_PIN, GPIO.LOW)

        print("Iniciando el bucle principal del script")
        while True:
            GPIO.output(EMISOR_PIN, GPIO.HIGH)

            if GPIO.input(RECEPTOR_PIN) == GPIO.HIGH:
                print("Contacto detectado, activando temporizador")
                enviar_get_request()  # Enviar solicitud GET al archivo PHP
                activar_rele()
            else:
                print("Esperando contacto...")

            time.sleep(1)

    except Exception as e:
        print(f"Error detectado: {e}. Reiniciando el bucle...")
    except KeyboardInterrupt:
        print("Interrupción del programa. Limpiando configuración GPIO.")
        break
    finally:
        GPIO.cleanup()
