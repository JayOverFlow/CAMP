import tkinter as tk

class AdminFaculty(tk.Frame):
    def __init__(self, parent, main, admin_landing):
        super().__init__(parent)
        self.main = main
        self.admin_landing = admin_landing

