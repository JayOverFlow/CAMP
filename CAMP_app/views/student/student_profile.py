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

        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        IMAGES_DIR = BASE_DIR / "static/images"

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
        ]
        # Student pfp directory
        PFP_DIR = BASE_DIR / "static/student_pfps"

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
        self.full_name.place(x=300, y=100)

        self.widgets = {}
        self.edit_mode = False
        self.image_data = self.student_session.get("profile_picture", None)
        self.create_profile_view()

        # Student pfp
        pfp_path = self.get_pfp_path(PFP_DIR, self.student_session["stu_id"])  # Get student pfp
        self.pfp = self.make_pfp_circle(pfp_path)
        # self.header_frame_canvas.create_image(50, 20, anchor=tk.NW, image=self.pfp)
        self.pfp_label = tk.Label(self, image=self.pfp, bg="#FFFFFF", borderwidth=0)
        self.pfp_label.image = self.pfp
        self.pfp_label.place(x=50, y=20)  # Adjust x, y for centering and floating effect

        # Create an upload button to trigger image upload
        self.upload_button = ttk.Button(self, text="Upload", command=lambda: self.upload_pfp(PFP_DIR))
        self.upload_button.place(x=170, y=90)

        self.update_profile_btn = ctk.CTkButton(
            self, text="UPDATE PROFILE", command=self.toggle_edit_mode,
            corner_radius=5, fg_color="#D92424", text_color="white"
        )
        self.update_profile_btn.place(x=700, y=550)

    def create_profile_view(self):

        # Profile Information Section Title
        ttk.Label(self, text="My Information", font=("Arial", 12, "bold"), foreground="#8D0404").place(x=45, y=175)

        for i, (label_text, key) in enumerate(self.fields):
            x_offset, y_offset = (50, 200 + (i % 7) * 40) if i < 7 else (400, 200 + ((i - 7) % 7) * 40)
            ttk.Label(self, text=f"{label_text}:", font=("Arial", 10, "bold"), foreground="#8D0404").place(x=x_offset,
                                                                                                           y=y_offset)
            value = self.student_session.get(key, 'N/A')
            self.widgets[key] = ttk.Label(self, text=value, font=("Arial", 10))
            self.widgets[key].place(x=x_offset + 150, y=y_offset)

    def toggle_edit_mode(self):
        if not self.edit_mode:
            self.enable_edit_mode()
        else:
            self.save_updates()

    def enable_edit_mode(self):
        for key, widget in self.widgets.items():
            widget.destroy()
        self.widgets.clear()

        for i, (label_text, key) in enumerate(self.fields):
            x_offset, y_offset = (50, 200 + (i % 7) * 40) if i < 7 else (400, 200 + ((i - 7) % 7) * 40)
            ttk.Label(self, text=f"{label_text}:", font=("Arial", 10, "bold"), foreground="#8D0404").place(x=x_offset,
                                                                                                           y=y_offset)
            if key == "stu_sex":
                gender_options = ["Male", "Female"]
                combobox = ttk.Combobox(self, values=gender_options, state="readonly")
                combobox.set(self.student_session.get(key, "Male"))
                combobox.place(x=x_offset + 150, y=y_offset)
                self.widgets[key] = combobox
            else:
                entry = tk.Entry(self)
                entry.insert(0, self.student_session.get(key, ''))
                entry.place(x=x_offset + 150, y=y_offset)
                self.widgets[key] = entry

        self.update_profile_btn.configure(text="Save")
        self.edit_mode = True

    def save_updates(self):
        updated_data = {
            key: (widget.get() if isinstance(widget, (tk.Entry, ttk.Combobox)) else self.student_session.get(key, ''))
            for key, widget in self.widgets.items()}
        self.student_session.update(updated_data)
        self.widgets.clear()
        self.create_profile_view()
        self.update_profile_btn.configure(text="UPDATE PROFILE")
        self.main.student_model.update_student_info(updated_data, self.student_session.get("stu_id"))
        self.edit_mode = False

    def get_pfp_path(self, PFP_DIR, stu_id):
        pfp_path = PFP_DIR / f"student_{stu_id}.png"
        default_pfp = PFP_DIR / "student_default.png"
        return pfp_path if pfp_path.exists() else default_pfp # Checks if the file actually exists in the directory, otherwise it will return None

    def make_pfp_circle(self, pfp_path):
        size = (150, 150)
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

    def upload_pfp(self, PFP_DIR):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
        )

        if not file_path:
            return  # User canceled file selection

        # Validate file extension
        valid_extensions = (".jpg", ".jpeg", ".png")
        if not file_path.lower().endswith(valid_extensions):
            messagebox.showerror("Invalid File", "Please upload a valid image file (.jpg, .jpeg, .png).")
            return

        try:
            # Define new filename and path
            new_filename = f"student_{self.student_session['stu_id']}.png"
            new_filepath = PFP_DIR / new_filename

            # Convert and save image as PNG
            img = Image.open(file_path).convert("RGBA")
            img.save(new_filepath, "PNG")

            # Update database with new profile picture filename
            self.main.student_model.update_student_pfp(self.student_session["stu_id"], new_filename)

            # Reload the updated image
            self.pfp = self.make_pfp_circle(new_filepath)
            self.pfp_label.configure(image=self.pfp)
            self.pfp_label.image = self.pfp  # Keep reference to prevent garbage collection

            messagebox.showinfo("Success", "Profile picture updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload profile picture: {e}")

    def save_updates(self):
        updated_data = {}

        for key, widget in self.widgets.items():
            if isinstance(widget, tk.Entry):
                value = widget.get()
            elif isinstance(widget, ttk.Combobox):  # Extract selected value from Combobox
                value = widget.get()
            else:
                continue

            self.student_session[key] = value
            updated_data[key] = value
            widget.destroy()

        self.widgets.clear()

        self.create_profile_view()

        self.update_profile_btn.configure(text="UPDATE PROFILE")

        self.main.student_model.update_student_info(updated_data, self.student_session.get("stu_id"))

        self.edit_mode = False





