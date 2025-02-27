import socket
import threading
import queue

class PollClient:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue = queue.Queue() # Line by ChatGPT
        self.running = True

    def start(self):
        self.client_socket.connect((self.host, self.port))
        print("Connected to the chatroom.\n")

        threading.Thread(target=self.receive_messages, daemon=True).start()
        
        threading.Thread(target=self.process_messages, daemon=True).start()


    ''' send_message() and process_message() were both created by ChatGPT and then tested using the unit tests.
    These functions were not previously here as client_release only dealt with messages through the command line.
    Once I tried to get it to work using the GUI in TKinter, I quickly realized that I was running to a lot of walls
    trying to get it to send through the GUI instead of using input().
    '''
    
    def send_message(self, message):
        if self.running:
            formatted_message = f"{self.username}: {message}"
            self.message_queue.put(formatted_message)

    def process_messages(self):
        while self.running:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                self.client_socket.sendall(message.encode())
                
    # Everything after this line is written by either myself or Landon

    def receive_messages(self):
        while self.running:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(data.decode())

    def stop(self):
        self.running = False
        self.client_socket.close()
