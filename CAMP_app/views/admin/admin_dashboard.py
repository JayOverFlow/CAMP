import ctypes
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import font, messagebox
from PIL import Image, ImageTk

from CAMP_app.views.admin.admit_student import AdmitStudent
from CAMP_app.views.admin.view_student_profile import ViewStudentProfile


class AdminDashboard(tk.Frame):
    def __init__(self, parent, main, admin_landing):
        super().__init__(parent)
        self.main = main
        self.admin_landing = admin_landing
        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        IMAGES_DIR = BASE_DIR / "static/images"

        FONT_DIR = BASE_DIR / "static/fonts"
        FONT_PATH = FONT_DIR / "LexandDeca-Bold.ttf"

        LEXAND_DECA_6 = font.Font(family="Lexand Deca", size=6)
        LEXAND_DECA_10 = font.Font(family="Lexand Deca", size=10)
        LEXAND_DECA_12 = font.Font(family="Lexand Deca", size=12)
        LEXAND_DECA_14 = font.Font(family="Lexand Deca", size=14)
        LEXAND_DECA_16 = font.Font(family="Lexand Deca", weight="bold", size=16)
        LEXAND_DECA_18 = font.Font(family="Lexand Deca",weight="bold",  size=18)
        LEXAND_DECA_20 = font.Font(family="Lexand Deca", size=20)
        LEXAND_DECA_40 = font.Font(family="Lexand Deca", weight="bold", size=40)

        try:
            ctypes.windll.gdi32.AddFontResourceW(str(FONT_PATH))
        except Exception as e:
            print(f"Error loading font: {e}")

        style = ttk.Style()
        style.theme_use("default")

        # Configure the Scrollbar style
        style.configure("Custom.Vertical.TScrollbar",
                        troughcolor="#D3D3D3",  # Background track color
                        background="#8D0404",  # Scrollbar color
                        arrowcolor="#FFFFFF",  # Arrow color
                        bordercolor="#8D0404",  # Border color
                        gripcount=0,  # Hide grip lines
                        relief="flat",  # Flat style
                        width=15)  # Width of the scrollbar
        style.configure("Custom.Treeview.Heading",
                        background="#8D0404",
                        foreground="white",
                        font=LEXAND_DECA_12,
                        padding=(5,5,5,5))
        style.configure("Custom.Treeview",
                        font=LEXAND_DECA_10,
                        rowheight=30)

        self.dashboard_canvas = tk.Canvas(self, bg="#D9D9D9")
        self.dashboard_canvas.pack(fill=tk.BOTH, expand=True)

        student_card_path = IMAGES_DIR / "StudentQuantityCard.png"
        student_card = Image.open(student_card_path)
        student_card = student_card.resize((350, 200), Image.Resampling.LANCZOS)
        self.student_card = ImageTk.PhotoImage(student_card)
        self.dashboard_canvas.create_image(30, 50, image=self.student_card, anchor=tk.NW)

        faculty_card_path = IMAGES_DIR / "FacultyQuantityCard.png"
        faculty_card = Image.open(faculty_card_path)
        faculty_card = faculty_card.resize((350, 200), Image.Resampling.LANCZOS)
        self.faculty_card = ImageTk.PhotoImage(faculty_card)
        self.dashboard_canvas.create_image(440, 50, image=self.faculty_card, anchor=tk.NW)

        # Student count
        self.dashboard_canvas.create_text(240,90, text=self.display_student_count(), font=LEXAND_DECA_40 ,fill="#000000",  anchor=tk.NW)


        # Female count
        self.dashboard_canvas.create_text(125, 203, text=self.display_female_count(), font=LEXAND_DECA_18 ,fill="#000000", anchor=tk.NW)

        # Male count
        self.dashboard_canvas.create_text(280, 203, text=self.display_male_count(), font=LEXAND_DECA_18 ,fill="#000000", anchor=tk.NW)

        # Faculty count
        self.dashboard_canvas.create_text(660, 120, text=self.display_faculty_count(), font=LEXAND_DECA_40,fill="#000000", anchor=tk.NW)

        # Admit student button
        self.enroll_btn = tk.Button(self.dashboard_canvas, text="+  Admit Student", command=lambda: self.admit_student(), font=LEXAND_DECA_10, anchor=tk.NW, bg="#8D0404", fg="#FFFFFF", padx=5, pady=5)
        self.enroll_btn.place(x=420, y=300)

        # Search bar
        self.search_var = tk.StringVar()  # Variable to store the entry string
        self.search_entry = tk.Entry(self.dashboard_canvas, textvariable=self.search_var, width=39)
        self.search_entry.insert(0, "Search by Name or ID")  # Initial as placeholder

        # Handle focus for placeholder
        self.search_entry.bind("<FocusIn>", self.toggle_placeholder)
        self.search_entry.bind("<FocusOut>", self.toggle_placeholder)
        self.search_entry.place(x=550,y=300, anchor=tk.NW, height=35)
        self.search_entry.bind("<KeyRelease>", self.filter_students)  # Filter students for live searching

        self.student_list_frame = tk.Frame(self.dashboard_canvas, width=750, height=250)
        self.student_list_frame.place(x=35, y=350, anchor=tk.NW)


        # Student list
        self.student_list = ttk.Treeview(self.student_list_frame, columns=("stu_full_name", "stu_id", "view_profile"),
                                         show="headings", style="Custom.Treeview", height=6)
        self.student_list.heading("stu_full_name", text="Full Name", anchor="center", )
        self.student_list.heading("stu_id", text="Student ID", anchor="center")
        self.student_list.heading("view_profile", text="", anchor="center")
        self.student_list.column("stu_full_name", anchor="center", width=300)
        self.student_list.column("stu_id", anchor="center", width=200)
        self.student_list.column("view_profile", anchor="center", width=250)

        self.scrollbar = ttk.Scrollbar(self.student_list_frame, orient="vertical", command=self.student_list.yview)
        self.student_list.configure(yscrollcommand=self.scrollbar.set)

        # self.display_students()
        self.display_data() # Display all data
        self.student_list.pack(side="left", fill="both", expand=True)
        self.student_list.bind("<ButtonRelease-1>", self.view_profile)  # When the user clicked the "View Profile"
        self.scrollbar.pack(side="right", fill="y")


    def display_data(self):
        self.display_student_count()
        self.display_female_count()
        self.display_male_count()
        self.display_faculty_count()
        self.display_students()

    def display_student_count(self):
        student_count = self.main.admin_model.get_student_count()

        return student_count

    def display_female_count(self):
        female_count = self.main.admin_model.get_female_count()

        return female_count

    def display_male_count(self):
        male_count = self.main.admin_model.get_male_count()

        return male_count

    def display_faculty_count(self):
        faculty_count = self.main.admin_model.get_faculty_count()

        return faculty_count
    def admit_student(self):
        self.admin_landing.attributes("-disabled", True) # Disable the interaction
        self.admin_landing.wait_window(AdmitStudent(self.main, self.admin_landing)) # Wait for the popup
        self.admin_landing.attributes("-disabled", False) # Re-enable the interaction
        self.admin_landing.focus_force() # Regain focus on the parent window

    def display_students(self):
        self.all_students = self.main.admin_model.get_students() # Get and store the students
        self.update_treeview(self.all_students) # Pass the students

    def update_treeview(self, students):
        # Clear and display
        self.student_list.delete(*self.student_list.get_children())
        for student in students:
            self.student_list.insert("", "end", values=(student["stu_full_name"], f"AU{student["stu_id"]}", "View Profile"))

    def filter_students(self, event=None):
        search_text = self.search_var.get().lower() # Get the user input
        # Manipulate the studentlist for filtering
        filtered_students = [
            s for s in self.all_students
            if search_text in s["stu_full_name"].lower() or search_text in str(s["stu_id"])
        ]
        self.update_treeview(filtered_students) # Update the student list with filtered students

    def toggle_placeholder(self, event):
        if event.type == "9":  # FocusIn
            if self.search_entry.get() == "Search by Name or ID":
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg="black")
        elif event.type == "10":  # FocusOut
            if not self.search_entry.get():
                self.search_entry.insert(0, "Search by Name or ID")
                self.search_entry.config(fg="gray")

    def view_profile(self, event):
        # Get the selected row
        selected_row = self.student_list.identify_row(event.y)

        # Get the clicked column
        column_id = self.student_list.identify_column(event.x) # OUtput #3

        # Define the column index
        VIEW_PROFILE_COLUMN_INDEX = 3

        # Convert column_id (e.g., "#3") to integer and check if it matches the 'View Profile' column
        if int(column_id[1:]) == VIEW_PROFILE_COLUMN_INDEX:
            values = self.student_list.item(selected_row, "values")

            if values:
                stu_id = values[1][2:]  # Adjust index based on your data structure
                student_data = self.main.admin_model.get_student_profile(stu_id)

                # Open Student Profile
                self.admin_landing.attributes("-disabled", True)  # Disable the interaction
                self.admin_landing.wait_window(ViewStudentProfile(self, self.admin_landing, self.main, student_data))  # Wait for the popup
                self.admin_landing.attributes("-disabled", False)  # Re-enable the interaction
                self.admin_landing.focus_force()  # Regain focus on the parent window