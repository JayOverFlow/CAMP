import tkinter as tk
from tkinter import ttk

class CourseApplication(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Course Application")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)

        self.lbl = tk.Label(self, text="COURSE APPLICATION", font=("Arial", 18, "bold"), fg="#8D0404")
        self.lbl.grid(column=0, row=0)

        self.courses = ttk.Treeview(self, columns= ["cou_name", "assigned_prof"])

        self.courses.heading("cou_name", text="Course Name")
        self.courses.heading("assigned_prof", text="Assigned Professor")

        self.courses.column("cou_name", width=100, anchor="center")
        self.courses.column("raw_grade", width=100, anchor="center")

        self.courses.place(x=5, y=50, width=800, height=500)

        self.course_data = [
            ("Understanding The Self", "Jihyo Hernandez"),
            ("Readings In Philippine History", "Mina Franco"),
            ("The Contemporary World", "Dahyun Cruz"),
            ("Mathematics in The Modern World", "Tzuyu Mercado"),
        ]

        self.selected_courses = []

        for i, (course, professor) in enumerate(self.course_data):
            tk.Label(course_frame, text=course, width=40, anchor="w").grid(row=i + 1, column=0)
            tk.Label(course_frame, text=professor, width=30, anchor="w").grid(row=i + 1, column=1)
            btn = tk.Button(course_frame, text="SELECT", bg="#8D0404", fg="white",
                            command=lambda c=course, p=professor: self.add_course(c, p))
            btn.grid(row=i + 1, column=2)

        # Selected Course Frame
        selected_frame = tk.Frame(self)
        selected_frame.pack(padx=10, pady=20)

        tk.Label(selected_frame, text="Selected Course", font=("Arial", 12, "bold"), bg="#8D0404", fg="white",
                 width=70).grid(row=0, column=0, columnspan=3)

        self.selected_list = tk.Frame(selected_frame)
        self.selected_list.grid(row=1, column=0, columnspan=3)

        # Confirm Button
        confirm_btn = tk.Button(self, text="Confirm Application", bg="#8D0404", fg="white",
                                command=self.confirm_application)
        confirm_btn.pack(pady=10)

    def add_course(self, course, professor):
        if (course, professor) not in self.selected_courses:
            self.selected_courses.append((course, professor))
            self.update_selected_list()

    def remove_course(self, course, professor):
        self.selected_courses.remove((course, professor))
        self.update_selected_list()

    def update_selected_list(self):
        for widget in self.selected_list.winfo_children():
            widget.destroy()

        for course, professor in self.selected_courses:
            row = tk.Frame(self.selected_list)
            row.pack(anchor="w")

            tk.Label(row, text=course, width=40, anchor="w").pack(side=tk.LEFT)
            tk.Label(row, text=professor, width=30, anchor="w").pack(side=tk.LEFT)
            tk.Button(row, text="X", fg="red", command=lambda c=course, p=professor: self.remove_course(c, p)).pack(
                side=tk.LEFT)

    def confirm_application(self):
        print("Selected Courses:", self.selected_courses)
        self.destroy()
