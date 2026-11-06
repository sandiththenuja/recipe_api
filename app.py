from flask import Flask, url_for
from flask_restful import Api
from flask_migrate import Migrate
from flask_uploads import configure_uploads
from dotenv import load_dotenv

from config import Config
from extensions import db, jwt, image_set

from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource, RecipeCoverUploadResource
from resources.user import UserListResource, UserResource, MeSource, UserRecipeListResource, UserActivateResource, UserAvatarUploadResource
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list

load_dotenv()

# app = Flask(__name__)
# api = Api(app)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    configure_uploads(app, image_set)
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 

    return app

def register_extensions(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in black_list

def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(UserRecipeListResource, '/users/<string:username>/recipes')
    api.add_resource(UserActivateResource, '/users/activate/<string:token>')
    api.add_resource(UserAvatarUploadResource, '/users/avatar')

    api.add_resource(MeSource, '/me')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')
    
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
    api.add_resource(RecipeCoverUploadResource, '/recipes/<int:recipe_id>/cover')
    

# api.add_resource(RecipeListResource, '/recipes')
# api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
# api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')

if __name__ == '__main__':
    app = create_app()
    # app.run(port=5000, debug=True)
    app.run()
