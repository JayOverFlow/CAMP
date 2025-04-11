import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from pathlib import Path
from PIL import ImageTk, Image, ImageDraw





class FacultyEvalView(tk.Toplevel):
    def __init__(self, parent, main, student_data, stu_id, faculty_id,faculty_name,course_name):
        super().__init__(parent)
        self.main = main
        self.student_data = student_data
        self.stu_id = stu_id
        self.faculty_id = faculty_id
        self.faculty_name_text = faculty_name  # Avoid overwriting the variable
        self.course_name_text = course_name  # Avoid overwriting the variable

        self.geometry("300x355")
        self.title("Faculty Eval")
        self.resizable(False, False)

        # Make this window modal
        self.grab_set()  # Prevents interaction with other windows
        self.transient(parent)  # Associates this window with the parent
        self.wait_visibility()  # Ensures the window is fully drawn before proceeding

        # Define the labels with font color
        self.faculty_name_label = ctk.CTkLabel(self, text=self.faculty_name_text,
                                               font=("Lexend Deca", 20, "bold"),
                                               text_color="#8D0404")
        self.faculty_name_label.pack()

        self.course_name_label = ctk.CTkLabel(self, text="Course: " + self.course_name_text,
                                              font=("Lexend Deca", 10, "normal"),
                                              text_color="#8D0404")
        self.course_name_label.pack()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        """Creates form fields for faculty evaluation input."""
        ctk.CTkLabel(self, text="Overall Performance",
                     font=("Lexend Deca", 14, "normal"),
                     text_color="#8D0404").pack(pady=5)

        # Label to show rating text (Good, Poor, etc.)
        self.rating_text = ttk.Label(self, text="Rating: ")
        self.rating_text.pack(pady=5)

        self.rating_frame = tk.Frame(self)
        self.rating_frame.pack()

        self.rating = tk.IntVar(value=0)  # Store selected rating
        self.stars = []

        for i in range(1, 6):
            star_btn = ctk.CTkButton(self.rating_frame, text="☆",
                                     font=("Arial", 14),
                                     fg_color="#020202",  # Black background
                                     text_color="#FFD700",
                                     hover_color="#4A4A4A",  # Slightly lighter black on hover
                                     width=30, height=30,  # Adjust size
                                     corner_radius=5,
                                     command=lambda i=i: self.set_rating(i))
            star_btn.grid(row=0, column=i - 1, padx=2)
            self.stars.append(star_btn)

        # Create the CTkTextbox for multi-line comments with placeholder
        self.comment_entry = ctk.CTkTextbox(self, width=250, height=80,
                                            fg_color="#D3D3D3", text_color="gray")
        self.comment_entry.pack(pady=5)

        # Placeholder text
        self.placeholder = "Enter your comment here..."
        self.comment_entry.insert("1.0", self.placeholder)

        # Bind focus events
        self.comment_entry.bind("<FocusIn>", self.clear_placeholder)
        self.comment_entry.bind("<FocusOut>", self.add_placeholder)

        submit_button = ctk.CTkButton(self, text="Submit",
                                      command=self.add_eval, fg_color="#8D0404")
        submit_button.pack(pady=10)

    def set_rating(self, value):
        """Updates the star rating display and rating text."""
        self.rating.set(value)

        for i in range(5):
            if i < value:
                self.stars[i].configure(text="★", fg_color="#020202")  # Gold color when selected
            else:
                self.stars[i].configure(text="☆", fg_color="#FFFFFF")  # Black when unselected

        # Update the rating text based on the selected rating
        rating_texts = ["Poor", "Need Improvement", "Good", "Very Good", "Excellent"]
        self.rating_text.config(text=rating_texts[value - 1])

    def add_eval(self):
        """Collects input and submits the evaluation."""
        student_id = self.stu_id
        faculty_id = self.faculty_id
        eval_rating = self.rating.get()
        eval_comment = self.comment_entry.get("1.0", tk.END).strip()

        try:
            eval_rating = float(eval_rating)
            if eval_rating < 1 or eval_rating > 5:
                messagebox.showerror("Error", "Rating must be between 1 and 5.")
                return
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number.")
            return

        # Debugging output
        print(
            f"Adding evaluation: student_id={student_id}, faculty_id={faculty_id}, rating={eval_rating}, comment={eval_comment}")

        # Call the database method to insert the evaluation
        insert_eval = self.main.student_model.add_eval(student_id, faculty_id, eval_rating, eval_comment)

        if insert_eval:
            messagebox.showinfo("Success", "Evaluation added successfully.")
            self.destroy()
        else:
            messagebox.showerror("Error", "Course already evaluated")
            self.destroy()

    def clear_placeholder(self, event):
        """Clears the placeholder when the user clicks inside the textbox."""
        if self.comment_entry.get("1.0", "end").strip() == self.placeholder:
            self.comment_entry.delete("1.0", "end")
            self.comment_entry.configure(text_color="#8D0404")  # Change text color when typing

    def add_placeholder(self, event):
        """Restores the placeholder if the textbox is empty when losing focus."""
        if not self.comment_entry.get("1.0", "end").strip():
            self.comment_entry.insert("1.0", self.placeholder)
            self.comment_entry.configure(text_color="gray")  # Restore placeholder color



