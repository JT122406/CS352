import datetime
import hashlib
import json
import random
import socket
import sys


def serverStart(socket1, port, address, timeout):
    socketserver = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    socketserver.bind((address, port))
    socketserver.listen(1)
    socketserver.settimeout(timeout)
    return socketserver


def post_request(connection, data):
    logger("POST REQUEST")

    headers = data.split("\r\n")
    username = None
    password = None

    for header in headers:
        if header.startswith("username: "):
            username = header.split(":")[1].strip()
        elif header.startswith("password: "):
            password = header.split(":")[1].strip()

    if username is None or password is None:
        connection.sendall("HTTP/1.0 501 Not Implemented\r\n".encode())
        logger("LOGIN FAILED")
        return
    elif authenticateUser(username, password):
        logger("LOGIN SUCCESSFUL: " + username + " : " + password)

        ## cookie = createCookie(username)
        ok(connection, "Logged in!")
        #ok(connection, cookie)
    else:
        logger("LOGIN FAILED: " + username + ":" + password)
        ok(connection, "Login failed!")


def get_request(connection):
    return


def listen(socket2):
    while True:
        connection = None
        try:
            connection, client_address = socket2.accept()

            data = connection.recv(1024).decode()
            if not data:
                continue

            print(data)
            http_method, request_target, http_version = data.split()[:3]

            if http_method == "POST" and request_target == '/':
                post_request(connection, data)
            elif http_method == "GET":
                get_request(connection)
            else:
                connection.sendall("HTTP/1.0 501 NotImplemented\r\n".encode())
        finally:
            if connection is not None:
                connection.close()


def authenticateUser(user, password):
    with open(sys.argv[3]) as json_file:
        data = json.load(json_file)
    if user in data:
        return data[user][0] == hashlib.sha256(password.encode() + data[user][1].encode()).hexdigest()

    return False


def ok(sock, message):
    sock.sendall(("HTTP/1.0 200 OK\r\n" + message).encode())


def createCookie(id1):
    return json.dumps({
        id1: format(random.getrandbits(64), '016x'),
        'timestamp': datetime.datetime.now(datetime.UTC)
    })


def logger(message):
    print("SERVERLOG: " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + " " + message)


def main():
    server_socket = serverStart(socket, int(sys.argv[2]), sys.argv[1], int(sys.argv[4]))
    userDirect = sys.argv[5]
    listen(server_socket)


if __name__ == "__main__":
    main()
