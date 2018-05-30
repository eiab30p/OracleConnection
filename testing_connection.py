"""
Oracle Flask SqlAlechmy Security.

The example is a long single file example of
 - Connecting to Oracle Express 11g
 - Setting Up FLask Security
 - Setting up Flask-SQLAlchemy
 - Setting up Flask_Migration

The idea of these three libraries is to establish a 
basic understanding on how to use SQLAlchemy with Oracle
and create a basic security understanding for users while
maintaining SQL iterations and updates.

This code does not have a user front end, it is just simply 
an example with hardcoded examples in this file. For a full 
detailed example look for microfi in my github.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command, Server
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate, MigrateCommand
from flask_security import Security, RoleMixin, UserMixin
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password
from os.path import join, dirname

###### EXTRA CODE FOR Future Projects ######

# from dotenv import load_dotenv
# import os
# Reading enviorment var. from .env file
# dotenv_path = join(dirname(__file_), '.env')
# load_dotenv(dotenv_path, verbose=True)
# Use the Below format when getting URI from .env file
# SQLALCHEMY_DATABASE_URI = os.environ.get('SQL_TYPE') + '://'\
#         + os.environ.get('SQL_USERNAME') + ':'\
#         + os.environ.get('SQL_PASSWORD') + '@'\
#         + os.environ.get('SQL_IP') + ':'
#         + os.environ.get('SQL_PORT') 
#         + '/' + os.environ.get('SQL_DBNAME') + ''


# Creating the Flask App
app = Flask(__name__)

# Creating envirorment variable normaly done in config.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://eddy:password@localhost:1521/xe'
app.config['SQLALCHEMY_MIGRATE_REPO'] = join(dirname(__file__), 'db_repository')
app.config['SECRET_KEY'] = 'RANDOMLETTERSFWLFHO212421049RFWFO'
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = 'RE2WOROWIER823NVSJNA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Establishing DB connection
db = SQLAlchemy(app)

# Letting Migration tool to mangage upgrades and downgrates to the DB
manager = Manager(app)
migrate = Migrate(app, db)


class Base(db.Model):
        """Base Model CLass.
        
        When called these fields will be added to the table. Prevents duplicated code.
        """
        __abstract__ = True
        id = db.Column(db.Integer, db.Sequence('id'), primary_key=True)

class Role(Base, RoleMixin):
        """
        Role Table.
        
        Simple table that will have the field in base and below to have a workable table.
        
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

# This is the helper table user in User Class for a Many to Many relationship
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
        """

        __tablename__ = 'auth_user'
        username = db.Column(db.String(255), nullable=False, unique=True)
        email = db.Column(db.String(255), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False)
        first_name = db.Column(db.String(255), nullable=False)
        last_name = db.Column(db.String(255))
        active = db.Column(db.Boolean())
        confirmed_at = db.Column(db.DateTime())
        last_login_at = db.Column(db.DateTime())
        current_login_at = db.Column(db.DateTime())
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

# user_datastore come with a great deal of functions for user and role creation. MUST PASS MODELS IN ORDER
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

class DBInit(Command):
        """
        THis Creates SQL Tables from models above.

        There are four manger commands for this. 
                - init: initionalize db
                - migrate: find changes
                - upgrade: upgrade database
                - downgrade: go back to previouse version
        """

        def __init__(self, db):
                """Initionalizes db object."""
                self.db = db

        def run(self):
                """Creates tables."""
                self.db.create_all()

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
                
                users = User.query.all()
                for u in users:
                        print('username:{} email:{} first name:{} last name:{}'.format(u.username, u.email, u.first_name, u.last_name))


manager.add_command('runserver', Server(host='localhost', post=5050))
manager.add_command('dbCreateRegUser', DBRegUser(db))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
        manager.run()
