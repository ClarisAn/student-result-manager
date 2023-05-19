import os
import datetime
import re
import logging
from main.src.database.database import Database

logging.basicConfig(level=logging.INFO)


# Create the class that handles the student information
class StudentManager():

    def create_student_info(self, username, surname, email, dateOfBirth):
        logging.info("ENTERING create_student_info")
        email = email.lower()
        createStudentFlag = True
        response = {"status": "FAILED", "message": ""}

        # Validate all parameters before creating DB entry. Note Email is the PRIM Key (as it's unique)
        if not self.sanitize_name(username):
            createStudentFlag = False
            response["message"] = "Name is not valid"

        if not self.sanitize_name(surname):
            createStudentFlag = False
            response["message"] = "Surname is not valid"

        if not self.sanitize_email(email):
            createStudentFlag = False
            response["message"] = "Email is not valid"

        if not self.sanitize_date(dateOfBirth):
            createStudentFlag = False
            response["message"] = "Date is not valid. Should be in format YYYY-MM-DD"
        else:
            if not self.check_age(dateOfBirth):
                createStudentFlag = False
                response["message"] = "Student is not old enough. Younger than 10 years."

        # Only is all parameters are valid, create student entry in DB
        if createStudentFlag:
            response["status"] = "SUCCESS"
            logging.info("Parameters are all valid. Creating student entry on DB...")
            # Call the database class
            logging.info("Calling database connector class...")

            database = Database(user=os.environ['dbUserName'],
                                password=os.environ['dbPwd'],
                                host=os.environ['dbHost'],
                                port=os.environ['dbPort'],
                                database=os.environ['dbName'],
                                reconnect="False")
            try:
                database.execute(
                    "INSERT INTO students(email, firstname, surname, dob) VALUES('{}', '{}', '{}', '{}');".format(email,
                                                                                                                  username,
                                                                                                                  surname,
                                                                                                                  dateOfBirth))
                database.close()
            except Exception as error:
                logging.error(error)
                response['message'] = "Query failed to execute. Check logs"
                response['status'] = 'FAILED'

        logging.info("EXITING create_student_info")
        return response

    def get_all_student_info(self):
        logging.info("ENTERING get_all_student_info")
        response = {"status": "SUCCESS", "message": ""}

        # Call the database class
        logging.info("Calling database connector class...")
        database = Database(user=os.environ['dbUserName'],
                            password=os.environ['dbPwd'],
                            host=os.environ['dbHost'],
                            port=os.environ['dbPort'],
                            database=os.environ['dbName'],
                            reconnect="False")

        try:
            data = database.execute_result("SELECT * FROM students;")
            database.close()

            for item in data:
                item[3] = item[3].strftime("%Y-%m-%d")
            response["message"] = data
        except Exception as error:
            logging.error(error)
            response['message'] = "Query failed to execute. Check logs"
            response['status'] = 'FAILED'
        logging.info("EXITING get_all_student_info")
        return response

    def delete_student(self, email):
        logging.info("ENTERING delete_student")
        response = {"status": "SUCCESS", "message": ""}
        email = email.lower()

        # Check that email is valid before deleting student and result

        if self.sanitize_email(email):
            # Call the database class
            logging.info("Calling database connector class...")
            database = Database(user=os.environ['dbUserName'],
                                password=os.environ['dbPwd'],
                                host=os.environ['dbHost'],
                                port=os.environ['dbPort'],
                                database=os.environ['dbName'],
                                reconnect="False")
            try:
                database.execute("DELETE FROM students WHERE email = '{}';".format(email))
                database.execute("DELETE FROM results WHERE email = '{}';".format(email))
                database.close()
            except Exception as error:
                logging.error(error)
                response['message'] = "Query failed to execute. Check logs"
                response['status'] = 'FAILED'

        else:
            response["status"] = "FAILED"
            response["message"] = "Email is not valid"

        logging.info("EXITING delete_student")
        return response

    # Function for validating an Email
    def sanitize_email(self, email):
        logging.info("ENTERING sanitize_email")
        sanitary = True
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.fullmatch(regex, email)):
            logging.info("Email is valid")
        else:
            sanitary = False
            logging.error("Email is invalid")
        logging.info("EXITING sanitize_email")
        return sanitary

    # Function to check that string is not empty
    def sanitize_name(self, name):
        logging.info("ENTERING sanitize_name")
        sanitary = True
        if len(name) == 0 or name.isspace():
            logging.error("Empty or whitespace")
            sanitary = False
        logging.info("EXITING sanitize_name")
        return sanitary

    # Function to check that date is in correct format
    def sanitize_date(self, dateOfBirth):
        logging.info("ENTERING sanitize_date")
        sanitary = True
        try:
            datetime.date.fromisoformat(dateOfBirth)
            if dateOfBirth.strip() == "":
                sanitary = False
        except ValueError:
            sanitary = False
            logging.error("Incorrect data format, should be YYYY-MM-DD")
        logging.info("EXITING sanitize_date")
        return sanitary

    # Function to check that student is older than 10 years
    def check_age(self, dateOfBirth):
        logging.info("ENTERING check_age")
        oldEnoughFlag = False

        # Format date string to date format/data type
        dateOfBirth = datetime.date.fromisoformat(dateOfBirth)
        today = datetime.date.today()
        age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
        if age > 10:
            oldEnoughFlag = True
            logging.info('Student is older than 10 years')
        logging.info("EXITING check_age")
        return oldEnoughFlag
