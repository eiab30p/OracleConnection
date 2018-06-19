"""
Migrate File.

This is simply running the migration function that PonyORM has.
All we need to do is have the database object and database
connection paramaters passed.

"""
from testing_conntection import db_params, db

db.migrate(**db_params)