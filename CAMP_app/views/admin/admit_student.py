import tkinter as tk
import customtkinter as ctk
import ctypes
from tkinter import ttk, messagebox, font
from tkcalendar import DateEntry
from pathlib import Path



class AdmitStudent(tk.Toplevel):
    def __init__(self, main, parent): # parent is the AdminDashboard
        super().__init__(parent)
        self.main = main
        self.admin_dashboard = parent

        self.title("Admit Student")
        self.geometry("800x495+240+70")
        self.resizable(False, False)
        BASE_DIR = Path(__file__).resolve().parent.parent

        IMAGES_DIR = BASE_DIR / "static/images"

        FONTS_DIR = BASE_DIR / "static/fonts"
        FONT_PATH = FONTS_DIR / "LexendDeca-Bold.ttf"
        # Font sizes
        LEXEND_DECA_8 = font.Font(family="Lexend Deca", size=8)
        LEXEND_DECA_12 = font.Font(family="Lexend Deca", size=12)
        LEXEND_DECA_14 = font.Font(family="Lexend Deca", size=14)
        LEXEND_DECA_16 = font.Font(family="Lexend Deca", size=16)
        LEXEND_DECA_18 = font.Font(family="Lexend Deca", size=18)
        LEXEND_DECA_20 = font.Font(family="Lexend Deca", size=20)
        try:
            ctypes.windll.gdi32.AddFontResourceW(str(FONT_PATH))
        except Exception as e:
            print(f"Error loading font: {e}")

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.fields_max_length = {
            "First Name": 50,
            "Middle Name": 20,
            "Last Name": 50,
            "Username": 50,
            "Password": 10,
            "Phone": 11,
            "LRN": 12,
            "Citizenship": 30,
            "Email": 50,
            "Religion": 70,
            "Address": 150,
        }

        # First name
        self.first_name_lbl = ctk.CTkLabel(self.main_frame, text="First Name", font=("Lexand Deca", 11, "bold"), text_color="#8D0404", anchor="e", height=20)
        self.first_name_lbl.place(x=50, y=18)
        self.first_name = ctk.CTkEntry(self.main_frame, width=320, height=32, corner_radius=0, border_width=1)
        self.first_name.place(x=50, y=35)

        # Middle name
        self.middle_name_lbl = ctk.CTkLabel(self.main_frame, text="Middle Name", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.middle_name_lbl.place(x=50, y=71)
        self.middle_name = ctk.CTkEntry(self.main_frame, width=320, height=32, corner_radius=0, border_width=1)
        self.middle_name.place(x=50, y=93)

        # Last name
        self.last_name_lbl = ctk.CTkLabel(self.main_frame, text="Last Name", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.last_name_lbl.place(x=50, y=128)
        self.last_name = ctk.CTkEntry(self.main_frame, width=320, height=32, corner_radius=0, border_width=1)
        self.last_name.place(x=50, y=148)

        # Sex
        self.sex_lbl = ctk.CTkLabel(self.main_frame, text="Sex", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.sex_lbl.place(x=50, y=185)
        self.sex_var = tk.StringVar(value="Select")  # Set placeholder value
        self.sex_dropdown = ttk.Combobox(self.main_frame, textvariable=self.sex_var, values=["Female", "Male"], state="readonly" , width=50)
        self.sex_dropdown.place(x=50, y=208)

        # Address
        self.address_lbl = ctk.CTkLabel(self.main_frame, text="Address", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.address_lbl.place(x=50, y=252)
        self.address = ctk.CTkTextbox(self.main_frame, height=90, width=320, corner_radius=0, border_width=1)
        self.address.place(x=50, y=272)

        # Citizenship
        self.citizenship_lbl = ctk.CTkLabel(self.main_frame, text="Citizenship", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.citizenship_lbl.place(x=420, y=15)
        self.citizenship = ctk.CTkEntry(self.main_frame, width=320, height=32, corner_radius=0, border_width=1)
        self.citizenship.place(x=420, y=35)

        # LRN
        self.lrn_lbl = ctk.CTkLabel(self.main_frame, text="LRN", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.lrn_lbl.place(x=420, y=71)
        self.lrn = ctk.CTkEntry(self.main_frame, width=320, height=32, corner_radius=0, border_width=1)
        self.lrn.place(x=420, y=93)

        # Phone
        self.phone_lbl = ctk.CTkLabel(self.main_frame, text="Phone", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.phone_lbl.place(x=420, y=128)
        self.phone = ctk.CTkEntry(self.main_frame, width=320, height=32, corner_radius=0, border_width=1)
        self.phone.place(x=420, y=148)

        # Email
        self.email_lbl = ctk.CTkLabel(self.main_frame, text="Email", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.email_lbl.place(x=420, y=185)
        self.email = ctk.CTkEntry(self.main_frame, width=320, height=32, corner_radius=0, border_width=1)
        self.email.place(x=420, y=208)

        # Birthdate
        self.birthdate_lbl = ctk.CTkLabel(self.main_frame, text="Birthdate", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.birthdate_lbl.place(x=420, y=252)
        self.birthdate = DateEntry(self.main_frame, width=22, height=40, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        self.birthdate.place(x=420, y=272)
        self.birthdate.delete(0, tk.END)

        # Religion
        self.religion_lbl = ctk.CTkLabel(self.main_frame, text="Religion", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.religion_lbl.place(x=590, y=252)
        self.religion = ctk.CTkEntry(self.main_frame, width=150, height=32, corner_radius=0, border_width=1)
        self.religion.place(x=590, y=272)

        # Username
        self.username_lbl = ctk.CTkLabel(self.main_frame, text="Username", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.username_lbl.place(x=420, y=309)
        self.username = ctk.CTkEntry(self.main_frame, width=150, height=32, corner_radius=0, border_width=1)
        self.username.place(x=420, y=330)

        # Password
        self.password_lbl = ctk.CTkLabel(self.main_frame, text="Password", font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.password_lbl.place(x=590, y=309)
        self.password = ctk.CTkEntry(self.main_frame, show="*", width=150, height=32, corner_radius=0, border_width=1)
        self.password.place(x=590, y=330)

        # Confirm Password
        self.confirm_password_lbl = ctk.CTkLabel(self.main_frame, text="Confirm Password",font=("Lexand Deca", 11, "bold"), text_color="#8D0404")
        self.confirm_password_lbl.place(x=590, y=370)
        self.confirm_password = ctk.CTkEntry(self.main_frame, show="*", corner_radius=0, border_width=1, width=150, height=32)
        self.confirm_password.place(x=590, y=390)

        self.admit_btn = ctk.CTkButton(self.main_frame, text="Enroll Student", command=self.validate_fields,fg_color="#8D0404", hover_color="#8D0404", corner_radius=10, width=150)
        self.admit_btn.place(x=590, y=440)

        self.close_btn = ctk.CTkButton(self.main_frame, text="Close", command=self.close, fg_color="#8D0404", hover_color="#8D0404", corner_radius=10)
        self.close_btn.place(x=430, y=440)

    def validate_fields(self):
        middle_name = None

        errors = []

        # For First Name
        first_name = self.first_name.get().strip()
        if len(first_name) > self.fields_max_length["First Name"]:
            errors.append(f"First Name exceeds {self.fields_max_length['First Name']} characters.")
        elif not first_name:
            errors.append("First Name cannot be empty.")

        # For Last Name
        last_name = self.last_name.get().strip()
        if len(last_name) > self.fields_max_length["Last Name"]:
            errors.append(f"Last Name exceeds {self.fields_max_length['Last Name']} characters.")
        elif not last_name:
            errors.append("Last Name cannot be empty.")

        # For Sex Field
        sex = self.sex_var.get()
        if sex == "Select":
            errors.append("Sex field is required.")

        # For Address
        address = self.address.get("1.0", "end-1c")
        if len(address) > self.fields_max_length["Address"]:
            errors.append(f"Address exceeds {self.fields_max_length['Address']} characters.")
        elif len(address) == 0:
            errors.append("Address cannot be empty.")

        # For Citizenship
        citizenship = self.citizenship.get().strip()
        if len(citizenship) > self.fields_max_length["Citizenship"]:
            errors.append(f"Citizenship exceeds {self.fields_max_length['Citizenship']} characters.")
        elif not citizenship:
            errors.append("Citizenship cannot be empty.")

        # For LRN
        lrn = self.lrn.get().strip()
        if len(lrn) > self.fields_max_length["LRN"] or len(lrn) < 12 :
            errors.append("LRN must be 12 digits.")
        elif not lrn:
            errors.append("LRN cannot be empty.")
        elif not lrn.isdigit():
            errors.append("LRN must be a pure digits.")

        # For Phone
        phone = self.phone.get().strip()
        if phone:
            if not phone.isdigit():
                errors.append("Phone must contain only digits.")
            elif len(phone) != 11:
                errors.append("Phone must be exactly 11 digits.")

        # For Email
        email = self.email.get().strip()
        email_domains = ("@email.com", "@gmail.com", "@yahoo.com", "@mail.com")
        if len(email) > self.fields_max_length["Email"]:
            errors.append(f"Email exceeds {self.fields_max_length['Email']} characters.")
        elif not email:
            errors.append("Email cannot be empty.")
        elif not any(email.endswith(domain) for domain in email_domains):
            errors.append(f"Email must end with {', '.join(email_domains)}")

        # For Birthdate (required)
        birth_date = self.birthdate.get().strip()
        if not birth_date:
            errors.append("Birthdate is required.")

        # For Religion
        religion = self.religion.get().strip()
        if len(religion) > self.fields_max_length["Religion"]:
            errors.append(f"Religion exceeds {self.fields_max_length['Religion']} characters.")
        elif not religion:
            errors.append("Religion cannot be empty.")

        # For Username
        username = self.username.get().strip()
        if len(username) > self.fields_max_length["Username"]:
            errors.append(f"Username exceeds {self.fields_max_length['Username']} characters.")
        elif not username:
            errors.append("Username cannot be empty.")
        elif self.main.admin_model.is_student_username_taken(self.username.get().strip().strip()):
            errors.append("Username is already taken.") # NOTE: Remove comment

        # For Password
        password = self.password.get().strip()
        confirm_password = self.confirm_password.get().strip()
        if len(password) > self.fields_max_length["Password"]:
            errors.append(f"Password exceeds {self.fields_max_length['Password']} characters.")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        elif not password:
            errors.append("Password cannot be empty.")
        elif password != confirm_password:
            errors.append("Passwords do not match.")

        # If errors exist, show messagebox
        if errors:
            messagebox.showerror("Input Error", "\n".join(errors))
        else:
            self.enroll_student(first_name, middle_name, last_name, birth_date, sex, username, password, phone, lrn, citizenship, email, religion, address)
            messagebox.showinfo("Success", "Student enrolled successfully!")
            self.close()

    def enroll_student(self, first_name, middle_name, last_name,birth_date, sex, username, password, phone_number, lrn, citizenship, email, religion, address):
        self.main.admin_model.admit_student(first_name, middle_name, last_name, birth_date, sex, username, password, phone_number, lrn, citizenship, email, religion, address)
        self.admin_dashboard.display_students() # Refresh the admin dashboard student list

    def close(self):
        self.destroy()

# Directly run the class for UI viewing
if __name__ == "__main__":
    import sys
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    test_app = AdmitStudent(None, None)  # Create the Toplevel window
    test_app.mainloop()
    sys.exit()