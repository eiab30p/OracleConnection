from flask import Flask, request, jsonify
import cx_Oracle
from pony import orm
import settings
from models import db, User, Role
from pony.orm.core import *

app = Flask(__name__)

@db_session
def populate_databse():
        r = Role(name='testingRole',
                 description='THis is a test.'
                )
        u = User(username='testingU',
                 email_address='testingE',
                 password='testingP',
                 roles=r
                )
        commit()


@app.before_request
def _():
        orm.db_session.__enter__()

@app.after_request
def _(response):
        orm.db_session.__exit__()
        return response

if __name__ == '__main__':
        db.connect(allow_auto_upgrade=True, **settings.db_params)
        # populate_databse()
        with db_session:
                u1 = User.get(username='testingU')
                print(u1.username)