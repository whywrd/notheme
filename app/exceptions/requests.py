from werkzeug.exceptions import HTTPException
from flask import abort


class InvalidUsage(HTTPException):
    code = 400

    def __init__(self, description=None, code=None, subdomain=None, query_params=None):
        if description is None:
            abort(code)
        self.subdomain = subdomain
        self.query_params = query_params
        if code is not None:
            self.code = code
        self.description = description
        HTTPException.__init__(self, description=self.description)
