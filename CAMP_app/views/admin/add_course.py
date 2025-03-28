import tkinter as tk
from tkinter import ttk, messagebox
import re


class AddCourse(tk.Toplevel):
    def __init__(self, parent, main, admin_courses):
        super().__init__(parent)
        self.main = main
        self.admin_courses = admin_courses
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Add Course")
        self.geometry("600x220+350+230")
        self.resizable(False, False)

        # Main frame
        self.main_frame = tk.Frame(self, bg="#FBFBF9")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Fields Header
        self.fields_header = tk.Label(self.main_frame, text="ADD COURSE", fg="#FFFFFF", bg="#8D0404",
                                      anchor="w", font=("Arial", 14, "bold"), padx=20, pady=10)
        self.fields_header.pack(fill=tk.X)

        # Fields Frame using Grid
        self.fields_frame = tk.Frame(self.main_frame, bg="#FBFBF9")
        self.fields_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Style Settings
        label_style = {"fg": "#8D0404", "bg": "#FBFBF9"}
        entry_style = {"width": 25}

        # Function to simplify label and field creation
        def create_label_field(label_text, row, column, widget_type="entry", options=[]):
            label = tk.Label(self.fields_frame, text=label_text, **label_style)
            label.grid(row=row, column=column * 2, padx=10, pady=10, sticky="w")

            if widget_type == "entry":
                field = tk.Entry(self.fields_frame, **entry_style)
            elif widget_type == "dropdown":
                field = ttk.Combobox(self.fields_frame, values=options, state="readonly")
                field.set("Select " + label_text)
            field.grid(row=row, column=column * 2 + 1, padx=10, pady=10, sticky="ew")
            return field

        # Options from database
        days_of_week = self.main.admin_model.get_schedule_days()
        faculty_names = self.main.admin_model.get_unassigned_faculties()
        schedule_times = self.main.admin_model.get_schedule_times()

        # Row 1 - Course Name and Day
        self.course_name = create_label_field("Course Name*", 0, 0)
        self.day_dropdown = create_label_field("Day*", 0, 1, widget_type="dropdown", options=days_of_week)

        # Row 2 - Professor and Time
        self.professor_dropdown = create_label_field("Professor*", 1, 0, widget_type="dropdown", options=faculty_names)
        self.time_dropdown = create_label_field("Time*", 1, 1, widget_type="dropdown", options=schedule_times)

        # Add Course Button
        self.add_course_btn = ttk.Button(self.main_frame, text="Add Course", command=self.add_course)
        self.add_course_btn.pack(pady=5)

    def add_course(self):
        if self.validate_fields():
            course_name = self.course_name.get().strip()
            faculty_name = self.professor_dropdown.get()
            day = self.day_dropdown.get()
            time_range = self.time_dropdown.get().split('-')
            time_start, time_end = time_range[0], time_range[1]

            # Get faculty_id and schedule_id
            faculty_id = self.main.admin_model.get_faculty_id_by_name(faculty_name)
            schedule_id = self.main.admin_model.get_schedule_id(day, time_start, time_end)

            if faculty_id is None or schedule_id is None:
                messagebox.showerror("Error", "Invalid Faculty or Schedule selection.")
                return

            # Add course
            if self.main.admin_model.add_course(course_name, faculty_id, schedule_id):
                messagebox.showinfo("Success", "Course added successfully!")
                self.refresh_course_list()
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to add course.")

    def validate_fields(self):
        if not self.course_name.get().strip():
            messagebox.showerror("Validation Error", "Course Name cannot be empty.")
            return False
        if self.day_dropdown.get() == "Select Day*":
            messagebox.showerror("Validation Error", "Please select a Day.")
            return False
        if self.professor_dropdown.get() == "Select Professor*":
            messagebox.showerror("Validation Error", "Please select a Professor.")
            return False
        if self.time_dropdown.get() == "Select Time*":
            messagebox.showerror("Validation Error", "Please select a Time.")
            return False

        # Extract selected time_start and time_end from the time dropdown (assuming it's in format 'start-end')
        selected_time = self.time_dropdown.get().split('-')
        time_start = selected_time[0].strip()
        time_end = selected_time[1].strip()

        # Check if the schedule is already taken
        if self.main.admin_model.is_schedule_taken(self.day_dropdown.get(), time_start, time_end):
            messagebox.showerror("Validation Error", "The selected schedule is already assigned to another course.")
            return False

        return True

    def refresh_course_list(self):
        course_list = self.admin_courses.course_list
        for row in course_list.get_children():
            course_list.delete(row)
        self.admin_courses.display_courses()

    def clear_fields(self):
        # Clear course name entry
        self.course_name.delete(0, tk.END)

        # Reset dropdowns to default values
        self.day_dropdown.set("Select Day*")
        self.professor_dropdown.set("Select Professor*")
        self.time_dropdown.set("Select Time*")

    def on_close(self):
        self.destroy()

