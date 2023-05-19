import os
import logging
from main.src.database.database import Database

logging.basicConfig(level=logging.INFO)


# Create the class that handles the student information
class CourseManager():

    def create_course_info(self, code, course):
        logging.info("ENTERING create_student_info")
        Flag = True
        response = {"status": "FAILED", "message": ""}
        code = code.upper()

        # Validate all parameters before creating DB entry. Note Email is the PRIM Key (as it's unique)
        if not self.sanitize_name(course):
            Flag = False
            response["message"] = "Name is not valid"

        if not self.check_code(code):
            Flag = False
            response["message"] = "Course Code must have 6 characters"

        # Only is all parameters are valid, create student entry in DB
        if Flag:
            response["status"] = "SUCCESS"
            logging.info("Parameters are all valid. Creating course entry on DB...")
            # Call the database class
            logging.info("Calling database connector class...")

            database = Database(user=os.environ['dbUserName'],
                                password=os.environ['dbPwd'],
                                host=os.environ['dbHost'],
                                port=os.environ['dbPort'],
                                database=os.environ['dbName'],
                                reconnect="False")

            database.execute(
                "INSERT INTO courses(code, course) VALUES('{}', '{}');".format(code, course))
            database.close()
        logging.info("EXITING create_student_info")
        return response

    def get_all_courses(self):
        logging.info("ENTERING get_all_courses")
        response = {"status": "SUCCESS", "message": ""}
        students_info = []
        # Call the database class
        logging.info("Calling database connector class...")

        database = Database(user=os.environ['dbUserName'],
                            password=os.environ['dbPwd'],
                            host=os.environ['dbHost'],
                            database=os.environ['dbName'],
                            port=os.environ['dbPort'],
                            reconnect="False")

        data = database.execute_result("SELECT course FROM courses;")
        response["message"] = data
        logging.info("EXITING get_all_student_info")
        return response

    def delete_course(self, code):
        logging.info("ENTERING delete_course")
        response = {"status": "SUCCESS", "message": ""}
        code = code.upper()

        # Check that course code is valid before deleting

        if self.check_code(code):
            # Call the database class
            logging.info("Calling database connector class...")

            database = Database(user=os.environ['dbUserName'],
                                password=os.environ['dbPwd'],
                                host=os.environ['dbHost'],
                                database=os.environ['dbName'],
                                port=os.environ['dbPort'],
                                reconnect="False")

            database.execute("DELETE FROM courses WHERE code = '{}';".format(code))
            database.execute("DELETE FROM results WHERE code = '{}';".format(code))
        else:
            response["status"] = "FAILED"
            response["message"] = "Course Code is Not Valid"
        logging.info("EXITING delete_student")
        return response

    # Function for checking that code is 6 characters
    def check_code(self, code):
        logging.info("ENTERING check_code")
        passFlag = False
        if len(code) == 6:
            passFlag = True
        logging.info("EXITING check_code")
        return passFlag

    # Function to check that string is not empty
    def sanitize_name(self, name):
        logging.info("ENTERING sanitize_name")
        sanitary = True
        if len(name) == 0 or name.isspace():
            logging.error("Empty or whitespace")
            sanitary = False
        logging.info("EXITING sanitize_name")
        return sanitary
