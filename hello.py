from tkinter import *

def on_key_press(event):
    print(f"Key pressed: {event.keysym}")

def on_left_click(event):
    print(f"Left click at ({event.x}, {event.y})")

def on_right_click(event):
    print(f"Right click at ({event.x}, {event.y})")

def on_mouse_motion(event):
    print(f"Mouse moved to ({event.x}, {event.y})")

root = Tk(screenName=None, baseName=None, className='Tk', useTk=1)

root.bind("<KeyPress>", on_key_press) # functions can be named anything we want but the text is what's important
root.bind("<Button-1>", on_left_click)
root.bind("<Button-3>", on_right_click)
root.bind("<Motion>", on_mouse_motion)

label_1 = Label(root, text="Example Text").grid(row=0, column=0)
entry_1 = Entry(root).grid(row=0, column=1)

button_1 = Button(root, text="Stop", width=25, command=root.destroy).grid(row=1)

checkbox_1 = IntVar()
Checkbutton(root, text="Checkbox", variable=checkbox_1).grid(row=1, column=1)

Choice_1 = IntVar()
Radiobutton(root, text='Option 1', variable=Choice_1, value=1).grid(row=2)
Radiobutton(root, text='Option 2', variable=Choice_1, value=2).grid(row=3)
Radiobutton(root, text='Option 3', variable=Choice_1, value=3).grid(row=4)

list_box_1 = Listbox(root)
list_box_1.insert(1, 'Option 1')
list_box_1.insert(2, 'Option 2')
list_box_1.insert(3, 'Option 3')
list_box_1.grid(row=5)

the_menu = Menu(root)
root.config(menu=the_menu)
filemenu = Menu(the_menu)
the_menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New')
filemenu.add_command(label='Open...')
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)

ourMessage = 'This can be used to write really long messages such as one we may recieve in the chatroom application'
messageVar = Message(root, text=ourMessage).grid(row=2, column=1)

root.mainloop()