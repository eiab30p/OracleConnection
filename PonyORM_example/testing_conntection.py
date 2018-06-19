"""
PonyOrm attempt to Integrate with Oracle.

Below is an overly commented and overly detailed
example of how to connect to Oracle by using Libraries
that work really well with PonyORM (AS OF 6/13/18). The
documentation for each Library can be found in the
Readme File.

Libraries
 - Flask-Script: extension provides support for writing external scripts in Flask
                - Running development Server
                - Custom Python Shell
                - Scripts to DB
                - Cronjobs
                - Other Command Line Needs
 - CX_Oracle: Python interface with Oracle Database

 The example below for Pony is a little bit more intensive thank SQLAlchemy because
 SQLAlchemy is more normalized (?) compared to Pony. To fully understand PonyORM a 
 more detailed example needs to be given.
"""

from flask import Flask, request, jsonify
from flask_script import Manager, Command, Server
from pony import orm
from pony.orm.core import *
from pony.orm import *
from datetime import datetime, date
import cx_Oracle
from decimal import Decimal
# This is how we connect to Oracle. 
## This will be in a settings or config file but it
## needs to be in a json format.
db_params = {
        'provider': 'oracle',
        'user':'eddy',
        'password':'password',
        'dsn':'xe',
        'migration_dir': './migrations'
}

# Creating the flask app
app = Flask(__name__)

# creating a database object
db = Database()
# This will be False in Production but when 
## debuging Pony you can see the SQL commands running
## in the background.
sql_debug(True)

# Initializing Manager Instance so Manger can keep 
## track of all commands 
manager = Manager(app, db)

# The below example is the Entity or Tables we will use for this example. 
##This is a school schedule for a College where these are different examples
##of relationships between the tables.
class Department(db.Entity):
    """
    Department Entity.

    Department table will have a unique number and name, which
    has groups and courses.

    """

    number = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    groups = Set("Group")
    courses = Set("Course")

class Group(db.Entity):
    """
    Group Entity.

    Group Entity has a unique number, a major, belongs to
    a department, and can have multiple students.
    """

    number = PrimaryKey(int)
    major = Required(str)
    dept = Required("Department")
    students = Set("Student")

class Course(db.Entity):
    """
    Course Entity.

    Courses Entity needs to have name, semester, lecture hours,
    number of credits, belongs to a department, and professor. 
    Students can be assigned to a course and the name and semester 
    must be unique.
    """

    name = Required(str)
    semester = Required(int)
    lect_hours = Required(int)
    lab_hours = Required(int)
    credits = Required(int)
    dept = Required(Department)
    students = Set("Student")
    professor = Required("Professor")
    PrimaryKey(name, semester)

class Student(db.Entity):
    """
    Student Entity.

    Student Entity must have name, date of birth, and belongs to a group.
    Students can have a professor and can be assigned a course.

    PonyORM uses byte type for images and files.
    """

    name = Required(str)
    tel = Optional(str)
    picture = Optional(bytes)
    dob = Required(date)
    gpa = Required(float, default=0)
    mentor = Optional("Professor")
    group = Required("Group")
    courses = Set("Course")

class Professor(db.Entity):
    """
    Professor Entity.

    Professor Entity are required to have a name and a degree. 
    They can have one or more students or courses.
    """

    name = Required(str)
    tel = Optional(str)
    degree = Required(str)
    students = Set("Student")
    courses = Set("Course")


