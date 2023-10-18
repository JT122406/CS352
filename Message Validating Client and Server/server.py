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
    this = toDecode.decode('ascii').strip()
    print(this)
    return this


def encodeMessage(toEncode):
    return toEncode.encode('ascii')


if __name__ == "__main__":
    server_socket = serverStart(socket, int(sys.argv[1]), 'localhost')
    keys = getKeys()
    client_socket, client_address = server_socket.accept()
    client_socket.settimeout(10)
    try:
        if decodeMessage(client_socket.recv(1024)) != 'HELLO':
            print("Error: Invalid message")
            client_socket.close()
            exit()

        client_socket.send(encodeMessage("260 OK\n"))  # Everything UP to here works perfectly

        while True:
            i = 0
            command = decodeMessage(client_socket.recv(1024))
            if command == 'DATA':
                message = decodeMessage(client_socket.recv(1024))
                client_socket.send(encodeMessage("270 SIG\n"))
                sha256_hash = hashlib.sha256()
                sha256_hash.update(encodeMessage(message))
                sha256_hash.update(encodeMessage(keys[i]))
                client_socket.send(encodeMessage(sha256_hash.hexdigest() + '\n'))

                message = decodeMessage(client_socket.recv(1024))
                if message == 'PASS' or message == 'FAIL':
                    client_socket.send(encodeMessage("260 OK\n"))
                    i += 1
                else:
                    print("error")
                    server_socket.close()
                    client_socket.close()
                    exit()
            elif command == 'QUIT':
                client_socket.close()
                server_socket.close()
                exit(1)
            else:
                print("Error: Invalid message else")
                client_socket.close()
                server_socket.close()
                exit()
    except Exception as e:
        print(e)
        server_socket.close()
        client_socket.close()
        exit()
