import socket
import ssl

def main():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations("server.crt")

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = context.wrap_socket(raw_socket, server_hostname="localhost")

    connection.connect(('localhost', 12345))

    try:
        while True:
            message = input("Message à envoyer: ")
            if message.lower() == 'quit':
                break
            connection.sendall(message.encode())
            response = connection.recv(1024)
            print(f"Réponse du serveur: {response.decode()}")
    except Exception as e:
        print(f"Erreur du client : {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
