import datetime
import hashlib
import json
import random
import socket
import sys

sessions = {}


def logger(message):
    print("SERVER LOG: " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + " " + message)


def serverStart(socket1, port, address):
    socketserver = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    socketserver.bind((address, port))
    socketserver.listen(1)
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
        logger("LOGIN FAILED: wronguser : " + password)
        connection.sendall("HTTP/1.0 200 OK\r\n\r\nLogin failed!".encode())
    else:  ## User is found, but password is wrong
        logger("LOGIN FAILED: " + username + " : " + password)
        connection.sendall("HTTP/1.0 200 OK\r\n\r\nLogin failed!".encode())


def get_request(connection, data):
    # print(data)
    headers = data.split("\r\n")
    sessionID = None
    target = None
    response = None
    fileName = headers[0].split()[1]
    print("fileName: " + fileName)
    print(headers)
    for header in headers:
        print("inside for loop (get_request)")
        if header.startswith("Cookie: "):
            print("header starts with sessionID")
            print(header)
            number = header.split("=")[1].strip()
            print("number: " + number)
            if sessions.keys().__contains__(number):
                print(sessions.keys().__contains__(number))
                time = sessions[number][1]
                userDirect = sys.argv[5] + sessions[number][0]
                print("userDirect: " + userDirect)
                if (datetime.datetime.now() - time).total_seconds() > int(sys.argv[4]):
                    logger("SESSION EXPIRED: " + sessions[number][0] + " : " + userDirect)
                    break
                else:
                    print("total directory: " + userDirect + fileName)
                    # file = open(userDirect + fileName, "r")
                    # print("file: " + file.read())
                    try:
                        with open(userDirect + fileName, "r") as file:
                            file_content = file.read()
                            print("file: " + file_content)
                            # connection.sendall("HTTP/1.0 200 OK\r\n".encode())
                            # connection.sendall(("Content-Type: text/html\r\n").encode())
                            # connection.sendall(("\r\n").encode())
                            # connection.sendall((file.read()).encode())
                            # logger("FILE SENT: " + sessions[number][0] + " : " + userDirect+fileName)

                            content_length = len(file_content)
                            print("content_length: " + content_length)
                            # response = (
                            #    "HTTP/1.0 200 OK\r\n"
                            #    "Content-Type: text/html\r\n"
                            #    "Content-Length: {len(file_content)}\r\n{file_content}"
                            # )
                            response = "HTTP/1.0 200 OK\r\n"
                            response += file_content + "\r\n"
                            # connection.sendall(response.encode())

                    except:
                        print("file not found")

                        break
                    break
    print("outside for loop")
    userDirect = sys.argv[5] + sessions[number][0]

    file = open(userDirect + fileName, "r")
    file_content = file.read()
    # connection.sendall("HTTP/1.0 401 Unauthorized\r\n".encode())
    print("filecontent: " + file_content)
    connection.sendall(("HTTP/1.0 200 OK\r\n\r\n" + file_content + "\r\n").encode())
    ## Get cookie and verify it isn't past timeout
    ## if it is, send 401 and return None

    return


def listen(socket2):
    while True:
        connection, client_address = socket2.accept()
        data = connection.recv(1024).decode()
        if data is None:
            continue
        ## print(data)

        http_method, request_target, http_version = data.split()[:3]

        if http_method == "POST" and request_target == '/':
            post_request(connection, data)
        elif http_method == "GET":
            get_request(connection, data)
        else:
            connection.sendall("HTTP/1.0 501 NotImplemented\r\n\r\n".encode())

        connection.close()


def authenticateUser(user, password):
    with open(sys.argv[3]) as json_file:
        data = json.load(json_file)
    if user in data:
        return data[user][0] == hashlib.sha256(password.encode() + data[user][1].encode()).hexdigest(), 0
    else:
        return False, 1


def generate_random_session_id():
    return format(random.randint(0, 2 ** 64 - 1), 'x')


def main():
    listen(serverStart(socket, int(sys.argv[2]), sys.argv[1]))


if __name__ == "__main__":
    main()
