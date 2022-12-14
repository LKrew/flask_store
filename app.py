from flask import Flask, jsonify
from flask_restful import Api
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from flask_jwt_extended import JWTManager
from db import db
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True

# uri = os.environ.get('HEROKU_DATABASE_URL', 'sqlite:///data.db')
# if uri.startswith('postgres://'):
#     uri = uri.replace('postgres://', 'postgresql://', 1)
# app.config['SQLALCHEMY_DATABASE_URI'] = uri

app.secret_key = 'luke'
api = Api(app)

jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin' : True}
    return {'is_admin' : False}

@jwt.token_in_blocklist_loader
def check_token_blacklist(headers, payload):
    print(str(headers) + " payload: " +str(payload))
    return payload['jti'] in BLACKLIST

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.expired_token_loader
def expired_token_callback():
    return {
        'description' : 'Token Expired',
        'error' : 'token_expired'
    },401

@jwt.unauthorized_loader
def invalid_token_callback(error):
    return jsonify({
        'description' : 'signature verification failed',
        'error' : 'invalid_token'
    }),401

@jwt.needs_fresh_token_loader
def token_not_freshh_callback(headers, payload):
    return jsonify({
        'description' : 'token is not fresh',
        'error' : 'fresh_token_required'
    }),401

@jwt.revoked_token_loader
def revoked_token_callback(headers, payload):
    return jsonify({
        'description' : 'Token has been revoked',
        'error' : 'revoked_token'
    }),401

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__=='__main__':

    db.init_app(app)

    app.run(port=5000, debug=True)