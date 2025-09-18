# IMPORTS and Setup
import tkinter as tk
import tkinter.messagebox
import sqlite3
import json

from tkinter import *
from tkinter import Button
from tkinter import ttk
from tkinter import Toplevel, Button


# Need this one to fix button background bug 
from tkmacosx import Button

from tkcalendar import Calendar
from datetime import datetime

class BudgetPage:
    def __init__(self, window, id, name, categories, currency, spending_limits, contributors):
        self.window = window
        self.id = id
        self.name = name
        self.budget_categories = categories
        self.currency = currency
        self.spending_limit = spending_limits

        norm = contributors or []
        if "You" not in norm:
            norm = ["You"] + norm
        else:
            norm = ["You"] + [c for c in norm if c != "You"]

        self.contributors = norm[:2]
        self.frame = tk.Frame(window, background="white")
        self.frame.pack(side="top", fill="both", expand=True)

####################################################################################################################################################################################        
############   MISC   ####################################################################################################################################################################################
####################################################################################################################################################################################

        def query_income_tree():
            conn = sqlite3.connect("moneywand.db")
            c = conn.cursor()
            c.execute("SELECT date, amount, source FROM income WHERE budget_id=?", (self.id,))
            rows = c.fetchall()
            income_tree.delete(*income_tree.get_children())
            for count, row in enumerate(rows):
                tag = "evenrow" if count % 2 == 0 else "oddrow"
                income_tree.insert('', 'end', values=row, tags=(tag,))
            conn.close()
            
        def on_budget_select(self, event):
            selected = event.widget.selection()
            if not selected:
                return
            year, month = event.widget.item(selected[0])["values"]
            self.display_report(year, month)

####################################################################################################################################################################################        
############   BOTTOM SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################

        # Bottom section - Treeview
        
        bottom_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        bottom_frame.place(relx=0.35, rely=0.2, relwidth=0.65, relheight=0.8)
        
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
        tree.tag_configure("you", foreground="#1976D2")      
        tree.tag_configure("person1", foreground="#C62828")    
        tree.tag_configure("person2", foreground="#388E3C")    
        tree.tag_configure("person3", foreground="#F9A825")   
    
             
