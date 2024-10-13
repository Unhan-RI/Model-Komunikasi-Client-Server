import socket
import threading

# Function to handle each client connection
def handle_client(client_socket, address):
    print(f"Connected to client: {address}")
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Message from {address}: {message}")
            response = f"Backend response: {message}"
            client_socket.send(response.encode())
        except ConnectionResetError:
            break
    print(f"Connection closed: {address}")
    client_socket.close()

# Main backend server function
def backend_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Backend server started on {ip}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    backend_server('127.0.0.1', 8002)  # Example for first backend server
