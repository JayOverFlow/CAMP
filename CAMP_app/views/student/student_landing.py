import ctypes
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, font

# Content Frames
from CAMP_app.views.student.student_courses import StudentCoursesTab
from CAMP_app.views.student.student_profile import StudentProfileTab
from CAMP_app.views.student.student_schedule import StudentScheduleTab


class StudentLanding(tk.Toplevel):
    def __init__(self, main, student_session):
        super().__init__()
        self.main = main
        self.student_session = student_session
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Student Landing")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)
        BASE_DIR = Path(__file__).resolve().parent.parent

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

        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.columnconfigure(0, minsize=140)
        self.main_frame.columnconfigure(1, weight=440)
        self.main_frame.rowconfigure(0, minsize=1000)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.dict_frames = {}
        self.content_frames = (StudentProfileTab, StudentCoursesTab, StudentScheduleTab)

        for CF in self.content_frames:
            frame = CF(self.main_frame, self.main, self)
            self.dict_frames[CF.__name__] = frame
            frame.grid(row=0, column=1, sticky=tk.NSEW)

        # Sidebar Frame
        self.sidebar = tk.Frame(self.main_frame, width=140, height=1000)
        self.sidebar.grid(row=0, column=0, sticky=tk.NSEW)
        self.sidebar.pack_propagate(False)

        # Canvas for sidebar
        self.sidebar_canvas = tk.Canvas(self.sidebar, bg="#8D0404")
        self.sidebar_canvas.pack(fill=tk.BOTH, expand=True)

        # Student Full Name
        self.sidebar_canvas.create_text(20, 20, text=self.student_session["stu_full_name"], font=LEXEND_DECA_10, fill="#FFFFFF", anchor=tk.NW)

        # Profile Button Tab
        self.profile_btn = tk.Button(self.sidebar, text="Profile", command=lambda: self.display_frame("StudentProfileTab"))
        self.profile_btn.place(x=2, y=100)

        # Course Button Tab
        self.course_btn = tk.Button(self.sidebar, text="Courses", command=lambda: self.display_frame("StudentCoursesTab"))
        self.course_btn.place(x=2, y=200)

        # Schedule Button Tab
        self.sched_btn = tk.Button(self.sidebar, text="Schedule", command=lambda: self.display_frame("StudentScheduleTab"))
        self.sched_btn.place(x=2, y=350)

        # Logout
        self.logout_btn = tk.Button(self.sidebar, text="Logout", command=self.log_out)
        self.logout_btn.place(x=2, y=500)

        self.display_frame("StudentProfileTab")


    def display_frame(self, frame_name):
        frame = self.dict_frames[frame_name]
        frame.lift()

    def on_close(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to close the application? You will be logged out.")

        if confirm:
            self.main.clear_user_session("Student")  # Log out the user
            self.destroy()  # Close the dashboard
            self.main.destroy()  # Stop the entire application

    def log_out(self):
        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")

        if confirm:
            self.main.clear_user_session("Student") # Clear the admin session
            self.destroy() # Close the dashboard
            self.main.deiconify() # Display the home screen