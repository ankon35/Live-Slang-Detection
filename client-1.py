# # import socket
# # import threading

# # # Server configuration
# # HOST = '127.0.0.1'  # Server IP (localhost for local testing)
# # PORT = 8080          # Server port

# # # Define function to handle receiving messages
# # def receive_messages(client_socket, user_name):
# #     """Function to receive messages from the server."""
# #     while True:
# #         try:
# #             message = client_socket.recv(1024).decode('utf-8')
# #             if message:
# #                 print(f"{user_name} received: {message}")  # Display the received message with the user's label
# #             else:
# #                 break
# #         except Exception as e:
# #             print(f"Error receiving message: {e}")
# #             break

# # def main():
# #     """Client main function to connect to the server."""
# #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     client_socket.connect((HOST, PORT))  # Connect to the server

# #     print("Connected to the server!")

# #     # Prompt for names of User 1 and User 2
# #     users = []
# #     for i in range(1, 3):
# #         user_name = input(f"Enter name for User {i}: ")
# #         users.append(user_name)

# #     # Start receiving messages for both users in separate threads
# #     threads = []
# #     for user_name in users:
# #         receive_thread = threading.Thread(target=receive_messages, args=(client_socket, user_name))
# #         threads.append(receive_thread)
# #         receive_thread.start()

# #     # Send messages to the server
# #     while True:
# #         for user_name in users:
# #             message = input(f"{user_name}, enter message to send: ")
# #             if message.lower() == 'exit':
# #                 break
# #             client_socket.sendall(message.encode('utf-8'))

# #     # Close the connection when done
# #     client_socket.close()

# # if __name__ == "__main__":
# #     main()



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
#                 print(f"{message}")  # Directly print the formatted message
#             else:
#                 break
#         except Exception as e:
#             print(f"Error receiving message: {e}")
#             break

# def main():
#     """Client main function to connect to the server."""
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((HOST, PORT))  # Connect to the server

#     print("User 1 connected to the server!")

#     # User 1-specific prompt
#     user_name = input("Enter name for User 1: ")

#     # Start receiving messages for User 1 in a separate thread
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