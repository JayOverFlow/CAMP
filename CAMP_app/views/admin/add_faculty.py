import tkinter as tk
from tkinter import ttk, messagebox
import re


class AddFaculty(tk.Toplevel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Add Faculty")
        self.geometry("800x600+220+20")
        self.resizable(False, False)

        # Main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas
        self.canvas = tk.Canvas(self.main_frame, bg="#D9D9D9")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Header
        self.canvas.create_text(50, 50,
                                text="ADD FACULTY",
                                font=("Arial", 18, "bold"),
                                fill="#8D0404",
                                anchor="w")

        # Fields Frame
        self.fields_frame = tk.Frame(self.main_frame, width=700, height=350, bg="#FBFBF9")
        self.fields_frame.place(x=50, y=100)
        self.fields_frame.pack_propagate(False)
        self.fields_frame.grid_propagate(False)

        # Adjust column weight for balancing
        self.fields_frame.grid_columnconfigure(0, weight=1)
        self.fields_frame.grid_columnconfigure(1, weight=1)

        # Fields Header
        self.fields_header = tk.Label(self.fields_frame, text="FACULTY DETAILS", fg="#FFFFFF", bg="#8D0404",
                                      anchor="w", font=("Arial", 14, "bold"), padx=20, pady=10)
        self.fields_header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Style Settings
        label_style = {"fg": "#8D0404", "bg": "#FBFBF9"}
        entry_style = {"width": 25}

        # Function to simplify label and entry creation
        def create_label_entry(label_text, row, column):
            label = tk.Label(self.fields_frame, text=label_text, **label_style)
            label.grid(row=row, column=column, padx=20, pady=(10, 0), sticky="w")
            entry = tk.Entry(self.fields_frame, **entry_style)
            entry.grid(row=row + 1, column=column, padx=20, pady=(0, 10), sticky="ew")
            return entry

        # Column 0
        self.first_name = create_label_entry("First Name*", 1, 0)
        self.middle_name = create_label_entry("Middle Name", 3, 0)
        self.last_name = create_label_entry("Last Name*", 5, 0)
        self.email = create_label_entry("Email*", 7, 0)

        # Column 1
        self.phone_num = create_label_entry("Phone Number*", 1, 1)
        self.username = create_label_entry("Username*", 3, 1)
        self.password = create_label_entry("Password*", 5, 1)
        self.password.config(show="*")

        # Add Faculty Button
        self.add_fac_btn = ttk.Button(self.fields_frame, text="Add Faculty", command=self.add_faculty)
        self.add_fac_btn.grid(row=9, column=0, columnspan=2, pady=20)

    def add_faculty(self):
        # Validate Fields
        validation_result = self.validate_fields()
        if validation_result is not True:
            messagebox.showerror("Validation Error", validation_result)
            return

        # Extract data from the fields and apply transformations
        first_name = self.first_name.get().strip().capitalize()
        middle_name = self.middle_name.get().strip() or None
        last_name = self.last_name.get().strip().capitalize()
        username = self.username.get().strip()
        password = self.password.get().strip()
        email = self.email.get().strip()
        phone_number = self.phone_num.get().strip()

        print(first_name)
        print(middle_name)
        print(last_name)
        print(username)
        print(password)
        print(email)
        print(phone_number)

        # Call the admin model to add faculty
        try:
            result = self.main.admin_model.add_faculty(username, password, first_name, middle_name, last_name, email,
                                                       phone_number)
            if result:
                messagebox.showinfo("Success", "Faculty added successfully!")
                self.clear_fields()
            else:
                messagebox.showerror("Error", "Failed to add faculty. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_fields(self):
        self.first_name.delete(0, 'end')
        self.middle_name.delete(0, 'end')
        self.last_name.delete(0, 'end')
        self.username.delete(0, 'end')
        self.password.delete(0, 'end')
        self.email.delete(0, 'end')
        self.phone_num.delete(0, 'end')

    def validate_fields(self):
        # Field values
        fields = {
            "First Name": (self.first_name.get(), 50),
            "Middle Name": (self.middle_name.get(), 30),
            "Last Name": (self.last_name.get(), 50),
            "Username": (self.username.get(), 50),
            "Password": (self.password.get(), 10),
            "Email": (self.email.get(), 50),
            "Phone Number": (self.phone_num.get(), 11),
        }

        # Check for empty fields (except middle name)
        for field_name, (value, max_length) in fields.items():
            if field_name != "Middle Name" and not value.strip():
                return f"{field_name} cannot be empty."

            # Check for max length
            if len(value.strip()) > max_length:
                return f"{field_name} exceeds max length of {max_length} characters."

        # Email Validation
        email = self.email.get().strip()
        valid_domains = ("@email.com", "@gmail.com", "@yahoo.com", "@mail.com")
        if not any(email.endswith(domain) for domain in valid_domains):
            return "Email must end with '@email.com', '@gmail.com', '@yahoo.com', or '@mail.com'."

        # Phone Number Validation (Only Digits)
        phone_number = self.phone_num.get().strip()
        if not phone_number.isdigit():
            return "Phone Number should contain only digits."
        elif len(phone_number) != 11:
            return "Phone Number must be exactly 11 digits."

        # All validations passed
        return True

    def on_close(self):
        self.destroy()