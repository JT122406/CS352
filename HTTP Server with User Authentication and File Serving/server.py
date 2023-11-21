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
    headers = data.split("\r\n")
    username = None
    password = None

    for header in headers:
        if header.startswith("username: "):
            username = header.split(":")[1].strip()
        elif header.startswith("password: "):
            password = header.split(":")[1].strip()

    if username is None or password is None:
        send_http_status(connection, "501 Not Implemented", "")
        logger("LOGIN FAILED")
        connection.close()
        return
    varthing = authenticateUser(username, password)
    if varthing[0]:
        logger("LOGIN SUCCESSFUL: " + username + " : " + password)

        ## cookie = createCookie(username)
        send_http_status(connection, "200 OK", "Logged in!")
        # ok(connection, cookie)
        connection.close()
    elif varthing[1] == 1:
        logger("LOGIN FAILED: wronguser : " + password)
        send_http_status(connection, "200 OK", "Login failed!")
    else:
        logger("LOGIN FAILED: " + username + " : wrongpassword")
        send_http_status(connection, "200 OK", "Login failed!")
        connection.close()


def get_request(connection):
    cookie = None
    if cookie is None:
        connection.sendall("HTTP/1.0 401 Unauthorized\r\n".encode())
        return None

    return


def listen(socket2):
    while True:
        connection, client_address = socket2.accept()

        data = connection.recv(1024).decode()
        if not data:
            continue

        http_method, request_target, http_version = data.split()[:3]

        if http_method == "POST" and request_target == '/':
            post_request(connection, data)
        elif http_method == "GET":
            get_request(connection)
        else:
            connection.sendall("HTTP/1.0 501 NotImplemented\r\n".encode())

        connection.close()


def authenticateUser(user, password):
    with open(sys.argv[3]) as json_file:
        data = json.load(json_file)
    if user in data:
        return data[user][0] == hashlib.sha256(password.encode() + data[user][1].encode()).hexdigest(), 0
    else:
        return False, 1


def ok(sock, message):
    send_http_status(sock, "200 OK", message)


def send_http_status(socket9, status_code, status_message):
    # HTTP response line
    response_line = f"HTTP/1.0 {status_code} {status_message}\r\n"

    # HTTP headers
    headers = "Content-Type: text/html\r\n"

    # Empty line to separate headers and body
    blank_line = "\r\n"

    # HTTP response body (you can customize this)
    response_body = "<html><body><h1>{}</h1></body></html>".format(status_message)

    # Concatenate the response
    response = response_line + headers + blank_line + response_body

    # Send the response through the socket
    socket9.sendall(response.encode())


def createCookie(id1):
    return "Cookie: sessionID=" + format(random.getrandbits(64), '016x')


def logger(message):
    print("SERVERLOG: " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + " " + message)


def main():
    server_socket = serverStart(socket, int(sys.argv[2]), sys.argv[1], int(sys.argv[4]))
    ## userDirect = sys.argv[5]
    listen(server_socket)


if __name__ == "__main__":
    main()
