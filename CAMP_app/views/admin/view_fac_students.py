import tkinter as tk
from tkinter import ttk


class ViewFacultyStudents(tk.Toplevel):
    def __init__(self, admin_dashboard, parent, main, fac_students): # parent is the AdminDashboard
        super().__init__(parent)
        self.main = main
        self.admin_dashboard = admin_dashboard
        self.fac_students = fac_students
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Student Profile")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)

        # Main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas
        self.canvas = tk.Canvas(self, bg="#D9D9D9")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Faculty student list
        self.faculty_stu_list = ttk.Treeview(self, columns=("count", "stu_full_name", "stu_id", "remove"),
                                         show="headings")
        # Headings
        self.faculty_stu_list.heading("count", text="")
        self.faculty_stu_list.heading("stu_full_name", text="Name")
        self.faculty_stu_list.heading("stu_id", text="Id")
        self.faculty_stu_list.heading("remove", text="")
        # Columns
        self.faculty_stu_list.column("count", anchor="center", width=100)
        self.faculty_stu_list.column("stu_full_name", anchor="center", width=100)
        self.faculty_stu_list.column("stu_id", anchor="center", width=100)
        self.faculty_stu_list.column("remove", anchor="center", width=100)
        self.faculty_stu_list.place(x=50, y=100)
        # self.faculty_stu_list.bind("<ButtonRelease-1>", self.remove_student)

        self.display_faculty_students(self.fac_students)

    def display_faculty_students(self, students):
        count = 1
        for student in students:
            self.faculty_stu_list.insert("", "end", values=(count, student["stu_full_name"], f"AU{student["stu_id"]}", "Remove"))
            count+=1
        
    def remove_student(self, event):
        selected_row = self.faculty_stu_list.identify_row(event.y)
        column_id = self.faculty_stu_list.identify_column(event.x)

    def on_close(self):
        self.destroy()