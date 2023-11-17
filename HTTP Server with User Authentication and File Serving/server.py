import socket
import sys
import json
import hashlib


def serverStart(socket1, port, address):
    socketserver = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    socketserver.bind((address, port))
    socketserver.listen(1)
    return socketserver


def authenticateUser(user, password, file):
    with open(file) as json_file:
        data = json.load(json_file)
    for name, values in data.items():
        if name == user:
            if hashlib.sha256(password.encode('utf-8')).hexdigest() == values["password"]:
                return True

    return False


def main():
    server_socket = serverStart(socket, int(sys.argv[2]), sys.argv[1])
    file = open(sys.argv[3], "r")
    timeout = sys.argv[4]
    userDirect = sys.argv[5]


if __name__ == "__main__":
    main()
