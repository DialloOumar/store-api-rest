import uuid
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

blp = Blueprint('stores', __name__, description='Operations on stores')

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(store_id):
        try:
            return jsonify(stores[store_id])
        except KeyError:
            abort(404, message='Store not found')
    
    def delete(store_id):
        try:
            del stores[store_id]
            return jsonify({'message': 'Store deleted'}), 202
        except KeyError:
            abort(404, message='Store not found')


@blp.route('/store')
class Stores(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, request_data):
        
        for store in stores.values():
            if store['name'] == request_data['name']:
                abort(400, message=f"Store already exists")
        
        store_id = uuid.uuid4().hex
        store = {**request_data, 'id': store_id}
        stores[store_id]=store

        return jsonify(store), 201