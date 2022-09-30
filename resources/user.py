from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
    )
from flask_restful import Resource
from flask import request
from models.user import UserModel
from hmac import compare_digest
from blacklist import BLACKLIST
from schemas.user import UserSchema
from marshmallow import ValidationError

BLANK_ERROR = "'{}' cannot be blank"
USER_ALREADY_EXISTS = 'A user with that username already exists'
CREATED_SUCCESSFULLY = 'User created successfully'
USER_NOT_FOUND = "User not found"
USER_DELETED = "User Deleted"
INVALID_CREDENTIALS = "Invalid Credentials"
USER_LOGGED_OUT = "Successfully Logged Out"

user_schema = UserSchema()

class UserRegister(Resource):

    @classmethod
    def post(cls):
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        if UserModel.find_by_username(user.username):
            return {'message' : USER_ALREADY_EXISTS}
        user.save_to_db()

        return {'message' : CREATED_SUCCESSFULLY}, 201

class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id).first()
        if not user:
            return {'message' : USER_NOT_FOUND}, 404
        return user_schema.dump(user), 200
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id).first()
        if not user:
            return {'message' : USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {'message' : USER_DELETED}

class UserLogin(Resource):  

    @classmethod
    def post(cls):
        user_data  = user_schema.load(request.get_json())

        user = UserModel.find_by_username(user_data['username'])

        if user and compare_digest(user.password, user_data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token' : access_token,
                'refresh_token' : refresh_token
            }, 200

        return {'message' : INVALID_CREDENTIALS}, 401
    
class UserLogout(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message' : USER_LOGGED_OUT}

class TokenRefresh(Resource):

    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=True)
        return {'access_token' : new_token}