import sys
import socket

if __name__ == "__main__":
    port = int(sys.argv[1])
    keyFileName = sys.argv[2]

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('localhost', port))
    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()

        data = client_socket.recv(1024).decode().strip()
        if data != 'HELLO':
            print("Error: Invalid message")
            client_socket.close()
            break
