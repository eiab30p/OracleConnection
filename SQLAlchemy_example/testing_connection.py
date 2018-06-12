"""
SQLAlachemy attempt to intigrate with Oracle.

Below is an overly commented and overly detailed 
example of how to connect to Oracle using Libraries
that work really well with SQLAlachemy. The 
documentation for each Library can be found in the 
Readme File.

Libraries
 - FLask Security: allows a user to quickly add 
        common security mechanisms to your flask application
                - Session Based Authentication
                - Role Management
                - Password Hashing
                - Basic HTTP Authentication
                - Token Based AUthentication / Account Activation / Password Recovery
                - User Registration
                - Login Tracking
                - Json/Ajax Support
 - Flask-Script: extenstion provides support for writing external scripts in Flask
                - Running development Server
                - Customed Python SHell
                - Scripts to DB
                - Cronjobs
                - Other Command Line Needs
 - Flask_Migration: Extension that handles SQLAlchemy Database Migrations using ALembic
 - CX_Oracle: Python interface with Oracle Databse
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_script import Manager, Command, Server
from flask_migrate import Migrate, MigrateCommand
from flask_security import Security, RoleMixin, UserMixin
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password
from os.path import join, dirname


# Creating the Flask App
app = Flask(__name__)

# Creating envirorment variable normaly done in config.py 

# Will Track modifications of objects and emit signals. 
### The default is None, which enables tracking but issues 
### a warning that it will be disabled by default in the future.
### This is more for a future tasks but when using events it will
### help automate task when doing a before or after insert. 
### Possible way to do triggers in python without changing DB
### docs.sqlalchemy.org/en/latest/core/event.html
### https://stackoverflow.com/questions/46044969/place-sqlalchemy-event-listener-on-many-to-many-table
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Connection to the Database. Format is <database type>://<username>:<password>@<ip>:<port>/<database name>
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://EDDY:password@localhost:1521/xe'
# This is used for hashing and other realated Flask_Security Features
app.config['SECRET_KEY'] = 'RANDOMLETTERSFWLFHO212421049RFWFO'
# This is the type of hashed used
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
# This is the salt used for the hash
app.config['SECURITY_PASSWORD_SALT'] = 'RE2WOROWIER823NVSJNA'
# THis is used so that Flask_Security can track user activities
app.config['SECURITY_TRACKABLE'] = True
# see which users have confirmed a new account.
app.config['SECURITY_CONFIRMABLE'] = True

# Establishing DB connection
db = SQLAlchemy(app)

# Initializing Manager instance so Manager can keep track of all commands.
manager = Manager(app)
# Initializing Migrate instance
migrate = Migrate(app, db)


class Base(db.Model):
        """Base Model CLass.
        
        When called, these fields will be added to the table. Prevents duplicated code.

        The format for this is in the column method we select the type which may or may
        not require the max length followed by any number of paramaters. 

        The paramaters used here is creating a Sequence called BASE_SEQ which starts
        at 1 and ofcourse this will be a primary key.

        When inheriting this column the id will be unique sequence just the same name.
        """
        __abstract__ = True
        id = db.Column(db.Integer, db.Sequence('BASE_SEQ', start=1), primary_key=True)

class Role(Base, RoleMixin):
        """
        Role Table.
        
        Simple table that will have the fields in the Base Model with the below table fields.
        
        RoleMixin is used for Flask Security. Mixin for Role model definitions"""

        __tablename__ = 'auth_role'
        name = db.Column(db.String(80))
        description = db.Column(db.String(255))

        def __init__(self, **kwargs):
                """Able to add roles when calling table without issues."""
                super(Role, self).__init__(**kwargs)
        def __repr__(self):
                """Returns Representation of Role Object."""
                return '<Role %r>' % self.name

# This is the helper table used in User Class for a Many to Many relationship
roles_users = db.Table('roles_users',
                        db.Column('user_id', db.Integer(),
                                   db.ForeignKey('auth_user.id')),
                        db.Column('role_id', db.Integer(),
                                   db.ForeignKey('auth_role.id')))

class User (Base, UserMixin):
        """
        User Model.
        
        backref: is a simple way to also declare a new property on the User Class.
        You can now use <role_name>.user to get information.

        lazy: defines when SQLAlchemy will load the data. 
                - 'select' (which is the default) means that SQLAlchemy will load 
                        the data as necessary in one go using a standard select statement.

                - 'joined' tells SQLAlchemy to load the relationship in the same 
                        query as the parent using a JOIN statement.

                - 'subquery' works like 'joined' but instead SQLAlchemy will use a subquery.

                - 'dynamic' is special and useful if you have many items. 
                        Instead of loading the items SQLAlchemy will return 
                        another query object which you can further refine before loading 
                        the items. This is usually what you want if you expect more than a 
                        handful of items for this relationship.

        UserMixin is used for FLask_Security. Mixin for User model definition
        """

        __tablename__ = 'auth_user'
        username = db.Column(db.String(255), nullable=False, unique=True)
        email = db.Column(db.String(255), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False)
        first_name = db.Column(db.String(255), nullable=False)
        last_name = db.Column(db.String(255))
        active = db.Column(db.Boolean(), default=True)
        # Required for Security Trackable and Confirmable
        confirmed_at = db.Column(db.DateTime(null=True))
        last_login_at = db.Column(db.DateTime())
        current_login_at = db.Column(db.DateTime())
        last_login_ip = db.Column(db.String(255))
        current_login_ip = db.Column(db.String(255))
        login_count = db.Column(db.Integer)
        # This is a Many to Many Relationship because I created a helper table
        # A one to Many I would NOT have secondary ex. "backref= 'users', lazy='dynamic'"
        # You can use multiple backref to have your relationship load in the same 
        #               query ex. "backref=db.backref('users,lazy='joined'), lazy='dynamic')"

        roles = db.relationship('Role', secondary=roles_users,
                                backref=db.backref('users', lazy='dynamic'))

        def __repr__(self):
                """Returns Representation of User Object."""
                return '<User %r>' % self.email

# user_datastore come with a great deal of functions for user and role creation. 
## MUST PASS MODELS IN ORDER
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# pass the user_datastore so we can use the Security fetures.
security = Security(app, user_datastore)

# At this point we are getting into FLask_Scripts we are going to create different 
## classes and declare what CLI command is for them
class DBRegUser(Command):
        """
        This creates a user in the DB.
        
        To find out what user_datastore can do look up 
        pythonhosted.org/Flask-Security/api.html
        """

        def __init__(self, db):
                """Initionalizes db object."""
                self.db = db

        def run(self):
                """We are creating a two roles and two users."""
                for i in range(2):
                        try:
                                user_datastore.find_or_create_role(
                                        name='user{}'.format(i),
                                        description='This is {} role'.format(i)
                                )
                                self.db.session.commit()
                       # The IntegrityError is due to duplicates because of how table is made
                        except IntegrityError:
                                pass

                for i in range(2):
                        try:
                                user_datastore.create_user(
                                        username='user{}'.format(i),
                                        email='test{}@test.com'.format(i),
                                        password=encrypt_password('test'),
                                        first_name='Person{}'.format(i),
                                        last_name='Last{}'.format(i)
                                )
                                self.db.session.commit()
                                user_datastore.add_role_to_user('test{}@test.com'.format(i),'user{}'.format(i))
                        # The IntegrityError is due to duplicates because of how table is made
                        except IntegrityError:
                                pass
                # This is the query to get user information
                users = User.query.all()
                for u in users:
                        print('username:{}, email:{}, first name:{}, last name:{}, '.format(u.username, u.email, u.first_name, u.last_name))

# These are the commands used in the CLI

# This the entire application but since we do not have API calles 
## or a Server Class it isn't worth it.
## mifrofi has a working example github.com/eiab30p/microfi
manager.add_command('runserver', Server(host='localhost', post=5050))
# THis will run the create user class mostly for testing
manager.add_command('dbCreateRegUser', DBRegUser(db))
# This calls the Migrate Command to activate migration tool
## You can call any of the following commands after db
## <init> <migrate> <upgrade> <downgrade> <--help>
## ex: python testing_connection db init
manager.add_command('db', MigrateCommand)

# This is just getting the project up and running.
if __name__ == '__main__':
        manager.run()
