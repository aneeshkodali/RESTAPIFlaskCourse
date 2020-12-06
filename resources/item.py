from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# define resource 
class Item(Resource):

    # parse request and see what arguments match those that are defined
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    # 'Item' resource can be accessed with GET method
    # GET info about one item
    @jwt_required() #authenticate before user can call get method
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # POST: Create new 'Item'
    def post(self, name):
        # check if item with name already exists, return status code 400 (bad request)
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name} already exists."}, 400

        # get data from body/payload
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        # insert item
        try:
            item.save_to_db()
        except:
            # 500 - internal server error
            return {'message': "An error occured inserting the item"}, 500 
        # return item, ALSO 201 (status code for created)
        return item.json(), 201

    # DELETE item
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    # PUT: update (or create if dne) item
    def put(self, name):
        # parse arguments and add valid ones in data
        data = Item.parser.parse_args()
        # find out if item exists, if not => create it; else update item dictionary
        item = ItemModel.find_by_name(name)
        if item is None:
           item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

 
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # same as:
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
