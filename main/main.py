from flask import Flask, render_template, request
from main.src.models.studentManagement import StudentManager
from main.src.models.courseManagement import CourseManager
from main.src.models.resultManagement import ResultsManager
import logging

app = Flask(__name__)


# home page
@app.route('/')
def index():
    return 'Hello World!'


@app.route('/students', methods=('GET', 'POST', 'DELETE'))
def student():
    student_manager = StudentManager()
    if request.method == 'POST':
        logging.info("Create new student entry")

        # Make sure that the user does not use whitespaces
        name = request.form['name'].strip()
        surname = request.form['surname'].strip()
        email = request.form['email'].strip().lower()
        dateOfBirth = request.form['date_of_birth'].strip()
        response = student_manager.create_student_info(name, surname, email, dateOfBirth)

    elif request.method == 'GET':
        logging.info("Get All Student Information")
        response = student_manager.get_all_student_info()

    elif request.method == 'DELETE':
        logging.info("Delete Student")
        email = request.form['email'].strip().lower()
        response = student_manager.delete_student(email)

    else:
        response = {'status': 'FAILED', 'message': 'No action for method'}

    return response


@app.route('/courses', methods=('GET', 'POST', 'DELETE'))
def courses():
    course_manager = CourseManager()
    if request.method == 'POST':
        logging.info("Create course")
        code = request.form['code'].strip().upper()
        courseDescription = request.form['course']
        response = course_manager.create_course_info(code, courseDescription)

    elif request.method == 'GET':
        logging.info("Get All Courses")
        response = course_manager.get_all_courses()

    elif request.method == 'DELETE':
        logging.info("Delete course")
        code = request.form['code'].strip().upper()
        response = course_manager.delete_course(code)

    else:
        response = {'status': 'FAILED', 'message': 'No action for method'}

    return response


@app.route('/results', methods=('GET', 'POST', 'DELETE'))
def results():
    result_manager = ResultsManager()
    if request.method == 'POST':
        logging.info("Provide student and course result")
        code = request.form['code'].strip().upper()
        courseDescription = request.form['course']
        name = request.form['name'].strip()
        surname = request.form['surname'].strip()
        email = request.form['email'].strip().lower()
        score = request.form['score'].strip().upper()

        response = result_manager.add_result(name, surname, email, courseDescription, code, score)

    elif request.method == 'GET':
        logging.info("Get results")
        response = result_manager.get_all_results()

    else:
        response = {'status': 'FAILED', 'message': 'No action for method'}

    return response
