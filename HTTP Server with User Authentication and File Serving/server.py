import socket
import sys


def serverStart(socket1, port, address):
    socketserver = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    socketserver.bind((address, port))
    socketserver.listen(1)
    return socketserver


def main():
    server_socket = serverStart(socket, int(sys.argv[2]), sys.argv[1])
    file = open(sys.argv[3], "r")
    timeout = sys.argv[4]
    userDirect = sys.argv[5]


if __name__ == "__main__":
    main()
