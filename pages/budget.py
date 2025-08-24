from tkinter import *
from tkinter import Button
from tkinter import ttk
from tkinter import Toplevel, Button

# Need this one to fix button background bug

from tkmacosx import Button
from tkcalendar import Calendar
from datetime import datetime

import tkinter as tk
import tkinter.font as font
import sqlite3

class BudgetPage:
    def __init__(self, window):
        self.window = window
        self.frame = tk.Frame(window, background="white")
        self.frame.pack(side="top", fill="both", expand=True)
        
####################################################################################################################################################################################        
############   BOTTOM SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################

        # Bottom section
        bottom_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        bottom_frame.place(relx=0.25, rely=0.2, relwidth=0.75, relheight=0.8)
        
        inner_bottom_section = tk.LabelFrame(bottom_frame, text="Expenses",font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_bottom_section.pack(padx=10, pady=10, fill="both", expand=True)
        
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
            fieldbackground="LightCyan2")
        
        # Selected Color
        
        style.map("Treeview",
            background=[('selected', 'blue2')])
        
        # Scrollbar
        
        tree_scroll = Scrollbar(inner_bottom_section)
        tree_scroll.pack(side="right", fill="y")
        
        tree = ttk.Treeview(inner_bottom_section, yscrollcommand=tree_scroll.set, selectmode="extended",
                            columns=("Date", "Category", "Amount", "Comment"), show="headings")
        
        # Config Scrollbar
        
        tree_scroll.config(command=tree.yview)
        
        # Format Columns
        
        tree.column("Date", anchor="w", width=120)
        tree.column("Category", anchor="center", width=120)
        tree.column("Amount", anchor="center", width=120)
        tree.column("Comment", anchor="e", width=120)
         
        # Heading
        
        tree.heading("Date", text="Date", anchor="w")
        tree.heading("Category", text="Category", anchor="center")
        tree.heading("Amount", text="Amount", anchor="center")
        tree.heading("Comment", text="Comment", anchor="center")
        
        tree.pack(fill="both", expand=True)
        
        # Placeholder Data
        
        sample_data = [
            ("2025-08-01", "Groceries", "45.20", "Weekly supermarket run"),
            ("2025-08-03", "Transport", "15.00", "Bus pass"),
            ("2025-08-05", "Dining", "32.50", "Dinner with friends"),
            ("2025-08-07", "Utilities", "120.75", "Electricity bill"),
            ("2025-08-10", "Entertainment", "60.00", "Concert ticket"),
            ("2025-08-12", "Health", "25.00", "Pharmacy"),
            ("2025-08-15", "Rent", "950.00", "Monthly rent"),
            ("2025-08-18", "Subscriptions", "12.99", "Streaming service"),
            ("2025-08-20", "Misc", "8.50", "Coffee and snack"),
            ("2025-08-22", "Savings", "200.00", "Transfer to savings account"),
            ("2025-08-23", "Groceries", "52.30", "Organic produce"),
            ("2025-08-24", "Transport", "18.00", "Taxi fare"),
            ("2025-08-25", "Dining", "40.00", "Lunch meeting"),
            ("2025-08-26", "Utilities", "95.60", "Water bill"),
            ("2025-08-27", "Entertainment", "75.00", "Movie night"),
            ("2025-08-28", "Health", "30.00", "Dental checkup"),
            ("2025-08-29", "Rent", "950.00", "Monthly rent"),
            ("2025-08-30", "Subscriptions", "9.99", "Music app"),
            ("2025-08-31", "Misc", "12.00", "Stationery"),
            ("2025-09-01", "Savings", "150.00", "Emergency fund"),
            ("2025-09-02", "Groceries", "47.80", "Weekly groceries"),
            ("2025-09-03", "Transport", "20.00", "Train ticket"),
            ("2025-09-04", "Dining", "28.50", "Takeout dinner"),
            ("2025-09-05", "Utilities", "110.00", "Gas bill"),
            ("2025-09-06", "Entertainment", "65.00", "Theater show"),
            ("2025-09-07", "Health", "22.00", "Vitamins"),
            ("2025-09-08", "Rent", "950.00", "Monthly rent"),
            ("2025-09-09", "Subscriptions", "14.99", "Online course"),
            ("2025-09-10", "Misc", "6.75", "Snacks"),
            ("2025-09-11", "Savings", "180.00", "Investment account"),
            ("2025-09-12", "Groceries", "50.00", "Weekly shopping"),
            ("2025-09-13", "Transport", "10.00", "Bike repair"),
            ("2025-09-14", "Dining", "35.00", "Brunch"),
            ("2025-09-15", "Utilities", "130.00", "Internet bill"),
            ("2025-09-16", "Entertainment", "55.00", "Game purchase"),
            ("2025-09-17", "Health", "40.00", "Massage therapy"),
            ("2025-09-18", "Rent", "950.00", "Monthly rent"),
            ("2025-09-19", "Subscriptions", "11.99", "News app"),
            ("2025-09-20", "Misc", "9.25", "Coffee"),
            ("2025-09-21", "Savings", "220.00", "Savings deposit"),
            ("2025-09-22", "Groceries", "48.90", "Weekly groceries"),
            ("2025-09-23", "Transport", "16.00", "Bus fare"),
            ("2025-09-24", "Dining", "30.00", "Dinner date"),
            ("2025-09-25", "Utilities", "105.00", "Heating bill"),
            ("2025-09-26", "Entertainment", "70.00", "Live show"),
            ("2025-09-27", "Health", "27.00", "Eye drops"),
            ("2025-09-28", "Rent", "950.00", "Monthly rent"),
            ("2025-09-29", "Subscriptions", "13.99", "Fitness app"),
            ("2025-09-30", "Misc", "7.80", "Tea and snack"),
            ("2025-10-01", "Savings", "250.00", "Long-term savings")
        ]
        
        # Striped Rows 
        
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="LightSteelBlue1")
        
        # Add data
        
        global count
        count = 0
        
        for record in sample_data:
            if count % 2 == 0:
                tree.insert(parent="", index="end", iid=count, text="", 
                    values=(record[0], record[1], record[2], record[3]),
                    tags=("evenrow",))
            else:
                tree.insert(parent="", index="end", iid=count, text="", 
                    values=(record[0], record[1], record[2], record[3]),
                    tags=("oddrow",))
            
            count += 1      
             
