import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from client_release import PollClient
from server_release import PollServer
import threading

class Chatroom(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Server_Page, Client_Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            
        self.server = None

        the_menu = Menu(self)
        self.config(menu=the_menu)
        filemenu = Menu(the_menu)
        the_menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New')
        filemenu.add_command(label='Open...')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.quit)

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
        label = tk.Label(self, text="Are you a Server or Client?", font=controller.title_font)
        label.grid(row=0, column=1)

        button1 = tk.Button(self, text="Server",
                            command=lambda: start_server(controller))
        button2 = tk.Button(self, text="Client",
                            command=lambda: controller.show_frame("Client_Page"))
        button1.grid(row=2, column=0)
        button2.grid(row=2, column=2)


class Server_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Waiting on Server...", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)
        
    def update_server_info(self, host, port):
        # Update the label with server host and port.
        self.label.config(text=f"Server running at {host}:{port}")


class Client_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


def start_server(controller):
    """Start the server in a separate thread to prevent UI freezing."""
    def run_server():
        controller.server = PollServer()
        controller.server.start()

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    controller.show_frame("Server_Page")


if __name__ == "__main__":
    app = Chatroom()
    app.mainloop()
