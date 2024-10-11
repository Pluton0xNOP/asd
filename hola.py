import subprocess

def ping_equipo(ip_address, packet_size):
    try:
        # Comando para Windows
        command = ["ping", ip_address, "-l", str(packet_size), "-n", "1"]

        # Comando para Unix/Linux/Mac
        # command = ["ping", "-s", str(packet_size), "-c", "1", ip_address]

        # Ejecutar el comando de ping
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Verificar el resultado del ping
        if "Tiempo de espera agotado" in result.stdout or "Request timed out" in result.stdout:
            print(f"No se recibió respuesta del equipo {ip_address}.")
        elif result.returncode == 0:
            print(f"Respuesta recibida de {ip_address} con tamaño de paquete {packet_size} bytes.")
        else:
            print(f"El ping falló. Código de retorno: {result.returncode}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Dirección IP y tamaño del paquete
ip_address = "192.168.101.30"
packet_size = 64  # Puedes ajustar el tamaño del paquete

# Ejecutar la función de ping
ping_equipo(ip_address, packet_size)
