import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk

from CAMP_app.views.student.faculty_eval import FacultyEvalView

from CAMP_app.views.student.course_apply import CourseApplication



class StudentCoursesTab(tk.Frame):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing
        self.student_session = student_landing.student_session

        # Initialize ttk.Style
        self.style = ttk.Style()  # ✅ Define self.style before using it

        # ✅ Define self.style as an instance attribute
        self.style.configure("Custom.TLabel", font=("Arial", 20, "bold"), foreground="#8D0404")

        self.lbl = ttk.Label(self, text="Courses", style="Custom.TLabel")
        self.lbl.grid(row=0, column=0, columnspan=3, pady=10)

        # Configure row height
        self.style.configure("Treeview", rowheight=30)

        self.style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"),
                        foreground="white",
                        background="#8D0404")
        # Force the header to stay red when hovered (removes hover effect)
        self.style.map("Treeview.Heading",
                       background=[("active", "#8D0404"), ("!active", "#8D0404")])

        self.course_list = ttk.Treeview(self,
                                        columns=["cou_name", "raw_grade", "final_grade", "assigned_prof", "evaluate"],style="Treeview")
        self.course_list.place(x=5, y=50, width=800, height=500)

        self.course_list.bind("<<TreeviewSelect>>", self.disable_selection)
        # Disable clicking on headers
        self.course_list.bind("<Button-1>", self.disable_header_click)

        # Define column headings
        self.course_list.heading("cou_name", text="Course Name")
        self.course_list.heading("raw_grade", text="Raw Grade")
        self.course_list.heading("final_grade", text="Final Grade")
        self.course_list.heading("assigned_prof", text="Assigned Professor")
        self.course_list.heading("evaluate", text="")

        # Define column widths
        self.course_list.column("#0", width=0, stretch=tk.NO)
        self.course_list.column("cou_name", width=100, anchor="center")
        self.course_list.column("raw_grade", width=100, anchor="center")
        self.course_list.column("final_grade", width=100, anchor="center")
        self.course_list.column("assigned_prof", width=150, anchor="center")
        self.course_list.column("evaluate", width=100, anchor="center")

        self.display_enrolled_courses(self.student_session["stu_id"])

        self.apply_btn = ctk.CTkButton(self, text="+ Apply for Course", corner_radius=7, fg_color="#8D0404",
                                       text_color="white", command=self.open_course_application)
        self.apply_btn.place(x=659, y=17)

    def display_enrolled_courses(self, stu_id):
        enrolled_courses = self.main.student_model.get_courses(stu_id)
        print("Displaying schedule for student ID:", stu_id)

        # Ensure button alignment starts properly
        button_y_offset = 74  # Align with the first row
        row_height = 31  # Approximate row height in the Treeview
        self.evaluate_buttons = []  # Store buttons for reference

        for index, course in enumerate(enrolled_courses):
            # Insert course data into the Treeview
            item_id = self.course_list.insert("", "end",
                                              values=(
                                                  course["course_name"],
                                                  course["raw_grade"],
                                                  course["final_grade"],
                                                  course["assigned_professor"],
                                                  ""  # Empty column for alignment
                                              )
                                              )

            # Create an Evaluate button that remembers its course & professor
            btn = ctk.CTkButton(self, text="Evaluate", corner_radius=5, fg_color="#8D0404",
                                text_color="white", width=90, height=25,
                                command=lambda c=course: self.evaluate_course(c["course_name"],
                                                                              c["assigned_professor"]))
            btn.place(x=705, y=button_y_offset + (index * row_height))  # Align button with row

            self.evaluate_buttons.append(btn)  # Store for future reference

    def open_course_application(self):
        # Get student ID from the current session
        stu_id = self.student_session["stu_id"]

        student_data = self.main.student_model.fetch_courses(stu_id)
        # Initialize the CourseApplication and pass the student ID
        CourseApplication(self, self.student_landing, self.main, student_data, stu_id)

    def evaluate_course(self, course_name, professor_name):
        """ Opens the Faculty Evaluation Form with the selected course & professor """
        stu_id = self.student_session["stu_id"]
        stu_full_name = self.student_session["stu_full_name"]

        # Retrieve faculty_id using professor's name
        faculty_id = self.main.student_model.get_faculty_id(professor_name)

        if not faculty_id:
            tk.messagebox.showerror("Error", f"Faculty ID not found for {professor_name}.")
            return

        print(f"Evaluating Course: {course_name}, Professor: {professor_name} (ID: {faculty_id})")  # Debugging

        # Open Faculty Evaluation Form with the correct details
        FacultyEvalView(self, self.main, self.student_session, stu_id, faculty_id,stu_full_name)

    def disable_selection(self, event):
        self.course_list.selection_remove(self.course_list.selection())

    # Function to disable header clicks
    def disable_header_click(self, event):
        """ Prevents column header clicks from sorting or being interactive """
        region = self.course_list.identify("region", event.x, event.y)
        if region == "heading":  # If clicked on the header, do nothing
            return "break"









