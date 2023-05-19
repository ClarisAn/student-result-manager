'''
Unit Tests for Student Result Manager App
'''
import os
import unittest
from main.src.models.studentManagement import StudentManager
from main.src.database.database import Database
from main.src.models.courseManagement import CourseManager
from main.src.models.resultManagement import ResultsManager

# Declare class in order to test functions in class

student_manager = StudentManager()
course_manager = CourseManager()
result_manager = ResultsManager()


class Test(unittest.TestCase):
    # Unit Tests for Database Class

    def test_connection(self):
        database = Database(user=os.environ['dbUserName'],
                            password=os.environ['dbPwd'],
                            host=os.environ['dbHost'],
                            port=os.environ['dbPort'],
                            database=os.environ['dbName'],
                            reconnect="False")

        result = database.connect(retry_counter=0)
        database.close()
        self.assertIsNone(result)

    def test_query(self):
        database = Database(user=os.environ['dbUserName'],
                            password=os.environ['dbPwd'],
                            host=os.environ['dbHost'],
                            port=os.environ['dbPort'],
                            database=os.environ['dbName'],
                            reconnect="False")

        result = database.execute("SELECT * FROM results WHERE id = '';")
        self.assertIsNone(result)

    # Unit Tests for Student Management Class
    def test_student_age(self):
        result = student_manager.check_age('1993-05-08')
        self.assertEqual(result, True)

    def test_student_mail(self):
        result = student_manager.sanitize_email('test@gmail.com')
        self.assertEqual(result, True)

    def test_student_name(self):
        result = student_manager.sanitize_name('John')
        self.assertEqual(result, True)

    def test_all_students(self):
        result = student_manager.get_all_student_info()
        self.assertIsNotNone(result)

    # Unit Tests for Course Management Class
    def test_all_courses(self):
        result = course_manager.get_all_courses()
        self.assertIsNotNone(result)

    def test_course_add(self):
        result = course_manager.create_course_info("TEST01", "Testing")
        status = result['status']
        self.assertEqual(status, 'SUCCESS')

    def test_course_delete(self):
        result = course_manager.delete_course("TEST01")
        status = result['status']
        self.assertEqual(status, 'SUCCESS')

    def test_code(self):
        result = course_manager.check_code("TEST01")
        self.assertEqual(result, True)

    # Unit Tests for Course Management Class
    def test_all_results(self):
        result = result_manager.get_all_results()
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
