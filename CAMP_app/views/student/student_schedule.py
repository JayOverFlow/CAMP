import tkinter as tk
from tkinter import ttk


class StudentScheduleTab(tk.Frame):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing
        self.student_session = student_landing.student_session

        # Ensure the frame fits and is managed by grid
        self.grid(row=0, column=0, sticky="nsew")

        # Configure parent to expand properly
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        style = ttk.Style(self)
        style.configure("Custom.TLabel", font=("Arial", 20, "bold"), foreground="#8D0404")

        # Header label
        self.lbl = ttk.Label(self, text="Schedule", style="Custom.TLabel")
        self.lbl.grid(row=0, column=0, columnspan=3, pady=10)

        self.display_schedule(self.student_session["stu_id"])

    def format_time(self, time_delta):
        # Convert datetime.timedelta to HH:MM format
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes = remainder // 60
        return f"{hours:02}:{minutes:02}"

    def display_schedule(self, stu_id):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        style = ttk.Style(self)
        style.configure("Custom.TLabel", font=("Arial", 20, "bold"), foreground="#8D0404")
        # Recreate header
        self.lbl = ttk.Label(self, text="Schedule", style="Custom.TLabel")
        self.lbl.grid(row=0, column=0, columnspan=3, pady=10)

        # Fetch schedule
        student_sched = self.main.student_model.get_sched(stu_id)


        # Populate the grid with the schedule
        for row, sched in enumerate(student_sched, start=2):
            # Day column
            tk.Label(self, text=sched["day_of_week"].upper(), fg='white', bg="#8B0000", font=("Arial", 18, "bold")) \
                .grid(row=row, column=0, sticky="nsew", pady=5)

            # Subject column
            tk.Label(self, text=sched["course_name"], bg="#E5E5E5", font=("Arial", 14), anchor="w") \
                .grid(row=row, column=1, sticky="nsew", pady=5)

            # Time column
            time_start = self.format_time(sched["time_start"])
            time_end = self.format_time(sched["time_end"])
            tk.Label(self, text=f"{time_start} - {time_end}", bg="#E5E5E5", font=("Arial", 14), anchor="e") \
                .grid(row=row, column=2, sticky="nsew", pady=5)



