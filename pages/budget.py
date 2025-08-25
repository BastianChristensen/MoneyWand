# IMPORTS and Setup
import tkinter as tk
import tkinter.font as font

from tkinter import *
from tkinter import Button
from tkinter import ttk
from tkinter import Toplevel, Button

# Need this one to fix button background bug 

from tkmacosx import Button
from tkcalendar import Calendar
from datetime import datetime

class BudgetPage:
    def __init__(self, window):
        self.window = window
        self.frame = tk.Frame(window, background="white")
        self.frame.pack(side="top", fill="both", expand=True)
        
####################################################################################################################################################################################        
############   BOTTOM SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################

        # Bottom section - Treeview
        
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
            fieldbackground="white")
        
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
        
        tree.heading("Date", text="Date", anchor="center")
        tree.heading("Category", text="Category", anchor="center")
        tree.heading("Amount", text="Amount", anchor="center")
        tree.heading("Comment", text="Comment", anchor="center")
        
        tree.pack(fill="both", expand=True)
        
        # Striped Rows 
        
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="LightSteelBlue1")
        
        # Remove entry
        
        def remove_entry():
            x = tree.selection()
            for entry in x:
                tree.delete(entry)
                
        categories = ["Food", "Utilities", "Transport", "Savings", "Insurance", "Debt", "Health", "Entertainment", "Misc"]
                
        # Edit entry
    
        def edit_entry():
            x = tree.selection()
            if not x:
                return
            
            item = tree.item(x[0])
            values = item["values"]
            
            # New window popup
            
            edit_window = Toplevel()
            edit_window.title("Edit Entry")

            fields = ["Date", "Category", "Amount", "Comment"]
            entries = []
            
            # Itterates through [0] - n in fields.
            for i, field in enumerate(fields):
                Label(edit_window, text=field).grid(row=i, column=0, padx=10, pady=5)

                if field == "Category":
                    combo = ttk.Combobox(edit_window, values=categories, state="readonly", width=28)
                    combo.configure(state="disabled")
                    combo.set(values[i])
                    combo.grid(row=i, column=1, padx=10, pady=5)
                    entries.append(combo)
                    
                elif field == "Date":
                    date_entry = Entry(edit_window, width=30)
                    date_entry.configure(state="disabled")
                    date_entry.insert(0, values[i])
                    date_entry.grid(row=i, column=1, padx=(10, 0), pady=5, sticky="w")

                    pick_btn = Button(edit_window, text="Pick", command=lambda e=date_entry: open_calendar(e), background="gray90")
                    pick_btn.grid(row=i, column=2, padx=(5, 10), pady=5, sticky="w")

                    entries.append(date_entry)                   
                    
                else:
                    entry = Entry(edit_window, width=30)
                    entry.insert(0, values[i])
                    entry.grid(row=i, column=1, padx=10, pady=5)
                    entries.append(entry)
        
            def save_changes():
                new_values = [e.get() for e in entries]
                tree.item(x[0], values=new_values)
                edit_window.destroy()
                
            save_btn = Button(edit_window, text="Save", command=save_changes, background="green2")
            save_btn.grid(row=4, column=0, columnspan=2, pady=10)
            
                 
             
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
        
        # Calender Widget
        
        def open_calendar(entry_widget):
            # Always set to normal before opening calendar
            entry_widget.config(state="normal", background="gray75", readonlybackground="gray90")
            popup = Toplevel()
            popup.title("Select Date")
            popup.configure(background="gray74")
            popup.grab_set()

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
        
        # Option Menu
        
        cat_var = tk.StringVar()
        
        # Content
        
        date_label = Label(form_wrapper, text="Date", font="system 10 bold", foreground="black", background="gray74")
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_entry = Entry(form_wrapper, highlightthickness=1, highlightcolor="blue", width=10, borderwidth=1, readonlybackground="gray90", foreground="black")
        date_entry.configure(state="readonly")
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        calendar_btn = Button(form_wrapper, text="Pick", command=lambda: open_calendar(date_entry), relief="raised", borderless=1)
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
        cat_entry = OptionMenu(form_wrapper, cat_var, *categories)
        cat_entry.configure(relief="sunken", background="gray74")
        cat_entry.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

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
        
        edit_btn = Button(form_wrapper, text="Edit", relief="raised", borderless=1, background="yellow2", width=60, command=edit_entry)
        edit_btn.grid(row=0, column=1, padx=[5, 5], pady=1, sticky="w") 
               
        # Note: Add message: No entry selected
        
        remove_btn = Button(form_wrapper, text="Remove", relief="raised", borderless=1, background="red2", width=70, command=remove_entry)
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

