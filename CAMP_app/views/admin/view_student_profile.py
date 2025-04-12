import ctypes
import re
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox, font, filedialog

from PIL import Image, ImageTk, ImageDraw


class ViewStudentProfile(tk.Toplevel):
    def __init__(self, admin_dashboard, parent, main, student_data): # parent is the AdminDashboard
        super().__init__(parent)
        self.main = main
        self.admin_dashboard = admin_dashboard
        self.student_data = student_data
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Student Profile")
        self.geometry("700x500+285+60")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

        # Get the base directory of the project
        BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Moves up two levels from "views"

        # Images directory
        IMAGES_DIR = BASE_DIR / "static/images"

        # Fonts directory
        FONTS_DIR = BASE_DIR / "static/fonts"
        FONT_PATH = FONTS_DIR / "LexendDeca-Bold.ttf"
        # Font sizes
        LEXEND_DECA_7 = font.Font(family="Lexend Deca", size=7)
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

        # Student pfp directory
        PFP_DIR = BASE_DIR / "static/student_pfps"

        # Main Frame
        self.main_frame = tk.Frame(self, bg="#FFFFFF")
        # self.main_frame.rowconfigure(0, minsize=25)
        # self.main_frame.rowconfigure(1, minsize=25)
        # self.main_frame.columnconfigure(0, minsize=50)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.pack_propagate(False)

        self.main_frame_canvas = tk.Canvas(self.main_frame, bg="#000000")
        self.main_frame_canvas.pack(fill=tk.BOTH, expand=True)


        self.style = ttk.Style(self.main_frame)
        # self.style.theme_use("clam")
        self.style.configure("TEntry", bg="#FFFFFF", fg="#8D0404", font=LEXEND_DECA_10)
        self.style.configure("TName", fg="#8D0404", font=LEXEND_DECA_16)
        self.style.configure("Tid", fg="#8D0404", font=LEXEND_DECA_10)
        self.style.configure("TButton",font=LEXEND_DECA_7, fg="#FFFFFF", bg="#8D0404")
        self.style.map("TButton", foreground=[("active","#FFFFFF"),("pressed","#FFFFFF")], background=[("active", "#8D0404"), ("pressed","#8D0404")])

        # Header Frame
        self.header_frame = tk.Frame(self.main_frame, width=700, height=150)
        self.header_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.header_frame.pack_propagate(False)

        # Canvas for header_frame
        self.header_frame_canvas = tk.Canvas(self.header_frame, bg="#FFFFFF")
        self.header_frame_canvas.pack(fill=tk.BOTH, expand=True)

        # Student pfp
        pfp_path = self.get_pfp_path(PFP_DIR, self.student_data["stu_id"])  # Get student pfp
        self.pfp = self.make_pfp_circle(pfp_path)
        # self.header_frame_canvas.create_image(50, 20, anchor=tk.NW, image=self.pfp)
        self.pfp_label = tk.Label(self, image=self.pfp, bg="#FFFFFF", borderwidth=0)
        self.pfp_label.image = self.pfp
        self.pfp_label.place(x=50, y=20)  # Adjust x, y for centering and floating effect


        # Full Name
        self.header_frame_canvas.create_text(210, 100, text=student_data["stu_full_name"], fill="#8D0404", font=LEXEND_DECA_16, anchor="w")

        # ID
        self.header_frame_canvas.create_text(235, 120, text=f"AU{student_data["stu_id"]}", fill="#8D0404", font=LEXEND_DECA_10)

        # Expel Button
        self.expel_btn = ttk.Button(self.header_frame, text="Expel Student", command=self.expel_student)
        self.header_frame_canvas.create_window(610, 120, window=self.expel_btn)

        # Entries Frame
        self.entries_frame = tk.Frame(self.main_frame, width=700, height=400, bg="#FFFFFF")
        # Rows
        self.entries_frame.rowconfigure(0, minsize=23)
        self.entries_frame.rowconfigure(1, minsize=45)
        self.entries_frame.rowconfigure(2, minsize=45)
        self.entries_frame.rowconfigure(3, minsize=45)
        self.entries_frame.rowconfigure(4, minsize=45)
        self.entries_frame.rowconfigure(5, minsize=45)
        self.entries_frame.rowconfigure(6, minsize=45)
        self.entries_frame.rowconfigure(7, minsize=45)
        # Columns
        self.entries_frame.columnconfigure(0, minsize=165)
        self.entries_frame.columnconfigure(1, minsize=165)
        self.entries_frame.columnconfigure(2, minsize=165)
        self.entries_frame.columnconfigure(3, minsize=165)
        self.entries_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.entries_frame.grid_propagate(False)

        # Canvas for entries_frame
        self.entries_frame_canvas = tk.Canvas(self.entries_frame, bg="#FFFFFF")
        self.entries_frame_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Username
        self.entries_frame_canvas.create_text(80, 43, text="Username: ", font=LEXEND_DECA_10)
        self.username = ttk.Entry(self.entries_frame, width=25)
        self.username.grid(row=1, column=1, ipady=4)

        # Password
        self.entries_frame_canvas.create_text(79, 88, text="Password: ", font=LEXEND_DECA_10)
        self.password= ttk.Entry(self.entries_frame, width=25)
        self.password.grid(row=2, column=1, ipady=4)

        # Birthdate
        self.entries_frame_canvas.create_text(80, 133, text="Birthdate: ", font=LEXEND_DECA_10)
        self.birthdate = ttk.Entry(self.entries_frame, width=25)
        self.birthdate.grid(row=3, column=1, ipady=4)

        # Phone
        self.entries_frame_canvas.create_text(70, 178, text="Phone: ", font=LEXEND_DECA_10)
        self.phone = ttk.Entry(self.entries_frame, width=25)
        self.phone.grid(row=4, column=1, ipady=4)

        # Email Address
        self.entries_frame_canvas.create_text(95, 223, text="Email Address: ", font=LEXEND_DECA_10)
        self.email = ttk.Entry(self.entries_frame, width=25)
        self.email.grid(row=5, column=1, ipady=4)

        # Address
        self.entries_frame_canvas.create_text(73, 268, text="Address: ", font=LEXEND_DECA_10)
        self.address = ttk.Entry(self.entries_frame, width=81)
        self.address.grid(row=6, column=1, columnspan=3, ipady=4)

        # LRN
        self.entries_frame_canvas.create_text(385, 43, text="LRN: ", font=LEXEND_DECA_10)
        self.lrn = ttk.Entry(self.entries_frame, width=25)
        self.lrn.grid(row=1, column=3, ipady=4)

        # Citizenship
        self.entries_frame_canvas.create_text(405, 88, text="Citizenship: ", font=LEXEND_DECA_10)
        self.citizenship = ttk.Entry(self.entries_frame, width=25)
        self.citizenship.grid(row=2, column=3, ipady=4)

        # Religion
        self.entries_frame_canvas.create_text(395, 133, text="Religion: ", font=LEXEND_DECA_10)
        self.religion = ttk.Entry(self.entries_frame, width=25)
        self.religion.grid(row=3, column=3, ipady=4)

        # Sex
        self.entries_frame_canvas.create_text(380, 178, text="Sex: ", font=LEXEND_DECA_10)
        # self.sex = ttk.Entry(self.entries_frame)
        # self.sex.grid(row=3, column=3)

        self.sex = ttk.Combobox(self.entries_frame, values=["Female", "Male"], width=24)
        self.sex.grid(row=4, column=3, ipady=4)

        self.load_student_data()

        # Edit Button
        self.is_edit_mode = False
        self.edit_btn = ttk.Button(self.entries_frame, text="Update Profile", command=self.toggle_edit_btn)
        self.entries_frame_canvas.create_window(618, 315, window=self.edit_btn)

        # Upload button
        self.upload_btn = tk.Button(self, text="📷", command=lambda: self.upload_pfp(PFP_DIR),font=LEXEND_DECA_10)
        self.upload_btn.place(x=165, y=110)  # Adjust position relative to pfp_label

        self.pfp_label.lift()  # Moves it above other widgets
        self.upload_btn.lift()

        self.load_student_data()

        # # Close Button
        # self.close_btn = tk.Button(self.entries_frame, text="Close", command=self.on_close)
        # self.close_btn.grid(row=6, column=2)



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
            new_filename = f"student_{self.student_data['stu_id']}.png"
            new_filepath = PFP_DIR / new_filename

            # Convert and save image as PNG
            img = Image.open(file_path).convert("RGBA")
            img.save(new_filepath, "PNG")

            # Update database with new profile picture filename
            self.main.admin_model.update_student_pfp(self.student_data["stu_id"], new_filename)

            # Reload the updated image
            self.pfp = self.make_pfp_circle(new_filepath)
            self.header_frame_canvas.create_image(48, 48, anchor=tk.NW, image=self.pfp)
            self.header_frame_canvas.image = self.pfp  # Keep reference to prevent garbage collection

            messagebox.showinfo("Success", "Profile picture updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload profile picture: {e}")

    def load_student_data(self):
        self.entries = {
            "stu_username": self.username,
            "stu_password": self.password,
            "stu_birthdate": self.birthdate,
            "stu_phone_number": self.phone,
            "stu_emailadd": self.email,
            "stu_address": self.address,
            "stu_lrn": self.lrn,
            "stu_citizenship": self.citizenship,
            "stu_religion": self.religion,
            "stu_sex": self.sex
        }

        # Insert student's data into entries and disable after
        for key, entry in self.entries.items():
            if entry == "self.sex":
                entry.set(self.student_data[key])
                entry.state(tk.DISABLED)
            entry.insert(0, self.student_data[key])
            entry.configure(state=tk.DISABLED)

    def expel_student(self):
        confirm = messagebox.askyesno("Expel Student?", f"Are you sure you want to expel {self.student_data["stu_full_name"]}?")
        if confirm:
            self.main.admin_model.expel_student(self.student_data["stu_id"])
            self.admin_dashboard.display_students()
            search_bar = self.admin_dashboard.search_entry
            if search_bar.get():
                search_bar.delete("0", tk.END)
                search_bar.focus_set()
            self.destroy()
            messagebox.showinfo("Expel Student", f"{self.student_data["stu_full_name"]} has been expelled.")

    def toggle_edit_btn(self):
        if not self.is_edit_mode:
            self.is_edit_mode = True
            self.edit_btn.config(text="Save")
            for entry in self.entries.values():
                entry.config(state=tk.NORMAL)

        else:  # Save
            updated_data = self.get_entries_values()

            # Validate inputs before saving
            if self.validate_update(self.entries):
                self.is_edit_mode = False
                self.edit_btn.config(text="Update Profile")
                self.save_changes(updated_data)

                # Disable entries
                for entry in self.entries.values():
                    entry.config(state=tk.DISABLED)

                messagebox.showinfo("Student Updated", "Student Profile Updated")

    def get_entries_values(self):
        updated_data = {key: entry.get() for key, entry in self.entries.items()}
        return updated_data

    def validate_update(self, entries):
        errors = []

        # Define max lengths for fields
        fields_max_length = {
            "Username": 50,
            "Password": 10,
            "Birthdate": 8,  # YY-MM-DD format
            "Phone": 11,
            "Email": 50,
            "Address": 150,
            "LRN": 12,
            "Citizenship": 30,
            "Religion": 70,
            "Sex": 6,  # "Female" or "Male"
        }

        # Define valid email domains
        valid_email_domains = ["@email.com", "@gmail.com", "@yahoo.com", "@mail.com"]

        # Validation checks
        for field, entry in entries.items():
            value = entry.get().strip()

            # Check if the field is empty
            if not value:
                errors.append(f"{field.replace('stu_', '').capitalize()} cannot be empty.")
                continue  # Skip further checks for empty fields

            # Check max length
            if field in fields_max_length and len(value) > fields_max_length[field]:
                errors.append(
                    f"{field.replace('stu_', '').capitalize()} exceeds max length ({fields_max_length[field]}).")

            # Birthdate format validation
            if field == "stu_birthdate":
                if not re.fullmatch(r"\d{2}-\d{2}-\d{2}|\d{4}-\d{2}-\d{2}", value):
                    errors.append("Birthdate must be in YY-MM-DD or YYYY-MM-DD format.")

            # Ensure phone and LRN contain only numbers
            if field in ["stu_phone_number", "stu_lrn"]:
                if not value.isdigit():
                    errors.append(f"{field.replace('stu_', '').capitalize()} must contain only numbers.")

            # Ensure stu_phone_number is exactly 11 digits
            if field == "stu_phone_number":
                if not (value.isdigit() and len(value) == fields_max_length["Phone"]):
                    errors.append("Phone number must be exactly 11 digits.")

            # Ensure stu_lrn is exactly 12 digits
            if field == "stu_lrn":
                if not (value.isdigit() and len(value) == fields_max_length["LRN"]):
                    errors.append("LRN must be exactly 12 digits.")

            # Validate email format
            if field == "stu_emailadd":
                if not any(value.endswith(domain) for domain in valid_email_domains):
                    errors.append("Email must end with @email.com, @gmail.com, @yahoo.com, or @mail.com.")

            # Validate sex field
            if field == "stu_sex" and value not in ["Female", "Male"]:
                errors.append("Sex must be either 'Female' or 'Male'.")

        # Show error messages if there are any
        if errors:
            messagebox.showerror("Invalid Input", "\n".join(errors))
            return None  # Validation failed
        return True  # Validation passed

    def save_changes(self, updated_data):
        self.main.admin_model.update_student_profile(
            self.student_data["stu_id"],
            updated_data["stu_username"],
            updated_data["stu_password"],
            updated_data["stu_birthdate"],
            updated_data["stu_phone_number"],
            updated_data["stu_emailadd"],
            updated_data["stu_address"],
            updated_data["stu_lrn"],
            updated_data["stu_citizenship"],
            updated_data["stu_religion"],
            updated_data["stu_sex"]

        )

    def on_close(self):
        if self.is_edit_mode:
            response = messagebox.askyesno("Unsaved Changes", "Do you want to save your changes before closing?")
            if response:
                updated_data = self.get_entries_values()
                if self.validate_update(self.entries):
                    self.save_changes(updated_data)
                    messagebox.showinfo("Saved", "Changes have been saved.")
                    self.destroy()
        self.destroy()






