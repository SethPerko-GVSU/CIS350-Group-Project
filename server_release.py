import socket
import threading
import datetime

class PollServer:
    def __init__(self, host, port, update_callback=None):
        self.host = host
        self.port = port
        self.connected_clients = []  
        self.lock = threading.Lock()
        self.username = 'SERVER_NAME'
        self.update_callback = update_callback

    def handle_client(self, conn, addr):
        msg = f"Client connected from {addr[0]}:{addr[1]}"
        print(msg)
        
        if self.update_callback:
            self.update_callback(msg)
        
        with self.lock:
            self.connected_clients.append(conn)

        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                
                timestamp = datetime.datetime.now().strftime("[%I:%M %p]")
                full_msg = f"{timestamp} {data}"
                print(full_msg)
                
                with self.lock:
                    for c in self.connected_clients:
                        c.sendall(full_msg.encode())
                    
                if self.update_callback:
                    self.update_callback(full_msg)
            except:
                break

    def server_input(self):
        while True:
            message = f'{self.username}: {input()}'
            with self.lock:
                for conn in self.connected_clients:
                    conn.sendall(message.encode())

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen()
        print(f"Server listening on {self.host}:{self.port}")
        
        if self.update_callback:
            self.update_callback(f"Server listening on {self.host}:{self.port}")

        threading.Thread(target=self.server_input, daemon=True).start()

        while True:
            conn, addr = self.s.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
            
    def stop(self):
        self.s.close()
        
        
