import datetime
import json
from functools import wraps

def marshal_with(schema_class):
    def wrapper(f):
        @wraps(f)
        def _f(*args, **kwargs):
            schema = schema_class()
            return  schema.dumps(f(*args, **kwargs)).data
        return _f
    return wrapper
