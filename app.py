import os

from flask import Flask
from flask_restful import Api
# NO NEED TO IMPORT JSONIFY - flask_restful does this
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)


# use jwt in app to authenticate users
jwt = JWT(app, authenticate, identity)
# creates new endpoint by default: '/auth'
# send '/auth' a username/password (via POST request)
# JWT sends username/password to authenticate function => returns user => auth endpoint returns JWT (JSON web token)
# token can now get sent through to any next request we make
# when its sent, it calls identity function - gets correct user/validates authentication


# Item is now accessible in api
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# run flask app
if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
