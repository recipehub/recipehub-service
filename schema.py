from marshmallow import Schema, fields

class RecipeDataSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    ingredients = fields.Dict()
    steps = fields.List(fields.Str())
    parent_id = fields.Int()
    message = fields.Str()

class RecipeSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    title = fields.Str()
    description = fields.Str()
    fork_of_id = fields.Int()
    user_id = fields.Int()
    data = fields.Nested(RecipeDataSchema)

    class Meta:
        ordered = True
