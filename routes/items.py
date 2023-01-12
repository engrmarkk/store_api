from flask.views import MethodView
from schemas import GetAllItemSchema, ItemSchema, UpdateItemSchema
from extensions import db
from models import ItemModel
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required

blp = Blueprint('Items', __name__)


@blp.route('/items/')
class stores(MethodView):
    @blp.response(200, GetAllItemSchema(many=True))
    def get(self):
        item = ItemModel.query.all()
        return item, 200

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    @jwt_required()
    def post(self, user_data):
        name = user_data['name'].lower()
        price = user_data['price']
        store_id = user_data['store_id']
        item = ItemModel.query.filter(ItemModel.name == name).first()
        if item:
            abort(409, message='Item already exist')
        new_item = ItemModel(name=name, price=price, store_id=store_id)
        db.session.add(new_item)
        db.session.commit()
        return new_item, 201


@blp.route('/items/<int:item_id>/')
class stores(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item, 200

    @blp.arguments(UpdateItemSchema)
    @blp.response(200, ItemSchema)
    @jwt_required()
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        name = item_data['name']
        price = item_data['price']
        store_id = item_data['store_id']
        if name:
            item.name = name
        if price:
            item.price = price
        if store_id:
            item.store_id = store_id

        db.session.commit()
        return item, 200

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted'}


"""
Check the users.py file for the comment that might aid in understanding the code
"""