# import fields and Schema from marshmallow
from marshmallow import fields, Schema


# Create a class for the user schema
class UserSchema(Schema):
    # the id is an integer field
    id = fields.Int()
    # username is a string field
    username = fields.Str()
    # password is also a string field
    # the password will not be displayed when getting user's info
    # because we set 'load_only=True'
    password = fields.Str(load_only=True)


# Create a class for the store schema
class StoreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


# Create a class for the item schema
class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Int()
    store_id = fields.Int(required=True, load_only=True)


# Create a class for the update store schema
class UpdateStoreSchema(Schema):
    name = fields.Str()


# Create a class for the update item schema
class UpdateItemSchema(Schema):
    name = fields.Str(required=False)
    price = fields.Int(required=False)
    store_id = fields.Int(required=False, load_only=True)


# Create a class for the get all items schema
# this inherits schema from the item schema
# the item schema with the store field inclusive will be returned when all item is being requested for
class GetAllItemSchema(ItemSchema):
    store = fields.Nested(StoreSchema(), dump_only=True)


# Create a class for the get all stores schema
# this inherits schema from the store schema
# the store schema with the items field inclusive will be returned when all store is being requested for
class GetAllStoreSchema(StoreSchema):
    # the many=True indicates that a list will be returned
    items = fields.Nested(ItemSchema(many=True), dump_only=True)
