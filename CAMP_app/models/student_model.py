import mysql

class StudentModel:
    def __init__(self, database):
        self.db = database

    def get_courses(self, stu_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = query = """
    SELECT 
        course_tbl.cou_id AS course_id,  
        course_tbl.cou_name AS course_name, 
        apply_tbl.raw_grade AS raw_grade,
        apply_tbl.final_grade AS final_grade,
        CONCAT(
            faculty_tbl.fac_first_name, ' ', 
            IFNULL(faculty_tbl.fac_middle_name, ''), ' ', 
            faculty_tbl.fac_last_name
        ) AS assigned_professor
    FROM apply_tbl
    INNER JOIN course_tbl ON apply_tbl.cou_id_fk = course_tbl.cou_id
    INNER JOIN faculty_tbl ON course_tbl.fac_id_fk = faculty_tbl.fac_id
    WHERE apply_tbl.stu_id_fk = %s
"""
            cursor.execute(query, (stu_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def update_student_info(self, updated_data, stu_id):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # ❌ Remove 'stu_full_name' if it exists (since it's auto-generated)
            if "stu_full_name" in updated_data:
                del updated_data["stu_full_name"]

            # Build the SET clause dynamically
            set_clause = ", ".join(f"{key} = %s" for key in updated_data.keys())

            # Prepare the query
            query = f"""
                UPDATE student_tbl
                SET {set_clause}
                WHERE stu_id = %s
            """

            # Convert dictionary values to a list and append stu_id
            values = list(updated_data.values()) + [stu_id]

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error updating student information:", err)

    def fetch_courses(self, student_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """SELECT 
                c.cou_id, 
                c.cou_name, 
                f.fac_full_name
            FROM course_tbl c
            JOIN faculty_tbl f ON c.fac_id_fk = f.fac_id
            WHERE NOT EXISTS (
                SELECT 1 
                FROM apply_tbl a
                WHERE a.cou_id_fk = c.cou_id
                AND a.stu_id_fk = %s
            )"""  # <-- Closing parenthesis added here

            cursor.execute(query, (student_id,))  # Pass the parameter properly
            result = cursor.fetchall()
            cursor.close()
            return result

        except mysql.connector.Error as error:
            print("Database error:", error)
            return None

        finally:
            conn.close()
    def get_sched(self, stu_id):
            conn = self.db.get_connection()

            if not conn:
                return None

            try:
                cursor = conn.cursor(dictionary=True)
                query = """SELECT * 
                    FROM db_camp.student_schedule
                    WHERE student_id = %s;
                    """
                cursor.execute(query, (stu_id,))
                result = cursor.fetchall()
                cursor.close()
                return result
            except mysql.connector.Error as error:
                print(error)
                return None
            finally:
                conn.close()

    def apply_for_course(self, stu_id, cou_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                INSERT IGNORE INTO apply_tbl (stu_id_fk, cou_id_fk)
                VALUES (%s, %s)
            """
            cursor.execute(query, (stu_id, cou_id))  # ✅ Pass values here!
            conn.commit()  # ✅ Commit the transaction
            cursor.close()
            return True  # ✅ Indicate success
        except mysql.connector.Error as error:
            print("Database Error:", error)
            return None
        finally:
            conn.close()

    def add_eval(self, student_id, professor_id, rating, comment):
        conn = self.db.get_connection()

        if not conn:
            print("Database connection failed.")
            return None

        try:
            cursor = conn.cursor(dictionary=True)  # Ensure dictionary cursor is supported
            query = """ 
                INSERT INTO evaluational_tbl (stu_id_fk, fac_id_fk, eval_rating, eval_comment, eval_date)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(query, (student_id, professor_id, rating, comment))
            conn.commit()  # Commit transaction
            print("Evaluation successfully added.")

        except Exception as e:
            print(f"Error adding evaluation: {e}")
            conn.rollback()  # Rollback in case of error

        finally:
            cursor.close()  # Close cursor
            conn.close()  # Close connection
