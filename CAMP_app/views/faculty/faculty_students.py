import ctypes
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import font, messagebox
from PIL import Image, ImageTk, ImageDraw


class FacultyStudents(tk.Frame):
    def __init__(self, parent, main, faculty_landing):
        super().__init__(parent)
        self.main = main
        self.faculty_landing = faculty_landing

        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        IMAGES_DIR = BASE_DIR / "static/images"

        FONT_DIR = BASE_DIR / "static/fonts"
        FONT_PATH = FONT_DIR / "LexandDeca-Bold.ttf"
        self.PFP_DIR = BASE_DIR / "static/student_pfps"

        LEXAND_DECA_6 = font.Font(family="Lexand Deca", size=6)
        LEXAND_DECA_10 = font.Font(family="Lexand Deca", size=10)
        LEXAND_DECA_12 = font.Font(family="Lexand Deca", size=12)
        LEXAND_DECA_14 = font.Font(family="Lexand Deca", size=14)
        LEXAND_DECA_16 = font.Font(family="Lexand Deca", weight="bold", size=16)
        LEXAND_DECA_18 = font.Font(family="Lexand Deca", weight="bold", size=18)
        LEXAND_DECA_20 = font.Font(family="Lexand Deca", weight="bold", size=20)
        LEXAND_DECA_40 = font.Font(family="Lexand Deca", weight="bold", size=40)

        self.students_canvas = tk.Canvas(self, bg="#D9D9D9")
        self.students_canvas.pack(fill=tk.BOTH, expand=True)

        # Headings
        self.fac_id = self.faculty_landing.faculty_session["fac_id"]
        result = self.main.faculty_model.get_faculty_course(self.fac_id)
        self.cou_id = result["cou_id"]
        fac_course = result["cou_name"]
        self.students_canvas.create_text(20, 20, text=fac_course, font=LEXAND_DECA_20, fill="#8D0404", anchor=tk.NW)
        self.students_canvas.create_text(540, 20, text="Student Profile", font=LEXAND_DECA_20, fill="#8D0404", anchor=tk.NW)

        self.create_student_list()

    def create_student_list(self):
        self.student_list_frame = tk.Frame(self, width=500, height=520)
        self.student_list_frame.place(x=20, y=60)
        self.student_list_frame.pack_propagate(False)

        # Student List
        self.student_list = ttk.Treeview(self.student_list_frame, columns=("index", "stu_full_name", "stu_id"), show="headings", height=15)
        # Headings
        self.student_list.heading("index", text="")
        self.student_list.heading("stu_full_name", text="Student Name")
        self.student_list.heading("stu_id", text="Student ID")
        # Columns
        self.student_list.column("index", anchor="center", width=20)
        self.student_list.column("stu_full_name", anchor="center", width=130)
        self.student_list.column("stu_id", anchor="center", width=100)
        self.student_list.pack(fill=tk.BOTH, expand=True)
        self.student_list.bind("<ButtonRelease-1>", self.view_stu_profile)
        self.display_students()

    def display_students(self):
        students = self.main.faculty_model.get_students(self.fac_id)
        i = 0
        for student in students:
            i+=1
            stu_full_name = f"{student["stu_last_name"]}, {student["stu_first_name"]} {student["stu_middle_name"]}"
            self.student_list.insert("", "end", values=(i, stu_full_name, f"AU{student["stu_id"]}"))

    def view_stu_profile(self, event):
        selected_row = self.student_list.identify_row(event.y)
        values = self.student_list.item(selected_row, "values")

        if values:
            stu_id = values[2][2:]  # Adjust index based on your data structure
            student_data = self.main.faculty_model.get_student_profile(stu_id)

            self.create_stu_profile_card(self.PFP_DIR, student_data)
            self.create_stu_scores_and_grades_card(self.cou_id, stu_id)


    def create_stu_profile_card(self, PFP_DIR, student_data):
        if hasattr(self, 'stu_profile_card'):
            self.stu_profile_card.destroy()

        stu_pfp = student_data["profile_picture"]
        stu_full_name = student_data["stu_full_name"]
        stu_id = student_data["stu_id"]
        stu_phone_num = student_data["stu_phone_number"]
        stu_email = student_data["stu_emailadd"]
        stu_address = student_data["stu_address"]

        # Card
        self.stu_profile_card = tk.Frame(self, width=300, height=280)
        self.stu_profile_card.place(x=540, y=60)
        self.stu_profile_card.pack_propagate(False)

        self.stu_profile_card_canvas = tk.Canvas(self.stu_profile_card, bg="#FFFFFF")
        self.stu_profile_card_canvas.pack(fill=tk.BOTH, expand=True)

        # Close Button
        self.close_profile_btn = tk.Button(self.stu_profile_card, text="x", command=self.close_stu_profile)
        self.close_profile_btn.place(x=100, y=0)

        # Student PFP
        pfp_path = self.get_pfp_path(PFP_DIR, stu_id)
        self.pfp = self.make_pfp_circle(pfp_path)
        self.stu_profile_card_canvas.create_image(50, 50, anchor=tk.NW, image=self.pfp)

        # Student Full Name
        self.stu_full_name = tk.Label(self.stu_profile_card, text=stu_full_name)
        self.stu_full_name.place(x=10, y=200)

        # Student ID
        self.stu_id = tk.Label(self.stu_profile_card, text=f"AU{stu_id}")
        self.stu_id.place(x=10, y=220)

        # Student Phone Number
        self.stu_phone_num = tk.Label(self.stu_profile_card, text=stu_phone_num)
        self.stu_phone_num.place(x=10, y=240)

        # Student Email Address
        self.stu_email = tk.Label(self.stu_profile_card, text=stu_email)
        self.stu_email.place(x=10, y=260)

        # Student Address
        self.stu_address = tk.Label(self.stu_profile_card, text=stu_address)
        self.stu_address.place(x=10, y=280)

        self.create_stu_scores_and_grades_card(self.cou_id, stu_id)

    def close_stu_profile(self):
        if hasattr(self, 'stu_profile_card'):
            self.stu_profile_card.destroy()

        if hasattr(self, 'stu_grades_card'):
            self.stu_grades_card.destroy()

    def create_stu_scores_and_grades_card(self, cou_id, stu_id):
        if hasattr(self, 'stu_grades_card'):
            self.stu_grades_card.destroy()  # Ensure previous card is removed before creating a new one
        self.stu_grades_card = tk.Frame(self, width=300, height=220)
        self.stu_grades_card.place(x=540, y=360)
        self.stu_grades_card.grid_propagate(False)

        # Header
        self.grades_header = tk.Label(self.stu_grades_card, text="Student Grades").grid(row=0, column=0, columnspan=2)

        # Fields
        self.written_works_lbl = tk.Label(self.stu_grades_card, text="Written Works (100):").grid(row=1, column=0)
        self.written_works = tk.Entry(self.stu_grades_card)
        self.written_works.grid(row=1, column=1)

        self.final_project = tk.Label(self.stu_grades_card, text="Final Project (100):").grid(row=2, column=0)
        self.final_project = tk.Entry(self.stu_grades_card)
        self.final_project.grid(row=2, column=1)

        self.examination = tk.Label(self.stu_grades_card, text="Examinations (150):").grid(row=3, column=0)
        self.examination = tk.Entry(self.stu_grades_card)
        self.examination.grid(row=3, column=1)

        # Raw Grade
        self.raw_grade_lbl = tk.Label(self.stu_grades_card, text="Raw Grade: ").grid(row=4, column=0)
        self.raw_grade = tk.Label(self.stu_grades_card, text="-")
        self.raw_grade.grid(row=4, column=1)

        # Final Grade
        self.final_grade_lbl = tk.Label(self.stu_grades_card, text="Final Grade: ").grid(row=5, column=0)
        self.final_grade = tk.Label(self.stu_grades_card, text="-")
        self.final_grade.grid(row=5, column=1)

        # Submit Button
        self.submit_btn = tk.Button(self.stu_grades_card, text="Submit", command=lambda: self.submit_scores(self.cou_id, stu_id))
        self.submit_btn.grid(row=10, column=0, columnspan=2)

        self.display_stu_score(cou_id, stu_id)

    def display_stu_score(self, cou_id, stu_id):
        # Fetch student's scores
        stu_scores = self.main.faculty_model.get_student_scores(cou_id, stu_id)
        stu_written_score = stu_scores["score_written"]
        stu_final_project_score = stu_scores["score_project"]
        stu_examination_score = stu_scores["score_exam"]

        # Display fetched scores in entry fields
        self.written_works.insert(0, stu_written_score)
        self.final_project.insert(0, stu_final_project_score)
        self.examination.insert(0, stu_examination_score)

        self.display_stu_grades(cou_id, stu_id)

    def submit_scores(self, cou_id, stu_id):
        if self.validate_grades_submission():
            written_works = self.written_works.get().strip()
            final_project = self.final_project.get().strip()
            examination = self.examination.get().strip()

            # Convert valid inputs to integers, leave None if empty
            written_works = int(written_works) if written_works else None
            final_project = int(final_project) if final_project else None
            examination = int(examination) if examination else None

            raw_grade = self.calculate_raw_grade(written_works, final_project, examination)
            final_grade = self.calculate_final_grade(raw_grade)

            # Insert scores and update grades
            add_scores = self.main.faculty_model.submit_scores(cou_id, stu_id, written_works, final_project, examination)
            update_grades = self.main.faculty_model.update_grades(cou_id, stu_id, raw_grade, final_grade)
            if add_scores and update_grades:
                messagebox.showinfo("Success", "Scores submitted successfully")
                self.display_stu_grades(cou_id, stu_id)
            else:
                messagebox.showerror("Failed", "Failed to submit scores")

    def validate_grades_submission(self):
        try:
            # Get and strip input values
            written_works = self.written_works.get().strip()
            final_project = self.final_project.get().strip()
            examination = self.examination.get().strip()

            # Ensure no field is empty
            if not written_works or not final_project or not examination:
                messagebox.showwarning("Input Error", "All fields must be filled.")
                return False

                # Ensure all fields contain only digits
            if not written_works.isdigit() or not final_project.isdigit() or not examination.isdigit():
                messagebox.showwarning("Input Error", "Only numeric values are allowed.")
                return False

                # Convert to integers
            written_works = int(written_works)
            final_project = int(final_project)
            examination = int(examination)

            # Validate ranges
            if not (0 <= written_works <= 100):
                messagebox.showwarning("Input Error", "Written Works must be between 0 and 100.")
                return False
            if not (0 <= final_project <= 100):
                messagebox.showwarning("Input Error", "Final Project must be between 0 and 100.")
                return False
            if not (0 <= examination <= 150):
                messagebox.showwarning("Input Error", "Examination must be between 0 and 150.")
                return False

            return True  # Validation successful
        except Exception as e:
            messagebox.showerror("Validation Error", f"An error occurred: {e}")
            return False

    def calculate_raw_grade(self, written_works, final_project, examination):
        try:
            written_works = int(written_works)
            final_project = int(final_project)
            examination = int(examination)
        except ValueError:
            return "Submit all scores to generate"

        raw_grade = (written_works + final_project + (examination / 150 * 100)) / 3
        return round(raw_grade, 2)

    def calculate_final_grade(self, raw_grade):
        # Determine final grade based on raw grade
        if raw_grade >= 98:
            return 1.00
        elif raw_grade >= 91:
            return 1.25
        elif raw_grade >= 85:
            return 1.50
        elif raw_grade >= 79:
            return 1.75
        elif raw_grade >= 73:
            return 2.00
        elif raw_grade >= 67:
            return 2.25
        elif raw_grade >= 61:
            return 2.50
        elif raw_grade >= 55:
            return 2.75
        elif raw_grade >= 50:
            return 3.00
        else:
            return 5.00

    def display_stu_grades(self, cou_id, stu_id):
        grades = self.main.faculty_model.get_student_grades(cou_id, stu_id)
        if grades:
            raw_grade = grades["raw_grade"]
            final_grade = grades["final_grade"]

            self.raw_grade.configure(text=raw_grade)
            self.final_grade.configure(text=final_grade)

    def get_pfp_path(self, PFP_DIR, stu_id):
        pfp_path = PFP_DIR / f"student_{stu_id}.png"
        default_pfp = PFP_DIR / "student_default.png"
        return pfp_path if pfp_path.exists() else default_pfp

    def make_pfp_circle(self, pfp_path):
        size = (100, 100)
        pfp = Image.open(pfp_path).convert("RGBA")
        pfp = pfp.resize(size, Image.Resampling.LANCZOS) # Open image and ensure transparency support

        # Create circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((1, 1, size[0] - 1, size[1] - 1), fill=255)  # Draw a filled circle

        # Apply the mask
        circular_pfp = Image.new("RGBA", size, (0, 0, 0, 0)) # Transparent BG
        circular_pfp.paste(pfp, (0, 0), mask)

        return ImageTk.PhotoImage(circular_pfp)