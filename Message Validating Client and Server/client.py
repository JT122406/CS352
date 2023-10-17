import sys
import socket

#python3 client.py localhost 62 message1.txt signature1.txt

if __name__ == "__main__":
    name = sys.argv[1]
    port = sys.argv[2]
    messageFileName = sys.argv[3]
    signatureFileName = sys.argv[4]

    # messageFile = open(messageFileName)
    # Lines = messageFile.readlines()

    # for line in Lines:
    # bytesT = bytes(line, 'utf-8')
    with open(messageFileName, 'r') as file:
        message = [line.strip().encode() for line in file]
    with open(signatureFileName, 'r') as s_file:
        signature = [line.strip() for line in s_file]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((name, int(port)))
        print("Connection to: ", name, ":", port)
        client_socket.send("HELLO\n".encode('utf-8'))
        print("HELLO")
        exit()
        response = client_socket.recv(1024).decode().strip()
        if response != "260 OK":
            print("Error: Server response not as expected")
            exit(1)
        message_counter = 0
        for message, signature in zip(message, signature):
            client_socket.send(b"DATA\n")
            client_socket.send(message)
            response = client_socket.recv(1024).decode().strip()
            if response != "270 SIG":
                print("Error: Server response not as expected")
                exit(1)
            server_signature = client_socket.recv(1024).decode().strip()
            if server_signature == signature:
                client_socket.send(b"PASS\n")
            else:
                client_socket.send(b"FAIL\n")
            response = client_socket.recv(1024).decode().strip()
            if response != "260 OK":
                print("Error: Server response not as expected")
                exit(1)
            message_counter += 1
        client_socket.send(b"QUIT\n")
        response = client_socket.recv(1024).decode().strip()
        if response != "260 OK":
            print("Error: Server response not as expected")
            exit(1)
    except Exception as e:
        print(e)
        exit(1)
