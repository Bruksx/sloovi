from flask import Blueprint, make_response, request
from ..models.models import User
from ..auth.auth import Token
from werkzeug.security import check_password_hash

bp = Blueprint("login", __name__, url_prefix="/login")
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH', 'VIEW', 'COPY', 'LINK', 'UNLINK', 'PURGE', 'LOCK', 'UNLOCK', 'PROPFIND']

@bp.route("", methods=HTTP_METHODS)
def login():
    allowed_methods = ["POST"]
    if request.method not in allowed_methods:
        return {"status":"error", "message":"method not allowed"}, 405
    try:
        email = request.json.get("email")
        password = request.json.get("password")
    except:
        print("here")
        return {}
    requird_fields = {
        "email": email,
        "password": password,
    }
    not_submitted = []
    for field in requird_fields:
        if not requird_fields[field]:
            not_submitted.append(field)

    if not_submitted:
        data = {
            "status": "error",
            "message": f"The following fields are required {not_submitted}",
        }
        return make_response(data,400)
    try:
        user = User.objects(email=email)[0]
    except IndexError:
        data = {
            "status":"error",
            "message":"No active account with this email",
        }
        response = make_response(data, 404)
        return response
    if user:
        if check_password_hash(user.password, password):
            token = Token.get_access_token(email,password)
            data = {"access_token":token}
            response = make_response(data, 200)
            return response
        else:
            data = {
                "status": "error",
                "message": "wrong email or password",
                }
            response = make_response(data, 400)
            return response

    print(user)
    return {}

