    


***PonyORM and PonyUp***
PonyORM is like SQLAlchemy 
PonyUp is like Migration or Alembic


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