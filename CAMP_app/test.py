# Faculty rendering

import tkinter as tk
from tkinter import ttk

# Sample function to trigger when clicking "Click Here"
def on_click(event):
    # Get selected item
    row = tree.identify_row(event.y)
    column = tree.identify_column(event.x)

    # Ensure the user clicked the "Click Here" column (column #3)
    if column == "#3" and row:
        faculty_id = tree.item(row, "values")[0]  # Get faculty ID
        print(f"Function triggered for Faculty ID: {faculty_id}")

# Create main window
root = tk.Tk()
root.title("Faculty Table")

# Create Treeview
columns = ("fac_full_name", "fac_id", "Action")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Define column headings
tree.heading("fac_full_name", text="Faculty Name")
tree.heading("fac_id", text="ID")
tree.heading("Action", text="Action")

# Define column widths
tree.column("fac_full_name", width=100)
tree.column("fac_id", width=200)
tree.column("Action", width=100, anchor="center")

# Insert sample data
faculty_data = [
    (101, "Dr. John Smith", "Click Here"),
    (102, "Prof. Jane Doe", "Click Here"),
    (103, "Dr. Emily White", "Click Here"),
]

for faculty in faculty_data:
    tree.insert("", "end", values=faculty, tags=("clickable",))

# Bind the function to the tree
tree.bind("<Button-1>", on_click)  # Left-click event

# Pack the Treeview
tree.pack(padx=10, pady=10, fill="both", expand=True)

# Run the application
root.mainloop()
