import mysql

class AdminModel:
    def __init__(self, database):
        self.db = database

    # Functionalities needed
    # 1. Read admin username
    # 2. Read all student count
    # 3. Read male student count
    # 4. Read male student count
    # 5. Read faculty count
    # 6. Read all student's full_name & stu_id for student list
    # 7. Read student's info for View Profile
    # 8. Search student by ful_name or stu_id
    # 9. Delete student by viewed profile
    # 10. Update student by viewed profile
    # 11. Create student account

    def get_student_count(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM student_tbl"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_female_count(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM student_tbl WHERE stu_sex = 'Female'"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_male_count(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM student_tbl WHERE stu_sex = 'Male'"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_faculty_count(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM faculty_tbl"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_students(self):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT stu_full_name, stu_id FROM student_tbl ORDER BY stu_id ASC"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_student_profile(self, stu_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM student_tbl WHERE stu_id = %s"
            cursor.execute(query, (stu_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def is_student_username_taken(self, username):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM student_tbl WHERE stu_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def enroll_student(self, first_name, middle_name, last_name,birth_date, sex, username, password, phone_number, lrn, citizenship, email, religion, address):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "INSERT INTO student_tbl (stu_first_name, stu_middle_name, stu_last_name, stu_birthdate, stu_sex, stu_username, stu_password, stu_phone_number, stu_lrn, stu_citizenship, stu_emailadd, stu_religion, stu_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (first_name, middle_name, last_name,birth_date, sex, username, password, phone_number, lrn, citizenship, email, religion, address))
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                return True
            else:
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def update_student_pfp(self, stu_id, file_name):
        conn = self.db.get_connection()

        if not conn:
            return None


        try:
            cursor = conn.cursor()
            query = "UPDATE student_tbl SET profile_picture = %s WHERE stu_id = %s"
            cursor.execute(query, (file_name, stu_id))
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                print("Profile picture updated successfully!")
                return True
            else:
                print("Failed to upload profile picture")
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def expel_student(self, stu_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "DELETE FROM student_tbl WHERE stu_id = %s"
            cursor.execute(query, (stu_id,))
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                print("Student Expelled")
                return True
            else:
                print("Student was not expelled")
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def update_student_profile(self, stu_id, new_username, new_password, new_birthdate, new_phone_number, new_emailadd,
                               new_address, new_lrn, new_citizenship, new_religion, new_sex):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "UPDATE student_tbl SET stu_username = %s, stu_password = %s, stu_birthdate = %s, stu_phone_number = %s, stu_emailadd = %s, stu_address = %s, stu_lrn = %s, stu_citizenship = %s, stu_religion = %s, stu_sex = %s WHERE stu_id = %s"
            cursor.execute(query, (
            new_username, new_password, new_birthdate, new_phone_number, new_emailadd, new_address, new_lrn,
            new_citizenship, new_religion, new_sex, stu_id))
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                return True
            else:
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()


    def get_faculties(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT f.fac_id, f.fac_full_name, c.cou_name AS course_name FROM faculty_tbl AS f LEFT JOIN course_tbl AS c ON f.fac_id = c.fac_id_fk"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_faculty_students(self, fac_id):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT DISTINCT s.stu_id, s.stu_full_name FROM apply_tbl a JOIN student_tbl s ON a.stu_id_fk = s.stu_id JOIN course_tbl c ON a.cou_id_fk = c.cou_id JOIN faculty_tbl f ON c.fac_id_fk = f.fac_id WHERE f.fac_id = %s"
            cursor.execute(query, (fac_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()
