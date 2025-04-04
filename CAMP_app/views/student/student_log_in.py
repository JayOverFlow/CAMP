import ctypes
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk, font
from PIL import Image, ImageTk



class StudentLogIn(tk.Frame):
    def __init__(self, parent, main): # parent is a container and the controller is referenced to the main for frame switching
        super().__init__(parent) # pass the parent parameter as container
        self.main = main

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Get the base directory of the project
        BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Moves up two levels from "views"

        # Images directory
        IMAGES_DIR = BASE_DIR / "static/images"

        # Fonts directory
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

        # CAMP Red Typography
        camp_typography = IMAGES_DIR / "CAMPRedTypography.png"
        camp_typography = Image.open(camp_typography)
        camp_typography = camp_typography.resize((600, 600), Image.Resampling.LANCZOS)
        self.camp_typography = ImageTk.PhotoImage(camp_typography)
        self.canvas.create_image(0, 0, image=self.camp_typography, anchor=tk.NW)

        # Frame
        input_frame = IMAGES_DIR / "InputFrame.png"
        input_frame = Image.open(input_frame)
        input_frame = input_frame.resize((480, 450), Image.Resampling.LANCZOS)
        self.input_frame = ImageTk.PhotoImage(input_frame)
        self.canvas.create_image(500, 120, image=self.input_frame, anchor=tk.NW)

        # CAMP Logo
        camp_logo = IMAGES_DIR / "CAMPLogoRed.png"
        camp_logo = Image.open(camp_logo)
        camp_logo = camp_logo.resize((150, 150), Image.Resampling.LANCZOS)
        self.camp_logo = ImageTk.PhotoImage(camp_logo)
        self.canvas.create_image(670, 85, image=self.camp_logo, anchor=tk.NW)

        self.canvas.create_text(600, 250, anchor=tk.NW, text="Student Username:", font=LEXEND_DECA_12, fill="#FFFFFF")

        self.student_username_entry = ttk.Entry(self)  # pass self
        self.student_username_entry.place(anchor=tk.NW, x=600, y=280, width=300, height=35)
        self.student_username_entry.bind("<Return>", self.log_in)

        self.canvas.create_text(600, 320, anchor=tk.NW, text="Password:", font=LEXEND_DECA_12, fill="#FFFFFF")

        self.student_password_entry = ttk.Entry(self, show="*")  # pass self
        self.student_password_entry.place(anchor=tk.NW, x=600, y=350, width=300, height=35)
        self.student_password_entry.bind("<Return>", self.log_in)

        style = ttk.Style()

        style.configure(
            'btnStyle.TButton',
            font=LEXEND_DECA_12,
            relief="solid",
            borderwidth=5,
            background="#7B1818",
            foreground="#7B1818",
            justify=tk.CENTER,
        )

        style.map(
            "btnStyle.TButton",
            background=[("active", "#5A1313"), ("pressed", "#3E0E0E"), ("!disabled", "#7B1818")],
            foreground=[("active", "#5A1313"), ("pressed", "#3E0E0E")]
        )

        self.log_in_btn = ttk.Button(self, text="Log In", command=self.log_in, style='btnStyle.TButton')
        self.log_in_btn.place(anchor=tk.NW, x=600, y=420, width=300, height=35)
        self.log_in_btn.bind("<Return>", self.log_in)

        self.back_btn = ttk.Button(self, text="◀", command=self.back, style='btnStyle.TButton')
        self.back_btn.place(anchor=tk.NW, x=900, y=30, width=50, height=50)


    def log_in(self, event=None):
        student_username = self.student_username_entry.get().strip()
        student_password = self.student_password_entry.get().strip()

        # If the input fields are empty
        if not student_username or not student_password:
            messagebox.showwarning("Login Failed", "Please make sure that Username and Password are not empty")
            return

        # Authenticate
        result = self.main.user_auth.authenticate_student(student_username, student_password)

        if result:
            student_data = {
                "stu_id": result["stu_id"],
                'stu_first_name': result["stu_first_name"],
                'stu_middle_name': result["stu_middle_name"],
                'stu_last_name': result["stu_last_name"],
                'stu_full_name': result["stu_full_name"],
                'stu_birthdate': result["stu_birthdate"],
                'stu_sex': result["stu_sex"],
                'stu_username': result["stu_username"],
                'stu_password': result["stu_password"],
                'stu_phone_number': result["stu_phone_number"],
                'stu_lrn': result["stu_lrn"],
                'stu_citizenship': result["stu_citizenship"],
                'stu_emailadd': result["stu_emailadd"],
                'stu_religion': result["stu_religion"],
                'stu_address': result["stu_address"],
            }

            self.student_username_entry.delete(0, tk.END)
            self.student_password_entry.delete(0, tk.END)

            self.main.withdraw()

            self.main.open_user_landing("Student", student_data)

        else:
            messagebox.showwarning("Login Failed", "Username or Password is invalid")
            self.student_password_entry.delete(0, tk.END)
            self.student_password_entry.focus_set()

    def back(self):
        self.main.display_frame("HomeScreen")

        self.student_username_entry.delete(0, tk.END)
        self.student_password_entry.delete(0, tk.END)