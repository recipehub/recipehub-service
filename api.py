from flask import Flask
from functools import wraps
from flask_restful import Resource, fields, Api
from data import (get_recipe, )


import db
import json

app = Flask(__name__)
api = Api(app)

from marshmallow import Schema, fields

class RecipeDataSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    ingredients = fields.Dict()
    steps = fields.List(fields.Str())
    parent_id = fields.Int()

class RecipeSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    title = fields.Str()
    fork_of = fields.Int()
    user_id = fields.Int()
    data = fields.Nested(RecipeDataSchema)

def marshal_with(schema_class):
    def wrapper(f):
        @wraps(f)
        def _f(*args, **kwargs):
            schema = schema_class()
            return  schema.dumps(f(*args, **kwargs)).data
        return _f
    return wrapper

class Recipe(Resource):
    @marshal_with(RecipeSchema)
    def get(self, recipe_id):
        return get_recipe(recipe_id)

class Ping(Resource):
    def get(self):
        return {'pong': True}

api.add_resource(Ping, '/ping')
api.add_resource(Recipe, '/recipe/<int:recipe_id>')

if __name__ == '__main__':
    app.run(debug=True)
