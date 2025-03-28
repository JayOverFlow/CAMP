import ctypes
import tkinter as tk
from pathlib import Path
from tkinter import font, ttk, messagebox

from CAMP_app.views.admin.add_course import AddCourse


class AdminCourses(tk.Frame):
    def __init__(self, parent, main, admin_landing):
        super().__init__(parent)
        self.main = main
        self.admin_landing = admin_landing

        # Paths
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        IMAGES_DIR = BASE_DIR / "static/images"
        FONTS_DIR = BASE_DIR / "static/fonts"
        FONT_PATH = FONTS_DIR / "LexendDeca-Bold.ttf"

        # Font sizes
        LEXEND_DECA_10 = font.Font(family="Lexend Deca", size=10)
        LEXEND_DECA_12 = font.Font(family="Lexend Deca", size=12)
        LEXEND_DECA_14 = font.Font(family="Lexend Deca", size=14)
        LEXEND_DECA_16 = font.Font(family="Lexend Deca", size=16)
        LEXEND_DECA_18 = font.Font(family="Lexend Deca", size=18)
        LEXEND_DECA_20 = font.Font(family="Lexend Deca", size=20)
        try:
            ctypes.windll.gdi32.AddFontResourceW(str(FONT_PATH))
        except Exception as e:
            print(f"Error loading font: {e}")

        # Canvas
        self.courses_canvas = tk.Canvas(self, bg="#D9D9D9")
        self.courses_canvas.pack(fill=tk.BOTH, expand=True)

        # Course Header
        self.courses_canvas.create_text(100, 50, text="Courses", font=LEXEND_DECA_20, fill="#8D0404")

        # Course List Frame
        self.course_list_frame = tk.Frame(self, width=700, height=350, bg="#FBFBF9")
        self.course_list_frame.place(x=50, y=100)
        self.course_list_frame.pack_propagate(False)
        self.course_list_frame.grid_propagate(False)

        # Course List
        self.course_list = ttk.Treeview(self.course_list_frame, columns=("course_name", "day", "time", "faculty", "delete"),
                                        show="headings")
        # Headings
        self.course_list.heading("course_name", text="Course Name")
        self.course_list.heading("day", text="Day")
        self.course_list.heading("time", text="Time")
        self.course_list.heading("faculty", text="Assigned Professor")
        self.course_list.heading("delete", text="")
        # Columns
        self.course_list.column("course_name", anchor="center", width=100)
        self.course_list.column("day", anchor="center", width=100)
        self.course_list.column("time", anchor="center", width=100)
        self.course_list.column("faculty", anchor="center", width=100)
        self.course_list.column("delete", anchor="center", width=50)
        self.course_list.pack(fill=tk.BOTH, expand=True)
        self.course_list.bind("<ButtonRelease-1>", self.remove_course)

        # Add Course Button
        self.add_course_btn = ttk.Button(self, text="Add Course ", command=self.add_course)
        self.add_course_btn.place(x=50, y=500)

        self.display_courses()

    def display_courses(self):
        courses = self.main.admin_model.get_courses()
        for course in courses:
            self.course_list.insert("", "end", values=(
                course["course_name"],
                course["day_of_week"],
                f"{course["time_start"]}-{course["time_end"]}",
                f"{course["faculty_name"]}",
                "del"
            ))

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
                    messagebox.showinfo("Success", "Course deleted successfully!")
                    self.course_list.delete(selected_row)
                else:
                    messagebox.showerror("Error", "Failed to delete the course.")

    def add_course(self):
        self.admin_landing.attributes("-disabled", True)
        self.admin_landing.wait_window(AddCourse(self.admin_landing, self.main, self))
        self.admin_landing.attributes("-disabled", False)
        self.admin_landing.focus_force()

