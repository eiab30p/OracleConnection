"""
Table definition.

Usful Liknks:
 > Great for first introductions and getting a feel how pony works.
    https://docs.ponyorm.com/firststeps.html
 > Understanding the methods and functions you can use. Super Useful a little overwhelming
    https://docs.ponyorm.com/api_reference.html#attribute-type
 > Understanding how to create your fields in more detail.
    https://docs.ponyorm.com/api_reference.html#entity-definition
    https://docs.ponyorm.com/entities.html#mapping-customization

 > Understanding Queries
    https://docs.ponyorm.com/aggregations.html
 > Relationships
    https://docs.ponyorm.com/working_with_relationships.html


 > Help with Triggers?
    https://docs.ponyorm.com/api_reference.html#entity-hooks

Tips:

Every field needs to have Required or Optional if it doesn't it won't update the DB


"""
from datetime import datetime
from pony.orm import *


db = Database()

sql_debug(True)

class StoredItem(db.Entity):
    url = Required(str)
    description = Optional(str)
    test = Optional(str)

# class TestingEncryption(db.Entity):
#     id = PrimaryKey(int)
#     foo = Required(str)
#     bar = Optional(int)

#     _table_options_ = {
#         'ENGINE': 'InnoDB',
#         'TABLESPACE': 'my_tablespace',
#         'ENCRYPTION': "'Y'",
#         'AUTO_INCREMENT': 10
#     }

class Base(db.Entity):
    #  id_base = PrimaryKey(int, auto=True)
     created_on = Required(datetime, default=datetime.utcnow())
     updated_on = Optional(datetime)

class User(db.Entity):

        # _table_ = 'auth_user'
        # user_id = PrimaryKey(int, auto=True)
        username = Required(str, unique=True)
        email_address = Required(str, column='email', unique=True)
        password = Required(str)
        first_name = Optional(str)
        last_name = Optional(str)
        active = Optional(bool)
        confirmed_at = Optional(datetime, sql_default='CURRENT_TIMESTAMP')
        last_login_at = Optional(datetime, sql_default='CURRENT_TIMESTAMP')
        current_login_at = Optional(datetime, sql_default='CURRENT_TIMESTAMP')
        login_count = Optional(int, default=0)
        roles = Set("Role", table="roles_users", column="role_id")

class Role(db.Entity):

        # _table_ = 'auth_role'
        # role_id = PrimaryKey(int, auto=True)
        name = Required(str, unique=True)
        description = Optional(str)
        users = Set(User, column="user_id")

