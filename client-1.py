import socket
import threading
import re

# Server configuration
HOST = '127.0.0.1'  # Server IP (localhost for local testing)
PORT = 8080          # Server port

# Define function to clean incoming chat message
def clean_message(message):
    """Function to clean the incoming chat message by removing non-text characters, including emojis."""
    # Regex to remove all non-alphanumeric characters, including emojis
    cleaned_message = re.sub(r'[^\w\s]', '', message)  # Removes non-word characters (including emojis)
    # print(cleaned_message)
    return cleaned_message

# Define function to handle receiving messages
def receive_messages(client_socket):
    """Function to receive messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # cleaned_message = clean_message(message)
                print(message)  # The cleaned message
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
