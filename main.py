############################################## IMPORTS ##############################################
from tkinter import *

import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, Button

from pages.budget import BudgetPage
from pages.year import YearPage
from pages.savings import SavingsPage
from pages.reports import ReportPage
from pages.help_1 import Guide

from tkmacosx import Button
from tkcalendar import Calendar
from datetime import datetime


############################################## Setup ##############################################

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

###################################################   MISC  ###################################################################

# Calender Widget
            
def open_calendar(entry_widget):
    # Always set to normal before opening calendar
    entry_widget.config(state="normal", background="gray74", readonlybackground="gray90")
    popup = Toplevel()
    popup.title("Select Date")
    popup.configure(background="gray74")
    popup.grab_set()
    
    style = ttk.Style(popup)
    style.theme_use('clam')

    cal = Calendar(popup, selectmode='day', background="blue2", foreground="white", headersbackground="gray60", headersforeground="black")
    cal.pack(padx=10, pady=10)

    def select_date():
        raw_date = cal.get_date()
        try:
            # Try parsing common formats
            parsed_date = datetime.strptime(raw_date, "%m/%d/%y")  
        except ValueError:
            parsed_date = datetime.strptime(raw_date, "%m/%d/%Y") 
            
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        entry_widget.delete(0, "end")
        entry_widget.insert(0, formatted_date)
        entry_widget.config(state="readonly", background="gray90", readonlybackground="gray90")
        popup.destroy()

    Button(popup, text="Select", command=select_date, borderless=1).pack(pady=5, padx=5)

# Limits size of option menu

cat_var = tk.StringVar()
width = 5

def strip_str(val):
    selected_value = cat_var.get()
    cat_var.set(selected_value[:width] + ("" if len(selected_value) <= width else "..."))
    print(val)
    
###################################################   MENUBAR  ###################################################################

# Menubar - Dark gray bar with bottons. Underneath the header

menu_frame = tk.Frame(root, background="gray60", height=30) 
menu_frame.pack(side="top", fill="x")

###################################################   MENUBAR BUTTONS  ###################################################################

# Budget Menu Button

budget_button = tk.Menubutton(menu_frame, text="Budget", font="arial 10 bold", relief="raised", background="gray60")
budget_button.pack(side="left", padx=5, pady=2)

###################################################   OPEN FUNCTIONS  ###################################################################

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

def show_year_page():
    # Cleares the Dashboard
    for widget in window.winfo_children():
        widget.destroy()
    
    # Creates the tab bar (dark gray)
    tab_bar = tk.Frame(window, background="gray40", height=30)
    tab_bar.pack(fill="x")
    
    # Creates the tab itself
    tab_label = tk.Label(tab_bar, text="Yearly Overview", font="Arial 10 bold", background="gray30", foreground="White")
    tab_label.pack(side="left", padx=10)
    
    YearPage(window)
    
def show_savings_page():
    # Cleares the Dashboard
    for widget in window.winfo_children():
        widget.destroy()
        
    # Creates the tab bar (dark gray)
    tab_bar = tk.Frame(window, background="gray40", height=30)
    tab_bar.pack(fill="x")
    
    # Creates the tab itself
    tab_label = tk.Label(tab_bar, text="Savings Page", font="Arial 10 bold", background="gray30", foreground="White")
    tab_label.pack(side="left", padx=10)
    
    SavingsPage(window)

def show_report_page():
    # Cleares the Dashboard
    for widget in window.winfo_children():
        widget.destroy()
        
    # Creates the tab bar (dark gray)
    tab_bar = tk.Frame(window, background="gray40", height=30)
    tab_bar.pack(fill="x")
    
    # Creates the tab itself
    tab_label = tk.Label(tab_bar, text="Reports Page", font="Arial 10 bold", background="gray30", foreground="White")
    tab_label.pack(side="left", padx=10)
    
    ReportPage(window)
      
