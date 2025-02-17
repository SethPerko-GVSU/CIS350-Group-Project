import socket
import threading

class PollClient:
    def __init__(self):
        self.host = input("Enter the chatroom server's IP: ")
        self.port = int(input("Enter the chatroom server's port number: "))
        self.lock = threading.Lock()
        self.username = input("Enter your username:")

    def start(self):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((self.host, self.port))
        print("Connected to the chatroom.\n")

        threading.Thread(target=self.receive_messages, args=(c,), daemon=True).start()

        while True:
            message = f'{self.username}: {input()}'
            c.sendall(message.encode())

    def receive_messages(self, c):
        while True:
            data = c.recv(1024)
            if not data:
                break
            print(data.decode())

if __name__ == "__main__":
    client = PollClient()
    client.start()
    client.receive_messages()