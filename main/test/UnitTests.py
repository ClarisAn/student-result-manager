'''
Unit Tests for Student Result Manager App
'''
import os
import unittest
from main.src.models.studentManagement import StudentManager
from main.src.database.database import Database

# Declare class in order to test functions in class

student_manager = StudentManager()


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

        result = database.execute('SELECT * FROM students')
        self.assertIsNotNone(result)

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


if __name__ == '__main__':
    unittest.main()
