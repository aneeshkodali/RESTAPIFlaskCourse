from app import app
from db import db

db.init_app(app)

# create db if DNE before first request is run
# SQLAlchemy can only create tables it sees (it sees tables because we import the resource which imports the model)
# we can also import models directly and db will create
# ex. import Store resource <= Store imports StoreModel <= StoreModel has tablename
@app.before_first_request
def create_tables():
    db.create_all()
