import socket
import ssl
import threading

def handle_client(connection, address):
    print(f"Connexion de {address}")
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print(f"Reçu de {address}: {data.decode()}")
            connection.sendall(data)
    finally:
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()

def main():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)

    print("Serveur en écoute sur le port 12345")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            connection = context.wrap_socket(client_socket, server_side=True)
            threading.Thread(target=handle_client, args=(connection, addr)).start()
    except Exception as e:
        print(f"Erreur du serveur : {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
