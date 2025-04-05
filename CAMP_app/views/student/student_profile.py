import ctypes
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import customtkinter as ctk
from pathlib import Path
from PIL import ImageTk, Image, ImageDraw

class StudentProfileTab(tk.Frame):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing
        self.student_session = student_landing.student_session

        self.fields = [
            ("First Name", "stu_first_name"),
            ("Middle Name", "stu_middle_name"),
            ("Last Name", "stu_last_name"),
            ("Birth Date", "stu_birthdate"),
            ("Gender", "stu_sex"),
            ("Cellphone No.", "stu_phone_number"),
            ("Email Address", "stu_emailadd"),
            ("Address", "stu_address"),
            ("Username", "stu_username"),
            ("Password", "stu_password"),
            ("LRN", "stu_lrn"),
            ("Citizenship", "stu_citizenship"),
            ("Religion", "stu_religion"),
            ("Profile Image", "profile_picture"),
        ]
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

        self.full_name = ttk.Label(self, text=self.student_session["stu_full_name"])
        self.full_name.place(x=5, y=100)

        self.widgets = {}
        self.edit_mode = False
        self.image_data = self.student_session.get("profile_picture", None)

        self.create_profile_view()

        self.update_profile_btn = ctk.CTkButton(
            self, text="UPDATE PROFILE", command=self.toggle_edit_mode,
            corner_radius=7, fg_color="#8D0404", text_color="white"
        )
        self.update_profile_btn.place(x=700, y=550)

    def create_profile_view(self):
        self.display_image()

        # Updated fields (excluding profile image)
        display_fields = [f for f in self.fields if f[1] != "profile_picture"]

        for i, (label_text, key) in enumerate(display_fields):
            x_offset = 30 if i < 7 else 400
            y_offset = 150 + (i % 7) * 50

            ttk.Label(self, text=label_text + ":", font=("Arial", 10, "bold"), foreground="#8D0404").place(x=x_offset,
                                                                                                           y=y_offset)

            value = self.student_session.get(key, 'N/A')

            label = ttk.Label(self, text=value, font=("Arial", 10))
            label.place(x=x_offset + 150, y=y_offset)
            self.widgets[key] = label

    def display_image(self):
        if self.image_data:
            image = Image.open(self.image_data)
        else:
            image = Image.new('RGB', (150, 150), 'gray')

        # Resize and create a circular mask for the profile picture
        image = image.resize((120, 120), Image.Resampling.LANCZOS)
        mask = Image.new('L', (120, 120), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 120, 120), fill=255)

        circular_image = Image.new('RGBA', (120, 120))
        circular_image.paste(image, (0, 0), mask)

        self.photo = ImageTk.PhotoImage(circular_image)

        # Place the circular profile image
        self.image_label = ttk.Label(self, image=self.photo)
        self.image_label.place(x=40, y=20)

        # Try loading the upload icon or create a default one
        try:
            upload_icon = Image.open("upload_icon.png").resize((30, 30), Image.Resampling.LANCZOS)
        except FileNotFoundError:
            upload_icon = self.create_default_upload_icon()

        self.upload_icon_img = ImageTk.PhotoImage(upload_icon)
        upload_button = ttk.Button(self, image=self.upload_icon_img, command=self.upload_image)
        upload_button.place(x=170, y=90)  # Position beside the profile image

    def create_default_upload_icon(self):
        """Creates a default upload icon dynamically."""
        icon_size = (30, 30)
        icon = Image.new('RGBA', icon_size, (200, 200, 200, 0))

        return icon

    def toggle_edit_mode(self):
        if not self.edit_mode:
            self.enable_edit_mode()
        else:
            self.save_updates()

    def enable_edit_mode(self):
        for i, (label_text, key) in enumerate(self.fields):
            if key == "profile_picture":
                continue

            widget = self.widgets.get(key)
            if widget:
                widget.destroy()

            x_offset = 30 if i < 7 else 400
            y_offset = 150 + (i % 7) * 50

            entry = tk.Entry(self)
            entry.insert(0, self.student_session.get(key, ''))
            entry.place(x=x_offset + 150, y=y_offset)
            self.widgets[key] = entry

        self.update_profile_btn.configure(text="Save")
        self.edit_mode = True

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_data = file_path
            self.display_image()

    def save_updates(self):
        updated_data = {}

        for key, widget in self.widgets.items():
            if isinstance(widget, tk.Entry):
                value = widget.get()
                self.student_session[key] = value
                updated_data[key] = value
                widget.destroy()

        self.widgets.clear()

        self.create_profile_view()

        self.update_profile_btn.configure(text="UPDATE PROFILE")

        self.main.student_model.update_student_info(updated_data, self.student_session.get("stu_id"))

        self.edit_mode = False




