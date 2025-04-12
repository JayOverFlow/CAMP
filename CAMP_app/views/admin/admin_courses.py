import tkinter as tk
from tkinter import font, ttk, messagebox

from CAMP_app.views.admin.add_course import AddCourse

class AdminCourses(tk.Frame):
    def __init__(self, parent, main, admin_landing, admin_faculty):
        super().__init__(parent)
        self.main = main
        self.admin_landing = admin_landing
        self.admin_faculty = admin_faculty

        # Canvas
        self.courses_canvas = tk.Canvas(self, bg="#D9D9D9", bd=0, highlightthickness=0)
        self.courses_canvas.pack(fill=tk.BOTH, expand=True)

        # Course Header
        self.courses_canvas.create_text(30, 20, text="Courses", font=("Lexend Deca", 20, "bold"), fill="#8D0404",
                                        anchor=tk.NW)

        # Course List Frame
        header_font = font.Font(family="Lexend Deca", size=10, weight="bold")
        row_font = font.Font(family="Lexend Deca", size=10)

        # Course List
        self.course_list = ttk.Treeview(
            self,  # Parent is course_list_frame
            columns=("course_name", "day", "time", "faculty", "delete"),
            show="headings",
            height=22
        )

        # Headings
        self.course_list.heading("course_name", text="")
        self.course_list.heading("day", text="")
        self.course_list.heading("time", text="")
        self.course_list.heading("faculty", text="")
        self.course_list.heading("delete", text="")

        # Column Widths
        col_width_cname = 250
        col_width_day = 90
        col_width_time = 140
        col_width_faculty = 240
        col_width_delete = 78

        # Columns
        self.course_list.column("course_name", anchor="center", width=col_width_cname)
        self.course_list.column("day", anchor="center", width=col_width_day)
        self.course_list.column("time", anchor="center", width=col_width_time)
        self.course_list.column("faculty", anchor="center", width=col_width_faculty)
        self.course_list.column("delete", anchor="center", width=col_width_delete)
        self.course_list.tag_configure("row", font=row_font)

        # Fake header
        course_header_height = 30
        course_header_frame = tk.Frame(
            self,
            bg="#8D0404",
            width=800,
            height=course_header_height
        )
        course_header_frame.pack_propagate(False)

        tk.Label(course_header_frame, text="Course Name", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=28, anchor="center").pack(side="left", padx=0)
        tk.Label(course_header_frame, text="Day", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=7, anchor="center").pack(side="left", padx=0)
        tk.Label(course_header_frame, text="Time", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=18, anchor="center").pack(side="left", padx=0)
        tk.Label(course_header_frame, text="Assigned Professor", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=24, anchor="center").pack(side="left", padx=0)
        tk.Label(course_header_frame, text="", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=10, anchor="center").pack(side="left", padx=0)

        course_header_x = 30
        course_header_y = 60
        course_header_frame.place(x=course_header_x, y=course_header_y)

        course_tree_x = course_header_x
        course_tree_y = course_header_y + 8
        self.course_list.place(x=course_tree_x, y=course_tree_y)
        self.course_list.bind("<ButtonRelease-1>", self.remove_course)
        course_header_frame.lift()
        self.course_list.bind("<ButtonRelease-1>", self.remove_course)

        # Add Course Button
        self.add_course_btn = tk.Button(
            self,
            width=14,
            text="+ Add Course",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 10, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.add_course
        )
        self.add_course_btn.place(x=696, y=550)
        self.add_course_btn.bind("<Enter>", lambda e: self.add_course_btn_hover_effect(e, True))
        self.add_course_btn.bind("<Leave>", lambda e: self.add_course_btn_hover_effect(e, False))

        self.display_courses()

    def add_course_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.add_course_btn.config(background=new_color)

    def display_courses(self):
        courses = self.main.admin_model.get_courses()
        for course in courses:
            self.course_list.insert("", "end", values=(
                course["course_name"],
                course["day_of_week"],
                f"{course["time_start"]}-{course["time_end"]}",
                f"{course["faculty_name"]}",
                "Remove"
            ), tags=("row",))

    def remove_course(self, event):
        selected_row = self.course_list.identify_row(event.y)
        column_id = self.course_list.identify_column(event.x)
        DELETE_COLUMN_INDEX = 5

        if int(column_id[1:]) == DELETE_COLUMN_INDEX and selected_row:
            values = self.course_list.item(selected_row, "values")
            course_name = values[0]
            confirm = messagebox.askyesno("Confirm Deletion",
                                          f"Are you sure you want to delete the course: {course_name}?")

            if confirm:
                course_id = self.main.admin_model.get_course_id_by_name(course_name)
                if course_id and self.main.admin_model.remove_course(course_id):
                    self.course_list.delete(selected_row)
                    messagebox.showinfo("Success", "Course deleted successfully!")
                    # Refresh the Faculty list
                    for row in self.admin_faculty.faculty_list.get_children():
                        self.admin_faculty.faculty_list.delete(row)
                    self.admin_faculty.display_faculties()
                else:
                    messagebox.showerror("Error", "Failed to delete the course.")

    def add_course(self):
        prof_names = self.main.admin_model.get_unassigned_faculties()
        if not prof_names:
            messagebox.showinfo("No Professors", "No available professors at the moment.")
            return
        self.admin_landing.attributes("-disabled", True)
        self.admin_landing.wait_window(AddCourse(self.admin_landing, self.main, self))
        self.admin_landing.attributes("-disabled", False)
        self.admin_landing.focus_force()

