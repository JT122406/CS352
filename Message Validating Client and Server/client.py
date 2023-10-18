import sys
import socket


# python3 client.py localhost 62 message1.txt signature1.txt

def startClient(address, port):
    socket1 = None
    connected = False
    while not connected:
        try:
            socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket1.connect((address, port))
            #print("Connection to: ", address, ":", port)
            connected = True
        except Exception:
            pass

    return socket1


if __name__ == "__main__":
    client_socket = startClient(sys.argv[1], int(sys.argv[2]))
    messageFileName = sys.argv[3]
    signatureFileName = sys.argv[4]

    # messageFile = open(messageFileName)
    # Lines = messageFile.readlines()

    # for line in Lines:
    # bytesT = bytes(line, 'ascii')
    with open(messageFileName, 'r') as file:
        message = [line.strip() for line in file]
    with open(signatureFileName, 'r') as s_file:
        signature = [line.strip() for line in s_file]

    try:
        client_socket.send("HELLO\n".encode('ascii'))
        #print("HELLO")
        response = client_socket.recv(1024).decode().strip()
        if response != "260 OK":
            print("Error: Server response not as expected")
            exit(1)

        message_counter = 1
        for messages in message:
            client_socket.send("DATA\n".encode('ascii'))
            client_socket.send(message[message_counter].encode('ascii'))
            #client_socket.send("Ethernet cables are like the roads of the Internet, carrying data traffic to its destinations.".encode('ascii'))
            response = client_socket.recv(1024).decode('ascii').strip()
            print(response)
            if response != "270 SIG":
                print("Error: Server response not as expected 1")
                exit(1)
            server_signature = client_socket.recv(1024).decode('ascii').strip()
            if server_signature == signature:
                client_socket.send("PASS\n".encode('ascii'))
            else:
                client_socket.send("FAIL\n".encode('ascii'))
            response = client_socket.recv(1024).decode().strip()
            if response != "260 OK":
                print("Error: Server response not as expected 2")
                exit(1)
            message_counter += 2
        client_socket.send("QUIT\n".encode('ascii'))
        response = client_socket.recv(1024).decode('ascii').strip()
        if response != "260 OK":
            print("Error: Server response not as expected")
            exit(1)
    except Exception as e:
        print(e)
        exit(1)
