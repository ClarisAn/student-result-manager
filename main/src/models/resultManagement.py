import os
import uuid
import logging
from main.src.database.database import Database

logging.basicConfig(level=logging.INFO)

# Set Global Variable Score
scoreList = ['A', 'B', 'C', 'D', 'F']


# Create the class that handles the course information
class ResultsManager():

    def add_result(self, name, surname, email, course, code, score):
        logging.info("ENTERING add_result")
        email = email.lower()
        response = {"status": "FAILED", "message": ""}

        # Check that name, surname or email exists before adding score
        responseStudent = self.check_student_exists(name, surname, email)
        responseCourse = self.check_course_exists(code, course)
        responseResult = self.check_result_exists(code, email)

        # Only is all parameters are valid, create student entry in DB
        if (responseStudent['status'] == "SUCCESS") and (responseCourse['status'] == "SUCCESS") and (
                responseResult['status'] == "SUCCESS"):

            logging.info("User and Course information is valid")

            if score.upper() in scoreList:
                response["status"] = "SUCCESS"

                # Call the database class
                logging.info("Calling database connector class...")

                database = Database(user=os.environ['dbUserName'],
                                    password=os.environ['dbPwd'],
                                    host=os.environ['dbHost'],
                                    database=os.environ['dbName'],
                                    port=os.environ['dbPort'],
                                    reconnect="False")

                student = name + ' ' + surname
                id = str(uuid.uuid4())
                logging.debug("About to execute: {}".format('''INSERT INTO results(id, email, course, code, student, score) 
                    VALUES('{}','{}', '{}', '{}', '{}', '{}');'''.format(
                    id,
                    email,
                    course,
                    code,
                    student,
                    score)))

                database.execute(
                    '''INSERT INTO results(id, email, course, code, student, score) 
                    VALUES('{}','{}', '{}', '{}', '{}', '{}');'''.format(
                        id,
                        email,
                        course,
                        code,
                        student,
                        score))
                database.close()

            else:
                response['message'] = 'Invalid score provided'
        else:
            response['message'] = 'Course or Student Does Not Exist'
        logging.info("EXITING create_student_info")
        return response

    def get_all_results(self):
        logging.info("ENTERING get_all_results")

        response = {"status": "SUCCESS", "message": ""}

        # Call the database class
        logging.info("Calling database connector class...")

        database = Database(user=os.environ['dbUserName'],
                            password=os.environ['dbPwd'],
                            host=os.environ['dbHost'],
                            port=os.environ['dbPort'],
                            database=os.environ['dbName'],
                            reconnect="False")

        response['message'] = database.execute_result("SELECT course,student,score FROM results;")
        database.close()
        logging.info("EXITING get_all_results")
        return response

    def check_student_exists(self, name, surname, email):
        logging.info("ENTERING check_student_exists")
        response = {"status": "SUCCESS", "message": ""}

        # Call the database class
        logging.info("Calling database connector class...")

        database = Database(user=os.environ['dbUserName'],
                            password=os.environ['dbPwd'],
                            host=os.environ['dbHost'],
                            database=os.environ['dbName'],
                            port=os.environ['dbPort'],
                            reconnect="False")

        data = database.execute_result(
            "SELECT * FROM students WHERE LOWER(email)=LOWER('{}') AND LOWER(firstname)=LOWER('{}') "
            "and LOWER(surname)=LOWER('{}') ;".format(email,
                                                      name,
                                                      surname))

        if len(data) != 1:
            logging.error("Student does not exist or more than one user. Use email for search.")
            response['message'] = "Student does not exist or more than one user. Use email for search."
            response['status'] = 'FAILED'
        logging.info("EXITING check_student_exists")
        return response

    def check_course_exists(self, code, course):
        logging.info("ENTERING check_course_exists")
        response = {"status": "FAILED", "message": "Course does not exist"}

        # Call the database class
        logging.info("Calling database connector class...")

        database = Database(user=os.environ['dbUserName'],
                            password=os.environ['dbPwd'],
                            host=os.environ['dbHost'],
                            database=os.environ['dbName'],
                            port=os.environ['dbPort'],
                            reconnect="False")

        data = database.execute_result(
            "SELECT * FROM courses WHERE UPPER(code)=UPPER('{}') AND LOWER(course)=LOWER('{}') ;".format(code, course))

        if len(data) >= 1:
            logging.error("Course exists")
            response['status'] = 'SUCCESS'
            response['message'] = ''
        logging.info("EXITING check_course_exists")
        return response

    def check_result_exists(self, code, email):
        logging.info("ENTERING check_result_exists")
        response = {"status": "SUCCESS", "message": ""}

        # Call the database class
        logging.info("Calling database connector class...")

        database = Database(user=os.environ['dbUserName'],
                            password=os.environ['dbPwd'],
                            host=os.environ['dbHost'],
                            database=os.environ['dbName'],
                            port=os.environ['dbPort'],
                            reconnect="False")

        data = database.execute_result(
            "SELECT * FROM results WHERE UPPER(code)=UPPER('{}') AND LOWER(email)=LOWER('{}') ;".format(code, email))
        logging.debug("There exists: {} entries".format(str(len(data))))
        if len(data) >= 1:
            logging.error("Result Already Exists.")
            response['message'] = "Course does not exist."
            response['status'] = 'FAILED'
        logging.info("EXITING check_result_exists")
        return response
