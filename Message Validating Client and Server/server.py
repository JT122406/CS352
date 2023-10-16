import hashlib
import sys
import socket


def serverStart(socket1, port, address):
    socketserver = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    socketserver.bind((address, port))
    socketserver.listen(1)
    return socketserver


def getKeys():
    with open(sys.argv[2], 'r') as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    server_socket = serverStart(socket, int(sys.argv[1]), 'localhost')
    keys = getKeys()

    try:
        client_socket, client_address = server_socket.accept()

        if client_socket.recv(1024).decode('utf-8').strip() != 'HELLO':
            print("Error: Invalid message")
            client_socket.close()
            exit()

        while True:
            match client_socket.recv(1024).decode().strip():
                case 'DATA':
                    sha256_hash = hashlib.sha256
                    while True:
                        message = client_socket.recv(1024).decode().strip()
                        if message == '.':
                            break

                case 'QUIT':
                    server_socket.close()
                    exit()
                case _:
                    print("Error: Invalid message")
                    client_socket.close()
                    exit()
    except Exception as e:
        print(e)
        server_socket.close()
        exit()
