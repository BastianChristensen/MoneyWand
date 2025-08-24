import tkinter as tk

root = tk.Tk()
entry = tk.Entry(root, bg="lightgray") # Sets background color to light gray
entry.pack()

# Or later:
entry.config(bg="#FFFF00") # Sets background color to yellow
root.mainloop()