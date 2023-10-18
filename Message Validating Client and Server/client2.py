import socket
import sys


def startClient(address, port):
    socket1 = None
    connected = False
    while not connected:
        try:
            socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket1.connect((address, port))
            connected = True
        except Exception:
            pass

    return socket1


def getMessages(file):
    i = 1
    messages = []
    with open(file, 'r') as file:
        for line in file.readlines():
            if i % 2 == 0:
                messages.append(line.strip())
            i += 1
    return messages


def getSignatures(file):
    with open(file, 'r') as file:
        return [line.strip() for line in file.readlines()]


def decodeMessage(toDecode):
    return toDecode.decode('ascii').strip()


def encodeMessage(toEncode):
    return (toEncode + '\n').encode('ascii')


def main():
    socket1 = startClient(sys.argv[1], int(sys.argv[2]))
    messages = getMessages(sys.argv[3])
    signatures = getSignatures(sys.argv[4])
    try:
        socket1.send(encodeMessage("HELLO"))
        reception = decodeMessage(socket1.recv(1024))
        print(reception)
        if reception != "260 OK":
            print("Error: Server response not as expected")
            socket1.close()
            exit(1)

        for message in messages:
            socket1.send(encodeMessage("DATA"))
            socket1.send(encodeMessage(message))
            response = decodeMessage(socket1.recv(1024))
            print(response)
            if response != '270 SIG':
                print("Error: Server response not as expected")
                socket1.close()
                exit(1)
            response2 = decodeMessage(socket1.recv(1024))
            print(response2)
            if response2 == signatures[messages.index(message)]:
                socket1.send(encodeMessage("PASS"))
            else:
                socket1.send(encodeMessage("FAIL"))

            response3 = decodeMessage(socket1.recv(1024))
            print(response3)
            if response3 != "260 OK":
                print("Error: Server response not as expected")
                socket1.close()
                exit(1)

        socket1.send(encodeMessage("QUIT"))

    except Exception as e:
        print(e)
        socket.close()
        exit(1)


if __name__ == "__main__":
    print("Starting client")
    main()
