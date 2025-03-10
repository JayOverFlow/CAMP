import tkinter as tk
from tkinter import ttk


class StudentProfileTab(tk.Frame):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing
        self.student_session = student_landing.student_session

        self.full_name = ttk.Label(self, text=self.student_session["stu_full_name"])
        self.full_name.place(x=5, y=100)

        self.course = ttk.Label(self, text=self.student_session["stu_courses_fk"])
        self.course.place(x=8, y=150)

        self.first_name = ttk.Label(self, text=self.student_session["stu_first_name"])
        self.first_name.place(x=20, y=170)

        self.middle_name = ttk.Label(self, text=self.student_session["stu_middle_name"])
        self.middle_name.place(x=20, y=200)

        self.last_name = ttk.Label(self, text=self.student_session["stu_last_name"])
        self.last_name.place(x=20, y=250)

        self.birth_date = ttk.Label(self, text=self.student_session["stu_birthdate"])
        self.birth_date.place(x=20, y=300)

        self.gender = ttk.Label(self, text=self.student_session["stu_sex"])
        self.gender.place(x=20, y=350)

        self.cellphone_number = ttk.Label(self, text=self.student_session["stu_phone_number"])
        self.cellphone_number.place(x=20, y=400)

        self.email_address = ttk.Label(self, text=self.student_session["stu_emailadd"])
        self.email_address.place(x=20, y=450)

        self.address = ttk.Label(self, text=self.student_session["stu_address"])
        self.address.place(x=20, y=500)

        self.username = ttk.Label(self, text=self.student_session["stu_username"])
        self.username.place(x=20, y=550)

        self.password = ttk.Label(self, text=self.student_session["stu_password"])
        self.password.place(x=20, y=600)

        self.lrn_number = ttk.Label(self, text=self.student_session["stu_lrn"])
        self.lrn_number.place(x=20, y=700)

        self.citizenship = ttk.Label(self, text=self.student_session["stu_citizenship"])
        self.citizenship.place(x=20, y=800)

        self.religion = ttk.Label(self, text=self.student_session["stu_religion"])
        self.religion.place(x=20, y=900)

        self.is_updating = False
        self.update_profile_btn = tk.Button(self, text="Update Profile")
        self.update_profile_btn.place(x=700, y=550)

    # def update_profile_btn(self):
    #     if not self.is_updating:
    #         self.is_updating = True
    #         self.update_profile_btn.configure("Save")
    #         for entry in self.student_session.values():
    #             entry.configure(state=tk.NORMAL)
    #
    #     else:
    #         updated_data = self.get_student_data()
    #
    #         if self.
    #
    # def get_student_data(self):
    #     updated_data = {key: entry.get() for key, entry in self.student_session.items()}
    #     return updated_data


