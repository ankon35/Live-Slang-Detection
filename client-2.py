# import socket
# import threading

# # Server configuration
# HOST = '127.0.0.1'  # Server IP (localhost for local testing)
# PORT = 8080          # Server port

# # Define function to handle receiving messages
# def receive_messages(client_socket, user_name):
#     """Function to receive messages from the server."""
#     while True:
#         try:
#             message = client_socket.recv(1024).decode('utf-8')
#             if message:
#                 print(f"{user_name} received: {message}")  # Display the received message with the user's label
#             else:
#                 break
#         except Exception as e:
#             print(f"Error receiving message: {e}")
#             break

# def main():
#     """Client main function to connect to the server."""
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((HOST, PORT))  # Connect to the server

#     print("User 2 connected to the server!")

#     # User 2-specific prompt
#     user_name = input("Enter name for User 2: ")

#     # Start receiving messages for User 2 in a separate thread
#     receive_thread = threading.Thread(target=receive_messages, args=(client_socket, user_name))
#     receive_thread.start()

#     # Send messages to the server
#     while True:
#         message = input(f"{user_name}, enter message to send: ")
#         if message.lower() == 'exit':
#             break
#         client_socket.sendall(message.encode('utf-8'))

#     # Close the connection when done
#     client_socket.close()

# if __name__ == "__main__":
#     main()




import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Server IP (localhost for local testing)
PORT = 8080          # Server port

# Define function to handle receiving messages
def receive_messages(client_socket):
    """Function to receive messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)  # The message already includes the sender's name
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def main():
    """Client main function to connect to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  # Connect to the server

    print("Connected to the server!")

    # Get user's name
    user_name = input("Enter your name: ")
    client_socket.sendall(user_name.encode('utf-8'))  # Send the name to the server first

    # Start receiving messages in a separate thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    # Send messages to the server
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client_socket.sendall(message.encode('utf-8'))

    # Close the connection when done
    client_socket.close()

if __name__ == "__main__":
    main()