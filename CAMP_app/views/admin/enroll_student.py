import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class EnrollStudent(tk.Toplevel):
    def __init__(self, main, parent): # parent is the AdminDashboard
        super().__init__(parent)
        self.main = main
        self.admin_dashboard = parent

        self.title("Enroll Student")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)

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
        self.first_name_lbl = tk.Label(self.main_frame, text="First Name")
        self.first_name_lbl.grid(row=0, column=0)
        self.first_name = tk.Entry(self.main_frame)
        self.first_name.grid(row=0, column=1)

        # Middle name
        self.middle_name_lbl = tk.Label(self.main_frame, text="Middle Name")
        self.middle_name_lbl.grid(row=1, column=0)
        self.middle_name = tk.Entry(self.main_frame)
        self.middle_name.grid(row=1, column=1)

        # Last name
        self.last_name_lbl = tk.Label(self.main_frame, text="Last Name")
        self.last_name_lbl.grid(row=2, column=0)
        self.last_name = tk.Entry(self.main_frame)
        self.last_name.grid(row=2, column=1)

        # Sex
        self.sex_lbl = tk.Label(self.main_frame, text="Sex")
        self.sex_lbl.grid(row=3, column=0)
        self.sex_var = tk.StringVar(value="Select")  # Set placeholder value
        self.sex_dropdown = ttk.Combobox(self.main_frame, textvariable=self.sex_var, values=["Female", "Male"], state="readonly")
        self.sex_dropdown.grid(row=3, column=1)

        # Address
        self.address_lbl = tk.Label(self.main_frame, text="Address")
        self.address_lbl.grid(row=4, column=0)
        self.address = tk.Text(self.main_frame, height=3, width=30)
        self.address.grid(row=4, column=1)

        # Citizenship
        self.citizenship_lbl = tk.Label(self.main_frame, text="Citizenship")
        self.citizenship_lbl.grid(row=0, column=2)
        self.citizenship = tk.Entry(self.main_frame)
        self.citizenship.grid(row=0, column=3)

        # LRN
        self.lrn_lbl = tk.Label(self.main_frame, text="LRN")
        self.lrn_lbl.grid(row=1, column=2)
        self.lrn = tk.Entry(self.main_frame)
        self.lrn.grid(row=1, column=3)

        # Phone
        self.phone_lbl = tk.Label(self.main_frame, text="Phone")
        self.phone_lbl.grid(row=2, column=2)
        self.phone = tk.Entry(self.main_frame)
        self.phone.grid(row=2, column=3)

        # Email
        self.email_lbl = tk.Label(self.main_frame, text="Email")
        self.email_lbl.grid(row=3, column=2)
        self.email = tk.Entry(self.main_frame)
        self.email.grid(row=3, column=3)

        # Birthdate
        self.birthdate_lbl = tk.Label(self.main_frame, text="Birthdate")
        self.birthdate_lbl.grid(row=4, column=2)
        self.birthdate = DateEntry(self.main_frame, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        self.birthdate.grid(row=4, column=3)
        self.birthdate.delete(0, tk.END)

        # Religion
        self.religion_lbl = tk.Label(self.main_frame, text="Religion")
        self.religion_lbl.grid(row=5, column=2)
        self.religion = tk.Entry(self.main_frame)
        self.religion.grid(row=5, column=3)

        # Username
        self.username_lbl = tk.Label(self.main_frame, text="Username")
        self.username_lbl.grid(row=6, column=2)
        self.username = tk.Entry(self.main_frame)
        self.username.grid(row=6, column=3)

        # Password
        self.password_lbl = tk.Label(self.main_frame, text="Password")
        self.password_lbl.grid(row=7, column=2)
        self.password = tk.Entry(self.main_frame, show="*")
        self.password.grid(row=7, column=3)

        # Confirm Password
        self.confirm_password_lbl = tk.Label(self.main_frame, text="Confirm Password")
        self.confirm_password_lbl.grid(row=7, column=2)
        self.confirm_password = tk.Entry(self.main_frame, show="*")
        self.confirm_password.grid(row=8, column=3)

        self.enroll_btn = tk.Button(self.main_frame, text="Enroll Student", command=self.validate_fields)
        self.enroll_btn.grid(row=4, column=4)

        self.close_btn = tk.Button(self.main_frame, text="Close", command=self.close)
        self.close_btn.grid(row=6, column=4)

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
        self.main.admin_model.enroll_student(first_name, middle_name, last_name,birth_date, sex, username, password, phone_number, lrn, citizenship, email, religion, address)
        self.admin_dashboard.display_students() # Refresh the admin dashboard student list

    def close(self):
        self.destroy()

# Directly run the class for UI viewing
if __name__ == "__main__":
    import sys
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    test_app = EnrollStudent(None, None)  # Create the Toplevel window
    test_app.mainloop()
    sys.exit()