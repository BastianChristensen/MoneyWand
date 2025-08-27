# Imports
import tkinter as tk

from tkinter import ttk
from tkinter import*
from tkmacosx import Button

class Guide:
    def __init__(self, window):
        self.window = window
        self.frame = tk.Frame(window, background="gray74")
        self.frame.pack(side="top", fill="both", expand=True)

####################################################################################################################################################################################        
############   LEFT SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################      

        left_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        left_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        
        inner_left_frame = tk.LabelFrame(left_frame, text="How do I...", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_left_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
####################################################################################################################################################################################        
############   RIGHT SECTION   ####################################################################################################################################################################################
####################################################################################################################################################################################      

        right_frame = tk.Frame(self.frame, background="gray74", highlightbackground="black", highlightthickness=None)
        right_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
        
        inner_right_frame = tk.LabelFrame(right_frame, text="Guide", font="system 15 bold", foreground="black", background="gray74", borderwidth=1, relief="sunken")
        inner_right_frame.pack(padx=10, pady=10, fill="both", expand=True)
        