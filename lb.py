import socket
import threading
import time
from datetime import datetime

# List of backend servers (IP, Port)
BACKEND_SERVERS = [
    ('127.0.0.1', 8001),
    ('127.0.0.1', 8002),
    ('127.0.0.1', 8003),
]

current_server = 0
lock = threading.Lock()

# Logging function
def log(message):
    with open('load_balancer.log', 'a') as f:
        f.write(f"{datetime.now()} - {message}\n")

# Function to forward traffic to backend servers
def forward_to_backend(client_socket, backend_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            backend_socket.sendall(data)
        except ConnectionResetError:
            break
    client_socket.close()

# Handle client connections and distribute to backend
def handle_client(client_socket, address):
    global current_server
    with lock:
        backend_ip, backend_port = BACKEND_SERVERS[current_server]
        current_server = (current_server + 1) % len(BACKEND_SERVERS)

    log(f"Connection from {address} forwarded to backend {backend_ip}:{backend_port}")

    try:
        # Connect to selected backend server
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect((backend_ip, backend_port))
        
        # Create threads to forward traffic in both directions
        threading.Thread(target=forward_to_backend, args=(client_socket, backend_socket)).start()
        forward_to_backend(backend_socket, client_socket)
    except Exception as e:
        log(f"Error forwarding to backend: {e}")
        client_socket.close()

# Load balancer main function
def load_balancer():
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.bind(('0.0.0.0', 12345))  # Load balancer listens on this port
    lb_socket.listen(5)
    log("Load Balancer started on port 12345...")

    while True:
        client_socket, address = lb_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    load_balancer()
