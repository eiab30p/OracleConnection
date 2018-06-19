# PonyORM 
PonyORM is the newest ORM available for Python and for multiple other languages. Unfortunently, it does not have the support community as other ORM. Since this is a young library it is still buggy and may need to change conditions in the library itself, especially the migration scripts they have started the library just in the last couple.

# Installing Libraries

All libraries used and installed will be explained in the code.

* The main library is pony-0.7.3
* THis is the migration library bakatrouble-pony-migrate-0.8.dev0
* flask_script-2.0.6
* cx_oracle-6.3.1

To install all libraries you will run the below command.

```sh
pip install -r requirements.txt
```

## Runing the Migration

To run the code for the first time you will need to do is to connect with the db. Change the paramaters in db_parms to your database below is the example used. Please look at notes before running on a live system. In fact DO NOT RUN ON A LIVE SYSTEM WHEN TESTING

```python
db_params = {
        'provider': 'oracle',
        'user':'eddy',
        'password':'password',
        'dsn':'xe',
        'migration_dir': './migrations'
}
```

Once the link is completed you will run the following sequence of commands.

##### You will need to create a migration directory for PonyORM to work

```sh
mkdir migrations
```

##### PonyORM uses two simple commands 'make' which creates a migration script that will need to apply. ENSURE YOU REVIEW THE SCRIPT

```sh
python migrations.py make
```

#### 'apply' which applies the changes into your database. Below is the simple command.

```sh
python migrations.py apply
```

There are other commands you can use as well. They won't be used as much but defiently worth knowing. 

* < apply --fake-initial > : This is used when the tables in the DB are already created.
* < make --empty > : When you need a custom migration due to data change and not a schema change
* < list > : list all migrations, and the + will apply whose changes
* < sql [version#] > : this will show the sql for the migration on x version
* < apply [version#] [version#] > : this will apply all migrations. (inclusive)

## Running Application

If this application had a front end or other applications are going to call the API of this application I would run the below command.

```python
python testing_conntection.py runserver
```

Since I just want to test the table and DB and see what Oracle interacts with PonyORM I will just run the below command which will run a function as explained in the code.

```python
python testing_connection.py dbCreateRegUser
```

For this example I needed to create another script to print out the results to ensure they are bing save. Therefore, I created multiple scripts for this example.

```python
python testing_connection.py GetData
```

## Query Example

In the code there are a few examples of queries mostly with selects with basic loops and inserts.

For inserting records ensure you have the commit() at the end, else it will not commit the data over.

For retrieving data you can use a series of different functions listed below

You declare the object outside of the select function for a lambda

```python
Customer.select(lambda c: c.country =='USA')
```

you can use count() to get a total within your select statment.

```python
select((c.country, count(c)) for c in Customer)
```

You can also chain up different functions as well as use such as

* order_by
* desc
* first
* top three
* left join

Example of an order_by descending by sum and return the first result. So it should return the most popular item.

```python
Product.select().order_by(lambda p : desc(sum(p.order_items.quantity))).first()
```

Example of another order_by but we want to get the first three most caluable customers

```python
Customer.select().order_by(lambda c : desc(sum(c.orders.total_price)))[:3]
```

Example of a left_join which will return cutomers who orders exist. You can use exists() but this is a left_join example

```python
left_join(c for c in Customer for o in c.orders if o is None)
```

Below is an example query when using datatime and timedelta

```python
select(o for o in Order if o.date_created >= date.now() - timedelta(days=3))[:]
```

Translates to

```SQL
SELECT "o"."id", "o"."state", "o."date_created", "o"."date_shipped",
       "o"."date_delivered", "o."total_price", "o"."customer"
FROM "Order" "O"
WHERE "o"."date_created" >= ?
```

DISCTINCT is almsot allways used in queries if you don't you will add .without_distinct() to the end of the query

Below are a list of functions that can be use inside when generator query

* avg() : averages
* abs() : absolute value
* exists() : Does it exist
* len() : length
* max() : maximum
* min() : minimum
* count() : returns a total number
* concat() : Concatenatenates arguments into one string
* random() : selects a random return
* select() : Select the table
* sum() : total by additon
* getattr() : python function that can get attribute value
* between() : returns results between such condtion looks like x >= a AND x<=b

concat() example

```python
select(concat(p.first_name, ' ', p.last_name)for p in Persons)
```

Raw Query Function: You can use two different functions

* select_by_sql()
* get_by_sql()

There isn't a diffirece between the two but the query will NOT return an object but alist of entity instances.

You can also make this pythonic when it comes to paramaters. Below is an exampel of this

```python
Product.select_by_sql("SELECT * FROM Product WHERE price > $x OR price = $( y * 2)", globals={'x':100}, locals={'y':200})
```

Variable and more complex expressions specified after the $ sign, will be automatically calculated and transferred into the query as parameters, which makes SQL-Injections impossible. Ony automatically replaces $x in the query string with "?", "%S" or with other paramstyle, used in your database.

If you need to use the $ sign in the query (for eample, in the name of a syustem table), you have write two $ signs in succession: $

## Inheritance (Don't Use unless you Fully understand it)

Working with PonyORM I tried to use inheritance like I did for base in SQLAlchemy. Unfortunently, it works in simple cases. For PonyORM, when using inheratance it creates one table for that inheratance, which isn't right when thinking of creating a database or how a database should be made. PonyORM claims this is faster but than creating joins and relationships but it is not easier and harder to create joins where you need them just like the example user in this file. 

## PonyORM Entity Attribute Types

For pony unlike SQLAlchemy you will need to import additional libraries for your attribute as you can see in the code for Date and Deciaml. Below are a possibly list of attributes that can be used.

* str
* unicode
* int
* float
* Decimal
* datetime
* date
* time
* timedelta
* bool
* buffer - used for binary data in Python 2 and 3
* bytes - used for binary data in Python 3
* LongStr - used for large strings
* LongUnicode - used for large strings
* UUID
* Json - used for mapping to native database JSON type

##### Source

[PonyORM](https://docs.ponyorm.com/firststeps.html)   
[Functions with Entities](https://docs.ponyorm.com/api_reference.html#attribute-type)
[Creating Fields](https://docs.ponyorm.com/api_reference.html#entity-definition)
[Entity Customizing](https://docs.ponyorm.com/entities.html#mapping-customization)
[Understanding Queries](https://docs.ponyorm.com/aggregations.html)
[Relationships](https://docs.ponyorm.com/working_with_relationships.html)
[Triggers?](https://docs.ponyorm.com/api_reference.html#entity-hooks)
[Attribute Types](https://docs.ponyorm.com/entities.html)
[Migration Help](https://github.com/ponyorm/pony/tree/orm-migrations/pony/migrate)
[Queries](https://docs.ponyorm.com/queries.html)
[API Reference](https://docs.ponyorm.com/api_reference.html#query-object)