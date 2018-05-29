# I'm using VS code to dev this project in a Ubuntu Box

The idea of this is to try out oracel to a colse work envirorment as possible. I'll list the libraries and extentions used in this IDE to hopefully better form in the real workstation in 3.0

VS CODE Extentions:
python (ms-python.python)
markdown lint (markdownlint)
pylint()

python3.0:
We are going to work in a virtuall env for this.
virtualenv (THis is to create an independent virtual env.)
cx_Oracle (Connection to the oracle DB)
sqlalchemy (pythonic modualr sql query)



use virtualenv by
    - python -m venv venv
    - run it by source venv/bin/activate
You can now feel free to use the python pip without worries




Oracle is all fucked up that you need to create a user to beable to create a table which you also need to allow privilages with it.Weird.

CREATE USER eddy;

GRANT CREATE SESSTION, CREATE TABLE, CREATE VIEW, CREATE TRIGGER to eddy;

Now our schema eddy now you can create objects in your schema.
ex. CREATE TABLE



to share your schema with others you need to grant privileges to do so

SYNONYMS can be aliases for longer reference example below

create public synonym supplies for other_schema.supplies;


CREATE SCHEMA ******DOES NOT CREATE SCHEMA********* it creates objects for the SCHEMA so stupid but your schema is part of the user. # OracleConnection
