import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk, font
from PIL import Image, ImageTk
import ctypes


class HomeScreen(tk.Frame):
    def __init__(self, parent, main): # parent
        super().__init__(parent)
        self.main = main

        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Get the base directory of the project
        BASE_DIR = Path(__file__).resolve().parent.parent  # Moves up two levels from "views"

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

        # Background
        bg_path = IMAGES_DIR / "home_screen_bg.png" # Get the path of a specific image
        bg = Image.open(bg_path) # Load the img file
        bg = bg.resize((1000, 600), Image.Resampling.LANCZOS) # Resize the img
        self.bg = ImageTk.PhotoImage(bg) # Convert into Python Object
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg) # Put the widget

        # CAMP Typography
        camp_typography_path = IMAGES_DIR / "CAMPWhiteTypography.png"
        camp_typography = Image.open(camp_typography_path)
        camp_typography = camp_typography.resize((600, 600), Image.Resampling.LANCZOS)
        self.camp_typography = ImageTk.PhotoImage(camp_typography)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.camp_typography)

        # CAMP Logo
        camp_logo_path = IMAGES_DIR / "CAMPLogoWhite.png"
        camp_logo = Image.open(camp_logo_path)
        camp_logo = camp_logo.resize((150, 150), Image.Resampling.LANCZOS)
        self.camp_logo = ImageTk.PhotoImage(camp_logo)
        self.canvas.create_image(680, 100, anchor=tk.NW, image=self.camp_logo)

        # Prompt
        self.canvas.create_text(600, 260, anchor=tk.NW, text="Choose your role to proceed:", font=LEXEND_DECA_16, fill="#FFFFFF" )

        style = ttk.Style()
        style.configure(
            "HomeScreen.TButton",
            font=LEXEND_DECA_16,
            foreground="#7B1818",
            background="white",
        )

        # Admin Button
        self.admin_btn = ttk.Button(
            self,
            text="Admin",
            style="HomeScreen.TButton",
            command=lambda: self.redirect_user("Admin")
        )
        self.admin_btn.place(x=680, y=320)

        # Faculty Button
        self.faculty_btn = ttk.Button(
            self,
            text="Faculty",
            style="HomeScreen.TButton",
            command=lambda: self.redirect_user("Faculty")
        )
        self.faculty_btn.place(x=680, y=380)

        self.student_btn = ttk.Button(
            self,
            text="Student",
            style="HomeScreen.TButton",
            command=lambda: self.redirect_user("Student")
        )
        self.student_btn.place(x=680, y=440)


    # Redirect user to its respective log in page
    def redirect_user(self, user_role):
        if user_role == "Admin":
            self.main.display_frame("AdminLogIn")
        elif user_role == "Faculty":
            self.main.display_frame("FacultyLogIn")
        elif user_role == "Student":
            self.main.display_frame("StudentLogIn")
        else:
            messagebox.showerror("System Error", "Oops! An unexpected error occurred")
