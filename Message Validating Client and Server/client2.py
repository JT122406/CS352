import socket


def main():
    server_address = "localhost"
    server_port = 62

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))

        # Send the "HELLO" message to the server
        client_socket.send("HELLO\n".encode('utf-8'))
        print("Sent 'HELLO' to the server")

        # Close the client socket
        client_socket.close()

    except ConnectionRefusedError:
        print("Connection to the server failed. Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
