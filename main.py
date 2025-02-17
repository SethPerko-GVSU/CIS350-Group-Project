import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from client_release import PollClient
from server_release import PollServer

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


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Are you a Server or Client?", font=controller.title_font)
        label.grid(row=0, column=1)

        button1 = tk.Button(self, text="Server",
                            command=lambda: controller.show_frame("Server_Page"))
        button2 = tk.Button(self, text="Client",
                            command=lambda: controller.show_frame("Client_Page"))
        button1.grid(row=2, column=0)
        button2.grid(row=2, column=2)


class Server_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class Client_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

def start_server(controller):
    controller.show_frame("Server_Page")
    server = PollServer()
    server.start()


if __name__ == "__main__":
    app = Chatroom()
    app.mainloop()