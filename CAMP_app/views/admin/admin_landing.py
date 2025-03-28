import ctypes
import tkinter as tk
from pathlib import Path
from tkinter import font, messagebox
from PIL import Image, ImageTk

# Content Frames
from CAMP_app.views.admin.admin_dashboard import AdminDashboard
from CAMP_app.views.admin.admin_faculty import AdminFaculty
from CAMP_app.views.admin.admin_courses import AdminCourses

class AdminLanding(tk.Toplevel):
    def __init__(self, main, admin_session):
        super().__init__()
        self.main = main
        self.admin_session = admin_session
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Admin Landing")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)

        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        IMAGES_DIR = BASE_DIR / "static/images"
        FONTS_DIR = BASE_DIR / "static/fonts"
        FONT_PATH = FONTS_DIR / "LexendDeca-Bold.ttf"

        LEXEND_DECA_10 = font.Font(family="Lexend Deca", size=10)
        LEXEND_DECA_6 = font.Font(family="Lexend Deca", size=6)

        try:
            ctypes.windll.gdi32.AddFontResourceW(str(FONT_PATH))
        except Exception as e:
            print(f"Error loading font: {e}")

        self.main_frame = tk.Frame(self)
        self.main_frame.columnconfigure(0, minsize=140)
        self.main_frame.columnconfigure(1, weight=440)
        self.main_frame.rowconfigure(0, minsize=1000)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.dict_frames = {}
        self.content_frames = (AdminDashboard, AdminFaculty, AdminCourses)

        for CF in self.content_frames:
            frame = CF(self.main_frame, self.main, self)
            self.dict_frames[CF.__name__] = frame
            frame.grid(row=0, column=1, sticky=tk.NSEW)

        self.sidebar = tk.Frame(self.main_frame, width=140, height=1000)
        self.sidebar.grid(row=0, column=0, sticky=tk.NSEW)
        self.sidebar.pack_propagate(False)

        self.sidebar_canvas = tk.Canvas(self.sidebar, bg="#8D0404")
        self.sidebar_canvas.pack(fill=tk.BOTH, expand=True)

        camp_logo_path = IMAGES_DIR / "CAMPLogoWhiteTypography.png"
        camp_logo = Image.open(camp_logo_path).resize((100, 35), Image.Resampling.LANCZOS)
        self.camp_logo = ImageTk.PhotoImage(camp_logo)
        self.sidebar_canvas.create_image(20, 20, image=self.camp_logo, anchor=tk.NW)

        icon_admin_path = IMAGES_DIR / "ProfileIcon.png"
        icon_admin = Image.open(icon_admin_path).resize((50, 50), Image.Resampling.LANCZOS)
        self.icon_admin = ImageTk.PhotoImage(icon_admin)
        self.sidebar_canvas.create_image(45, 90, image=self.icon_admin, anchor=tk.NW)
        self.sidebar_canvas.create_text(36, 145, text=self.admin_session["adm_username"], font=LEXEND_DECA_10, fill="#FFFFFF", anchor=tk.NW)
        self.sidebar_canvas.create_text(55, 167, text="ADMIN", font=LEXEND_DECA_6, fill="#FFFFFF", anchor=tk.NW)

        # Image Paths
        self.image_paths = {
            'dashboard_active': IMAGES_DIR / "DashboardButtonActive.png",
            'dashboard_inactive': IMAGES_DIR / "DashboardButton.png",
            'faculty_active': IMAGES_DIR / "FacultyButtonActive.png",
            'faculty_inactive': IMAGES_DIR / "FacultyButton.png",
            'courses_active': IMAGES_DIR / "CoursesButtonActive.png",
            'courses_inactive': IMAGES_DIR / "CoursesButton.png",
        }

        self.dashboard_btn = self.create_nav_button("AdminDashboard", 200, 'dashboard')
        self.faculty_btn = self.create_nav_button("AdminFaculty", 270, 'faculty')
        self.courses_btn = self.create_nav_button("AdminCourses", 340, 'courses')

        self.display_frame("AdminDashboard")

    def create_nav_button(self, frame_name, y_pos, name):
        img_path = self.image_paths[f'{name}_active'] if frame_name == "AdminDashboard" else self.image_paths[f'{name}_inactive']
        img = Image.open(img_path).resize((136, 72), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)

        button = tk.Button(self.sidebar, width=134, height=70, borderwidth=0, image=img, command=lambda: self.display_frame(frame_name))
        button.image = img
        button.place(x=2, y=y_pos)
        return button

    def update_nav_buttons(self, active_frame_name):
        for name, button in [('dashboard', self.dashboard_btn), ('faculty', self.faculty_btn), ('courses', self.courses_btn)]:
            state = 'active' if active_frame_name == f'Admin{name.capitalize()}' else 'inactive'
            img_path = self.image_paths[f'{name}_{state}']
            img = Image.open(img_path).resize((136, 72), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            button.config(image=img)
            button.image = img

    def display_frame(self, frame_name):
        self.update_nav_buttons(frame_name)
        frame = self.dict_frames[frame_name]
        frame.lift()

    def log_out(self):
        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")
        if confirm:
            self.main.clear_user_session("Admin")
            self.destroy()
            self.main.deiconify()

    def on_close(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to close the application? You will be logged out.")
        if confirm:
            self.main.clear_user_session("Admin")
            self.destroy()
            self.main.destroy()
