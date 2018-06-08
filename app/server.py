from flask import Flask, request, jsonify
import cx_Oracle
from pony import orm
from . import settings
from .models import db


app = Flask(__name__)

# db = Database('oracle', 'eddy/password@xe')

# db = Database()

# class EDDYTEST(db.Entity):
#         _table_ = 'EDDYTEST'
#         name = Required(str)
#         somethingNew = Optional(str)

# sql_debug(True)

# # try:
# # db.connect( **settings.db_params)
# db.migrate(command='make', migration_dir='migration_pony', **settings.db_params)
        
# except:
#         # pony_model.db.bind(provider='oracle', user='eddy', password='password', dsn='xe')
#         db.generate_mapping(create_tables=True)
#         print("testing")

# @db_session
# def create_entities():
#         test = EDDYTEST(name='jsfhsdjfhjksdfhksdh', something_new="new?")

# create_entities()



@app.before_request
def _():
        orm.db_session.__enter__()

@app.after_request
def _(response):
        orm.db_session.__exit__()
        return response

if __name__ == '__main__':
        db.connect(**settings.db_params)
        app.run()