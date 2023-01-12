from extensions import db


# creating the database table for the store model table
class StoreModel(db.Model):
    # the table name
    __tablename__ = 'stores'
    # the unique id's column for each store created
    id = db.Column(db.Integer, primary_key=True)
    # the column for each store's name
    name = db.Column(db.String(49),unique=True, nullable=False)
    # this creates a relationship between the store and item model
    # the back_populate is used to get the particular store an item is linked to
    items = db.relationship("ItemModel", back_populates="store")
