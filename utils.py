import datetime
import json
from functools import wraps
from marshmallow import pprint

def marshal_with(schema_class, many=False):
    def wrapper(f):
        @wraps(f)
        def _f(*args, **kwargs):
            schema = schema_class(many=many)
            return schema.dump(f(*args, **kwargs)).data
        return _f
    return wrapper
