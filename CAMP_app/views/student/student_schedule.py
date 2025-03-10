import tkinter as tk
from tkinter import ttk


class StudentScheduleTab(tk.Frame):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing

        self.lbl = ttk.Label(self,text="Student Schedule")
        self.lbl.place(x=20, y=50)