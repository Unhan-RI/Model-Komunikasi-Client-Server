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

total_rtt = 0
total_latency = 0
total_throughput = 0
num_requests = 0

# Logging function
def log(message):
    with open('load_balancer.log', 'a') as f:
        f.write(f"{datetime.now()} - {message}\n")

# Function to forward traffic to backend servers
def forward_to_backend(client_socket, backend_socket, address, start_time):
    global total_rtt, total_latency, total_throughput, num_requests
    received_data_size = 0
    latency = None

    try:
        # Receive data from the client and forward to backend
        data = client_socket.recv(1024)
        if data:
            backend_socket.sendall(data)
            received_data_size += len(data)
            latency = (datetime.now() - start_time).total_seconds()  # Calculate latency
        
        # Receive response from the backend and send back to client
        response = backend_socket.recv(1024)
        if response:
            client_socket.sendall(response)
            received_data_size += len(response)

        # Calculate round-trip time (RTT)
        end_time = datetime.now()
        rtt = (end_time - start_time).total_seconds()

        # Update global statistics
        with lock:
            total_rtt += rtt
            total_latency += latency if latency is not None else 0
            if rtt > 0:
                total_throughput += received_data_size / rtt  # Avoid division by zero
            num_requests += 1

        log(f"Client {address} - RTT: {rtt:.6f}s, Latency: {latency:.6f}s, Throughput: {received_data_size / rtt:.2f} bytes/sec" if rtt > 0 else f"Client {address} - RTT: {rtt:.6f}s, Latency: {latency:.6f}s")
    
    except ConnectionResetError:
        log(f"Connection reset by {address}")
    finally:
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
        
        # Start timing for latency and RTT calculation
        start_time = datetime.now()

        # Forward traffic and calculate stats
        forward_to_backend(client_socket, backend_socket, address, start_time)
    
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

# Summary function for RTT, latency, and throughput
def print_summary():
    global total_rtt, total_latency, total_throughput, num_requests
    if num_requests > 0:
        avg_rtt = total_rtt / num_requests
        avg_latency = total_latency / num_requests
        avg_throughput = total_throughput / num_requests  # Average throughput

        log(f"\n--- SUMMARY ---\nTotal Requests: {num_requests}\nAverage RTT: {avg_rtt:.6f}s\nAverage Latency: {avg_latency:.6f}s\nAverage Throughput: {avg_throughput:.2f} bytes/sec\n")
        print(f"\n--- SUMMARY ---\nTotal Requests: {num_requests}\nAverage RTT: {avg_rtt:.6f}s\nAverage Latency: {avg_latency:.6f}s\nAverage Throughput: {avg_throughput:.2f} bytes/sec\n")
    else:
        log("No requests processed.")
        print("No requests processed.")

if __name__ == "__main__":
    try:
        threading.Thread(target=load_balancer).start()

        while True:
            time.sleep(60)  # Print summary every 60 seconds
            print_summary()

    except KeyboardInterrupt:
        log("Shutting down load balancer...")
        print("Shutting down load balancer...")
        print_summary()
