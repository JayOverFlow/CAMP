import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from customtkinter import CTkButton
from CAMP_app.views.student.course_apply import CourseApplication



class StudentCoursesTab(tk.Frame):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing
        self.student_session = student_landing.student_session

        self.lbl = ttk.Label(self, text="Courses")
        self.lbl.place(x=1, y=20)

        self.course_list = ttk.Treeview(self, columns=["cou_name", "raw_grade", "final_grade", "assigned_prof", "evaluate"])
        self.course_list.place(x=5, y=50, width=800, height=500)
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=25)
        self.style.configure("Treeview.Heading", background="#8D0404", foreground="white")
        self.course_list.tag_configure("Treeview.Heading", background="#8D0404")

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

        self.apply_btn = ctk.CTkButton(self, text="Apply for Course", corner_radius=7, fg_color="#8D0404",
                                       text_color="white", command=self.open_course_application)
        self.apply_btn.place(x=100, y=100)

    def display_enrolled_courses(self, stu_id):
        enrolled_courses = self.main.student_model.get_courses(stu_id)
        print("Displaying schedule for student ID:", stu_id)

        # Ensure button alignment starts properly
        button_y_offset = 75  # Align with the first row
        row_height = 25  # Approximate row height in the Treeview

        for index, course in enumerate(enrolled_courses):
            # Insert course data
            item_id = self.course_list.insert("", "end",
                                              values=(
                                                  course["course_name"],
                                                  course["raw_grade"],
                                                  course["final_grade"],
                                                  course["assigned_professor"],
                                                  ""  # Placeholder for the Evaluate column
                                              )
                                              )

            # Create an Evaluate button aligned with each row
            btn = ctk.CTkButton(self, text="Evaluate", corner_radius=7, fg_color="#8D0404",
                                text_color="white",width=50,height= 20, command= self.evaluate_course)
            btn.place(x=705, y=button_y_offset + (index * row_height))

    def open_course_application(self):
        # Get student ID from the current session
        stu_id = self.student_session["stu_id"]

        student_data = self.main.student_model.fetch_courses(stu_id)
        # Initialize the CourseApplication and pass the student ID
        CourseApplication(self, self.student_landing, self.main, student_data, stu_id)

    def evaluate_course(self):
        pass








