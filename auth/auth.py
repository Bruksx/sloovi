import jwt
from flask import request, jsonify
from dotenv import load_dotenv, dotenv_values
from functools import wraps
from ..models.models import User

load_dotenv()
config = dotenv_values()


class Token:
    def get_access_token(email, password):
        payload = {"email":email, "password":password}
        encoded = jwt.encode(payload, config["SECRET_KEY"], "HS256")
        return encoded
    
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            content_type = request.headers.get("Content-Type")
            if not content_type:
                return {"status": "error", "message":"Set Content-type"}

            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'][7:]
            if not token:
                return jsonify({'message' : 'No token in request'}), 401
            try:
                data = jwt.decode(token, config['SECRET_KEY'], 'HS256')
                current_user = User.objects(email = data["email"])
            except:
                return jsonify({
                    'message' : 'Invalid token'
                }), 401
            return  f(current_user[0], *args, **kwargs)
  
        return decorated