class DBRegUser(Command):
    """
    DBRegUser.

    This class is used by manager to run the script 
    to insert data in the database as a test. 

    It is called by python testing_conntection.py dbCreateRegUser
    """

    def __init__(self, db):
        """initializes database object."""

        self.db = db

    # You can add paramaters to db_session such as serializable =True
    @orm.db_session
    def run(self):
        """
        run function.

        This is inserting all the information needed for this test. 
        Normally would call a library or helper function.
        """
    
        d1 = Department(name="Department of Computer Science")
        d2 = Department(name="Department of Mathematical Science")
        d3 = Department(name="Department of Applied Physics")

        g101 = Group(number=101, major='B.E. in Computer Engineering', dept=d1)
        g102 = Group(number=102, major='B.S./M.S. in Computer Science', dept=d1)
        g103 = Group(number=103, major='B.S. in Applied Mathematics and Statistics', dept=d2)
        g104 = Group(number=104, major='B.S./M.S. in Pure Mathematics', dept=d2)
        g105 = Group(number=105, major='B.E. in Electronics', dept=d3)
        g106 = Group(number=106, major='B.S./M.S. in Nuclear Engineering', dept=d3)

        p1 = Professor(name="Teddy", degree="PhD in Computer Science")
        p2 = Professor(name="Freddy", degree="PhD in Mathematical Science") 
        p3 = Professor(name="Eddy", degree="PhD in Applied Physics")

        c1 = Course(name="Web Design", semester=1, dept=d1,
                    lect_hours=30, lab_hours=30, credits=3, professor=p1)
        c2 = Course(name="Data Structures and Algorithm", semester=3, dept=d1,
                    lect_hours=40, lab_hours=20, credits=4, professor=p1)

        c3 = Course(name="Linear Algebra", semester=1, dept=d2,
                    lect_hours=30, lab_hours=30, credits=4, professor=p2)
        c4 = Course(name="Thermodynamics", semester=2, dept=d2,
                    lect_hours=50, lab_hours=25, credits=5, professor=p2)
        
        c5 = Course(name="Statistical Methods", semester=2, dept=d3,
                    lect_hours=25, lab_hours=40, credits=4, professor=p2)
        c6 = Course(name="Quantum Mechanics", semester=3, dept=d3,
                    lect_hours=40, lab_hours=30, credits=5, professor=p2)

        s1 = Student(name='John Smith', dob=date(2008, 6, 10), tel='407-484-6711', gpa=4, group=g101,
                     courses=[c1, c2, c4, c6])
        s2 = Student(name='Jan Doe', dob=date(1998, 7, 20), tel='407-484-6712', gpa=3.3, group=g101,
                     courses=[c1, c3, c4, c5])
        s3 = Student(name='Johnny Depp', dob=date(2018, 8, 30), tel='407-484-6713', gpa=2.5, group=g101,
                     courses=[c3, c5, c6])
        s4 = Student(name='Charlie Sheen', dob=date(2018, 9, 1), tel='407-484-6714', gpa=3.5, group=g102,
                     courses=[c1, c4, c5, c6])
        s5 = Student(name='Ann Smith', dob=date(2008, 10, 10), tel='407-484-6715', gpa=3, group=g102,
                     courses=[c1, c2, c4, c6])
        s6 = Student(name='Joe Smith', dob=date(1998, 11, 20), tel='407-484-6716', gpa=3.1, group=g102,
                     courses=[c1, c2, c5])
        s7 = Student(name='Ann Lovelace', dob=date(1988, 12, 30), tel='407-484-6710', gpa=4, group=g102,
                     courses=[c1, c3, c5, c6])
        # Always put a commit function once you have completed inserting data.
        commit()


class GetData(Command):
    """
    GetData Class.

    For some reason I needed another command to pull in information. 
    It is cleaner just an extra command when running. 

    You would call this class by running python testing_conntection.py GetData
    """

    def __init__(self, db):
        """initializes database object."""

        self.db = db

    # You can add paramaters to db_session such as serializable =True
    @orm.db_session
    def run(self):
        """
        run function.

        This is console print out the results of the data entered.
        by creation command. Mostly it is examples of different
        types of queries.
        """

        print("Studnets Names: ")
        students = select(s for s in Student)
        for s in students:
            print(s.name)
        print()

        print("Student Name starts with A: ")
        students = select(s for s in Student if s.name.startswith("A"))
        for s in students:
            print(s.name)
        print()

        print("Students in Computer Science")
        students = select(s for s in Student 
                          if s.group.dept.name == "Department of Computer Science")
        for s in students:
            print(s.name)
        print()

        print("Professors Name: ")
        professors = select(p for p in Professor)
        for p in professors:
            print(p.name)
        print()

        print("Professor Freddy's Classes: ")
        professor = select(p for p in Professor if p.name == "Freddy")
        for p in professor:
            print(p.courses.name)
        print()

        print("Courses and there Professor")
        course = select(c for c in Course)
        for c in course:
            print("Course: ", c.name, "     Professor: ", c.professor.name)
        print()

@app.before_request
def _():
    """Connection establish before request."""
        orm.db_session.__enter__()

@app.after_request
def _(response):
    """Terminate Connection after request."""
        orm.db_session.__exit__()
        return response

# Below are command line calls to run different classes.
manager.add_command('dbCreateRegUser', DBRegUser(db))
manager.add_command('GetData', GetData(db))

if __name__ == '__main__':
        db.connect(allow_auto_upgrade=True, **db_params)
        manager.run()