####################################################################################################################################################################################        
############   LEFT SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################        
        
        # Left section
        
        left_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        left_frame.place(relx=0, rely=0, relwidth=0.35, relheight=0.6)
        
        # Inner left section
        
        budget_name = self.name 
        inner_left_section = tk.LabelFrame(left_frame, text=f"{budget_name}", font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_left_section.pack(padx=10, pady=5, fill="both", expand=True)
        
        lscroll = Scrollbar(inner_left_section)
        lscroll.pack(side="right", fill="y")
        
        # Progressbars
        self.progress_widgets = {}

        def get_spent_for_category(cat):
            conn = sqlite3.connect("moneywand.db")
            c = conn.cursor()
            c.execute(
                """
                SELECT SUM(amount)
                FROM expenses
                WHERE budget_id=? AND category=?
                  AND COALESCE(contributor, '') <> 'You'
                """,
                (self.id, cat)
            )
            result = c.fetchone()
            conn.close()
            return result[0] if (result and result[0] is not None) else 0

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Green.Horizontal.TProgressbar", troughcolor="gray90", background="#2DD133")
        style.configure("Yellow.Horizontal.TProgressbar", troughcolor="gray90", background="#EDD100")
        style.configure("LightOrange.Horizontal.TProgressbar", troughcolor="gray90", background="#FBB142")
        style.configure("DarkOrange.Horizontal.TProgressbar", troughcolor="gray90", background="#FF7B00")
        style.configure("Blue.Horizontal.TProgressbar", troughcolor="gray90", background="#0009FF")
        style.configure("Red.Horizontal.TProgressbar", troughcolor="gray90", background="#F44336")

        # Sets the color of the progress bar
        def get_bar_style(percent):
            if percent <= 0.25:
                return "Green.Horizontal.TProgressbar"
            elif percent <= 0.5:
                return "Yellow.Horizontal.TProgressbar"
            elif percent <= 0.75:
                return "LightOrange.Horizontal.TProgressbar"
            elif percent < 1.0:
                return "DarkOrange.Horizontal.TProgressbar"
            elif percent == 1.0:
                return "Blue.Horizontal.TProgressbar"
            else:
                return "Red.Horizontal.TProgressbar"

        # Updates the progressbar
        def update_progress_bars():
            def fmt(val):
                try:
                    return f"{float(val):.2f}"
                except Exception:
                    return str(val)
            
            for cat in self.budget_categories:
                spent = get_spent_for_category(cat)
                limit = self.spending_limit.get(cat, 0)
                pb, lim_label = self.progress_widgets[cat]
                pb["maximum"] = limit if limit > 0 else 1
                pb["value"] = spent
                percent = spent / limit if limit > 0 else 0
                pb.config(style=get_bar_style(percent))
                lim_label.config(text=f"{fmt(spent)} / {fmt(limit)}")

        # Shortens the labels in the left frame
        def truncate_label(label, max_len=10):
            return label if len(label) <= max_len else label[:max_len-3] + "..."

        # Add categories and progressbars for each category
        for idx, cat in enumerate(self.budget_categories):
            row_frame = tk.Frame(inner_left_section, background="gray74")
            row_frame.pack(fill="x", padx=1, pady=2)

            short_cat = truncate_label(cat, max_len=12)
            cat_label = tk.Label(row_frame, text=short_cat, font="system 10 bold", background="gray74", anchor="w", width=12, foreground="black")
            cat_label.grid(row=0, column=0, sticky="w", padx=(5, 5))

            pb = ttk.Progressbar(row_frame, orient="horizontal", mode="determinate")
            pb.grid(row=0, column=1, sticky="ew", padx=(0, 10))
            row_frame.grid_columnconfigure(1, weight=1)

            lim_label = tk.Label(row_frame, text="", font="system 10", background="gray74", anchor="e", foreground="black", width=12)
            lim_label.grid(row=0, column=2, sticky="e", padx=(0, 2))
            row_frame.grid_columnconfigure(2, weight=0)

            self.progress_widgets[cat] = (pb, lim_label)
        
        # LEFT BOTTOM
        left_bot = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        left_bot.place(relx=0, rely=0.6, relwidth=0.3, relheight=0.4)
        
        inner_left_bot = tk.LabelFrame(left_bot, text="Income", font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_left_bot.pack(padx=10, pady=[0, 10], fill="both", expand=True)
        
        # TREEVIEW

        # Scrollbar
        inc_tree_scroll = Scrollbar(inner_left_bot)
        inc_tree_scroll.pack(side="right", fill="y")
        
        income_tree = ttk.Treeview(inner_left_bot, yscrollcommand=inc_tree_scroll.set, selectmode="extended",
                            columns=("Date", "Amount", "Source"), show="headings")
                
        # Config Scrollbar        
        inc_tree_scroll.config(command=tree.yview)
        
        # Format Columns        
        income_tree.column("Date", anchor="w", width=40)
        income_tree.column("Amount", anchor="center", width=40)
        income_tree.column("Source", anchor="e", width=40)
         
        # Heading 
        income_tree.heading("Date", text="Date", anchor="center")
        income_tree.heading("Amount", text="Amount", anchor="center")
        income_tree.heading("Source", text="Source", anchor="center")
        
        income_tree.pack(fill="both", expand=True)
        
        # Striped Rows 
        income_tree.tag_configure("oddrow", background="white")
        income_tree.tag_configure("evenrow", background="LightSteelBlue1")
        
        # Income Functions
        
        def income():
            # Pop Up
            inc_win = Toplevel()
            inc_win.title("Income")
            inc_win.geometry("850x50+550+650")
            inc_win.maxsize(850, 50)
            inc_win.minsize(850, 50)
            inc_win.configure(background="gray74")
            
            inc_win.grab_set()
            inc_win.transient(window)
            
            pop_view = tk.Frame(inc_win, background="gray74", highlightbackground="black", highlightthickness=None)
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

            source_label = Label(pop_view, text="Source", font="system 10 bold", foreground="black", background="gray74")
            source_label.grid(row=0, column=7, padx=5, pady=5, sticky="e")
            source_entry = Entry(pop_view, highlightthickness=1, highlightcolor="blue", width=10, borderwidth=1, background="gray90", foreground="black")
            source_entry.grid(row=0, column=8, padx=5, pady=5, sticky="e")
                
            separator3 = ttk.Separator(pop_view, orient=tk.VERTICAL)    
            separator3.grid(row=0, column=9, rowspan=3, padx=[20, 20], pady=0, sticky=tk.NS)
            
            # Function for adding input data
            def inc_add():     
                date = date_entry.get()
                amount = amount_entry.get().replace(",", ".")
                source = source_entry.get()
                if not date or not amount or not source:
                    tkinter.messagebox.showerror("Error", "All fields are required.")
                    return
            
                try:
                    amount = float(amount)
                except ValueError:
                    tkinter.messagebox.showerror("Error", "Amount must be a number.")
                    return
                
                # Fetch data
                conn = sqlite3.connect("moneywand.db")
                c = conn.cursor()
                c.execute("INSERT INTO income (date, amount, source, budget_id) VALUES (?, ?, ?, ?)",
                        (date, amount, source, self.id))
                conn.commit()
                conn.close()
                query_income_tree()
                query_database()

            add_button = Button(pop_view, text="Add", background="PaleGreen1", relief="raised", width=50, borderless=1,
                                activebackground="green2", command=inc_add)
            add_button.grid(row=0, column=10, padx=5, pady=5, sticky="e")
            
            cancel_button = Button(pop_view, text="Close", background="gray90", relief="raised", width=50, borderless=1, activebackground="red2", command=inc_win.destroy)
            cancel_button.grid(row=0, column=12, padx=5, pady=5, sticky="e")
        
                # LEFT BOTTOM RIGHT PART
        
        def edit_income():
            x = income_tree.selection()
            if not x:
                return
            
            item = income_tree.item(x[0])
            values = item["values"]
            
            # New window popup
            
            edit_window = Toplevel()
            edit_window.title("Edit Entry")
         
            edit_window.grab_set()
            edit_window.transient(window)

            fields = ["Date", "Amount", "Source"]
            entries = []
            
            for i, field in enumerate(fields):
                Label(edit_window, text=field).grid(row=i, column=0, padx=10, pady=5)
                    
                if field == "Date":
                    date_entry = Entry(edit_window, width=10)
                    date_entry.configure(state="disabled")
                    date_entry.insert(0, values[i])
                    date_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="w")

                    pick_btn = Button(edit_window, text="Pick", command=lambda e=date_entry: open_calendar(e), background="gray90")
                    pick_btn.grid(row=i, column=2, padx=(5, 10), pady=5, sticky="w")

                    entries.append(date_entry)                   
            
                elif field == "Amount":
                    entry = Entry(edit_window, width=10)
                    entry.insert(0, values[i])
                    entry.grid(row=1, column=1, padx=10, pady=5)
                    entries.append(entry)
                    
                elif field == "Source":
                    source = Entry(edit_window, width=10)
                    source.insert(0, values[i])
                    source.grid(row=2, column=1, padx=10, pady=5)
                    entries.append(source)

            def save_changes():
                new_values = [e.get() for e in entries]

                if not new_values[0]:
                    new_values[0] = values[0]
                    
                try:
                    new_values[1] = float(new_values[1])
                    
                except ValueError:
                    tkinter.messagebox.showerror("Error", "Amount must be a number.")
                    return
                
                income_tree.item(x[0], values=new_values)
                conn = sqlite3.connect("moneywand.db")
                c = conn.cursor()
                old_values = values
                c.execute("""
                    UPDATE income SET date=?, amount=?, source=?
                    WHERE date=? AND amount=? AND source=? AND budget_id=?
                """, (*new_values, *old_values, self.id))
                conn.commit()
                conn.close()
                query_income_tree()
                edit_window.destroy()
            
            save_btn = Button(edit_window, text="Save", command=save_changes, background="green2")
            save_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        def del_income():
            x = income_tree.selection()
            if not x:
                return
            
            conn = sqlite3.connect("moneywand.db")
            c = conn.cursor()
            for entry in x:
                values = income_tree.item(entry)["values"]
                
                c.execute("DELETE FROM income WHERE date=? AND amount=? AND source=? AND budget_id=?",
                          (values[0], values[1], values[2], self.id))
                income_tree.delete(entry)
            
            conn.commit()
            conn.close()
            query_database()
    
        # INCOME TOOL BAR
        
        l2b = tk.Frame(self.window, background="gray74", highlightbackground="black", highlightthickness=None)
        l2b.place(relx=0.3, rely=0.6, relwidth=0.05, relheight=0.4)
        
        l2ib = tk.LabelFrame(l2b, text="Tools", font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        l2ib.pack(padx=0, pady=[7.5, 10], fill="both", expand=True)   
        
        # Center the Add Income button horizontally in l2ib
        add_inc = Button(l2ib, text="Add", command=income, relief="raised", borderless=1,
                 background="green2", foreground="black", width=50)
        add_inc.pack(pady=(20,5), padx=0, expand=True)
        
        edit_inc = Button(l2ib, text="Edit", relief="raised", borderless=1,
            background="yellow2", foreground="black", width=50, command=edit_income)
        edit_inc.pack(pady=(5, 5), padx=0, expand=True)
        
        del_inc = Button(l2ib, text="Remove", relief="raised", borderless=1,
            background="red2", foreground="black", width=60, command=del_income)
        del_inc.pack(pady=(5, 20), padx=0, expand=True)

####################################################################################################################################################################################        
############   TOP SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################
        
        # Top Left section
        
        top_left_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        top_left_frame.place(relx=0.35, rely=0, relwidth=0.50, relheight=0.2)
        
        # Inner Top section
        
        inner_top_left_section = tk.LabelFrame(top_left_frame, text="Entry", font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_top_left_section.pack(padx=(10, 2), pady=10, fill="both", expand=True)

        form_wrapper = tk.Frame(inner_top_left_section, relief="sunken", background="gray74")
        form_wrapper.pack(expand=True, fill="both")

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
            entry_widget.config(state="normal", background="gray74", readonlybackground="gray90")
            popup = Toplevel()
            popup.title("Select Date")
            popup.configure(background="gray74")
            popup.grab_set()

            cal = Calendar(popup, selectmode='day', background="blue2", foreground="white", headersbackground="gray60", headersforeground="black")
            cal.pack(padx=10, pady=10)

            def select_date():
                raw_date = cal.get_date()
                try:
                    parsed_date = datetime.strptime(raw_date, "%m/%d/%y")
                except ValueError:
                    parsed_date = datetime.strptime(raw_date, "%m/%d/%Y")
                formatted_date = parsed_date.strftime("%Y-%m-%d")
                entry_widget.delete(0, "end")
                entry_widget.insert(0, formatted_date)
                entry_widget.config(state="readonly", background="gray90", readonlybackground="gray90")
                popup.destroy()

            Button(popup, text="Select", command=select_date, borderless=1).pack(pady=5, padx=5)

        cat_var = tk.StringVar()

        # Content
        date_label = Label(form_wrapper, text="Date", font="system 10 bold", foreground="black", background="gray74")
        date_label.grid(row=0, column=0, padx=(2,2), pady=5, sticky="e")
        date_entry = Entry(form_wrapper, highlightthickness=1, highlightcolor="blue", width=10, borderwidth=1, readonlybackground="gray90", foreground="black")
        date_entry.configure(state="readonly")
        date_entry.grid(row=0, column=1, padx=(2,2), pady=5, sticky="ew")
        calendar_btn = Button(form_wrapper, text="Pick", command=lambda: open_calendar(date_entry), relief="raised", borderless=1)
        calendar_btn.grid(row=0, column=2, padx=(2,2), pady=5, sticky="w")

        amount_label = Label(form_wrapper, text="Amount", font="system 10 bold", foreground="black", background="gray74")
        amount_label.grid(row=1, column=0, padx=(2,2), pady=5, sticky="e")
        amount_entry = Entry(form_wrapper, **entry_opts)
        amount_entry.grid(row=1, column=1, padx=(2,2), pady=5, sticky="ew")

        cat_label = Label(form_wrapper, text="Category", font="system 10 bold", foreground="black", background="gray74")
        cat_label.grid(row=0, column=3, padx=(2,2), pady=5, sticky="e")
        cat_entry = OptionMenu(form_wrapper, cat_var, *categories)
        cat_entry.configure(relief="sunken", background="gray74", foreground="black")
        cat_entry.grid(row=0, column=4, padx=(2,2), pady=5, sticky="ew")

        com_label = Label(form_wrapper, text="Comment", font="system 10 bold", foreground="black", background="gray74")
        com_label.grid(row=1, column=3, padx=(2,2), pady=5, sticky="e")
        com_entry = Entry(form_wrapper, **entry_opts)
        com_entry.grid(row=1, column=4, padx=(2,2), pady=5, sticky="ew")
        
        # Add entry
        def add_entry():
            date = date_entry.get()
            category = cat_var.get()
            amount_str = amount_entry.get().replace(",", ".")
            comment = com_entry.get()
            if not date or not category or not amount_str:
                tkinter.messagebox.showerror("Error", "Date, Category and Amount are required.")
                return
            try:
                amount = float(amount_str)
            except ValueError:
                tkinter.messagebox.showerror("Error", "Amount must be a number.")
                return

            conn = sqlite3.connect("moneywand.db")
            c = conn.cursor()
            c.execute("INSERT INTO expenses (date, category, amount, comment, budget_id) VALUES (?, ?, ?, ?, ?)",
                    (date, category, amount, comment, self.id))
            conn.commit()
            conn.close()
            query_database()
            date_entry.delete(0, "end")
            amount_entry.delete(0, "end")
            com_entry.delete(0, "end")
        
        # Remove entry
        def remove_entry():
            x = tree.selection()
            if not x:
                return
            
            conn = sqlite3.connect("moneywand.db")
            c = conn.cursor()
            for entry in x:
                values = tree.item(entry)["values"]
                
                c.execute("DELETE FROM expenses WHERE date=? AND category=? AND amount=? AND comment=? AND budget_id=?",
                          (values[0], values[1], values[2], values[3], self.id))
                tree.delete(entry)
            
            conn.commit()
            conn.close()
            query_database()
        
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
         
            edit_window.grab_set()
            edit_window.transient(window)

            fields = ["Date", "Category", "Amount", "Comment"]
            entries = []
            
            for i, field in enumerate(fields):
                Label(edit_window, text=field).grid(row=i, column=0, padx=10, pady=5)

                if field == "Category":
                    combo = ttk.Combobox(edit_window, values=categories, state="readonly", width=28)
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
                    # If date field is empty, keep the old value
                    if not new_values[0]:
                        new_values[0] = values[0]
                    try:
                        new_values[2] = float(new_values[2])
                    except ValueError:
                        tkinter.messagebox.showerror("Error", "Amount must be a number.")
                        return
                    tree.item(x[0], values=new_values)
                    conn = sqlite3.connect("moneywand.db")
                    c = conn.cursor()
                    old_values = values
                    c.execute("""
                        UPDATE expenses SET date=?, category=?, amount=?, comment=?
                        WHERE date=? AND category=? AND amount=? AND comment=? AND budget_id=?
                    """, (*new_values, *old_values, self.id))
                    conn.commit()
                    conn.close()
                    query_database()
                    edit_window.destroy()
                
            save_btn = Button(edit_window, text="Save", command=save_changes, background="green2")
            save_btn.grid(row=4, column=0, columnspan=2, pady=10)
  

####################################################################################################################################################################################        
############   TOP RIGHT UPPER SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################
           
        # Top Right section
        
        top_right_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        top_right_frame.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.12)
        
        # Inner Top Right section
        
        inner_top_right_section = tk.LabelFrame(top_right_frame, text="Actions",font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_top_right_section.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Wrapper frame to center grid content
        
        form_wrapper = tk.Frame(inner_top_right_section, relief="sunken", background="gray74")
        form_wrapper.pack(expand=True)
        
        # Content 
        
        add_btn = Button(form_wrapper, text="Add", relief="raised", borderless=1, background="green2", width=50, command=add_entry)
        add_btn.grid(row=0, column=0, padx=[1, 5], pady=1, sticky="w")
        
        edit_btn = Button(form_wrapper, text="Edit", relief="raised", borderless=1, background="yellow2", width=60, command=edit_entry)
        edit_btn.grid(row=0, column=1, padx=[5, 5], pady=1, sticky="w") 
                     
        remove_btn = Button(form_wrapper, text="Remove", relief="raised", borderless=1, background="red2", width=70, command=remove_entry)
        remove_btn.grid(row=0, column=2, padx=[5, 1], pady=1, sticky="w")

####################################################################################################################################################################################        
############   TOP RIGHT LOWER SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################
        
        # Top Right Lower section
        
        top_right_low_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        top_right_low_frame.place(relx=0.75, rely=0.1, relwidth=0.25, relheight=0.12)
        
        # Inner Top Right Lower section
        
        inner_top_right_low_section = tk.LabelFrame(top_right_low_frame, text="Tools",font="system 12 bold", foreground="black", background="gray74", borderwidth=2, relief="sunken")
        inner_top_right_low_section.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Wrapper frame to center grid content
        
        form_wrapper = tk.Frame(inner_top_right_low_section, relief="sunken", background="gray74")
        form_wrapper.pack(expand=True)
        
        # Content
        
        # Edit limits popup 
        def edit_limits():
            p = Toplevel(window)
             
            p.title("Edit")
            p.geometry("450x250+350+300")
            p.maxsize(450, 400)
            p.minsize(450, 400)
            p.configure(background="gray74")
            
            p.grab_set()
            p.transient(window)
            
            win = tk.Frame(p, background="gray74")
            win.place(relx=0, rely=0, relheight=0.9, relwidth=1)
            
            iwin = tk.LabelFrame(win, text="", font="system 15 bold", foreground="black", background="gray90",
                              borderwidth=1, relief="sunken")
            iwin.pack(padx=5, pady=5, fill="both", expand=True)
            
            bot = tk.Frame(p, background="gray74")
            bot.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)
            
            scroll = Scrollbar(iwin)
            scroll.pack(side="right", fill="y")
            
            limit_entries = {}

            for idx, cat in enumerate(self.budget_categories):
                row = tk.Frame(iwin, background="gray90")
                row.pack(fill="x", padx=5, pady=2)
                tk.Label(row, text=cat, background="gray90", font="system 11", width=18, anchor="w").pack(side="left")
                entry = tk.Entry(row, width=10)
                entry.insert(0, str(self.spending_limit.get(cat, "")))
                entry.pack(side="left", padx=10)
                limit_entries[cat] = entry

            def save_limits():
                new_limits = {}
                for cat, entry in limit_entries.items():
                    try:
                        val = float(entry.get())
                    except ValueError:
                        tk.messagebox.showerror("Error", f"Limit for '{cat}' must be a number.")
                        return
                    new_limits[cat] = val
                self.spending_limit = new_limits

                # Save to DB
                conn = sqlite3.connect("moneywand.db")
                c = conn.cursor()
                c.execute(
                    "UPDATE budgets SET spending_limits=? WHERE id=?",
                    (json.dumps(new_limits), self.id)
                )
                conn.commit()
                conn.close()

                update_progress_bars()
                p.destroy()

            bot = tk.Frame(p, background="gray74")
            bot.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)
            save_btn = Button(bot, text="Save", command=save_limits, background="gray90", borderless=1)
            save_btn.pack(pady=5)
            
        # Assign popup                
        def assign_entry():
            x = tree.selection()
            if not x:
                return

            item = tree.item(x[0])
            values = item["values"]

            # Popup for assigning
            assign_win = Toplevel(self.window)
            assign_win.title("Assign Entry")
            assign_win.geometry("300x150")
            assign_win.configure(background="gray90")
            assign_win.grab_set()
            assign_win.transient(self.window)

            tk.Label(assign_win, text="Assign to:", background="gray90", font="system 11").pack(pady=(15, 5))

            assign_var = tk.StringVar(value=self.contributors[0] if self.contributors else "You")
            assign_menu = tk.OptionMenu(assign_win, assign_var, *self.contributors)
            assign_menu.pack(pady=(0, 10))

            def do_assign():
                contributor = assign_var.get()
                conn = sqlite3.connect("moneywand.db")
                c = conn.cursor()
                c.execute(
                    "UPDATE expenses SET contributor=? WHERE date=? AND category=? AND amount=? AND comment=? AND budget_id=?",
                    (contributor, values[0], values[1], values[2], values[3], self.id)
                )
                conn.commit()
                conn.close()
                query_database()
                assign_win.destroy()

            Button(assign_win, text="Assign", background="PaleGreen1", borderless=1, command=do_assign).pack(pady=5)
            Button(assign_win, text="Cancel", background="gray90", borderless=1, command=assign_win.destroy).pack()

        lim_btn = Button(form_wrapper, text="Limits", relief="raised", borderless=1, 
                        background="gray90", width=75, command=edit_limits)
        lim_btn.grid(row=0, column=0, padx=[5, 1], pady=1, sticky="w")
                
        assign_btn = Button(form_wrapper, text="Assign", relief="raised", borderless=1,
                        background="gray90", width=75, command=assign_entry)
        assign_btn.grid(row=0, column=1, padx=[5, 5], pady=1, sticky="w") 
        
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        
        export_btn = Button(form_wrapper, text="Export PDF", bg="royalblue", fg="white",
                                 borderless=1, command=self.export_to_pdf, width=75)
        export_btn.grid(row=0, column=2, padx=[5, 1], pady=1, sticky="w")


        ########### RUN ##########
        def query_database():
            conn = sqlite3.connect("moneywand.db")
            c = conn.cursor()
            c.execute("SELECT * FROM expenses WHERE budget_id=?", (self.id,))
            expenses = c.fetchall()
            tree.delete(*tree.get_children()) 

            spent_per_cat = {cat: 0 for cat in self.budget_categories}

            for count, expense in enumerate(expenses):
                contributor = expense[7] if len(expense) > 7 else None
                
                if contributor == "You":
                    tag = "you"
                    
                elif contributor and contributor != "You":
                    idx = self.contributors.index(contributor) if contributor in self.contributors else 1
                    tag = f"person{idx}"
                    if expense[2] in self.budget_categories:
                        spent_per_cat[expense[2]] += expense[3]
                        
                else:
                    tag = "evenrow" if count % 2 == 0 else "oddrow"
                    if expense[2] in self.budget_categories:
                        spent_per_cat[expense[2]] += expense[3]
                tree.insert('', 'end', iid=count, values=(expense[1], expense[2], expense[3], expense[4]), tags=(tag,))
            conn.close()

            def fmt(val):
                try:
                    return f"{float(val):.2f}"
                except Exception:
                    return str(val)
            
            for cat in self.budget_categories:
                pb, lim_label = self.progress_widgets[cat]
                limit = self.spending_limit.get(cat, 0)
                pb["maximum"] = limit if limit > 0 else 1
                pb["value"] = spent_per_cat[cat]
                percent = spent_per_cat[cat] / limit if limit > 0 else 0
                pb.config(style=get_bar_style(percent))
                lim_label.config(text=f"{fmt(spent_per_cat[cat])} / {fmt(limit)}")  
                        
        query_database()
        query_income_tree()

# PDF Exporter for BudgetPage
def _budget_export_to_pdf(self):
    # Ensure ReportLab is available
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    except Exception:
        tkinter.messagebox.showerror(
            "ReportLab not available",
            "ReportLab is required to export PDFs.\nInstall with:\n\npip install reportlab",
        )
        return

    # Gather basic metadata
    conn = sqlite3.connect("moneywand.db")
    c = conn.cursor()
    month = year = None
    try:
        c.execute("SELECT month, year FROM budgets WHERE id=?", (self.id,))
        row = c.fetchone()
        if row:
            month, year = row[0], row[1]
    except Exception:
        pass

    title = f"{month} {year}" if month and year else (self.name or "Budget Report")

    # Categories, limits, contributors
    categories = list(self.budget_categories)
    limits = dict(self.spending_limit or {})
    contributors = list(self.contributors or [])

    # Spent per category
    spent_per_cat = {}
    total_spent = 0.0
    for cat in categories:
        c.execute("SELECT SUM(amount) FROM expenses WHERE budget_id=? AND category=?", (self.id, cat))
        val = c.fetchone()[0] or 0
        spent_per_cat[cat] = float(val)
        total_spent += float(val)

    # Income entries
    c.execute("SELECT source, amount FROM income WHERE budget_id=?", (self.id,))
    income_entries = c.fetchall()
    total_income = sum(float(a or 0) for _, a in income_entries)

    # Assigned expenses per contributor
    c.execute(
        """
            SELECT date, category, amount, comment, contributor
            FROM expenses
            WHERE budget_id=? AND contributor IS NOT NULL AND TRIM(contributor) <> ''
            ORDER BY date ASC
        """,
        (self.id,)
    )
    assigned = c.fetchall()

    contrib_map = {name: [] for name in contributors}
    for d, cat, amt, com, contr in assigned:
        if contr in contrib_map:
            contrib_map[contr].append((d or '', cat or '', com or '', float(amt or 0)))

    contrib_totals = {name: sum(amt for _, _, _, amt in contrib_map.get(name, [])) for name in contributors}

    # Full expense rows
    c.execute(
        """
            SELECT date, category, comment, contributor, amount
            FROM expenses
            WHERE budget_id=?
            ORDER BY date ASC
        """,
        (self.id,)
    )
    expense_rows = c.fetchall()
    conn.close()

    balance = total_income - total_spent

    # Ask path
    safe_title = str(title).replace("/", "-").replace("\\", "-")
    initial = f"{safe_title}.pdf"
    try:
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            title="Save Report as PDF",
            defaultextension=".pdf",
            initialfile=initial,
            filetypes=[("PDF files", "*.pdf")]
        )
    except Exception:
        file_path = None
    if not file_path:
        return

    # Build PDF
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(file_path, pagesize=A4, title=title)
    story = []

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Income and Expenses", styles["Heading2"]))
    story.append(Spacer(1, 6))

    cat_data = [["Category", "Spent"]]
    for cat in categories:
        cat_data.append([cat, f"{float(spent_per_cat.get(cat, 0)):.2f}"])
    if len(cat_data) > 1:
        t = Table(cat_data, hAlign='LEFT', colWidths=[200, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    story.append(Paragraph(f"Total Spent: <b>{float(total_spent):.2f}</b>", styles["Normal"]))
    story.append(Spacer(1, 6))

    income_data = [["Source", "Amount"]]
    for source, amount in income_entries:
        income_data.append([str(source), f"{float(amount or 0):.2f}"])
    if len(income_data) > 1:
        t = Table(income_data, hAlign='LEFT', colWidths=[200, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    story.append(Paragraph(f"Total Income: <b>{float(total_income):.2f}</b>", styles["Normal"]))
    bal_color = 'green' if balance >= 0 else 'red'
    story.append(Paragraph(f"Balance: <font color='{bal_color}'><b>{float(balance):.2f}</b></font>", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Budget Details", styles["Heading2"]))
    details_data = [["Category", "Spending Limit", "Amount Spent", "Over / Under"]]
    for cat in categories:
        limit_val = float(limits.get(cat, 0) or 0)
        spent_val = float(spent_per_cat.get(cat, 0) or 0)
        diff = spent_val - limit_val
        details_data.append([
            cat,
            f"{limit_val:.2f}",
            f"{spent_val:.2f}",
            f"{diff:.2f}",
        ])
    if len(details_data) > 1:
        t = Table(details_data, hAlign='LEFT', colWidths=[160, 80, 80, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

    if contributors:
        story.append(Paragraph("Contributors", styles["Heading2"]))
        for name in contributors:
            story.append(Paragraph(name, styles["Heading3"]))
            cdata = [["Entry", "Amount"]]
            for d, cat, com, amt in contrib_map.get(name, []):
                left = cat if not com else f"{cat} - {com}"
                if d:
                    left = f"{d} | {left}"
                cdata.append([left, f"{float(amt or 0):.2f}"])
            total_val = float(contrib_totals.get(name, 0))
            cdata.append(["Total", f"{total_val:.2f}"])
            t = Table(cdata, hAlign='LEFT', colWidths=[300, 80])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 6))

    if expense_rows:
        story.append(Paragraph("Expense Details", styles["Heading2"]))
        exp_data = [["Date", "Category", "Comment", "Contributor", "Amount"]]
        for d, cat, com, contr, amt in expense_rows:
            exp_data.append([
                str(d or ''), str(cat or ''), str(com or ''), str(contr or ''), f"{float(amt or 0):.2f}"
            ])
        t = Table(exp_data, hAlign='LEFT', colWidths=[70, 100, 190, 90, 70])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
            ('ALIGN', (4,1), (4,-1), 'RIGHT'),
        ]))
        story.append(t)

    try:
        doc.build(story)
    except Exception as e:
        tkinter.messagebox.showerror("Export PDF", f"Failed to export PDF:\n{e}")
        return

    tkinter.messagebox.showinfo("Export PDF", "Report exported successfully.")


# Bind the exporter to the class so existing button works
BudgetPage.export_to_pdf = _budget_export_to_pdf