####################################################################################################################################################################################        
############   LEFT SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################        
        
        # Left section
        
        left_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        left_frame.place(relx=0, rely=0, relwidth=0.25, relheight=1)
        
        # Inner left section
        
        inner_left_section = tk.LabelFrame(left_frame, text="Overview",font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_left_section.pack(padx=10, pady=10, fill="both", expand=True)
        
####################################################################################################################################################################################        
############   TOP LEFT SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################
        
        # Top Left section
        
        top_left_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        top_left_frame.place(relx=0.25, rely=0, relwidth=0.50, relheight=0.2)
        
        # Inner Top section
        
        inner_top_left_section = tk.LabelFrame(top_left_frame, text="Entry",font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_top_left_section.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Wrapper frame to center grid content
        
        form_wrapper = tk.Frame(inner_top_left_section, relief="sunken", background="gray74")
        form_wrapper.pack(expand=True)
        
        
        # Common styling
        
        entry_opts = {
            "background": "gray90",
            "foreground": "black",       
            "highlightthickness": 1,
            "highlightcolor": "blue",
            "width": 10,
            "borderwidth": 1
        }
        
        # Calender
        
        def open_calendar(entry_widget):
            popup = Toplevel()
            popup.title("Select Date")
            popup.configure(background="gray74")
            popup.grab_set()

            cal = Calendar(popup, selectmode='day', background="blue2", foreground="white", headersbackground="gray60", headersforeground="black")
            cal.pack(padx=10, pady=10)

            def select_date():
                selected = cal.get_date()
                entry_widget.delete(0, "end")
                entry_widget.insert(0, selected)
                popup.destroy()

            Button(popup, text="Select", command=select_date, borderless=1).pack(pady=5, padx=5)
        
        # Option Menu
        
        category_opt = ["opt1", "opt2", "opt3"]
        
        cat_var = tk.StringVar()
        
        # Content
        
        date_label = Label(form_wrapper, text="Date", font="system 10 bold", foreground="black", background="gray74")
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_entry = Entry(form_wrapper, **entry_opts)
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        calendar_btn = Button(form_wrapper, text="Pick", command=lambda: open_calendar(date_entry), relief="raised", borderless=1, background="gray90")
        calendar_btn.grid(row=0, column=2, padx=[0, 5], pady=5, sticky="w")
        
        # Should only accept numbers. Optional: auto-change "," to "."
        
        amount_label = Label(form_wrapper, text="Amount", font="system 10 bold", foreground="black", background="gray74")
        amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        amount_entry = Entry(form_wrapper, **entry_opts)
        amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Should set currency - TBD - Could be implemented in settings elsewhere.
        
        # amount_btn = Button(form_wrapper, text="Currency", relief="raised", borderless=1, background="gray90")
        # amount_btn.grid(row=1, column=2, padx=[0, 5], pady=5, sticky="w")
        
        cat_label = Label(form_wrapper, text="Category", font="system 10 bold", foreground="black", background="gray74")
        cat_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")
        cat_entry = OptionMenu(form_wrapper, cat_var, *category_opt)
        cat_entry.configure(relief="sunken", background="gray74")
        cat_entry.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        
        # Note: Button should change add/remove/edit the options in OptionMenu cat_entry
        
        cat_btn = Button(form_wrapper, text="Edit", relief="raised", borderless=1, background="gray90")
        cat_btn.grid(row=0, column=5, padx=[0, 5], pady=5, sticky="e")

        com_label = Label(form_wrapper, text="Comment", font="system 10 bold", foreground="black", background="gray74")
        com_label.grid(row=1, column=3, padx=5, pady=5, sticky="e")
        com_entry = Entry(form_wrapper, **entry_opts)
        com_entry.grid(row=1, column=4, padx=5, pady=5, sticky="ew")
    
####################################################################################################################################################################################        
############   TOP RIGHT UPPER SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################
           
        # Top Right section
        
        top_right_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        top_right_frame.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.12)
        
        # Inner Top Right section
        
        inner_top_right_section = tk.LabelFrame(top_right_frame, text="Tools",font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_top_right_section.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Wrapper frame to center grid content
        
        form_wrapper = tk.Frame(inner_top_right_section, relief="sunken", background="gray74")
        form_wrapper.pack(expand=True)
        
        # Content 

        # Note: Add message: Missing Date/Cat/Amount (comment is allways optional)
        
        add_btn = Button(form_wrapper, text="Add", relief="raised", borderless=1, background="green2", width=50)
        add_btn.grid(row=0, column=0, padx=[1, 5], pady=1, sticky="w")
        
        # Note: Add message: No entry selected
        
        edit_btn = Button(form_wrapper, text="Edit", relief="raised", borderless=1, background="yellow2", width=60)
        edit_btn.grid(row=0, column=1, padx=[5, 5], pady=1, sticky="w") 
               
        # Note: Add message: No entry selected
        
        remove_btn = Button(form_wrapper, text="Remove", relief="raised", borderless=1, background="red2", width=70)
        remove_btn.grid(row=0, column=2, padx=[5, 1], pady=1, sticky="w")

####################################################################################################################################################################################        
############   TOP RIGHT LOWER SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################
        
        # Top Right Lower section
        
        top_right_low_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        top_right_low_frame.place(relx=0.75, rely=0.1, relwidth=0.25, relheight=0.12)
        
        # Inner Top Right Lower section
        
        inner_top_right_low_section = tk.LabelFrame(top_right_low_frame, text="Settings",font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_top_right_low_section.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Wrapper frame to center grid content
        
        form_wrapper = tk.Frame(inner_top_right_low_section, relief="sunken", background="gray74")
        form_wrapper.pack(expand=True)
        
        # Content 

        # Note: Add message: Missing Date/Cat/Amount (comment is allways optional)
        
        curr_btn = Button(form_wrapper, text="Currency", relief="raised", borderless=1, background="gray90", width=75)
        curr_btn.grid(row=0, column=0, padx=[5, 1], pady=1, sticky="w")
        
        # Note: Add message: No entry selected
        
        opt_btn = Button(form_wrapper, text="Setting 2", relief="raised", borderless=1, background="gray90", width=75)
        opt_btn.grid(row=0, column=1, padx=[5, 5], pady=1, sticky="w") 
               
        # Note: Add message: No entry selected
        
        col_btn = Button(form_wrapper, text="Colors", relief="raised", borderless=1, background="gray90", width=75)
        col_btn.grid(row=0, column=2, padx=[5, 1], pady=1, sticky="w")   

