import socket
import threading
import re
import os
import json
from dotenv import load_dotenv

# Voice recognition imports
from vosk import Model, KaldiRecognizer
import pyaudio

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

# Server configuration
HOST = '127.0.0.1'
PORT = 8080

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# --- LangChain Setup for Slang Detection ---
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant for a chat application. Your task is to analyze user messages and classify them.
    Return 'slang' if the message contains vulgar language, profanity, or is overly aggressive.
    Return 'neutral' for all other messages.
    Do not respond with anything other than 'slang' or 'neutral'."""),
    ("user", "{message}")
])
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
slang_detection_chain = prompt | llm | StrOutputParser()

# --- Voice Recognition Setup ---
MODEL_PATH = "vosk-model-small-en-us-0.15"
if not os.path.exists(MODEL_PATH):
    print(f"Error: Vosk model not found at path '{MODEL_PATH}'.")
    print("Please download a model from https://alphacephei.com/vosk/models and extract it to your project directory.")
    exit(1)

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# --- Function to handle receiving messages ---
def receive_messages(client_socket):
    """Function to receive messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# --- Main client logic ---
def main():
    """Client main function to connect to the server and handle user input."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # PyAudio stream setup, but don't start it yet
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=2048)

    try:
        client_socket.connect((HOST, PORT))
        print("Connected to the server!")
        
        user_name = input("Enter your name: ")
        client_socket.sendall(user_name.encode('utf-8'))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

        # --- Initial mode selection ---
        mode_choice = input("Select input mode (1 for text, 2 for voice): ")
        current_mode = 'text' if mode_choice == '1' else 'voice'
        
        print("\nType 'change' to switch modes at any time.")
        print("Type 'exit' or say 'exit' to quit.")

        # --- Main loop for handling different input modes ---
        while True:
            if current_mode == 'text':
                print("\n--- TEXT MODE ---")
                try:
                    text_message = input("> ")
                    
                    if text_message.lower().strip() == 'change':
                        current_mode = 'voice'
                        continue
                    if text_message.lower().strip() == 'exit':
                        print("Exiting chat client.")
                        break

                    if text_message:
                        try:
                            api_result = slang_detection_chain.invoke({"message": text_message})
                            if api_result.lower().strip() == 'slang':
                                print("⚠️ Warning: Your message contains slang or vulgar language and was not sent.")
                            else:
                                client_socket.sendall(text_message.encode('utf-8'))
                        except Exception as e:
                            print(f"Error analyzing message with Gemini API: {e}")
                            client_socket.sendall(text_message.encode('utf-8'))

                except (IOError, KeyboardInterrupt):
                    print("\nExiting chat client.")
                    break

            elif current_mode == 'voice':
                print("\n--- VOICE MODE ---")
                print("Listening...")
                # Start the audio stream for voice input
                stream.start_stream()
                
                while current_mode == 'voice':
                    data = stream.read(4096, exception_on_overflow=False)
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text_message = result.get('text', '')
                        
                        if text_message:
                            print(f"Transcribed: {text_message}")
                            
                            if text_message.lower().strip() == 'change':
                                current_mode = 'text'
                                # Stop the audio stream before switching mode
                                stream.stop_stream()
                                break
                            
                            if text_message.lower().strip() == 'exit':
                                print("Exiting chat client.")
                                current_mode = 'exit' # Flag to break the outer loop
                                stream.stop_stream()
                                break
                            
                            cleaned_message = re.sub(r'[^\w\s]', '', text_message)
                            
                            try:
                                api_result = slang_detection_chain.invoke({"message": cleaned_message})
                                if api_result.lower().strip() == 'slang':
                                    print("⚠️ Warning: Your message contains slang or vulgar language and was not sent.")
                                else:
                                    client_socket.sendall(text_message.encode('utf-8'))
                            except Exception as e:
                                print(f"Error analyzing message with Gemini API: {e}")
                                client_socket.sendall(text_message.encode('utf-8'))

                # If the outer loop is broken by 'exit' from voice mode
                if current_mode == 'exit':
                    break

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    except KeyboardInterrupt:
        print("\nExiting chat client.")
    finally:
        # Close all resources
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()

if __name__ == "__main__":
    main()