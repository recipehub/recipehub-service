from flask import Flask, request
from flask_restful import Resource, fields, Api, reqparse
from data import (get_recipe, get_recipes_for_user, fork_recipe, get_recipes_for_users, new_recipe, update_recipe, get_forks, get_versions, get_version)
from utils import marshal_with
from schema import RecipeSchema, RecipeDataSchema
from werkzeug.exceptions import BadRequest

import db
import json

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, help='User ID', action="append")
parser.add_argument('recipe_id', type=int, help='Recipe ID')
parser.add_argument('version_id', type=int, help='Version ID')

class Recipe(Resource):
    @marshal_with(RecipeSchema)
    def get(self, recipe_id):
        args = parser.parse_args()
        version_id = args.get('version_id')
        if not version_id:
            return get_recipe(recipe_id)
        return get_version(recipe_id, version_id)

    @marshal_with(RecipeSchema)
    def put(self, recipe_id):
        recipe_data = json.loads(request.data)
        if not recipe_data.get('ingredients') or not recipe_data.get('steps'):
            raise BadRequest
        return update_recipe(recipe_id, ingredients=recipe_data['ingredients'], steps=recipe_data['steps'])


class RecipeList(Resource):

    @marshal_with(RecipeSchema, many=True)
    def get(self):
        args = parser.parse_args()
        if not args.get('user_id'):
            raise BadRequest
        if len(args.get('user_id')) == 1:
            return get_recipes_for_user(args['user_id'][0])
        else:
            return get_recipes_for_users(args['user_id'])

    @marshal_with(RecipeSchema)
    def post(self):
        recipe = json.loads(request.data)
        return new_recipe(**recipe)

class ForkList(Resource):
    @marshal_with(RecipeSchema, many=True)
    def get(self):
        args = parser.parse_args()
        recipe_id = args.get('recipe_id')
        if not recipe_id:
            raise BadRequest
        return get_forks(recipe_id)


class Fork(Resource):
    @marshal_with(RecipeSchema)
    def post(self, recipe_id):
        user_id = json.loads(request.data).get('user_id')
        if not user_id:
            raise BadRequest
        return fork_recipe(user_id, recipe_id)

class Version(Resource):
    @marshal_with(RecipeSchema, many=True)
    def get(self, recipe_id):
        return get_versions(recipe_id)



class Ping(Resource):
    def get(self):
        return {'pong': True}

api.add_resource(Ping,       '/ping/')
api.add_resource(Recipe,     '/recipe/<int:recipe_id>/')
api.add_resource(Fork,       '/fork/<int:recipe_id>/')
api.add_resource(RecipeList, '/recipe/')
api.add_resource(ForkList,   '/fork/')
api.add_resource(Version,     '/version/<int:recipe_id>/')

@app.route('/clean')
def _clean():
    from tests import clean
    clean()
    return 'done'


if __name__ == '__main__':
    app.run(debug=True)
