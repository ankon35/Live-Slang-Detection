# import socket
# import threading

# # Server configuration
# HOST = '127.0.0.1'
# PORT = 8080

# # List of connected clients
# clients = []

# # Handle client connections
# def handle_client(client_socket, client_address):
#     """Handle a client connection."""
#     while True:
#         try:
#             message = client_socket.recv(1024).decode('utf-8')
#             if message:
#                 print(f"Received: {message}")
#                 # Broadcast message to all other clients
#                 sender_name = client_address[0]  # Get sender's IP or use a custom name
#                 for client in clients:
#                     if client != client_socket:  # Don't send back to the sender
#                         try:
#                             client.sendall(f"{sender_name}: {message}".encode('utf-8'))
#                         except:
#                             continue
#             else:
#                 break
#         except Exception as e:
#             print(f"Error: {e}")
#             break

#     # Remove client from the list and close the connection
#     clients.remove(client_socket)
#     client_socket.close()

# def main():
#     """Server main function."""
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((HOST, PORT))
#     server_socket.listen(5)
#     print("Server listening on", HOST, PORT)

#     while True:
#         client_socket, addr = server_socket.accept()
#         print(f"Client {addr} connected.")
#         clients.append(client_socket)
#         client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
#         client_thread.start()

# if __name__ == "__main__":
#     main()



import socket
import threading

HOST = '127.0.0.1'
PORT = 8080

clients = []
names = []

def broadcast(message, sender=None):
    """Send a message to all clients."""
    for client in clients:
        try:
            if sender:
                client.sendall(f"{sender}: {message}".encode('utf-8'))
            else:
                client.sendall(message.encode('utf-8'))
        except:
            # Remove broken connections
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            names.remove(name)
            broadcast(f"{name} has left the chat.", "Server")

def handle_client(client):
    """Handle a single client connection."""
    try:
        # First message is the client's name
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)
        
        broadcast(f"{name} has joined the chat.", "Server")
        
        while True:
            message = client.recv(1024).decode('utf-8')
            if message:
                broadcast(message, name)
            else:
                break
    except:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        name = names[index]
        names.remove(name)
        broadcast(f"{name} has left the chat.", "Server")

def start_server():
    """Start the chat server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    start_server()