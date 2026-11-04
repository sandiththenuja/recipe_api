from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

from webargs import fields
from webargs.flaskparser import use_kwargs

from  utils import hash_password
from models.user import User
from models.recipe import Recipe

from schemas.user import UserSchema
from schemas.recipe import RecipeSchema

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))

recipe_list_schema = RecipeSchema(many=True)

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        # username = json_data.get('username')
        # email = json_data.get('email')
        # password = json_data.get('password')

        # if User.get_by_username(username):
        #     return {'message': 'username already registered'}, HTTPStatus.BAD_REQUEST

        # if User.get_by_email(email):
        #     return {'message': 'email already registered'}, HTTPStatus.BAD_REQUEST

        # hashed_pass = hash_password(password)

        # user = User(
        #     username=username,
        #     email=email,
        #     password=hashed_pass
        # )
        # user.save()

        # data = {
        #     'id': user.id,
        #     'username': user.username,
        #     'email': user.email
        # }
        # return data, HTTPStatus.CREATED

        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': 'validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()
        return user_schema.dump(user), HTTPStatus.CREATED
        

class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self, username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user and int(current_user) == user.id:
            # data = {
            #     'id': user.id,
            #     'username': user.username,
            #     'email': user.email
            # }
            data = user_schema.dump(user)
        else:
            # data = {
            #     'id': user.id,
            #     'username': user.username,
            # }
            data = user_public_schema.dump(user)
        return data, HTTPStatus.OK

class MeSource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity() 
        user = User.get_by_id(id=int(current_user_id))
        
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        
        # data = {
        #     'id': int(user.id), 
        #     'username': str(user.username),
        #     'email': str(user.email)
        # }
        data = user_schema.dump(user)
        
        return data, HTTPStatus.OK

class UserRecipeListResource(Resource):
    @jwt_required(optional=True)
    @use_kwargs({'visibility': fields.Str(load_default='public')})
    def get(self, username, visibility):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user and int(current_user) == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'

        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)

        return recipe_list_schema.dump(recipes), HTTPStatus.OK
