import tkinter as tk
from tkinter import ttk

from CAMP_app.views.admin.enroll_student import EnrollStudent
from CAMP_app.views.admin.view_student_profile import ViewStudentProfile


class AdminDashboard(tk.Frame):
    def __init__(self, parent, main, admin_landing):
        super().__init__(parent)
        self.main = main
        self.admin_landing = admin_landing

        # Student count
        self.student_count = tk.Label(self, text="")
        self.student_count.pack()

        # Femalae count
        self.female_count = tk.Label(self, text="")
        self.female_count.pack()

        # Male count
        self.male_count = tk.Label(self, text="")
        self.male_count.pack()

        # Faculty count
        self.faculty_count = tk.Label(self, text="")
        self.faculty_count.pack()

        # Enroll student button
        self.enroll_student_btn = tk.Button(self, text="Enroll Student", command=self.enroll_student)
        self.enroll_student_btn.pack()

        # Search bar
        self.search_var = tk.StringVar()  # Variable to store the entry string
        self.search_entry = tk.Entry(self, textvariable=self.search_var, width=30)
        self.search_entry.insert(0, "Search by Name or ID")  # Initial as placeholder
        # Handle focus for placeholder
        self.search_entry.bind("<FocusIn>", self.toggle_placeholder)
        self.search_entry.bind("<FocusOut>", self.toggle_placeholder)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_students)  # Filter students for live searching

        # Student list
        self.student_list = ttk.Treeview(self, columns=("stu_full_name", "stu_id", "view_profile"),
                                         show="headings")
        self.student_list.heading("stu_full_name", text="Full Name")
        self.student_list.heading("stu_id", text="Student ID")
        self.student_list.heading("view_profile", text="")
        self.student_list.column("stu_full_name", anchor="center", width=100)
        self.student_list.column("stu_id", anchor="center", width=100)
        self.student_list.column("view_profile", anchor="center", width=100)
        self.student_list.pack()

        # self.display_students()

        self.display_data() # Display all data

        self.student_list.bind("<ButtonRelease-1>", self.view_profile)  # When the user clicked the "View Profile"

    def display_data(self):
        self.display_student_count()
        self.display_female_count()
        self.display_male_count()
        self.display_faculty_count()
        self.display_students()

    def display_student_count(self):
        student_count = self.main.admin_model.get_student_count()

        self.student_count.config(text=student_count)

    def display_female_count(self):
        female_count = self.main.admin_model.get_female_count()

        self.female_count.config(text=female_count)

    def display_male_count(self):
        male_count = self.main.admin_model.get_male_count()

        self.male_count.config(text=male_count)

    def display_faculty_count(self):
        faculty_count = self.main.admin_model.get_faculty_count()

        self.faculty_count.config(text=faculty_count)

    def enroll_student(self):
        self.admin_landing.attributes("-disabled", True) # Disable the interaction
        self.admin_landing.wait_window(EnrollStudent(self.main, self.admin_landing)) # Wait for the popup
        self.admin_landing.attributes("-disabled", False) # Re-enable the interaction
        self.admin_landing.focus_force() # Regain focus on the parent window

    def display_students(self):
        self.all_students = self.main.admin_model.get_students() # Get and store the students
        self.update_treeview(self.all_students) # Pass the students

    def update_treeview(self, students):
        # Clear and display
        self.student_list.delete(*self.student_list.get_children())
        for student in students:
            self.student_list.insert("", "end", values=(student["stu_full_name"], f"AU{student["stu_id"]}", "View Profile"))

    def filter_students(self, event=None):
        search_text = self.search_var.get().lower() # Get the user input
        # Manipulate the studentlist for filtering
        filtered_students = [
            s for s in self.all_students
            if search_text in s["stu_full_name"].lower() or search_text in str(s["stu_id"])
        ]
        self.update_treeview(filtered_students) # Update the student list with filtered students

    def toggle_placeholder(self, event):
        if event.type == "9":  # FocusIn
            if self.search_entry.get() == "Search by Name or ID":
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg="black")
        elif event.type == "10":  # FocusOut
            if not self.search_entry.get():
                self.search_entry.insert(0, "Search by Name or ID")
                self.search_entry.config(fg="gray")

    def view_profile(self, event):
        # Get the selected row
        selected_row = self.student_list.identify_row(event.y)

        # Get the clicked column
        column_id = self.student_list.identify_column(event.x) # OUtput #3

        # Define the column index
        VIEW_PROFILE_COLUMN_INDEX = 3

        # Convert column_id (e.g., "#3") to integer and check if it matches the 'View Profile' column
        if int(column_id[1:]) == VIEW_PROFILE_COLUMN_INDEX:
            values = self.student_list.item(selected_row, "values")

            if values:
                stu_id = values[1][2:]  # Adjust index based on your data structure
                student_data = self.main.admin_model.get_student_profile(stu_id)

                # Open Student Profile
                self.admin_landing.attributes("-disabled", True)  # Disable the interaction
                self.admin_landing.wait_window(ViewStudentProfile(self, self.admin_landing, self.main, student_data))  # Wait for the popup
                self.admin_landing.attributes("-disabled", False)  # Re-enable the interaction
                self.admin_landing.focus_force()  # Regain focus on the parent window