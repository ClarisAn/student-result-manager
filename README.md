# Student Result Management System

This is a README file for a Student Result Management System built using Flask application in Python 3, with PostgreSQL as the database.

## Description

The Student Result Management System is a web-based application that allows users to manage and store student information, their courses and results. It is built using the Flask framework in Python 3 and utilizes a PostgreSQL database for data storage.


## Prerequisites
Before running the Flask app, make sure you have the following installed:

- Python 3.x
- Flask
- PostgresSQL

Optional
- Docker

### Installation

1. Clone the repository:

   ```bash
   gh repo clone ClarisAn/student-result-manager
   ```

2. Navigate to the project directory:

   ```bash
   cd student-result-manager
   ```

3. Create a virtual environment:

   ```bash
   python3 -m venv env
   ```

4. Activate the virtual environment:

   ```bash
   source env/bin/activate
   ```

5. Install the required dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

6. Set up the PostgreSQL database:

   - Create a new database in PostgreSQL.
   - Use new Postgres credentials in .env file

7. Set up database:
   Create the database tables using the provided schemas
   ```sql
    CREATE TABLE students (
    email VARCHAR ( 255 ) PRIMARY KEY,
    firstName VARCHAR ( 255 ) NOT NULL,
    surName VARCHAR ( 255 ) NOT NULL,
    dob date NOT NULL); 

    CREATE TABLE course (
    coursecode VARCHAR ( 6 ) PRIMARY KEY,
    course VARCHAR ( 255 ) UNIQUE NOT NULL); 

    CREATE TABLE results (
    id VARCHAR (255) PRIMARY KEY,
    email VARCHAR ( 255 ) NOT NULL,
    course VARCHAR ( 255 ) NOT NULL,
    code VARCHAR ( 6 )  NOT NULL,
    student  VARCHAR ( 255 ) NOT NULL,
    score VARCHAR ( 1 ) NOT NULL);
   ```

8. SetUp Environment Variables. Create a file .env

```bash
dbName=pgName
dbPwd=pgPassword
dbUserName=pgName
dbHost=host
dbPort=portNo
```

Structure

```project
+-- student-result-manager
|   +-- .env
```       
                  
 
### Usage

#### bash
1. Start the Flask App:

```bash
   python3 app.py
```

2. By default, the application will run on `http://localhost:5050/`.

3. Access the application in your web browser or on Postman etc.

#### docker (OPTIONAL)
Steps 1 & 2 are for context. Execute step 3 to build and run docker container

1. Run the dockerfile to build image

```bash
   docker build --tag python-docker .
```
2. Run docker image

```bash
    docker run -p 5050:5050 -d python-docker
```
3. Run the docker-compose.yml to create docker image
   
```bash
  docker-compose build
  docker-compose up
````

### Features

The Student Result Management System includes the following features:

- Student management: Add, view and delete student records. 
- Result management:  Add, view and delete courses.
- Course Managment:  Add and view student results.

### Future Features 

1. User Authentication (0Auth2)
   User registration and login functionality to ensure secure access.
   Different user roles with appropriate permissions.
2. Functional tests
3. Performance test
4. App to auto build tables for database


### Contributing

Contributions are welcome! If you find any issues or want to enhance the application, feel free to open a pull request.

### Contact

For any inquiries or questions, please contact clarissa1coetzee@gmail.com

Thank you for using the Student Result Management System!