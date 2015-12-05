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
