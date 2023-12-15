import datetime
import hashlib
import json
import random
import socket
import sys

sessions = {}


def logger(message: str) -> None:
    print("SERVER LOG: " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + " " + message)


def serverStart(socket1: socket, port: int, address: str) -> socket:
    socketserver = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    socketserver.bind((address, port))
    socketserver.listen(1)
    return socketserver


def post_request(connection: socket, data: str) -> None:
    headers = data.split("\r\n")
    username = None
    password = None

    for header in headers:
        if header.startswith("username: "):
            username = header.split(":")[1].strip()
        elif header.startswith("password: "):
            password = header.split(":")[1].strip()

    if username is None or password is None:
        connection.sendall("HTTP/1.0 501 Not Implemented\r\n\r\n".encode())
        logger("LOGIN FAILED")
        return

    authVar = authenticateUser(username, password)
    if authVar[0]:  ## User is found and password is correct
        logger("LOGIN SUCCESSFUL: " + username + " : " + password)
        cookie = generate_random_session_id()
        connection.sendall(("HTTP/1.0 200 OK\r\n" + "Set-Cookie: sessionID=" + cookie + "\r\n\r\nLogged in!").encode())
        sessions[cookie] = (username, datetime.datetime.now())
    elif authVar[1] == 1:  ## User is not found
        logger("LOGIN FAILED: " + username + " : " + password)
        connection.sendall("HTTP/1.0 200 OK\r\n\r\nLogin failed!".encode())
    else:  ## User is found, but password is wrong
        logger("LOGIN FAILED: " + username + " : " + password)
        connection.sendall("HTTP/1.0 200 OK\r\n\r\nLogin failed!".encode())


def get_request(connection: socket, data: str) -> None:
    headers = data.split("\r\n")
    sessionID = None

    for header in headers:
        if header.startswith("Cookie: "):
            sessionID = header.split("=")[1].strip()

    if sessionID is None:  # No cookie in header
        connection.sendall("HTTP/1.0 401 Unauthorized\r\n\r\n".encode())
    elif sessionID in sessions:  # Check if cookie matches one from our list
        if (datetime.datetime.now() - sessions[sessionID][1]).total_seconds() < int(
                sys.argv[4]):  # see if cookie is expired
            # cookie is valid, update cookie time
            sessions[sessionID] = (sessions[sessionID][0], datetime.datetime.now())
            # get file path
            userDirect = sys.argv[5] + sessions[sessionID][0] + headers[0].split()[1]
            try:  # attempt to open file
                with open(userDirect, 'r') as f:
                    logger("GET SUCCEEDED: " + sessions[sessionID][0] + " : " + headers[0].split()[1])
                    connection.sendall(("HTTP/1.0 200 OK\r\n\r\n" + f.read() + "\r\n").encode())
            except FileNotFoundError:  # file not found
                logger("GET FAILED: " + sessions[sessionID][0] + " : " + headers[0].split()[1])
                connection.sendall("HTTP/1.0 404 Not Found\r\n\r\n".encode())
        else:
            # cookie expired
            logger("SESSION EXPIRED: " + sessions[sessionID][0] + " : " + headers[0].split()[1])
            connection.sendall("HTTP/1.0 401 Unauthorized\r\n\r\n".encode())
    else:
        logger("COOKIE INVALID: " + headers[0].split()[1])
        connection.sendall("HTTP/1.0 401 Unauthorized\r\n\r\n".encode())


def listen(socket2: socket) -> None:
    while True:
        connection, client_address = socket2.accept()
        data = connection.recv(1024).decode()
        if data is None:
            continue

        http_method, request_target, http_version = data.split()[:3]

        if http_method == "POST" and request_target == '/':
            post_request(connection, data)
        elif http_method == "GET":
            get_request(connection, data)
        else:
            connection.sendall("HTTP/1.0 501 NotImplemented\r\n\r\n".encode())

        connection.close()


def authenticateUser(user: str, password: str) -> (bool, int):
    with open(sys.argv[3]) as json_file:
        data = json.load(json_file)
    if user in data:
        return data[user][0] == hashlib.sha256(password.encode() + data[user][1].encode()).hexdigest(), 0
    else:
        return False, 1


def generate_random_session_id() -> str:
    return format(random.randint(0, 2 ** 64 - 1), 'x')


def main() -> None:
    listen(serverStart(socket, int(sys.argv[2]), sys.argv[1]))


if __name__ == "__main__":
    main()
