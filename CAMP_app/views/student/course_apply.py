import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

class CourseApplication(tk.Toplevel):
    def __init__(self, parent,student_courses,main,student_data):
        super().__init__(parent)
        self.student_courses = student_courses
        self.main = main
        self.student_data = student_data

        self.title("Course Application")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)

        # Frame for Available Courses
        frame = tk.Frame(self, bd=2, relief="ridge")
        frame.pack(pady=10, padx=10, fill="x")

        self.lbl = tk.Label(frame, text="Course Application", font=("Arial", 14, "bold"),
                            fg="white", bg="#8D0404")
        self.lbl.pack(fill="x")

        self.courses = ttk.Treeview(frame, columns=("cou_name", "assigned_prof"), show="headings")
        self.courses.heading("cou_name", text="Course Name")
        self.courses.heading("assigned_prof", text="Assigned Professor")

        self.courses.column("cou_name", width=350, anchor="center")
        self.courses.column("assigned_prof", width=350, anchor="center")

        self.courses.pack(side="left", fill="both", expand=True)

        self.get_initial_courses()

        self.selected_courses_list = []
        self.course_buttons = {}  # Track buttons for selected courses
        print(self.course_buttons)

        # Frame for Selected Courses
        self.selected_frame = tk.Frame(self, bd=2, relief="ridge")
        self.selected_frame.pack(pady=10, padx=10, fill="x")

        self.selected_label = tk.Label(self.selected_frame, text="Selected Course", font=("Arial", 14, "bold"),
                                       fg="white", bg="#8D0404")
        self.selected_label.pack(fill="x")

        self.selected_list = ttk.Treeview(self.selected_frame, columns=("cou_name", "assigned_prof"), show="headings")
        self.selected_list.heading("cou_name", text="Course Name")
        self.selected_list.heading("assigned_prof", text="Assigned Professor")

        self.selected_list.column("cou_name", width=350, anchor="center")
        self.selected_list.column("assigned_prof", width=350, anchor="center")
        self.selected_list.pack(fill="both", expand=True)

        self.confirm_btn = ctk.CTkButton(self, text="Confirm Application", fg_color="#8D0404", text_color="white",
                                         command=self.confirm_application)
        self.confirm_btn.pack(side="bottom", pady=10, anchor="e")

        # Back Button (Compact "X")
        self.back_btn = ctk.CTkButton(self, text="X", fg_color="#8D0404", text_color="white",
                                      width=30, font=("Arial", 14, "bold"),
                                      command=self.go_back)
        self.back_btn.place(x=900, y=10)  # Adjust position for better alignment

    def get_initial_courses(self):
        initial_courses = self.main.student_model.fetch_courses()
        if initial_courses and isinstance(initial_courses[0], dict):
            initial_courses = [(course.get("cou_name", "N/A"), course.get("fac_full_name", "N/A")) for course in
                               initial_courses]

        self.courses.delete(*self.courses.get_children())
        for course in initial_courses:
            row_id = self.courses.insert("", "end", values=course)
            btn = ctk.CTkButton(
                self, text="Select", corner_radius=7, fg_color="#8D0404", text_color="white", width=100, height=10,
                command=lambda c=course: self.selected_courses(c)
            )
            btn.place(x=850, y=60 + (len(self.courses.get_children()) - 1) * 25)

    def selected_courses(self, course):
        if course not in self.selected_courses_list:
            self.selected_courses_list.append(course)
            row_id = self.selected_list.insert("", "end", values=course)

            # Ensure GUI updates before getting row coordinates
            self.update_idletasks()

            # Get row position inside the Treeview
            bbox = self.selected_list.bbox(row_id)
            if bbox:  # Ensure bbox is valid
                x_pos = self.selected_list.winfo_width() - 50  # Align button to the right
                y_pos = bbox[1] + bbox[3]  # Move button lower by adding row height

                # Create "Remove" button
                remove_btn = ctk.CTkButton(
                    self.selected_frame, text="X", fg_color="red", width=30, height=20,
                    command=lambda c=course: self.remove_course(c)
                )

                # Place button dynamically inside selected_frame
                self.after(100, lambda: remove_btn.place(x=x_pos, y=y_pos + 5))  # Move 5 pixels lower

                # Store row ID and button reference
                self.course_buttons[course] = (row_id, remove_btn)

            # 🔹 Adjust all button positions
            self.realign_buttons()

    def realign_buttons(self):
        """ Adjusts button positions to match row positions dynamically """
        self.update_idletasks()  # Ensure all widgets update first

        for course, (row_id, btn) in self.course_buttons.items():
            bbox = self.selected_list.bbox(row_id)
            if bbox:  # Ensure row is still visible
                x_pos = self.selected_list.winfo_width() - 50  # Keep aligned
                y_pos = bbox[1] + bbox[3]  # Move button lower by adding row height

                btn.place(x=x_pos, y=y_pos + 5)  # Move 5 pixels lower

    def remove_course(self, course):
        if course in self.course_buttons:
            row_id, btn = self.course_buttons.pop(course)
            self.selected_list.delete(row_id)
            btn.destroy()  # Remove the button
            self.selected_courses_list.remove(course)

            # Ensure the UI updates properly
            self.update_selected_buttons()

    def update_selected_buttons(self):
        self.update_idletasks()  # Ensure GUI refreshes
        for course, (row_id, btn) in self.course_buttons.items():
            bbox = self.selected_list.bbox(row_id)
            if bbox:
                x_pos = self.selected_list.winfo_width() - 50
                y_pos = bbox[1] + bbox[3] // 2
                btn.place(x=x_pos, y=y_pos)

    def confirm_application(self):
        print("Confirmed Courses:", self.selected_courses_list)

    def go_back(self):
        self.destroy()  # Closes the current window





