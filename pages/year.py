# Imports
import tkinter as tk

from tkinter import ttk
from tkinter import*
from tkmacosx import Button

class YearPage:
    def __init__(self, window):
        self.window = window
        self.frame = tk.Frame(window, background="white")
        self.frame.pack(side="top", fill="both", expand=True)
        
        
####################################################################################################################################################################################        
############   TOP SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################

        top_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        
        inner_top_section = tk.LabelFrame(top_frame, text="Overview",font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_top_section.pack(padx=10, pady=0, fill="both", expand=True)
        
####################################################################################################################################################################################        
############   MIDDLE SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################
        
        mid_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        mid_frame.place(relx=0, rely=0.15, relwidth=1, relheight=0.75)
        
        inner_mid_section = tk.LabelFrame(mid_frame, text="2025",font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_mid_section.pack(padx=10, pady=0, fill="both", expand=True)
        
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
        
        # tree_scroll = Scrollbar(inner_mid_section)
        # tree_scroll.pack(side="right", fill="y")
        
        tree = ttk.Treeview(inner_mid_section, selectmode="extended",
                            columns=("January", "February", "Mars", "April", "May", "June",
                                     "July", "August", "September", "October", "November", "December"), show="headings")
        
        # Config Scrollbar
        
        # tree_scroll.config(command=tree.yview)
        
        # Format Columns
        
        tree.column("January", anchor="center", width=30)
        tree.column("February",anchor="center",  width=30)
        tree.column("Mars", anchor="center",  width=30) 
        tree.column("April", anchor="center",  width=30)
        tree.column("May", anchor="center",  width=30)
        tree.column("June", anchor="center",  width=30)
        tree.column("July", anchor="center",  width=30)
        tree.column("August", anchor="center",  width=30)
        tree.column("September", anchor="center",  width=30)
        tree.column("October", anchor="center", width=30)
        tree.column("November", anchor="center", width=30)
        tree.column("December", anchor="center", width=30)
        
        # Heading
        tree.heading("January", text="January")
        tree.heading("February", text="February")
        tree.heading("Mars", text="Mars")
        tree.heading("April", text="April")
        tree.heading("May", text="May")
        tree.heading("June", text="June")
        tree.heading("July", text="July")
        tree.heading("August", text="August")
        tree.heading("September", text="September")
        tree.heading("October", text="October")
        tree.heading("November", text="November")
        tree.heading("December", text="December")
        
        tree.pack(fill="both", expand=True)
        
        # Striped Rows 
        
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="LightSteelBlue1")
        
####################################################################################################################################################################################        
############   BOTTOM SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################

        low_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        low_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
        
        inner_low_section = tk.LabelFrame(low_frame, text="Settings",font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_low_section.pack(padx=10, pady=[0, 5], fill="both", expand=True)
        