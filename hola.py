import socket

def cliente():
    # Dirección IP y puerto del servidor
    ip_servidor = "192.168.101.30"
    puerto_servidor = 12345

    # Crear un socket TCP/IP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar al servidor
    cliente_socket.connect((ip_servidor, puerto_servidor))

    # Enviar el mensaje
    mensaje = "linea6"
    cliente_socket.sendall(mensaje.encode())

    # Cerrar la conexión
    cliente_socket.close()

# Ejecutar el cliente
cliente()
