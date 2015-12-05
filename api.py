from flask import Flask
from flask_restful import Resource, fields, Api, reqparse
from data import (get_recipe, get_recipes_for_user, fork_recipe)
from utils import marshal_with
from schema import RecipeSchema, RecipeDataSchema
from werkzeug.exceptions import BadRequest

import db
import json

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, help='User ID', action="append")

class Recipe(Resource):
    @marshal_with(RecipeSchema)
    def get(self, recipe_id):
        args = parser.parse_args()
        return get_recipe(recipe_id)

class RecipeList(Resource):

    @marshal_with(RecipeSchema, many=True)
    def get(self):
        args = parser.parse_args()
        if args.get('user_id') and len(args.get('user_id')) == 1:
            return get_recipes_for_user(args['user_id'][0])

class Fork(Resource):
    @marshal_with(RecipeSchema)
    def post(self, recipe_id):
        args = parser.parse_args()
        if not len(args.get('user_id')) == 1:
            raise BadRequest
        user_id = args['user_id'][0]
        fork_recipe(user_id, recipe_id)

class Ping(Resource):
    def get(self):
        return {'pong': True}

api.add_resource(Ping, '/ping/')
api.add_resource(Recipe, '/recipe/<int:recipe_id>/')
api.add_resource(Fork, '/fork/<int:recipe_id>/')
api.add_resource(RecipeList, '/recipe/')

if __name__ == '__main__':
    app.run(debug=True)
