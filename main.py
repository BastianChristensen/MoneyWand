############################################## IMPORTS ##############################################

from tkinter import *

import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import Toplevel, Button

from pages.budget import BudgetPage
from pages.year import YearPage
from pages.savings import SavingsPage
from pages.reports import ReportPage
from pages.help_1 import Guide
from db.database import *

from tkmacosx import Button
from tkcalendar import Calendar
from datetime import datetime

############################################## Setup ##############################################

root = Tk()
root.geometry("1152x700+100+0")
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

# Global lists 
    
new_budget_pop_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

new_budget_pop_years = list(range(2020, 2051))

###################################################   MENUBAR  ###################################################################

# Menubar - Dark gray bar with bottons. Underneath the header

menu_frame = tk.Frame(root, background="gray60", height=30) 
menu_frame.pack(side="top", fill="x")

###################################################   MENUBAR BUTTONS  ###################################################################

# Budget Menu Button

budget_button = tk.Menubutton(menu_frame, text="Budget", font="arial 10 bold", relief="raised", background="gray60")
budget_button.pack(side="left", padx=5, pady=2)

###################################################   OPEN FUNCTIONS  ###################################################################

def show_budget_page(id):
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
    BudgetPage(window, id)

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

def new_budget():
    new_bud_pop = tk.Toplevel()
    new_bud_pop.title("New Budget")
    new_bud_pop.geometry("450x100+350+300")
    new_bud_pop.maxsize(450, 100)
    new_bud_pop.minsize(450, 100)
    new_bud_pop.configure(background="gray74")
    
    new_bud_pop.grab_set()
    new_bud_pop.transient(root)
    
    ######### TOP SECTION ##########
    # Limits size of option menu

    cat_var = tk.StringVar()
    cat_var2 = tk.StringVar()
    
    top_frame = tk.Frame(new_bud_pop, background="gray74")
    top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.70)
    
    top_inner_frame = tk.LabelFrame(new_bud_pop, text="", background="gray74", borderwidth=1, relief="flat")
    top_inner_frame.pack(padx=10, pady=0, fill="both", expand=True)
    
    year_label = Label(top_inner_frame, background="gray74", text="Select Year", font="system 10", foreground="black")
    year_label.grid(row=0, column=0, padx=10, pady=[10, 5])
    
    year = tk.OptionMenu(top_inner_frame, cat_var, *new_budget_pop_years)
    year.configure(relief="sunken", background="gray74", foreground="black")
    year.grid(row=0, column=1, padx=10, pady=[10, 5])
    
    month_label = Label(top_inner_frame, background="gray74", text="Select Month", font="system 10", foreground="black")
    month_label.grid(row=0, column=2, padx=10, pady=[10, 5])
    
    months = tk.OptionMenu(top_inner_frame, cat_var2, *new_budget_pop_months)
    months.configure(relief="sunken", background="gray74", foreground="black")
    months.grid(row=0, column=3, padx=10, pady=[10, 5])
    
    # Update label text based on selected year and month
    
    def update_label(*args):
        year_val = cat_var.get()
        month_val = cat_var2.get()
        text.config(text=f"Create new budget for {month_val}, {year_val}")

    text = Label(top_inner_frame, background="gray74", text="Create new budget for {}, {}", font="system 10", foreground="black")
    text.grid(row=1, column=0, padx=10, pady=10, columnspan=4, sticky="ew")
    # Center it
    top_inner_frame.grid_columnconfigure(0, weight=1)
    top_inner_frame.grid_columnconfigure(1, weight=1)
    top_inner_frame.grid_columnconfigure(2, weight=1)
    top_inner_frame.grid_columnconfigure(3, weight=1)

    # Trace changes to update label
    
    cat_var.trace_add("write", update_label)
    cat_var2.trace_add("write", update_label)
    text.grid(row=1, column=0, padx=10, pady=10)
        
    def create():
        # Get info
        sel_year = cat_var.get()
        sel_month = cat_var2.get()
        
        conn = sqlite3.connect("moneywand.db")
        c = conn.cursor()
        
        # Check if year/month combo is unique
        c.execute("SELECT 1 FROM budgets WHERE year=? AND month=?", (sel_year, sel_month))
        exists = c.fetchone()
        if exists:
            tkinter.messagebox.showerror("Error", f"Budget for {sel_month}, {sel_year} already exists.")
            conn.close()
            return
        
        # Check if both are selected
        elif sel_year == "" or sel_month == "":
            tkinter.messagebox.showerror("Error", "Please select both month and year.")
            conn.close()
            return
        
        else:
            # Add budget to database
            # Budget Setup 
            def setup_pop():
                pop = tk.Toplevel()
                pop.title("Budget Setup")
                pop.geometry("360x700+150+50")
                pop.maxsize(360, 700)
                pop.minsize(360, 700)
                pop.configure(background="gray74")
                
                pop.grab_set()
                pop.transient(root)
                
                categories = ["Housing", "Food", "Utilities", "Transport", "Savings", "Insurance", "Debt", "Health", "Entertainment", "Misc"]
                cat_var3 = tk.StringVar()
                
                ######### TOP SECTION ##########
                top = tk.Frame(pop, background="gray74")
                top.place(relx=0, rely=0, relwidth=1, relheight=0.5)
                
                t_inner = tk.LabelFrame(top, text="Settings", font="system 15 bold", foreground="black", background="gray82",
                                        borderwidth=1, relief="sunken")
                t_inner.pack(padx=10, pady=[0, 10], fill="both", expand=True)

                ######### BOTTOM SECTION ##########
                
                botm = tk.Frame(pop, background="gray74")
                botm.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
                
                b_inner = tk.LabelFrame(botm, text="Info", font="system 15 bold", foreground="black", background="lightsteelblue1",
                                        borderwidth=1, relief="sunken")
                b_inner.pack(padx=10, pady=10, fill="both", expand=True)
                
                ######### CONTENT #########
                
                
                ######################################## NAME ########################################
                
                
                name_label = tk.Label(t_inner, text="Name", font="system 10 bold", background="gray82")
                name_label.grid(row=0, column=0, padx=10, pady=10)
                
                name_label_b = tk.Label(b_inner, text="Name", font="system 10 bold", background="lightsteelblue1")
                name_label_b.grid(row=0, column=0, padx=10, pady=10) 
                
                name_data = tk.Label(b_inner, text=f"{sel_month}, {sel_year}", font="system 10 bold", background="lightsteelblue1", anchor="e")
                name_data.grid(row=0, column=1, padx=10, pady=10)
                
                name_entry = tk.Entry(t_inner, highlightthickness=1, highlightcolor="blue", width=10, borderwidth=1, readonlybackground="gray90", foreground="black")
                name_entry.grid(row=0, column=1, padx=10, pady=10)
                
                def apply_name_func():
                    entered_name = name_entry.get()
                    if entered_name:
                        name_data.config(text=entered_name)

                apply_name = Button(t_inner, text="Apply", relief="raised", borderless=1, command=apply_name_func)
                apply_name.grid(row=0, column=2, padx=10, pady=10)
                
                separator1 = ttk.Separator(t_inner, orient=tk.HORIZONTAL)
                separator1.grid(row=1, column=0, columnspan=3, pady=[10, 10], padx=5, sticky="ew")
                
                bseparator1 = ttk.Separator(b_inner, orient=tk.HORIZONTAL)
                bseparator1.grid(row=1, column=0, columnspan=3, pady=[10, 10], padx=5, sticky="ew")
                
                
                ######################################### CURRENCY ########################################
                
                
                curr_label = tk.Label(t_inner, text="Currency", font="system 10 bold", background="gray82")
                curr_label.grid(row=2, column=0, padx=10, pady=10)
                
                curr_label_b = tk.Label(b_inner, text="Currency", font="system 10 bold", background="lightsteelblue1")
                curr_label_b.grid(row=2, column=0, padx=10, pady=10) 
                
                curr_data = tk.Label(b_inner, text="NOK", font="system 10 bold", background="lightsteelblue1", anchor="e")
                curr_data.grid(row=2, column=1, padx=10, pady=10)
                
                cat_var = tk.StringVar()
                def strip_str(val):
                    width = 5
                    selected_value = cat_var.get()
                    cat_var.set(selected_value[:width] + ("" if len(selected_value) <= width else "..."))
                    print(val)
                currency_codes = ["NOK", "USD", "EUR", "GBP"]
                
                curr_entry = tk.OptionMenu(t_inner, cat_var, *currency_codes, command=strip_str)
                curr_entry.configure(relief="sunken", background="gray82", foreground="black")
                curr_entry.grid(row=2, column=1, padx=10, pady=10)
                
                def apply_curr_func():
                    entered_curr = cat_var.get()
                    if entered_curr:
                        curr_data.config(text=entered_curr)

                apply_curr = Button(t_inner, text="Apply", relief="raised", borderless=1, command=apply_curr_func)
                apply_curr.grid(row=2, column=2, padx=10, pady=10)
                
                separator2 = ttk.Separator(t_inner, orient=tk.HORIZONTAL)
                separator2.grid(row=3, column=0, columnspan=3, pady=[10, 10], padx=5, sticky="ew")
                
                bseparator2 = ttk.Separator(b_inner, orient=tk.VERTICAL)
                bseparator2.grid(row=3, column=0, columnspan=3, pady=[10, 10], padx=5, sticky="ew")


                ######################################## CATEGORIES ########################################    
                
                
                cat_label = tk.Label(t_inner, text="Categories", font="system 10 bold", background="gray82")
                cat_label.grid(row=4, column=0, padx=10, pady=10)

                b_cat_label = tk.Label(b_inner, text="Categories", font="system 10 bold", background="lightsteelblue1")
                b_cat_label.grid(row=4, column=0, padx=10, pady=10)
                
                cat_data = tk.Label(
                    b_inner,
                    text=", ".join(categories),
                    font="system 10 bold",
                    background="lightsteelblue1",
                    anchor="e",
                    wraplength=200,
                    justify="left"
                )
                cat_data.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
                
                cat_entry = tk.OptionMenu(t_inner, cat_var3, *categories, command=strip_str)
                cat_entry.configure(relief="sunken", background="gray82", foreground="black")
                cat_entry.grid(row=4, column=1, padx=10, pady=10)
                
                def edit_cat_pop():
                    p = tk.Toplevel(pop)
                    p.title("Edit Categories")
                    p.geometry("300x400")
                    p.configure(background="gray90")
                    
                    p.grab_set()
                    p.transient(pop)
            
                    listbox = tk.Listbox(p, selectmode=tk.SINGLE)
                    listbox.pack(fill="both", expand=True, padx=10, pady=10)
                    for cat in categories:
                        listbox.insert(tk.END, cat)

                    new_cat_entry = tk.Entry(p)
                    new_cat_entry.pack(padx=10, pady=5)

                    def add_category():
                        new_cat = new_cat_entry.get().strip()
                        if new_cat and new_cat not in categories:
                            categories.append(new_cat)
                            listbox.insert(tk.END, new_cat)
                            update_categories()

                    def remove_category():
                        selected = listbox.curselection()
                        if selected:
                            cat = listbox.get(selected)
                            categories.remove(cat)
                            listbox.delete(selected)
                            update_categories()

                    add_btn = Button(p, text="Add", background="white", borderless=1, activebackground="blue", command=add_category)
                    add_btn.pack(padx=10, pady=5, side="left")
                    remove_btn = Button(p, text="Remove", background="white", borderless=1, activebackground="red", command=remove_category)
                    remove_btn.pack(padx=10, pady=5, side="right")

                    def update_categories():
                        # Update OptionMenu
                        menu = cat_entry["menu"]
                        menu.delete(0, "end")
                        for cat in categories:
                            menu.add_command(label=cat, command=lambda value=cat: cat_var2.set(value))
                        # Update display
                        cat_data.config(text=", ".join(categories))
                
                edit_cat = Button(t_inner, text="Edit", relief="raised", borderless=1, command=edit_cat_pop)
                edit_cat.grid(row=4, column=2, padx=10, pady=10)
                
                separator3 = ttk.Separator(t_inner, orient=tk.HORIZONTAL)
                separator3.grid(row=5, column=0, columnspan=3, pady=[10, 10], padx=5, sticky="ew")
     
                
                ######################################## SPENDING LIMIT ########################################


                spending_limits = {cat: 0 for cat in categories}

                def edit_limit_pop():
                    limit_pop = tk.Toplevel(pop)
                    limit_pop.title("Edit Spending Limits")
                    limit_pop.geometry("300x400")
                    limit_pop.configure(background="gray90")
                    
                    limit_pop.grab_set()
                    limit_pop.transient(pop)

                    entries = {}

                    # Create entry for each category
                    for i, cat in enumerate(categories):
                        lbl = tk.Label(limit_pop, text=cat, background="gray90", font="system 10")
                        lbl.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                        ent = tk.Entry(limit_pop, width=10)
                        ent.insert(0, str(spending_limits.get(cat, 0)))
                        ent.grid(row=i, column=1, padx=10, pady=5)
                        entries[cat] = ent

                    def save_limits():
                        for cat, ent in entries.items():
                            try:
                                spending_limits[cat] = float(ent.get())
                            except ValueError:
                                spending_limits[cat] = 0
                        # Optionally update display in main popup here
                        limit_pop.destroy()
                
                    save_btn = Button(limit_pop, text="Save", background="PaleGreen1", borderless=1, command=save_limits)
                    save_btn.grid(row=len(categories), column=0, columnspan=2, pady=10)
                         
                lim_label = tk.Label(t_inner, text="Spending Limit", font="system 10 bold", background="gray82")
                lim_label.grid(row=6, column=0, padx=10, pady=10)
                
                lim_edit = Button(t_inner, text="Edit", relief="raised", borderless=1, command=edit_limit_pop)
                lim_edit.grid(row=6, column=2, padx=10, pady=10)     
                       
                crt_btn = Button(t_inner, text="Continue", relief="raised", borderless=1, font="system 15 bold")
                crt_btn.grid(row=7, column=0, columnspan=3, padx=10, pady=[20, 10], sticky="ew")
                
                # Insert budget into database
                c.execute("INSERT INTO budgets (year, month) VALUES (?, ?)", (sel_year, sel_month))
                conn.commit()
                budget_id = c.lastrowid
                
            setup_pop()
        
            conn.close()
            # # Opens budget with a uniqe ID
            # new_bud_pop.destroy()
            # show_budget_page(budget_id)
    

            
    ######### BOTTOM SECTION #########
    
    b_frame = tk.Frame(new_bud_pop, background="gray74")
    b_frame.place(relx=0, rely=0.70, relwidth=1, relheight=0.30)
    
    create_btn = Button(b_frame, text="Create", background="PaleGreen1", relief="raised", width=75,
                        borderless=1, activebackground="green2", command=create) 
    create_btn.pack(side="left", padx=[30, 5], pady=2.5)
    
    cancel = Button(b_frame, text="Cancel", background="gray90", relief="raised", width=75, 
                  borderless=1, activebackground='red', command=new_bud_pop.destroy)
    cancel.pack(side="right", padx=[5, 30], pady=2.5)
    
    
  
