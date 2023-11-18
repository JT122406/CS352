import hashlib
import json
import secrets
import socket
import sys
from http import cookies


def serverStart(socket1, port, address):
    socketserver = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    socketserver.bind((address, port))
    socketserver.listen(1)
    return socketserver


def authenticateUser(user, password, file):
    with open(file) as json_file:
        data = json.load(json_file)
    for name in data.items():
        if name == user:
            values = data.get(name, [])
            if values[0] == hashlib.sha256(password + values[1]).hexdigest():
                return True

    return False


def ok(socket):
    socket.send("HTTP/1.1 200 OK\r\n\r\n")
    return


def main():
    server_socket = serverStart(socket, int(sys.argv[2]), sys.argv[1])
    file = open(sys.argv[3], "r")
    timeout = sys.argv[4]
    userDirect = sys.argv[5]

    ## post receive
    if authenticateUser("user", "password", file):
        cookie = cookies.SimpleCookie()
        cookie['sessionID'] = secrets.token_hex(8)
        ok(server_socket)
    else:
        ok(server_socket)



if __name__ == "__main__":
    main()
