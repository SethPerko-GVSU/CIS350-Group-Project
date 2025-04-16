import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from client_release import PollClient
from server_release import PollServer
import threading
import datetime

def start_server(controller, host, port):
    def server_callback(msg):
        try:
            server_page = controller.frames["Server_Page"]
            server_page.append_message(msg)
        except Exception as e:
            print(f"Callback error: {e}")

    controller.server = PollServer(host, port, update_callback=server_callback)
    
    def run_server():
        controller.server.start()

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    controller.show_frame("Server_Page")
    
def start_client(controller, IP, Port, Username):
    controller.client = PollClient(IP, int(Port), Username)
    def run_client():
        controller.client.start()
        controller.client.receive_messages()

    thread = threading.Thread(target=run_client, daemon=True)
    thread.start()
    
    if not controller.username:
        with open("chatroom_info.txt", "w") as f:
            f.write(Username + '\n' + IP + '\n' + str(Port) + '\n')
        controller.username = Username
        controller.IP = IP
        controller.Port = str(Port)

    controller.show_frame("Chatroom_Page")

class Chatroom(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        try:
            with open("chatroom_info.txt", "r") as f:
                self.username = f.readline().strip()
                self.IP = f.readline().strip()
                self.Port = f.readline().strip()
        except:
            with open("chatroom_info.txt", "w") as f:
                self.username = ""
                self.IP = ""
                self.Port = ""
            
        try:
            with open("chatroom_text.txt", "r") as f: 
                self.chatroom_text = f.read()
        except:
            with open("chatroom_text.txt", "w") as f: 
                self.chatroom_text = ""
        
        self.server = None
        self.client = None
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        self.frames = {}
        for F in (StartPage, Server_Page, Client_Page, Chatroom_Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
        if page_name == "Server_Page":
            frame.update_server_info(self.server.host, self.server.port)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Are you a Server or Client?", font=controller.title_font).grid(row=0, column=0, columnspan=2, rowspan=2)

        button1 = tk.Button(self, text="Server",
                            command=lambda: controller.show_frame("Server_Page"))
        button2 = tk.Button(self, text="Client",
                            command=lambda: controller.show_frame("Client_Page"))
        button1.grid(row=2, column=0)
        button2.grid(row=2, column=1)


class Server_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.message_log = tk.StringVar()
        self.message_log.set("")
        
        IP_info = tk.StringVar()
        Port = tk.StringVar()
        self.text_var = tk.StringVar()
        self.text_var.set("Set up server settings...")
         
        label = tk.Label(self, textvariable=self.text_var, font=controller.title_font).grid(row=0, column=0, columnspan=3)
        local_button = tk.Button(self, text="Local", command=lambda: start_server(controller, "127.0.0.1", 53827)).grid(row=1, column=0)
        IP_label = tk.Label(self, text="Server IP:").grid(row=1, column=1)
        Port_label = tk.Label(self, text="Server Port:").grid(row=2, column=1)
        IP_entry = tk.Entry(self, textvariable=IP_info).grid(row=1, column=2)
        Port_entry = tk.Entry(self, textvariable=Port).grid(row=2, column=2)
        public_button = tk.Button(self, text="Use Values", command=lambda: start_server(controller, IP_info.get(), int(Port.get()))).grid(row=2, column=0)
        
        self.message_display = Message(self, textvariable=self.message_log, width=500)
        self.message_display.grid(row=3, column=0, columnspan=3)
        
    def update_server_info(self, host, port):
        self.text_var.set(f"Server running at {host}:{port}")
        
    def append_message(self, msg):
        current = self.message_log.get()
        self.message_log.set(current + "\n" + msg)


class Client_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        IP_info = tk.StringVar()
        Port = tk.StringVar()
        self.Username = tk.StringVar()
        
        if controller.username:
            self.Username.set(controller.username)
            
        if controller.IP:
            IP_info.set(controller.IP)
        
        if controller.Port:
            Port.set(controller.Port)
        
        IP_label = tk.Label(self, text="Server IP:").grid(row=0, column=0)
        Port_label = tk.Label(self, text="Server Port:").grid(row=1, column=0)
        Username_label = tk.Label(self, text="Username:").grid(row=2, column=0)
        IP_entry = tk.Entry(self, textvariable=IP_info).grid(row=0, column=1)
        Port_entry = tk.Entry(self, textvariable=Port).grid(row=1, column=1)
        Username_entry = tk.Entry(self, textvariable=self.Username).grid(row=2, column=1)
        continue_button = tk.Button(self, text="Continue", command=lambda: start_client(controller, IP_info.get(), Port.get(), self.Username.get())).grid(row=3, column=1)

class Chatroom_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.curr_message = tk.StringVar()
        self.chat_box_text = tk.StringVar()
        self.chat_box_text.set(self.controller.chatroom_text)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        chat_box = Message(self, textvariable=self.chat_box_text, width=500, anchor="w", padx=10, pady=10, justify="left")
        chat_box.grid(row=0, column=1, padx=100, pady=10, sticky="nsew")
        
        message_entry = tk.Entry(self, textvariable=self.curr_message, width=50)
        message_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=1)

        send_button = tk.Button(button_frame, text="Send", command=self.send_message).pack(side="left", padx=(0, 10))
        clear_button = tk.Button(button_frame, text="Clear Chat", command=self.clear_chat).pack(side="left")
        
    def send_message(self):
        client_page = self.controller.frames["Client_Page"]
        username = client_page.Username.get()
        self.controller.client.send_message(self.curr_message.get())
        self.update_chat_box(self.curr_message.get(), username)
        self.curr_message.set("")
        
    def update_chat_box(self, text, sender):
        timestamp = datetime.datetime.now().strftime("[%I:%M %p]")
        final_message = f"{timestamp} {sender}: {text}"
        self.chat_box_text.set(self.chat_box_text.get().strip() + '\n' + final_message)
        self.controller.chatroom_text = self.chat_box_text.get()
        
        with open("chatroom_text.txt", "w") as f: 
            f.write(self.controller.chatroom_text)
    
    def clear_chat(self):
        self.chat_box_text.set("")
        self.controller.chatroom_text = ""

        with open("chatroom_text.txt", "w") as f:
            f.write("")
        

if __name__ == "__main__":
    app = Chatroom()
    app.mainloop()
