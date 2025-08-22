from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as font

# Properties - Window

root = Tk()
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

##################################################################################################################################
###################################################   MENUBAR  ###################################################################
##################################################################################################################################

menu_frame = tk.Frame(root, background="gray60", height=30)
menu_frame.pack(side="top", fill="x")

# Budget Menu Button

budget_button = tk.Menubutton(menu_frame, text="Budget", font="arial 10 bold", relief="raised", background="gray60")
budget_button.pack(side="left", padx=5, pady=2)

budget_menu = tk.Menu(budget_button, tearoff=0)
budget_menu.add_command(label="New")
budget_menu.add_command(label="Edit")
budget_menu.add_command(label="View")

budget_button.config(menu=budget_menu)

# Saving Menu Button

saving_button = tk.Menubutton(menu_frame, text="Saving", font="arial 10 bold", relief="raised", background="gray60")
saving_button.pack(side="left", padx=5, pady=2)

saving_menu = tk.Menu(saving_button, tearoff=0)

saving_menu.add_command(label="Set Savings Goal")
saving_menu.add_command(label="Edit Savings Goal")
saving_menu.add_separator()
saving_menu.add_command(label="Add Entry")
saving_menu.add_command(label="Edit Entry")
saving_menu.add_command(label="Remove Entry")

saving_button.config(menu=saving_menu)

# Year Menu Button

year_button = tk.Menubutton(menu_frame, text="Year", font="arial 10 bold", relief="raised", background="gray60")
year_button.pack(side="left", padx=5, pady=2)

year_menu = tk.Menu(year_button, tearoff=0)

year_menu.add_command(label="New")
year_menu.add_command(label="Edit")
year_menu.add_command(label="Load")

year_button.config(menu=year_menu)

report_button = tk.Menubutton(menu_frame, text="Reports", font="arial 10 bold", relief="raised", background="gray60")
report_button.pack(side="left", padx=5, pady=2)

report_menu = tk.Menu(report_button, tearoff=0)

report_menu.add_command(label="Generate")
report_menu.add_command(label="Load")
report_menu.add_command(label="Download")

report_button.config(menu=report_menu)


root.mainloop()