# SQLAlachemy attempt to intigrate with Oracle

SQLAlachemy is probably one of the most popular ORMs for python. It has a large community support with lots of library intergration to achive different task with the least amount of code. Normally SQLAlachemy would be my number one choice but due to the need of database version control it is not ideal. The resoults, findings, and code can be found in the directory. EDIT: SQLAlchemy does work!!!!!!!!!!!!!!!!!!!!!!!!

DON'T FORGET TO BE IN YOUR VENV

* SQLAlchemy relies on common design pattern to allow developers to create and ship enterprise-grade, production-ready applications easily.
* Uses Object Pool Pattern to assist in caching frequently used objects instead of creating objects each request such as databse connections. Normally the maximum would be 5 connections when connecting to the database.
* Uses Unit of Work design pattern. It is used to maintain a list of objects affected by a business transaction and to coordinate the writting out of these changes. For SQLAlchemy this is why we uses session.

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

## Query Example

In SQLALchemy we just have one simple query which returns the user but you can do a lot more than just that. Below are other examples of this.

below are a list of functions that can be use when generator query

* all() : returns everything
* count() : returns the total number of rows of a query
* filter() : filters the query by applying criteria
* delete() : removes record that is matching
* distinct() : applies distinct statement
* exists() : adds an exists operator to a subquery
* first() : returns first row
* get() : returns the row referenced by the primary ket parameter passed as argument
* join() : creates a join
* limit() : limits the number of rows returned
* orcer_by() : sets an order in the rows

Below is an example of filter() which should return all movies after 15-01-01

```python
movies = session.query(Movie) \
                .filter(Movie.realse_date > date(2015, 1, 1)) \
                .all()
```

Theres also a filter_by() function which is different below is an example of how it is used. filter_by() uses attributes not objects

```python
db.users.filter_by(name='Jose')
```

Below is an example of a join() which should return all movies Dwayne Johnson participated in

```python
the_rock_movies = session.query(Movie) \
                         .join(Actor, Movie.actors) \
                         .filter(Actor.name == 'Dwayne Johnson') \
                         .all()
```

When returning from a FLask view it is often used to return a 404 error for missing enties. Flask-SQLAlchemy provides a helper for this exact purpose. Instead of using get() you can use get_or_404() or instead of first() you can use first_or_404().

```python
@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)
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

To have auto increamence, WITH ORACLE ONLY, you will need to use Sequence. SqlAlchemy does not know how to create sequences on it's own aparently. Therefore we have to change the upgrade code in the migration folder.

Below is an example sequence. You'll go to your migration folder, then to a version#.py file and under the upgrades function you will need to have line like below. (id is the name of the sequence)

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

##### Events, MapperEvents, and Listeners in SQLAlchemy
Todo: This is a cool feature that could be useful once fully understood.
docs.sqlalchemy.org/en/latest/orm/events.html#mapper-events

## SQLAlchemy Model Column Types

For SQLAlchemy unlike PonyORM they come with column types to assist when creating tables. Below are are a list of column types, which you can see there are a lot of different choices for a column when using SQLAlchemy. PLEASE LOOK UP EACH COLUMN TYPE TO ENSURE YOU ARE USING IT PROPERLY AND IS PERMISTED FOR YOUR DB.

* ARRAY
* BIGINT
* BINARY
* BLOB
* BOOLEAN
* BOOLEANTYPE
* BigInteger
* Binary
* Boolean
* CHAR
* CLOB
* Concatenable
* DATE
* DATETIME
* DECIMAL
* Date
* DateTime
* Emulated
* Enum
* FLOAT
* Float
* INT
* INTEGER
* INTEGERTYPE
* Indexable
* Integer
* Interval
* JSON
* LargeBinary
* MATCHTYPE
* MatchType
* NCHAR
* NULLTYPE
* NUMERIC
* NVARCHAR
* NativeForEmulated
* NullType
* Numeric
* PickleType
* REAL
* SMALLINT
* STRINGTYPE
* SmallInteger
* String
* TEXT
* TIME
* TIMESTAMP
* Time
* Unicode
* UnicodeText
* VARBINARY
* VARCHAR

##### Source

[SQLAlchemy Documentation](sqlalchemy.org)
[Sequence Changes](https://stackoverflow.com/questions/35775342/using-sqlalchemy-with-racle-and-flask-to-create-sequences-for-primary-key?rq=1)
[Sequences in Oracle DB](http://nullege.com/codes/show/src%40r%40g%40RGVRSEF-HEAD%40RGVRSEF%40models.py/9/flask.ext.sqlalchemy.SQLAlchemy.Sequence/python)
[Column Change Detection](blog.code4hire.com/2017/06/setting-up-alembic-to-detect-the-column-length-change/)
[Flask_Migration](flask-migrate.readthedocs.io/en/latest/)
[Flask_Scripts](flask-script.readthedocs.io/en/latest)
[Flask_Security](pythonhosted.org/Flask-Security)
[cx_Oracle](oracle.github.io/python-cx_Oracle)
[SQLALchemy Developer Help](https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/) *GREAT FOR SSO Example*
[Column Type Information](https://docs.sqlalchemy.org/en/latest/core/type_basics.html#generic-types)
[filter() vs filter_by()](https://stackoverflow.com/questions/2128505/whats-the-difference-between-filter-and-filter-by-in-sqlalchemy)
[404 function](flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records)