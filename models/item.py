from db import db

# link class to database by extending (inheriting) db.Model
class ItemModel(db.Model):

     # tell SQLAlchemy which table maps to this class
    __tablename__ = 'items'

    # specify table columns
    # add id to table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # foreign key to store id: db.ForeignKey(<tablename>.<columnname>)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # 'join'
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # method to return JSON representation of model - a dictionary
    def json(self):
        return {'name': self.name, 'price': self.price}

    # class method
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # originally called insert; SQLAlchemy will insert new record/update existing record as needed
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()