# SQLAlachemy attempt to intigrate with Oracle

SQLAlachemy is probably one of the most popular ORMs for python. It has a large community support with lots of library intergration to achive different task with the least amount of code. Normally SQLAlachemy would be my number one choice but due to the need of database version control it is not ideal. The resoults, findings, and code can be found in the directory.EDIT: SQLAlchemy does work!!!!!!!!!!!!!!!!!!!!!!!!

DON'T FORGET TO BE IN YOUR VENV

## Installing Libraries

All libraries used and installed will be explained in the code.

* The main library is flask_sqlalchemy-2.3.2
* flask-1.0.2
* flask_script-2.0.6
* flask_migrate-2.1.1
* flask_security-3.0.0
* cx_oracle-6.3.1

To install all libraries you will run the below command.

```sh
pip install -r requirements.txt
```

## Runing the Migration

To run the code for the first time you will need to create the database tables. PLEASE change the database link in the code to your personal one. Please look at notes before running on a live system. In fact DO NOT RUN ON A LIVE SYSTEM WHEN TESTING

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://username:password@localhost:1521/xe'
```

Once the link is completed you will run the following sequence of commands.

##### This is going to create all the scripts to beable to handle the migration including creating a new database table

```sh
python testing_connection.py db init
```

##### This detects the models or tables name and column information. It also creats relation tables that are needed. It will then create a script for when you are ready to migrate the information. This will be in your version directory with a number

```sh
python testing_connection.py db migrate --message "Initional Migration"
```

##### You will run this command when you are ready to change your database. You SHOULD go to your version that you are going to migrate and make any changes if SQLAlchemy Almbric did wrong. Here is where I found for Oracle the table being deleted and recreated. BIG NO NO when data already exists

```sh
python testing_connection.py db upgrade
```

##### If a mistake has happened and you want to revert the change you will simply run a downgrade like below

```sh
python testing_connection.py db downgrade
```

Other db commands that can be used are mentioned below

* < --help >: See available commands
* *additional argument*  < command >  < --multidb >: Manage and migrate multiple databases.
* < revision > : Creates an empty revision script. This is if you want to create manual scripts.
* *optional additonal argument*  migration <--message MESSAGE>: Like git commit -m you should put a message of why the changes and what the changes were
* < current >: Shows the current revision of the database
* *optional additonal argument* < history > < --rev-range REV_RANGE>: This will show a list of migrations. If not range is selected it will show the entire history
* *additional argument* < merge > < --message MESSAGE > < revisions >: THis will Merge two revisions together.

with all of these commands except for help and merge you can add a --sql tag at the end and a print out of the SQL statment will be printed in the console.

## Running Application

If this application had a front end or other applications are going to call the API of this application I would run the below command.

```python
python testing_conntection.py runserver
```

Since I just want to test the table and DB and see what Oracle and do with SQLAlchemy I will just run the blow command which will run a function as explained in the code.

```python
python testing_connection.py dbCreateRegUser
```

## Detecting Column Changes

After running the db init command Alembic does not automaticly add column change detection. Which is a bummber but a simple fix. In the evn.py file  under the migrations directory you will add the below line. **evn.py line 75**

```python
compare_type=True
```

Complete Configuration

```python
 context.configure(connection=connection,
                   target_metadata=target_metadata,
                   compare_type=True,
                   process_revision_directives=process_revision_directives,
                   **current_app.extensions['migrate'].configure_args)
```

## SQLALchemy Sequence Notes Edited: 6/12/2018

~~To have auto increamence, WITH ORACLE ONLY, you will need to use Sequence. SqlAlchemy does not know how to create sequences on it's own aparently. Therefore we have to change the upgrade code in the migration folder.~~

~~Below is an example sequence. You'll go to your migration folder, then to a version#.py file and under the upgrades function you will need to have line like below. (id is the name of the sequence)~~

You can add sequences in the Models in python. You do not have to make changes in the migration but it is nice to know.

```python
op.execute('create sequence id start with 1 increment by 1 nocache nocycle')
```

## SQLAlchemy Alembric Notes Edited: 6/12/2018

~~As mentioned before Alembric does not like Oracle and did not alter the columns as requested. It would delted the DB and apply the changes as if it was a new table or result in an error because the table already exist. If you were like me you just said FML. Well a work around is by hard coding each migration alteration. With this you will need to do an upgrade and downgrade. Below is an example of wow this will look.~~

You do not need to do a manual upgrade or downgrade but is is good to know.

```python

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('auth_user', 'first_name', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('auth_user', 'first_name', nullable=True)
    # ### end Alembic commands ###
```

##### Source

[SQLAlchemy Documentation](sqlalchemy.org)

[Sequence Changes](https://stackoverflow.com/questions/35775342/using-sqlalchemy-with-racle-and-flask-to-create-sequences-for-primary-key?rq=1) <no longer tru>

[Sequences in Oracle DB](http://nullege.com/codes/show/src%40r%40g%40RGVRSEF-HEAD%40RGVRSEF%40models.py/9/flask.ext.sqlalchemy.SQLAlchemy.Sequence/python)

[Column Change Detection](blog.code4hire.com/2017/06/setting-up-alembic-to-detect-the-column-length-change/)

[Flask_Migration](flask-migrate.readthedocs.io/en/latest/)

[Flask_Scripts](flask-script.readthedocs.io/en/latest)

[Flask_Security](pythonhosted.org/Flask-Security)

[cx_Oracle](oracle.github.io/python-cx_Oracle)
