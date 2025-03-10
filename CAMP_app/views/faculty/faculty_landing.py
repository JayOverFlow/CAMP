import tkinter as tk
from tkinter import messagebox


class FacultyLanding(tk.Toplevel):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Admin Dashboard")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)

    def on_close(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to close the application? You will be logged out.")

        if confirm:
            self.main.clear_user_session("Faculty")  # Log out the user
            self.destroy()  # Close the dashboard
            self.main.destroy()  # Stop the entire application