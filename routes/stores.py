from flask.views import MethodView
from schemas import GetAllStoreSchema, StoreSchema, UpdateStoreSchema
from extensions import db
from models import StoreModel
from models import ItemModel
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required

blp = Blueprint("store", __name__)


@blp.route('/stores/')
class stores(MethodView):
    @blp.response(200, GetAllStoreSchema(many=True))
    def get(self):
        store = StoreModel.query.all()
        return store, 200

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    @jwt_required()
    def post(self, user_data):
        name = user_data['name'].lower()
        store = StoreModel.query.filter(StoreModel.name == name).first()
        if store:
            abort(409, message='Store already exist')
        new_store = StoreModel(name=name)
        db.session.add(new_store)
        db.session.commit()
        return new_store, 201


@blp.route('/stores/<int:store_id>/')
class stores(MethodView):
    @blp.response(200, StoreSchema)
    @jwt_required()
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store, 200

    @blp.arguments(UpdateStoreSchema)
    @blp.response(200, StoreSchema)
    @jwt_required()
    def put(self, store_data, store_id):
        store = StoreModel.query.get_or_404(store_id)
        name = store_data['name']
        if name:
            store.name = name
        db.session.commit()
        return store, 200

    @jwt_required()
    def delete(self, store_id):
        store_items = ItemModel.query.filter_by(store_id=store_id).all()
        for item in store_items:
            db.session.delete(item)
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {'message': 'Store deleted'}


"""
Check the users.py file for the comment that might aid in understanding the code
"""