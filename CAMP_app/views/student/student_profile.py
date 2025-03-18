import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import customtkinter as ctk
from pathlib import Path

from  PIL import ImageTk, Image, ImageDraw

class StudentProfileTab(tk.Frame):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing
        self.student_session = student_landing.student_session

        self.fields = [
            ("Full Name", "stu_full_name"),
            ("First Name", "stu_first_name"),
            ("Middle Name", "stu_middle_name"),
            ("Last Name", "stu_last_name"),
            ("Birth Date", "stu_birthdate"),
            ("Gender", "stu_sex"),
            ("Cellphone Number", "stu_phone_number"),
            ("Email Address", "stu_emailadd"),
            ("Address", "stu_address"),
            ("Username", "stu_username"),
            ("Password", "stu_password"),
            ("LRN Number", "stu_lrn"),
            ("Citizenship", "stu_citizenship"),
            ("Religion", "stu_religion"),
            ("Profile Image", "profile_picture"),
        ]

        self.widgets = {}
        self.edit_mode = False
        self.image_data = self.student_session.get("profile_picture", None)
        self.upload_btn = None

        self.create_profile_view()

        self.update_profile_btn = ctk.CTkButton(self, text="Update Profile", command=self.toggle_edit_mode, corner_radius=7, fg_color="#8D0404", text_color="white")
        self.update_profile_btn.place(x=700, y=550)

    def create_profile_view(self):
        self.display_image()

        for i, (label_text, key) in enumerate(self.fields):
            ttk.Label(self, text=f"{label_text}:").place(x=20 + (i % 2) * 280, y=150 + (i // 2) * 50)

            value = self.student_session.get(key, '')
            if key == "profile_picture" and value != '':
                value = "Image Uploaded"

            label = ttk.Label(self, text=value)
            label.place(x=150 + (i % 2) * 280, y=150 + (i // 2) * 50)
            self.widgets[key] = label

    def display_image(self):
        if self.image_data:
            image = Image.open(self.image_data)
        else:
            image = Image.new('RGB', (100, 100), 'gray')

        image = image.resize((100, 100))
        self.photo = ImageTk.PhotoImage(image)

        self.image_label = ttk.Label(self, image=self.photo)
        self.image_label.place(x=20, y=30)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_data = file_path
            self.display_image()

    def toggle_edit_mode(self):
        if not self.edit_mode:
            self.enable_edit_mode()
        else:
            self.save_updates()

    def enable_edit_mode(self):
        for i, (label_text, key) in enumerate(self.fields):
            widget = self.widgets[key]
            widget.destroy()

            if key == "profile_picture":
                if not self.upload_btn:  # Ensure the button is created once
                    self.upload_btn = ctk.CTkButton(self, text="Upload Image", command=self.upload_image, corner_radius=7)
                self.upload_btn.place(x=150 + (i % 2) * 280, y=150 + (i // 2) * 50)
            else:
                entry = tk.Entry(self)
                entry.insert(0, self.student_session.get(key, ''))
                entry.place(x=150 + (i % 2) * 280, y=150 + (i // 2) * 50)
                self.widgets[key] = entry

        self.update_profile_btn.configure(text="Save")
        self.edit_mode = True

    def save_updates(self):
        updated_data = {}

        for key, widget in self.widgets.items():
            # Only extract data from Entry widgets
            if isinstance(widget, tk.Entry):
                value = widget.get()
                self.student_session[key] = value
                updated_data[key] = value
                widget.destroy()  # Clean up Entry widget

            else:
                value = self.student_session.get(key, '')
                updated_data[key] = value

        self.widgets.clear()

        # Recreate labels for display mode
        self.create_profile_view()

        # Update button text back to "Update Profile"
        self.update_profile_btn.configure(text="Update Profile")

        # Save updated data to the database
        self.main.student_model.update_student_info(updated_data, self.student_session.get("stu_id"))

        self.edit_mode = False




