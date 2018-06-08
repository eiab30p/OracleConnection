# I'm using VS code to dev this project in a Ubuntu Box

The idea of this is to try out oracel to a colse work envirorment as possible. I'll list the libraries and extentions used in this IDE to hopefully better form in the real workstation in 3.0

VS CODE Extentions:

- python (ms-python.python)
- markdown lint (markdownlint)
- pylint()

python3.0:
We are going to work in a virtuall env for this.

- virtualenv (THis is to create an independent virtual env.)
- cx_Oracle (Connection to the oracle DB)
- sqlalchemy (pythonic modualr sql query)

use virtualenv

    - run "python -m venv venv" to get virtual env
    - run "source venv/bin/activate" to get in your virtual env
    - run pip install -r requirements.txt to install python libraries

Once you have all that set up you are good to go. You can now feel free to use the python pip without worries

use migration

    - If it is your first migration you will need to run init to create the repo folder.
        - python testing_connection.py db init
    - Once the folder is created you will need the migration to detect changes in your    tables.
        - python testing_connection.py db migrate
    - *STOP!* At this point you may need to help SQLAlchemy with the upgrade for          Sequencesing *PLEASE LOOK AT NOTES!* Then run the below command
        -python testing_connection.py db upgrade

Run the Application:
Traditionally if I had a front end I would tell you to run it by

    python testing_conntection.py runserver

Since I do not have a front end we are going to use the test case.

    python testing_connection.py dbCreateRegUser

**NOTES Oracle:***

Ensure a user(schema) has all the needed permissions to run queries. Below are the ones I used to achive the bare minimum

    grant CREATE SESSION, ALTER SESSION, CREATE DATABASE LINK, CREATE MATERIALIZED VIEW, CREATE PROCEDURE, CREATE PUBLIC SYNONYM, CREATE ROLE, CREATE SEQUENCE, CREATE SYNONYM, CREATE TABLE, CREATE TRIGGER, CREATE TYPE,CREATE VIEW, UNLIMITED TABLESPACE, DROP ANY SEQUENCE, CREATE SEQUENCE, CREATE ANY SEQUENCE, ALTER ANY SEQUENCE to eddy;

**More Oracle:**
If the application is not connecting to Oracle make sure the listener is running. For Ubunutu below is how I ran it.

    sudo su oracle-xe start

Oracale Express is orginized at XE is your databse and then each user is the schema where you can share schemas between each other and the "OBJECTS" are the tables and other normal databse functions.

**NOTES Migration:**

To have auto increamence you will need to use Sequence. SqlAlchemy does not know how to
create sequences aparently. Therefore we have to change the upgrade code in the migration folder.

    https://stackoverflow.com/questions/35775342/using-sqlalchemy-with-racle-and-flask-to-create-sequences-for-primary-key?rq=1

In your migration folder, version#.py file under upgrades you will need to have something like below.

    op.execute('create sequence id start with 1 increment by 1 nocache nocycle')

Now you can call it in your model as I did in my Base class

**MORE**

The migration only creates tables but does not create modifications in file. Meaning we may need to create our alter statments. FML Below is an example

    def upgrade():
        # ### commands auto generated by Alembic - please adjust! ###
        op.alter_column('auth_user', 'first_name', nullable=False)
        # ### end Alembic commands ###


    def downgrade():
        # ### commands auto generated by Alembic - please adjust! ###
        op.alter_column('auth_user', 'first_name', nullable=True)

     # ### end Alembic commands ###

***PonyORM and PonyUp***
PonyORM is like SQLAlchemy 
PonyUp is like Migration or Alembic


