import uuid
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint('items', __name__, description='Operations on items')



@blp.route('/item/<string:item_id>')
class Item(MethodView):
    
    def get(self,item_id):
        try:
            return jsonify(items[item_id])
        except KeyError:
            abort(404, message='Item not found')
    def delete(self,item_id):
        try:
            del items[item_id]
            return jsonify({'message': 'Item deleted'}), 202
        except KeyError:
            abort(404, message='Item not found')

    @blp.arguments(ItemUpdateSchema)
    def put(self,item_data, item_id):
        try:
            item = items[item_id]
            item.update(item_data)
            return jsonify(item), 200
        except KeyError:
            abort(404, message='Item not found')

@blp.route('/item')
class Items(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):

        if item_data['store_id'] not in stores:
            abort(400, message='Store not found')

        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        items[item_id] = item

        return jsonify(item), 201