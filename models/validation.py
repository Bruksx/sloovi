import re
from mongoengine.errors import NotUniqueError
from .models import User
from werkzeug.security import generate_password_hash

def create_user(first_name, last_name, email, password):
    requird_fields = {
        "first_name":first_name,
        "last_name": last_name,
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
            "code": 400,
        }
        return data
    
    if not validate_email(email):
        data = {
            "status": "error",
            "message": "Invalid email address",
            "code": 400,
        }
        return data
    
    if not validate_password(password):
        data = {
            "status":"error",
            "message": "Invalid password: Password must contain at least 8 characters, 1 uppercase, 1 lowercase ,  and one digit",
            "code":400,
        }
        return data
    
    else:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password),
        )
        try:
            user.save()
            data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "code": 201,
                "status":"success"
            }
            return data
        except NotUniqueError:
            data = {
                "status": "error",
                "message": "this email is already taken",
                "code": 400,
            }
            return data
    
def validate_email(email):
    pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,9}$' 
    if re.search(pattern,email):
        return True
    else:
        return False

def validate_password(password):
    pattern = "^(?=.*?[A-Z])(?=.*?[a-z]).{8,}$"
    if re.search(pattern, password):
        return True
    else:
        return False

    

