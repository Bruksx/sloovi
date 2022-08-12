from flask import Blueprint, request
from ..models.validation import create_user

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH', 'VIEW', 'COPY', 'LINK', 'UNLINK', 'PURGE', 'LOCK', 'UNLOCK', 'PROPFIND']

bp = Blueprint("register", __name__, url_prefix="/register")

@bp.route("", methods=HTTP_METHODS)
def register():
    allowed_methods = ["POST"]
    if request.method not in allowed_methods:
        return {"status":"error", "message":"method not allowed"}, 405
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    password = request.json.get("password")
    response = create_user(
        first_name,
        last_name,
        email,
        password,
    )
    response = response, response["code"]
    return response