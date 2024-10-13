import socket

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))  # Connect to load balancer

    try:
        message = "Hello from client!"
        client_socket.send(message.encode())  # Send message
        response = client_socket.recv(1024).decode()  # Receive response
        print(f"Client received: {response}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    client_program()
