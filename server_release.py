import socket
import threading
import json

class PollServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 53827
        self.connected_clients = []  
        self.lock = threading.Lock()
        self.username = input("Enter your username:")

    def handle_client(self, conn, addr):
        print(f"Client connected from {addr[0], addr[1]}")
        with self.lock:
            self.connected_clients.append(conn)

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            print(data)
        

    def server_input(self):
        while True:
            message = f'{self.username}: {input()}'
            with self.lock:
                for conn in self.connected_clients:
                    try:
                        conn.sendall(message.encode())
                    except Exception as e:
                        print(f"Error sending message: {e}")

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        print(f"Server listening on {self.host}:{self.port}")


        threading.Thread(target=self.server_input, daemon=True).start()

        while True:
            conn, addr = s.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    server = PollServer()
    server.start()