def show_guide_page():
    # Cleares the Dashboard
    for widget in window.winfo_children():
        widget.destroy()
        
    # Creates the tab bar (dark gray)
    tab_bar = tk.Frame(window, background="gray40", height=30)
    tab_bar.pack(fill="x")
    
    # Creates the tab itself
    tab_label = tk.Label(tab_bar, text="Reports Page", font="Arial 10 bold", background="gray30", foreground="White")
    tab_label.pack(side="left", padx=10)
    
    Guide(window)

###################################################   POPUP FUNCTIONS  ###################################################################
    
def load_budget_pop():
    budg_pop = tk.Toplevel()
    budg_pop.title("Load Budget")
    budg_pop.geometry("450x250+350+300")
    budg_pop.maxsize(450, 250)
    budg_pop.minsize(450, 250)
    budg_pop.configure(background="gray74")
    
    ######### LEFT SECTION ##########
    
    left_frame = tk.Frame(budg_pop, background="gray74", highlightbackground="black", highlightthickness=None)
    left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=0.8)
    
    inner_l_frame = tk.LabelFrame(left_frame, text="Year", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
    inner_l_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    ######### RIGHT SECTION #########
    
    right_frame = tk.Frame(budg_pop, background="gray74", highlightbackground="black", highlightthickness=None)
    right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.8)
    
    inner_r_frame = tk.LabelFrame(right_frame, text="Month", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
    inner_r_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    ######### BOTTOM SECTION ########

    bot_frame = tk.Frame(budg_pop, background="gray74", highlightbackground="black", highlightthickness=None)
    bot_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
    
    inner_bot_frame = tk.LabelFrame(bot_frame, text="", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="flat")
    inner_bot_frame.pack(padx=10, pady=0, fill="both", expand=True)
    
    # TO DO: Load function
    
    load = Button(inner_bot_frame, text="Load", background="PaleGreen1", relief="raised", width=75, 
                  borderless=1, activebackground='green2')
    load.pack(side="left", padx=[100, 0])
    
    cancel = Button(inner_bot_frame, text="Cancel", background="gray90", relief="raised", width=75, 
                    borderless=1, command=budg_pop.destroy, activebackground='red2')
    cancel.pack(side="right", padx=[0, 100])

def quick_add_savings():
    
    goals = ["Car", "House", "E-Bike", "New PC", "TEEEEEEEEEEEEST"] # NEEDS TO IMPORT USERS DEFINED GOALS
    
    quick_pop = tk.Toplevel()
    quick_pop.title("Quick Add")
    quick_pop.geometry("850x50+150+175")
    quick_pop.maxsize(850, 50)
    quick_pop.minsize(850, 50)
    quick_pop.configure(background="gray74")
    
    pop_view = tk.Frame(quick_pop, background="gray74", highlightbackground="black", highlightthickness=None)
    pop_view.pack(padx=5, pady=5, fill="both", expand=True)
    
    date_label = Label(pop_view, text="Date", font="system 10 bold", foreground="black", background="gray74")
    date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    date_entry = Entry(pop_view, highlightthickness=1, highlightcolor="blue", width=10, borderwidth=1, readonlybackground="gray90", foreground="black")
    date_entry.configure(state="readonly")
    date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    calendar_btn = Button(pop_view, text="Pick", command=lambda: open_calendar(date_entry), relief="raised", borderless=1)
    calendar_btn.grid(row=0, column=2, padx=[0, 5], pady=5, sticky="w")
    
    separator1 = ttk.Separator(pop_view, orient=tk.VERTICAL)
    separator1.grid(row=0, column=3, rowspan=3, padx=[20, 20], pady=0, sticky=tk.NS)
    
    amount_label = Label(pop_view, text="Amount", font="system 10 bold", foreground="black", background="gray74")
    amount_label.grid(row=0, column=4, padx=5, pady=5, sticky="e")
    amount_entry = Entry(pop_view, highlightthickness=1, highlightcolor="blue", width=10, borderwidth=1, background="gray90", foreground="black")
    amount_entry.grid(row=0, column=5, padx=5, pady=5, sticky="e")
    
    separator2 = ttk.Separator(pop_view, orient=tk.VERTICAL)    
    separator2.grid(row=0, column=6, rowspan=3, padx=[20, 20], pady=0, sticky=tk.NS)
            
    cat_label = Label(pop_view, text="Category", font="system 10 bold", foreground="black", background="gray74")
    cat_label.grid(row=0, column=7, padx=5, pady=5, sticky="e")
    cat_entry = tk.OptionMenu(pop_view, cat_var, *goals, command=strip_str)
    cat_entry.configure(relief="sunken", background="gray74", foreground="black")
    cat_entry.grid(row=0, column=8, padx=5, pady=5, sticky="ew")
        
    separator3 = ttk.Separator(pop_view, orient=tk.VERTICAL)    
    separator3.grid(row=0, column=9, rowspan=3, padx=[20, 20], pady=0, sticky=tk.NS)
    
    add_button = Button(pop_view, text="Add", background="PaleGreen1", relief="raised", width=50, borderless=1, activebackground="green2")
    add_button.grid(row=0, column=10, padx=5, pady=5, sticky="e")
    
    cancel_button = Button(pop_view, text="Cancel", background="gray90", relief="raised", width=50, borderless=1, activebackground="red2", command=quick_pop.destroy)
    cancel_button.grid(row=0, column=12, padx=5, pady=5, sticky="e") 
       
# Budget Menu Dropdown Options

budget_menu = tk.Menu(budget_button, tearoff=0, relief="raised")

# Currently: opens budget. Ideally: open popup where creation and settings are

budget_menu.add_command(label="New", command=show_budget_page)

# Currently: nothing. Ideally: open popup showing loadable budgets

budget_menu.add_command(label="Load", command=load_budget_pop)

budget_button.config(menu=budget_menu)

### Saving Menu Button ###

savings_button = tk.Menubutton(menu_frame, text="Saving", font="arial 10 bold", relief="raised", background="gray60")
savings_button.pack(side="left", padx=5, pady=2)

savings_menu = tk.Menu(savings_button, tearoff=0)

savings_menu.add_command(label="Open", command=show_savings_page)
savings_menu.add_separator()
savings_menu.add_command(label="Quick Add", command=quick_add_savings)

savings_button.config(menu=savings_menu)

### Year Menu Button ###

year_button = tk.Menubutton(menu_frame, text="Year", font="arial 10 bold", relief="raised", background="gray60")
year_button.pack(side="left", padx=5, pady=2)

year_menu = tk.Menu(year_button, tearoff=0)

year_menu.add_command(label="Open", command=show_year_page)
year_menu.add_command(label="New")

year_button.config(menu=year_menu)

### Reports Button ###

report_button = tk.Menubutton(menu_frame, text="Reports", font="arial 10 bold", relief="raised", background="gray60")
report_button.pack(side="left", padx=5, pady=2)

report_menu = tk.Menu(report_button, tearoff=0)

report_menu.add_command(label="Open", command=show_report_page)


report_button.config(menu=report_menu)

### Help Button ###

help_button = tk.Menubutton(menu_frame, text="Help", font="arial 10 bold", relief="raised", background="gray60")
help_button.pack(side="left", padx=5, pady=2)

help_menu = tk.Menu(help_button, tearoff=0)

help_menu.add_command(label="Guide", command=show_guide_page)
help_menu.add_command(label="Report A Problem") # Set up link to Formspree page on website.

help_button.config(menu=help_menu)

###################################################   CONTENT   ##################################################################

# Content of window will go here: Some sort of visuals and summary of current months budget.

window = tk.Frame(root, background="white")
window.pack(side="top", fill="both", expand=True)

root.mainloop()