#!/usr/bin/env python3
import sys
from socket import *


class Server:
    def __init__(self, host="0.0.0.0", port=1025, storage_directory="."):
        # 0.0.0.0 is what allows us to run the program on any machine
        # This is because 0.0.0.0 listens on all available interfaces and not just a specific address
        self.host = host
        self.port = port
        self.storage_directory = storage_directory
        self.server_socket = socket(AF_INET, SOCK_DGRAM)  # UDP
        self.server_socket.bind((self.host, self.port))
        print(f"SERVER_PORT={self.port}")
        print(f"Server Address={self.host}")

    def receive_get_request(self):
        """
        Receive GET request via UDP socket and creates new TCP socket to send the requested file.
        """
        while True:
            print("Waiting for GET request...")
            message, client_address = self.server_socket.recvfrom(2048)
            print(f"Received message: {message.decode()} from {client_address}")

            parts = message.decode().split()
            if len(parts) == 3 and parts[0] == "GET":
                filename = parts[1]

                try:
                    file = open(f"{self.storage_directory}/{filename}", "rb")
                    if parts[2] == "PASV":
                        tcp_server_socket = socket(AF_INET, SOCK_STREAM)
                        tcp_server_socket.bind(("", 0))  # Bind to any available port
                        tcp_server_socket.listen(1)
                        pasv_port = tcp_server_socket.getsockname()[1]
                        print(f"R_PORT={pasv_port}")
                        # Send PASV response via UDP
                        pasv_response = f"PASV {pasv_port}"
                        self.server_socket.sendto(
                            pasv_response.encode(), client_address
                        )
                        print(
                            f"Sent PASV response: {pasv_response} to {client_address}"
                        )

                        # Accept connection from client
                        conn, addr = tcp_server_socket.accept()
                        print(f"Connected to client at {addr} via TCP")
                        # Send file via TCP
                        data = file.read(1024)
                        while data:
                            conn.send(data)
                            data = file.read(1024)
                        print(f"File '{filename}' sent successfully.")
                        conn.close()
                        tcp_server_socket.close()
                    else:  # Port Number from Client
                        tcp_port = int(parts[2])
                        # Create TCP socket to send the file
                        tcp_server_socket = socket(AF_INET, SOCK_STREAM)
                        tcp_server_socket.connect((client_address[0], tcp_port))
                        print(
                            f"Connected to client at {(client_address[0], tcp_port)} via TCP"
                        )

                        # Send 200 OK response via UDP
                        self.server_socket.sendto("200 OK".encode(), client_address)
                        print(f"Sent 200 OK to {client_address}")

                        # Send file via TCP
                        data = file.read(1024)
                        while data:
                            tcp_server_socket.send(data)
                            data = file.read(1024)
                        print(f"File '{filename}' sent successfully.")

                        tcp_server_socket.close()
                    file.close()
                except (FileNotFoundError, IsADirectoryError):
                    # Send 404 NOT FOUND response via UDP
                    self.server_socket.sendto("404 NOT FOUND".encode(), client_address)
                    print(
                        f"File '{filename}' not found. Sent 404 NOT FOUND to {client_address}"
                    )
                    continue


def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <storage_directory>")
        sys.exit(1)

    storage_directory = sys.argv[1]
    if not storage_directory:
        print("Please provide a valid storage directory.")
        sys.exit(1)

    server = Server(storage_directory=storage_directory)
    server.receive_get_request()


if __name__ == "__main__":
    main()
