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
        self.resizable(False, False)# Get the base directory of the project
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

        # Main Frame
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

        # Sidebar Frame
        self.sidebar = tk.Frame(self.main_frame, width=140,height=1000)
        self.sidebar.grid(row=0, column=0, sticky=tk.NSEW)
        self.sidebar.pack_propagate(False)

        # Canvas for sidebar
        self.sidebar_canvas = tk.Canvas(self.sidebar, bg="#8D0404")
        self.sidebar_canvas.pack(fill=tk.BOTH, expand=True)

        # Admin username
        self.sidebar_canvas.create_text(10, 10, text=self.admin_session["adm_username"], font=LEXEND_DECA_10, fill="#FFFFFF",anchor=tk.NW)

        # Dashboard button tab
        dashboard_path = IMAGES_DIR / "DashboardButtonActive.png"
        dashboard_img = Image.open(dashboard_path)
        dashboard_img = dashboard_img.resize((136, 72), Image.Resampling.LANCZOS)
        self.dashboard_img = ImageTk.PhotoImage(dashboard_img)
        self.dashboard_btn = tk.Button(self.sidebar, width=134, height=70, borderwidth=0, image=self.dashboard_img, command=lambda: self.display_frame("AdminDashboard"))
        self.dashboard_btn.place(x=2, y=100)

        # Faculty button tab
        faculty_path = IMAGES_DIR / "FacultyButton.png"
        faculty_img = Image.open(faculty_path)
        faculty_img = faculty_img.resize((136, 72), Image.Resampling.LANCZOS)
        self.faculty_img = ImageTk.PhotoImage(faculty_img)
        self.faculty_btn = tk.Button(self.sidebar, width=134, height=70, borderwidth=0, image=self.faculty_img, command=lambda: self.display_frame("AdminFaculty"))
        self.faculty_btn.place(x=2, y=200)

        # Courses button tab
        courses_path = IMAGES_DIR / "CoursesButton.png"
        courses_img = Image.open(courses_path)
        courses_img = courses_img.resize((136, 72), Image.Resampling.LANCZOS)
        self.courses_img = ImageTk.PhotoImage(courses_img)
        self.courses_btn = tk.Button(self.sidebar, width=134, height=70, borderwidth=0, image=self.courses_img, command=lambda: self.display_frame("AdminCourses"))
        self.courses_btn.place(x=2, y=300)

        # Logout button
        logout_path = IMAGES_DIR / "LogOutButton.png"
        logout_img = Image.open(logout_path)
        logout_img = logout_img.resize((136, 26), Image.Resampling.LANCZOS)
        self.logout_img = ImageTk.PhotoImage(logout_img)
        self.logout_btn = tk.Button(self.sidebar, width=134, height=24
                                    , borderwidth=0, image=self.logout_img, command=self.log_out)
        self.logout_btn.place(x=2, y=500)

        # Logout button
        self.logout_btn = tk.Button(self.sidebar, text="Logout", command=self.log_out)
        self.logout_btn.pack()

        self.display_frame("AdminDashboard")

        # self.load_admin_session() # Admin session # NOTE: Remove this

    def on_close(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to close the application? You will be logged out.")

        if confirm:
            self.main.clear_user_session("Admin")  # Log out the user
            self.destroy()  # Close the dashboard
            self.main.destroy()  # Stop the entire application

    def display_frame(self, frame_name):
        frame = self.dict_frames[frame_name]
        frame.lift()


    def log_out(self):
        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")

        if confirm:
            self.main.clear_user_session("Admin") # Clear the admin session
            self.destroy() # Close the dashboard
            self.main.deiconify() # Display the home screen
