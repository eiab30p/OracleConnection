# from app import settings
# from app.models import db
from testing_conntection import db_params, db

db.migrate(**db_params)