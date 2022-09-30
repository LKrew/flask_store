from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.store import StoreModel
from schemas.store import StoreSchema

STORE_NOT_FOUND = "Store Not Found"
ERROR_INSERT = "An Error Occured While Inserting Store"
STORE_DELETED = "Store Deleted"
NAME_ALREADY_EXISTS = "A store with the name '{}' already exists"

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

class Store(Resource):

    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), 200
        return {'message' : STORE_NOT_FOUND}, 404
    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {'message' : NAME_ALREADY_EXISTS.format(name)}, 400
        
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {'message' : ERROR_INSERT}, 500
        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message' : STORE_DELETED}, 200


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {'stores' : store_list_schema.dump(StoreModel.find_all()) }, 200