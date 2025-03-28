import ctypes
import tkinter as tk
from pathlib import Path
from tkinter import font, ttk

from CAMP_app.views.admin.add_faculty import AddFaculty
from CAMP_app.views.admin.view_fac_students import ViewFacultyStudents


class AdminFaculty(tk.Frame):
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
        self.faculty_canvas = tk.Canvas(self, bg="#D9D9D9")
        self.faculty_canvas.pack(fill=tk.BOTH, expand=True)

        # Faculty Label
        self.faculty_canvas.create_text(100, 50, text="Faculty", font=LEXEND_DECA_20, fill="#8D0404")

        # Faculty List Frame
        self.fac_list_frame = tk.Frame(self, width=700, height=350, bg="#FBFBF9")
        self.fac_list_frame.place(x=50, y=100)
        self.fac_list_frame.pack_propagate(False)
        self.fac_list_frame.grid_propagate(False)

        # Faculty List
        self.faculty_list = ttk.Treeview(self.fac_list_frame, columns=("fac_full_name", "fac_id", "course", "view_student"), show="headings")
        # Headings
        self.faculty_list.heading("fac_full_name", text="Name")
        self.faculty_list.heading("fac_id", text="ID")
        self.faculty_list.heading("course", text="Course")
        self.faculty_list.heading("view_student", text="")
        # Columns
        self.faculty_list.column("fac_full_name", anchor="center", width=100)
        self.faculty_list.column("fac_id", anchor="center", width=100)
        self.faculty_list.column("course", anchor="center", width=100)
        self.faculty_list.column("view_student", anchor="center", width=100)
        self.faculty_list.pack(fill=tk.BOTH, expand=True)
        self.faculty_list.bind("<ButtonRelease-1>", self.view_student)

        # Add Faculty Button
        self.add_fac_btn = ttk.Button(self, text="Add Faculty", command=self.add_faculty)
        self.add_fac_btn.place(x=50, y=500)

        self.display_faculties()

    def display_faculties(self):
        faculties = self.main.admin_model.get_faculties()
        for faculty in faculties:
            self.faculty_list.insert("", "end", values=(faculty["fac_full_name"], faculty["fac_id"], faculty["course_name"], "View Students"))

    def view_student(self, event):
        selected_row = self.faculty_list.identify_row(event.y)
        column_id = self.faculty_list.identify_column(event.x)

        VIEW_STUDENT_COLUMN_INDEX = 4

        if int(column_id[1:]) == VIEW_STUDENT_COLUMN_INDEX:
            values = self.faculty_list.item(selected_row, "values")

            if values:
                fac_id = values[1]
                cou_id = self.main.admin_model.get_course_id_by_faculty(fac_id)
                if not cou_id:
                    print("No course found for this faculty.")
                    return

                fac_students = self.main.admin_model.get_faculty_students(fac_id)

                self.admin_landing.attributes("-disabled", True)  # Disable the interaction
                self.admin_landing.wait_window(
                    ViewFacultyStudents(self.admin_landing, self.main, fac_students, cou_id))  # Wait for the popup
                self.admin_landing.attributes("-disabled", False)  # Re-enable the interaction
                self.admin_landing.focus_force()  # Regain focus on the parent window

    def add_faculty(self):
        self.admin_landing.attributes("-disabled", True)
        self.admin_landing.wait_window(AddFaculty(self.admin_landing, self.main))
        self.admin_landing.attributes("-disabled", False)
        self.admin_landing.focus_force()