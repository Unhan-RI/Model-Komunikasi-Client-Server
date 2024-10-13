import socket
import threading
from datetime import datetime

# Logging function for clients
def log(message):
    with open('client.log', 'a') as f:
        f.write(f"{datetime.now()} - {message}\n")

# Function to simulate a single client
def client_program(client_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))  # Connect to the Load Balancer
    message = f"Hello from client {client_id}"

    start_time = datetime.now()
    log(f"Client {client_id} connected at {start_time}")

    try:
        # Send message to Load Balancer
        client_socket.send(message.encode())
        log(f"Client {client_id} sent: {message}")

        # Receive response from backend server
        response = client_socket.recv(1024).decode()
        end_time = datetime.now()
        round_trip_time = (end_time - start_time).total_seconds()
        
        log(f"Client {client_id} received: {response} (Round-trip time: {round_trip_time:.6f} seconds)")
        print(f"Client {client_id} received: {response}")
    finally:
        client_socket.close()

# Function to simulate multiple clients
def simulate_multiple_clients(client_count):
    client_threads = []
    
    for i in range(client_count):
        # Create a thread for each client
        t = threading.Thread(target=client_program, args=(i,))
        client_threads.append(t)
        t.start()
    
    # Wait for all clients to finish
    for t in client_threads:
        t.join()

if __name__ == "__main__":
    num_clients = 20  # Number of clients to simulate
    simulate_multiple_clients(num_clients)
