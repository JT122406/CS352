import sys
import socket


def serverstart(socket1, port, address):
    socketserver = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    socketserver.bind((address, port))
    socketserver.listen(1)
    return socketserver


def getKeys():
    with open(sys.argv[2], 'r') as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    server_socket = serverstart(socket, int(sys.argv[1]), 'localhost')
    keys = getKeys()

    while True:
        client_socket, client_address = server_socket.accept()

        data = client_socket.recv(1024).decode().strip()
        if data != 'HELLO':
            print("Error: Invalid message")
            client_socket.close()
            exit()
