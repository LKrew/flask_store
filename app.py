from flask import Flask, jsonify
from flask_restful import Api
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout, UserConfirm
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from flask_jwt_extended import JWTManager
from db import db
from blacklist import BLACKLIST
from ma import ma
from marshmallow import ValidationError


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'luke'
api = Api(app)

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 200

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_token_blacklist(headers, payload):
    print(str(headers) + " payload: " +str(payload))
    return payload['jti'] in BLACKLIST

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserConfirm, '/user_confirm/<int:user_id>')
if __name__=='__main__':

    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
