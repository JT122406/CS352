import hashlib
import sys
import socket


def serverStart(socket1, port, address):
    socketserver = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
    socketserver.bind((address, port))
    socketserver.listen(1)
    return socketserver


# python3 server.py 62 key.txt

def getKeys():
    with open(sys.argv[2], 'r') as file:
        return [line.strip() for line in file.readlines()]


def decodeMessage(toDecode):
    return toDecode.decode('ascii').strip()


def encodeMessage(toEncode):
    return toEncode.encode('ascii')


if __name__ == "__main__":
    server_socket = serverStart(socket, int(sys.argv[1]), 'localhost')
    keys = getKeys()
    try:
        client_socket, client_address = server_socket.accept()
        if decodeMessage(client_socket.recv(1024)) != 'HELLO':
            print("Error: Invalid message")
            client_socket.close()
            exit()

        client_socket.send(encodeMessage("260 OK\n"))  # Everything UP to here works perfectly

        while True:
            match decodeMessage(client_socket.recv(1024)):
                case 'DATA':
                    for keys1 in keys:
                        message = decodeMessage(client_socket.recv(1024))
                        if message == '\\.\\r\\n':
                            break
                        client_socket.send(encodeMessage("270 SIG\n"))
                        sha256_hash = hashlib.sha256()
                        sha256_hash.update(encodeMessage(message))
                        sha256_hash.update(encodeMessage(keys1))
                        client_socket.send(encodeMessage(sha256_hash.hexdigest() + '\n'))

                        message = client_socket.recv(1024).decode('ascii').strip()
                        if message == 'PASS' or message == 'FAIL':
                            client_socket.send(encodeMessage("260 OK\n"))
                        else:
                            print("error")
                            client_socket.close()
                            exit()

                case 'QUIT':
                    server_socket.close()
                    exit(1)
                case _:
                    print("Error: Invalid message")
                    client_socket.close()
                    exit()
    except Exception as e:
        print(e)
        server_socket.close()
        exit()
