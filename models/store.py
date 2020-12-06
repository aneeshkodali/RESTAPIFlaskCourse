from db import db

# link class to database by extending (inheriting) db.Model
class StoreModel(db.Model):

     # tell SQLAlchemy which table maps to this class
    __tablename__ = 'stores'

    # specify table columns
    # add id to table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # reference to item
    # lazy=dynamic tells SQLAlchemy to NOT create an object for each item in database that matches store id
    # => in json(self) - have to use self.items.all() instead of just self.items
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # method to return JSON representation of model - a dictionary
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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