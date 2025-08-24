import tkinter as tk
from tkinter import ttk

def update_record():
    selected_item = tree.focus()  # Get the ID of the selected item
    if selected_item:
        # Get new values from entry widgets (e.g., entry_name.get(), entry_age.get())
        new_name = name_entry.get()
        new_age = age_entry.get()

        # Update the Treeview item
        tree.item(selected_item, values=(new_name, new_age))
        
        # Clear entry widgets after update (optional)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)

def select_record(event):
    # This function is called when a row is selected in the Treeview
    selected_item = tree.focus()
    if selected_item:
        values = tree.item(selected_item, 'values')
        # Populate entry widgets with selected row's data
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[0])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, values[1])

root = tk.Tk()
root.title("Treeview Edit Example")

# Create Treeview
tree = ttk.Treeview(root, columns=("Name", "Age"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.pack(pady=10)

# Sample data
tree.insert("", "end", values=("Alice", 30))
tree.insert("", "end", values=("Bob", 25))

# Entry widgets for editing
name_label = ttk.Label(root, text="Name:")
name_label.pack()
name_entry = ttk.Entry(root)
name_entry.pack()

age_label = ttk.Label(root, text="Age:")
age_label.pack()
age_entry = ttk.Entry(root)
age_entry.pack()

# Edit button
edit_button = ttk.Button(root, text="Update Record", command=update_record)
edit_button.pack(pady=10)

# Bind selection event
tree.bind("<<TreeviewSelect>>", select_record)

root.mainloop()