import socket
import threading
import queue

class PollClient:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue = queue.Queue()  # Queue to hold messages from the GUI
        self.running = True  # Control flag for stopping the client

    def start(self):
        """Starts the client and begins listening for messages."""
        self.client_socket.connect((self.host, self.port))
        print("Connected to the chatroom.\n")

        # Start a thread to receive messages
        threading.Thread(target=self.receive_messages, daemon=True).start()
        
        # Start a thread to send messages from the queue
        threading.Thread(target=self.process_messages, daemon=True).start()


    def send_message(self, message):
        """Sends a message from the GUI to the server."""
        if self.running:
            formatted_message = f"{self.username}: {message}"
            self.message_queue.put(formatted_message)  # Add message to queue

    def process_messages(self):
        """Processes messages from the queue and sends them to the server."""
        while self.running:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                self.client_socket.sendall(message.encode())
                

    def receive_messages(self):
        """Continuously receives messages from the server."""
        while self.running:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(data.decode())  # Display received messages in console

    def stop(self):
        """Stops the client gracefully."""
        self.running = False
        self.client_socket.close()
