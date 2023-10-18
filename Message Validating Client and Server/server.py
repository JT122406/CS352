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
    print(keys)
    try:
        client_socket, client_address = server_socket.accept()
        one = decodeMessage(client_socket.recv(1024))
        print(one)
        print("Connection from: ", client_address)
        if one != 'HELLO':
            print("Error: Invalid message 1")
            client_socket.close()
            exit()

        client_socket.send("260 OK\n".encode('ascii'))
        while True:
            i = 0
            print("Waiting for message")
            string1 = decodeMessage(client_socket.recv(1024))
            print(string1)
            match string1:
                case 'DATA':
                    while True:
                        sha256_hash = hashlib.sha256()
                        message = decodeMessage(client_socket.recv(1024))
                        if message == '.':
                            break
                        sha256_hash.update(encodeMessage(message))
                        sha256_hash.update(encodeMessage(keys[i]))
                        i += 1
                        sign = sha256_hash.hexdigest()
                        print(sign)
                        client_socket.send(encodeMessage("270 SIG\n"))
                        client_socket.send(encodeMessage(sign + '\n'))

                        message = client_socket.recv(1024).decode('ascii').strip()
                        if message != 'PASS' and message != 'FAIL':
                            print("error")
                            client_socket.close()
                            exit()
                        else:
                            client_socket.send(encodeMessage("260 OK\n"))
                case 'QUIT':
                    server_socket.close()
                    exit()
                case _:
                    print("Error: Invalid message 2")
                    client_socket.close()
                    exit()
    except Exception as e:
        print(e)
        server_socket.close()
        exit()
