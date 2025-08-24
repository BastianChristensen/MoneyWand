############################################## IMPORTS ##############################################
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as font
from pages.budget import BudgetPage

############################################## ROOT Setup ##############################################

root = Tk()
root.geometry("1152x700")
root.title("Dashboard")
root.minsize(1152, 700)
root.maxsize(1152, 700)

# Header - banner at the top of the screen (gray part)

header_frame = tk.Frame(root, background="gray88", height=75)
header_frame.pack(side="top", fill="x", anchor="ne")

# Image - App Logo - overlayed the header

title = tk.PhotoImage(file="assets/title.png")
title_label = tk.Label(header_frame, image=title, background="gray88")
title_label.place(x=10, y=0)

icon = tk.PhotoImage(file="assets/icon.png")
icon_label = tk.Label(header_frame, image=icon, background="gray88")
icon_label.place(x=360, y=-5)

###################################################   MENUBAR  ###################################################################

# Menubar - Dark gray bar with bottons. Underneath the header

menu_frame = tk.Frame(root, background="gray60", height=30)
menu_frame.pack(side="top", fill="x")

###################################################   MENUBAR BUTTONS  ###################################################################

# Budget Menu Button

budget_button = tk.Menubutton(menu_frame, text="Budget", font="arial 10 bold", relief="raised", background="gray60")
budget_button.pack(side="left", padx=5, pady=2)

# Function that opens a budget 

def show_budget_page():
    
    # Cleares the Dashboard
    for widget in window.winfo_children():
        widget.destroy()
    
    # Creates the tab bar (dark gray)
    tab_bar = tk.Frame(window, background="gray40", height=30)
    tab_bar.pack(fill="x")

    # Creates the tab itself
    tab_label = tk.Label(tab_bar, text="Budget", font="Arial 10 bold", background="gray30", foreground="White")
    tab_label.pack(side="left", padx=10)
    
    # BudgetPage class with window as input
    BudgetPage(window)

# Budget Menu Dropdown Options

budget_menu = tk.Menu(budget_button, tearoff=0, relief="raised")

# Currently: opens budget. Ideally: open popup where creation and settings are

budget_menu.add_command(label="New", command=show_budget_page)

# Currently: nothing. Ideally: open popup showing loadable budgets

budget_menu.add_command(label="Load")

budget_button.config(menu=budget_menu)

### Saving Menu Button ###

# NOT IMPLEMENTED YET

savings_button = tk.Menubutton(menu_frame, text="Saving", font="arial 10 bold", relief="raised", background="gray60")
savings_button.pack(side="left", padx=5, pady=2)

savings_menu = tk.Menu(savings_button, tearoff=0)

savings_menu.add_command(label="Set Savings Goal")
savings_menu.add_command(label="Edit Savings Goal")
savings_menu.add_separator()
savings_menu.add_command(label="Add Entry")
savings_menu.add_command(label="Edit Entry")
savings_menu.add_command(label="Remove Entry")

savings_button.config(menu=savings_menu)

### Year Menu Button ###

# NOT IMPLEMENTED YET

year_button = tk.Menubutton(menu_frame, text="Year", font="arial 10 bold", relief="raised", background="gray60")
year_button.pack(side="left", padx=5, pady=2)

year_menu = tk.Menu(year_button, tearoff=0)

year_menu.add_command(label="New")
year_menu.add_command(label="Edit")
year_menu.add_command(label="Load")

year_button.config(menu=year_menu)

### Reports Button ###

# NOT IMPLEMENTED YET

report_button = tk.Menubutton(menu_frame, text="Reports", font="arial 10 bold", relief="raised", background="gray60")
report_button.pack(side="left", padx=5, pady=2)

report_menu = tk.Menu(report_button, tearoff=0)

report_menu.add_command(label="Generate")
report_menu.add_command(label="Load")
report_menu.add_command(label="Download")

report_button.config(menu=report_menu)

### Help Button ###

# NOT IMPLEMENTED YET

help_button = tk.Menubutton(menu_frame, text="Help", font="arial 10 bold", relief="raised", background="gray60")
help_button.pack(side="left", padx=5, pady=2)

help_menu = tk.Menu(help_button, tearoff=0)

help_menu.add_command(label="Guide")
help_menu.add_command(label="Report A Problem")

help_button.config(menu=help_menu)



###################################################   CONTENT   ##################################################################

# Content of window will go here: Some sort of visuals and summary of current months budget.

window = tk.Frame(root, background="white")
window.pack(side="top", fill="both", expand=True)

root.mainloop()