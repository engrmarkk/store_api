# import the dependencies
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from extensions import db
from schemas import UserSchema
from models import UserModel
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity, get_jwt
from blocklist import BLOCKLIST
from datetime import timedelta

# instantiate the blueprint imported from flask_smorest
blp = Blueprint('Users', __name__)


# use the instantiated blueprint to create a rute for register class
@blp.route('/register/')
# create a register class
class register(MethodView):
    # when inputting datas, the schema in which we want the datas to be serialized (the format we want the data)
    @blp.arguments(UserSchema)
    # the status code and the schema iin which the response should be serialized
    @blp.response(200, UserSchema)
    # the post request for the register class
    # the user_data passed is the data we are input when sending a post request
    def post(self, user_data):
        # get the username from the data
        username = user_data['username'].lower()
        # get the password from the data
        password = user_data['password']
        # hash the password
        password = pbkdf2_sha256.hash(password)
        # query the database, filtering by the username and get the first details to be returned
        user = UserModel.query.filter(UserModel.username == username).first()

        # if the user with that username exist
        if user:
            # abort the process with a status code of 409
            abort(409, message='User already exist')

        # if the user doesn't exist in the database, add and commit the new user's details into the database
        new_user = UserModel(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        # then return the new user's details with a status code of 201
        return new_user, 201


# use the instantiated blueprint to create a route for login class
@blp.route('/login/')
# create a login class
class login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # get the username from the data
        username = user_data['username'].lower()
        # get the password from the data
        password = user_data['password']
        # check the database if the user with that database exist
        user = UserModel.query.filter(UserModel.username == username).first()

        # if the user exist and also the password matches the one in the database
        if user and pbkdf2_sha256.verify(password, user.password):
            # create an access and a refresh token for the user with the user's id as the identity
            token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            # return the tokens created
            return {"access_token": token, "refresh_token": refresh_token}
        # if the user doesn't exist in the database, then abort the process
        abort(401, message='Invalid details')


# this is an endpoint that uses the refresh token to generate a new access token
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, expires_delta=timedelta(hours=2))

        return {"access_token": new_token}


# This is the endpoint for logout
@blp.route("/logout")
class Logout(MethodView):
    # the jwt_required indicates that the access token will be required to log out
    @jwt_required()
    def post(self):
        # get the current user's token
        jti = get_jwt()['jti']
        # send the token to the BLOCKLIST set in the blocklist.py file
        # this will revoke the token. A new access token will be created for you when you log in again
        BLOCKLIST.add(jti)
        # return this message for a successful logout
        return {"message": "Successfully logged out"}


# creating a route to get a specif user using the user's id
@blp.route('/users/<int:user_id>/')
class each_user(MethodView):
    # the response should be serialized using the UserSchema
    @blp.response(200, UserSchema)
    # the jwt_required indicates that the access token will be required to get the user's details
    @jwt_required()
    # the get function to get the user's details, the user_id is a parameter representing the user's id
    def get(self, user_id):
        # get the details of the user with that id from the database
        # if the user doesn't exist, then return a 404 message
        user = UserModel.query.get_or_404(user_id)
        # return the user with a status code of 200
        return user, 200

    @jwt_required()
    # delete function to delete specific user using the user's id
    def delete(self, user_id):
        # get the user with the id
        user = UserModel.query.get_or_404(user_id)
        # delete the user and commit it into the database
        db.session.delete(user)
        db.session.commit()
        # the return this message with a status code of 200
        return {'message': 'user deleted'}, 200


# the class to get all users available in the database
@blp.route('/users/')
class all_users(MethodView):
    # the response should be serialized using the UserSchema
    # the many=True simply means we want it to be returned in a list
    @blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        # query the database and get all the user in the database
        all_user = UserModel.query.all()
        # return the data gotten from the database
        # if no user is present in the database, an empty list is being returned
        return all_user, 200


"""
The explanation here will help in understanding the codes in the
stores and items file
"""