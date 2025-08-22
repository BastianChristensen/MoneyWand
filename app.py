from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as font

# Properties - Window

root = tk.Tk()
root.geometry("1152x720")
root.title("Dashboard")
root.minsize(1152, 720)

# Header

header_frame = tk.Frame(root, background="gray88", height=75)
header_frame.pack(side="top", fill="x", anchor="ne")

# Image

title = tk.PhotoImage(file="assets/title.png")
title_label = tk.Label(header_frame, image=title, background="gray88")
title_label.place(x=10, y=0)

icon = tk.PhotoImage(file="assets/icon.png")
icon_label = tk.Label(header_frame, image=icon, background="gray88")
icon_label.place(x=360, y=-5)

root.mainloop()