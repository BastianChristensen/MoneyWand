# Imports
import tkinter as tk

from tkinter import ttk
from tkinter import*
from tkmacosx import Button

class SavingsPage:
    def __init__(self, window):
        self.window = window
        self.frame = tk.Frame(window, background="gray74")
        self.frame.pack(side="top", fill="both", expand=True)

####################################################################################################################################################################################        
############   LEFT TOP SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################      

        left_top_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        left_top_frame.place(relx=0, rely=0, relwidth=0.5, relheight=0.8)
        
        inner_left_top_frame = tk.LabelFrame(left_top_frame, text="Entries", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_left_top_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
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
        
        tree_scroll = Scrollbar(inner_left_top_frame)
        tree_scroll.pack(side="right", fill="y")
        
        tree = ttk.Treeview(inner_left_top_frame, selectmode="extended",
                            columns=("Date", "Amount", "Goal"), show="headings")
        
        # Config Scrollbar
        
        tree_scroll.config(command=tree.yview)
        
        # Format Columns
        
        tree.column("Date", anchor="center", width=30)
        tree.column("Amount",anchor="center",  width=30)
        tree.column("Goal", anchor="center",  width=30) 

        # Heading
        tree.heading("Date", text="Date")
        tree.heading("Amount", text="Amount")
        tree.heading("Goal", text="Goal")
        
        tree.pack(fill="both", expand=True)
        
        # Striped Rows 
        
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="LightSteelBlue1")

####################################################################################################################################################################################        
############   LEFT BOTTOM SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################      

        left_bottom_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        left_bottom_frame.place(relx=0, rely=0.8, relwidth=0.5, relheight=0.2)
        
        inner_bottom_frame = tk.LabelFrame(left_bottom_frame, text="Tools", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_bottom_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
####################################################################################################################################################################################        
############   LEFT BOTTOM SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################      

        right_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)
        
        inner_right_frame = tk.LabelFrame(right_frame, text="Saving Goals", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_right_frame.pack(padx=10, pady=10, fill="both", expand=True)