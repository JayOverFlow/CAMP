import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk


class FacultyEvalView(tk.Toplevel):
    def __init__(self, parent, main, student_data, stu_id, faculty_id, stu_full_name):
        super().__init__(parent)
        self.main = main
        self.student_data = student_data
        self.stu_id = stu_id
        self.faculty_id = faculty_id
        self.student_full_name = stu_full_name

        self.geometry("300x300")
        self.title("Faculty Eval")

        self.student_name = ttk.Label(self, text=self.student_full_name)
        self.student_name.pack()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        """Creates form fields for faculty evaluation input."""

        ttk.Label(self, text="Rating:").pack(pady=5)
        self.rating_frame = tk.Frame(self)
        self.rating_frame.pack()

        self.rating = tk.IntVar(value=0)  # Store selected rating
        self.stars = []

        for i in range(1, 6):
            star_btn = tk.Button(self.rating_frame, text="☆", font=("Arial", 14),foreground="#FFEA00",
                                 command=lambda i=i: self.set_rating(i))
            star_btn.grid(row=0, column=i - 1, padx=2)
            self.stars.append(star_btn)

        # Create a StringVar to hold the text from the entry
        self.comment = tk.StringVar(value="write your comment")
        # Create a CTkLabel (if you want to show a label, here it's an empty string)
        self.comment_label = ctk.CTkLabel(self, text="", text_color="black")
        self.comment_label.pack(pady=5)

        # Create the CTkEntry and bind the focus_in event to clear the text
        self.comment_entry = ctk.CTkEntry(self, textvariable=self.comment)
        self.comment_entry.pack(pady=5)

        # Bind the focus_in event to clear the text when clicked
        self.comment_entry.bind("<FocusIn>", self.clear_comment)

        # Optionally, bind the focus_out event to restore the default text if empty
        self.comment_entry.bind("<FocusOut>", self.restore_comment)

        submit_button = ctk.CTkButton(self, text="Submit", command=self.add_eval)
        submit_button.pack(pady=10)

    def set_rating(self, value):
        """Updates the star rating display."""
        self.rating.set(value)
        for i in range(5):
            self.stars[i].config(text="★" if i < value else "☆")

    def add_eval(self):
        """Collects input and submits the evaluation."""
        student_id = self.stu_id
        faculty_id = self.faculty_id
        eval_rating = self.rating.get()
        eval_comment = self.comment_entry.get()

        try:
            eval_rating = float(eval_rating)
            if eval_rating < 1 or eval_rating > 5:
                messagebox.showerror("Error", "Rating must be between 1 and 5.")
                return
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number.")
            return

        # Debugging output
        print(f"Adding evaluation: student_id={student_id}, faculty_id={faculty_id}, rating={eval_rating}, comment={eval_comment}")

        # Call the database method to insert the evaluation
        insert_eval = self.main.student_model.add_eval(student_id, faculty_id, eval_rating, eval_comment)

        if insert_eval:
            messagebox.showinfo("Success", "Evaluation added successfully.")
            self.destroy()
        else:
            self.destroy()
            messagebox.showerror("Error", "Course already evaluated")

    # Function to clear the default text when the entry is clicked
    def clear_comment(self,event):
        if self.comment.get() == "write your comment":
            self.comment.set("")  # Clear the entry when clicked

    # Function to restore the default text if the entry is empty
    def restore_comment(self,event):
        if self.comment.get() == "":
            self.comment.set("write your comment")  # Restore default text if empty






