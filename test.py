from tkinter import *
from tkcalendar import DateEntry

root = Tk()
root.configure(background="gray74")

date_entry = DateEntry(
    root,
    background="green2",
    foreground="white",
    headersbackground="red2",
    headersforeground="white",
    selectbackground="blue2",
    selectforeground="white"
)
date_entry.pack(padx=20, pady=20)

root.mainloop()
