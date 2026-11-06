from flask import request, url_for, render_template
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
import os

from webargs import fields
from webargs.flaskparser import use_kwargs

from  utils import hash_password, generate_token, verify_token, save_image
from models.user import User
from models.recipe import Recipe

from schemas.user import UserSchema
from schemas.recipe import RecipeSchema

from mailgun import MailgunApi

from extensions import image_set

mailgun = MailgunApi(domain=os.environ.get('MAILGUN_DOMAIN'), api_key=os.environ.get('MAILGUN_API_KEY'))

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))
user_avatar_schema = UserSchema(only=('avatar_url',))

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

        try:
            data = user_schema.load(data=json_data)
        except ValidationError as err:
            return {'message': "Validation errors", 'errors': err.messages}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        token = generate_token(user.email, salt='activate')
        subject = 'Confirm your registration'
        link = url_for('useractivateresource', token=token, _external=True)
        text = 'Hello, Thanks for using SmileCook! Pleasse confirm your registration by clicking on the link: {}'.format(link)

        mailgun.send_email(to=user.email, subject=subject, text=text, html=render_template('email/confirmation.html', link=link))

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
    @use_kwargs({'visibility': fields.Str(load_default='public')}, location="query")  # location tells to look specifically in query which is visibility
    @jwt_required(optional=True)
    def get(self, username, visibility):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        print(f"DEBUG: Visibility requested is: {visibility}") # 👈 Debug print
        print(f"DEBUG: Current user is: {current_user}") 

        if current_user and int(current_user) == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'

        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)

        return recipe_list_schema.dump(recipes), HTTPStatus.OK

class UserActivateResource(Resource):
    def get(self, token):
        email = verify_token(token, salt='activate')

        if email is False:
            return {'message': 'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email=email)

        if not user:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        if user.is_active is True:
            return {'message': 'user account is already activated'}, HTTPStatus.BAD_REQUEST

        user.is_active = True

        user.save()
        return {}, HTTPStatus.NO_CONTENT

class UserAvatarUploadResource(Resource):
    @jwt_required()
    def put(self):
        file = request.files.get('avatar')
        if not file:
            return {'message': 'Not a valid image'}, HTTPStatus.BAD_REQUEST
        if not image_set.file_allowed(file, file.filename):
            return {'message': 'File type not allowed'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_id(id=int(get_jwt_identity()))

        if user.avatar_image:
            avatar_path = image_set.path(folder='avatars', filename=user.avatar_image)

            if os.path.exists(avatar_path):
                os.remove(avatar_path)

        filename = save_image(image=file, folder='avatars')

        user.avatar_image = filename
        user.save()
        return user_avatar_schema.dump(user), HTTPStatus.OK
