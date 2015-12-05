from flask import Flask
from flask_restful import Resource, fields, Api, reqparse
from data import (get_recipe, get_recipes_for_user)
from utils import marshal_with
from schema import RecipeSchema, RecipeDataSchema

import db
import json

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, help='User ID')

class Recipe(Resource):
    @marshal_with(RecipeSchema)
    def get(self, recipe_id):
        args = parser.parse_args()
        return get_recipe(recipe_id)

class RecipeList(Resource):

    @marshal_with(RecipeSchema, many=True)
    def get(self):
        args = parser.parse_args()
        if args.get('user_id'):
            return get_recipes_for_user(args['user_id'])

class Ping(Resource):
    def get(self):
        return {'pong': True}

api.add_resource(Ping, '/ping')
api.add_resource(Recipe, '/recipe/<int:recipe_id>')
api.add_resource(RecipeList, '/recipe/')

if __name__ == '__main__':
    app.run(debug=True)
