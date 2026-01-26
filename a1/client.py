import sys
from socket import *


class Client:
    def __init__(
        self,
        server_address="localhost",
        server_port=1025,
        mode="ACTV",
        filename="hello_world.txt",
    ):
        self.server_address = server_address
        self.server_port = server_port
        self.mode = mode
        self.filename = filename
        self.udp_client_socket = socket(AF_INET, SOCK_DGRAM)  # UDP
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)  # TCP

    def send_get_request(self):
        """
        Send GET request to the server via UDP socket.
        The request contains the filename and port number of TCP client socket
        for the server to send the requested file on.

        In ACTV mode, client sends GET request containing file requested and client TCP port number for
        the server to connect on via UDP. Client receives 200 OK or 404 NOT FOUND response via UDP.
        If 200 OK, client expects server to connect to its TCP socket to send the file.

        In PASV mode, client sends GET request containing file requested and "PASV" via UDP. Server responds
        with "PASV <port>" via UDP which specifies the port number the client should connect to via TCP
        to receive the file.
        404 NOT FOUND is also sent via UDP if file not found.

        In ACTV, client listens on TCP socket for server to connect to.
        In PASV, server listens on TCP socket for client to connect to.
        """
        if self.mode == "ACTV":
            self.tcp_client_socket.bind(("", 0))  # Bind to any available port
            self.tcp_client_socket.listen(1)
            tcp_port = self.tcp_client_socket.getsockname()[1]
            print(f"R_PORT={tcp_port}")
            get_request = f"GET {self.filename} {tcp_port}"
            self.udp_client_socket.sendto(
                get_request.encode(), (self.server_address, self.server_port)
            )
            print(f"Sent GET request: {get_request}")

            # Accept 200 OK or 404 NOT FOUND response from server
            response, _ = self.udp_client_socket.recvfrom(2048)
            response = response.decode()
            print(f"Received response: {response}")
            if response == "404 NOT FOUND":
                print(f"File '{self.filename}' not found on server.")
                self.tcp_client_socket.close()
                self.udp_client_socket.close()
                return

            # Receive file via TCP
            conn, addr = (
                self.tcp_client_socket.accept()
            )  # conn is on the same port as tcp_client_socket
            print(f"Connected to server at {addr} via TCP")
            with open(f"received_{self.filename}", "wb") as file:
                data = conn.recv(1024)
                while data:
                    file.write(data)
                    data = conn.recv(1024)
            print(f"File 'received_{self.filename}' received successfully.")
            conn.close()
            self.tcp_client_socket.close()
        elif self.mode == "PASV":
            get_request = f"GET {self.filename} PASV"
            self.udp_client_socket.sendto(
                get_request.encode(), (self.server_address, self.server_port)
            )
            print(f"Sent GET request: {get_request}")

            # Receive PASV response from server
            response, _ = self.udp_client_socket.recvfrom(2048)
            response = response.decode()
            print(f"Received response: {response}")
            if response == "404 NOT FOUND":
                print(f"File '{self.filename}' not found on server.")
                self.udp_client_socket.close()
                return

            parts = response.split()
            if len(parts) == 2 and parts[0] == "PASV":
                pasv_port = int(parts[1])
                # Create TCP socket to receive the file
                self.tcp_client_socket.connect((self.server_address, pasv_port))
                print(
                    f"Connected to server at {(self.server_address, pasv_port)} via TCP"
                )

                # Receive file via TCP
                with open(f"received_{self.filename}", "wb") as file:
                    data = self.tcp_client_socket.recv(1024)
                    while data:
                        file.write(data)
                        data = self.tcp_client_socket.recv(1024)
                print(f"File 'received_{self.filename}' received successfully.")
                self.tcp_client_socket.close()
            else:
                print("Invalid PASV response from server.")
        else:
            print("Invalid mode. Use 'ACTV' or 'PASV'.")


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python client.py <server_address> <server_port> <mode> <filename>"
        )
        sys.exit(1)

    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        mode = sys.argv[3]
        filename = sys.argv[4]

        if mode not in ["ACTV", "PASV"]:
            raise ValueError("Mode must be 'ACTV' or 'PASV'")

        if server_port < 1024 or server_port > 65535:
            raise ValueError("Port number must be between 1024 and 65535")

        if not filename:
            raise ValueError("Filename cannot be empty")

        if not server_address:
            raise ValueError("Server address cannot be empty")
    # catch all
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        print(
            "Usage: python client.py <server_address> <server_port> <mode> <filename>"
        )
        sys.exit(1)

    client = Client(server_address, server_port, mode, filename)
    client.send_get_request()


if __name__ == "__main__":
    main()
