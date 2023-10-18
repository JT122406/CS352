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


def hashMessage(message, key):
    hash = hashlib.sha256()
    hash.update(encodeMessage(message))
    hash.update(encodeMessage(key))
    return encodeMessage(hash.hexdigest())


def main():
    server_socket = serverStart(socket, int(sys.argv[1]), 'localhost')
    keys = getKeys()
    client_socket, client_address = server_socket.accept()
    try:
        message1 = decodeMessage(client_socket.recv(1024))
        print(message1)
        if message1 != 'HELLO':
            print("Error: Invalid message")
            client_socket.close()
            exit()

        client_socket.send(encodeMessage("260 OK\n"))
        while True:
            for key in keys:
                command = decodeMessage(client_socket.recv(1024))
                print(command)
                if command == 'DATA':
                    message = ''
                    while True:
                        chars = client_socket.recv(1).decode('ascii')
                        if chars == '.':
                            break
                        else:
                            message += chars
                    client_socket.recv(1024)
                    print(message)
                    client_socket.send(encodeMessage("270 SIG\n"))
                    client_socket.send(hashMessage(message, key))
                    output = decodeMessage(client_socket.recv(1024))
                    print(output)
                    if output == 'PASS' or output == 'FAIL':
                        client_socket.send(encodeMessage("260 OK\n"))
                    else:
                        print("Error: Invalid message here?")
                        client_socket.close()
                        server_socket.close()
                        exit()
                elif command == 'QUIT':
                    client_socket.close()
                    server_socket.close()
                    exit()
                else:
                    print("Error: Invalid message")
                    client_socket.close()
                    server_socket.close()
                    exit()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
