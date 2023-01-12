from extensions import db


# creating the database table for the item model table
class ItemModel(db.Model):
    # stating the table name
    __tablename__ = 'items'
    # the unique id's column for each item created
    id = db.Column(db.Integer, primary_key=True)
    # the column for each item's name
    name = db.Column(db.String(77), nullable=False)
    # the column for each item's price
    price = db.Column(db.Integer, nullable=False)
    # the foreign key linking the item table and the store's table
    # it takes the id of the store rhe item is being added to
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),
                         unique=False, nullable=False)
    # this creates a relationship between the store and item model
    store = db.relationship("StoreModel", back_populates='items')


"""
{
'name': '',
'price': 0,
'store_id': 0
}
"""