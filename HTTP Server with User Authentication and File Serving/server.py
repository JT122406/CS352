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

def handle_post_request(connection):
    return
def handle_get_request(connection):
    return

def listen(socket2):
    while True:
        connection = None
        try:
            connection, client_address = socket2.accept()

            data = connection.recv(1024).decode()
            if not data: break

            http_method, request_target, http_version = data.split()[:3]

            if http_method == "POST" and request_target == "/":
                handle_post_request(connection)
            elif http_method == "GET":
                handle_get_request(connection)
            else:
                # Send HTTP status "501 NotImplemented"
                response = "HTTP/1.1 501 NotImplemented\r\n\r\n"
                connection.sendall(response.encode())
        finally:
            if connection:
                connection.close()


def authenticateUser(user, password, file):
    with open(file) as json_file:
        data = json.load(json_file)

    if user in data:
        if data[user][0] == hashlib.sha256(password + user[1]).hexdigest():
            return True

    return False


def ok(sock):
    sock.send("HTTP/1.0 200 OK\r\n\r\n")
    return


def createCookie(id1):
    return json.dumps({
        id1: format(random.getrandbits(64), '016x'),
        'timestamp': datetime.datetime.now(datetime.UTC)
    })


def logger(message):
    print("SERVERLOG: " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + " " + message)
    print('\n')


def main():
    server_socket = serverStart(socket, int(sys.argv[2]), sys.argv[1], int(sys.argv[4]))
    file = open(sys.argv[3], "r")
    userDirect = sys.argv[5]

    ## post receive
    if authenticateUser("user", "password", file):
        cookie = createCookie('sessionID')
        logger("LOGIN SUCCESSFUL: " + "user" + ":" + "password")
        ok(server_socket)
    else:
        ok(server_socket)


if __name__ == "__main__":
    main()
