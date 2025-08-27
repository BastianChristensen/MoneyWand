import tkinter as tk

width = 10

def strip_str(val):
    selected_value = var.get()
    var.set(selected_value[:width] + ("" if len(selected_value) <= width else "..."))
    print(val)


r = tk.Tk()
r.option_add("*font", ("Consolas", 10))
value_list = ["arc (arc, chord, or pieslice)","bitmap (built-in or read from XBM file)","image (a BitmapImage or PhotoImage instance)","line","oval (a circle or an ellipse)","polygon","rectangle","text","window"]
var = tk.StringVar()
menu = tk.OptionMenu(r, var, *value_list, command=strip_str)
menu.pack()

r.mainloop()