from werkzeug.security import safe_str_cmp
from models.user import UserModel

# authenticate a user
# used when someone goes to the '/auth' endpoint
def authenticate(username, password):
    # find user by username
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user # used to generate jwt token

# used when someone makes request to an endpoint and needs to be authenticated
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)