def load_budget_pop():
    budg_pop = tk.Toplevel()
    budg_pop.title("Load Budget")
    budg_pop.geometry("450x250+350+300")
    budg_pop.maxsize(450, 250)
    budg_pop.minsize(450, 250)
    budg_pop.configure(background="gray74")
    
    budg_pop.grab_set()
    budg_pop.transient(root)
    
    ######### TOP SECTION ##########
    
    top = tk.Frame(budg_pop, background="gray74")
    top.place(relx=0, rely=0, relwidth=1, relheight=0.8)
    
    top_inner = tk.LabelFrame(top, text="", font="system 15 bold", foreground="black", background="gray74",
                              borderwidth=1, relief="flat")
    top_inner.pack(padx=10, pady=0, fill="both", expand=True)
    
    # TREEVIEW
    
    # Style
    style = ttk.Style()
    
    # Theme 
    style.theme_use("default")
    
    # Config. Colors
    style.configure("Treeview",
        background="LightCyan2",
        foreground="black",
        rowheight=25,
        fieldbackground="white")
    
    # Selected Color
    style.map("Treeview",
        background=[('selected', 'blue2')])
    
    # Scrollbar
    tree_scroll = Scrollbar(top_inner)
    tree_scroll.pack(side="right", fill="y")
    tree = ttk.Treeview(top_inner, selectmode="extended",
                        columns=("Year", "Month"), show="headings")
    
    # Config Scrollbar
    tree_scroll.config(command=tree.yview)
    
    # Format Columns
    tree.column("Year", anchor="center", width=80)
    tree.column("Month",anchor="center",  width=120)

    # Heading
    tree.heading("Year", text="Year")
    tree.heading("Month", text="Month")
    
    tree.pack(fill="both", expand=True)
    
    # Striped Rows 
    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("evenrow", background="lightsteelblue1")
    
    # Load budgets from database
    conn = sqlite3.connect("moneywand.db")
    c = conn.cursor()
    # Sort months in their true order (not alphabeticaly)
    c.execute("""
        SELECT year, month FROM budgets
        ORDER BY year DESC,
        CASE month
            WHEN 'January' THEN 1
            WHEN 'February' THEN 2
            WHEN 'March' THEN 3
            WHEN 'April' THEN 4
            WHEN 'May' THEN 5
            WHEN 'June' THEN 6
            WHEN 'July' THEN 7
            WHEN 'August' THEN 8
            WHEN 'September' THEN 9
            WHEN 'October' THEN 10
            WHEN 'November' THEN 11
            WHEN 'December' THEN 12
        END DESC
    """)
    rows = c.fetchall()
    conn.close()
    for i, (year, month) in enumerate(rows):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=(year, month), tags=(tag,))
    
    ######### BOTTOM SECTION ########

    bot_frame = tk.Frame(budg_pop, background="gray74")
    bot_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
    
    inner_bot_frame = tk.LabelFrame(bot_frame, text="", font="system 15 bold", foreground="black", background="gray74"
                                    , borderwidth=1, relief="flat")
    inner_bot_frame.pack(padx=10, pady=0, fill="both", expand=True)
    
    def load_budget():
        selected = tree.selection()
        if not selected:
            tkinter.messagebox.showerror("Error", "Please select a budget to load.")
            return

        # Get selected year and month from treeview
        item = selected[0]
        values = tree.item(item, "values")
        year, month = values

        # Fetch the budget id from the database
        conn = sqlite3.connect("moneywand.db")
        c = conn.cursor()
        c.execute("SELECT id FROM budgets WHERE year=? AND month=?", (year, month))
        x = c.fetchone()
        conn.close()

        if x is None:
            tkinter.messagebox.showerror("Error", "Budget not found in database.")
            return

        budget_id = x[0]

        # Opens budget with a unique ID
        budg_pop.destroy()
        show_budget_page(budget_id)
    
    load = Button(inner_bot_frame, text="Load", background="green1", relief="raised", width=75, 
                  borderless=1, activebackground='green2', command=load_budget)
    load.grid(row=0, column=0, padx=[10, 50], pady=5)
    
    def delete_entry():
        selected = tree.selection()
        if not selected:
            tkinter.messagebox.showerror("Error", "Please select a budget to delete.")
            return

        item = selected[0]
        values = tree.item(item, "values")
        year, month = values
        
        # Warning
        if tkinter.messagebox.askquestion("Warning!", "Do you want to delete this budget?") == "yes":
            # Remove from Treeview
            tree.delete(item)

            # Remove from database
            conn = sqlite3.connect("moneywand.db")
            c = conn.cursor()
            c.execute("DELETE FROM budgets WHERE year=? AND month=?", (year, month))
            conn.commit()
            conn.close()
        else:
            pass
        
    delete = Button(inner_bot_frame, text="Delete", background="red", relief="raised", width=75, 
                  borderless=1, activebackground='red2', foreground="white", command=delete_entry)
    delete.grid(row=0, column=1, padx=[50, 50], pady=5)
    
    cancel = Button(inner_bot_frame, text="Cancel", background="gray90", relief="raised", width=75, 
                    borderless=1, command=budg_pop.destroy, activebackground='blue')
    cancel.grid(row=0, column=2, padx=[40, 10], pady=5)

def quick_add_savings():
    goals = ["Car", "House", "E-Bike", "New PC", "TEEEEEEEEEEEEST"] # NEEDS TO IMPORT USER-DEFINED GOALS
    cat_var = tk.StringVar()
    width = 5
    def strip_str(val):
        selected_value = cat_var.get()
        cat_var.set(selected_value[:width] + ("" if len(selected_value) <= width else "..."))
        print(val)
    
    quick_pop = tk.Toplevel()
    quick_pop.title("Quick Add")
    quick_pop.geometry("850x50+150+175")
    quick_pop.maxsize(850, 50)
    quick_pop.minsize(850, 50)
    quick_pop.configure(background="gray74")
    
    quick_pop.grab_set()
    quick_pop.transient(root)
    
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

budget_menu.add_command(label="New", command=new_budget)

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