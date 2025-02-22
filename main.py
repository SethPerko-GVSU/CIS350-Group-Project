import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from client_release import PollClient
from server_release import PollServer
import threading

def start_server(controller, host, port):
    """Start the server in a separate thread to prevent UI freezing."""
    def run_server():
        controller.server = PollServer(host, port)
        controller.server.start()

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    controller.show_frame("Server_Page")
    
def start_client(controller, IP, Port, Username):
    """Start the client in a separate thread to prevent UI freezing."""
    def run_client():
        controller.client = PollClient(IP, int(Port), Username)
        controller.client.start()
        controller.client.receive_messages()

    server_thread = threading.Thread(target=run_client, daemon=True)
    server_thread.start()

    controller.show_frame("Chatroom_Page")

class Chatroom(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (StartPage, Server_Page, Client_Page, Chatroom_Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            
        self.server = None
        self.client = None

        ''' the_menu = Menu(self)
        self.config(menu=the_menu)
        filemenu = Menu(the_menu)
        the_menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New')
        filemenu.add_command(label='Open...')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.quit) '''

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
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
        
    def update_server_info(self, host, port):
        # Update the label with server host and port.
        self.text_var.set(f"Server running at {host}:{port}")


class Client_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        IP_info = tk.StringVar()
        Port = tk.StringVar()
        Username = tk.StringVar()
        
        IP_label = tk.Label(self, text="Server IP:").grid(row=0, column=0)
        Port_label = tk.Label(self, text="Server Port:").grid(row=1, column=0)
        Username_label = tk.Label(self, text="Username:").grid(row=2, column=0)
        IP_entry = tk.Entry(self, textvariable=IP_info).grid(row=0, column=1)
        Port_entry = tk.Entry(self, textvariable=Port).grid(row=1, column=1)
        Username_entry = tk.Entry(self, textvariable=Username).grid(row=2, column=1)
        continue_button = tk.Button(self, text="Continue", command=lambda: start_client(controller, IP_info.get(), Port.get(), Username.get())).grid(row=3, column=1)

class Chatroom_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.curr_message = tk.StringVar()
        
        message_entry = tk.Entry(self, textvariable=self.curr_message).grid(row=0, column=1)
        send_button = tk.Button(self, text="Send", command=lambda: self.send_message()).grid(row=1, column=1)
        
    def send_message(self):
        self.controller.client.send_message(self.curr_message.get())
        self.curr_message.set("")
        

if __name__ == "__main__":
    app = Chatroom()
    app.mainloop()
