from flask import Blueprint,  request 
from ..auth.auth import Token
from ..models.models import Template
from mongoengine.errors import ValidationError

bp = Blueprint("template", __name__, url_prefix="/template")
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH', 'VIEW', 'COPY', 'LINK', 'UNLINK', 'PURGE', 'LOCK', 'UNLOCK', 'PROPFIND']


@bp.route("", methods=HTTP_METHODS)
@Token.token_required
def insert_or_get_template(user):
    allowed_methods = ["GET","POST"]
    if request.method not in allowed_methods:
        return {"status":"error", "message":"method not allowed"}, 405
    if request.method == "POST":
        template_name = request.json.get("template_name")
        subject = request.json.get("subject")
        body = request.json.get("body")

        template = Template(
            template_name = template_name,
            subject = subject,
            body = body,
            user = user,
        )
        try:
            template.save()
            data = {
                "id": str(template.id),
                "template_name": template_name,
                "subject": subject,
                "body": body,
                "user_id":str(user.id)
            }
            return data,201
        except ValidationError as e:
            data = e.errors
            response = {}
            for i in data:
                response[i] = str(data[i])
            return response,400
    
    if request.method == "GET":
        user_templates = Template.objects(user=str(user.id))
        response = []
        for template in user_templates:
            json_form = {
                "id": str(template.id),
                "template_name": template.template_name,
                "subject": template.subject,
                "body": template.body,
            }
            response.append(json_form)
        return response, 200
    
@bp.route("<template_id>", methods=HTTP_METHODS)
@Token.token_required
def get_template_by_id(user, template_id):
    allowed_methods = ["GET","PUT","DELETE"]
    if request.method not in allowed_methods:
        return {"status":"error", "message":"method not allowed"}, 405
    template_name = request.json.get("template_name")
    subject = request.json.get("subject")
    body = request.json.get("body")
    if request.method == "GET":
        try:
            template = Template.objects(id=template_id)[0]
            data = {
                "id": str(template.id),
                "template_name": template.template_name,
                "subject": template.subject,
                "body": template.body,
            }
            return data,200
        except :
            return {"status": "error", "message":"not found"}, 404

    if request.method == "PUT":
        try:
            template = Template.objects(id = template_id)[0]
            template.template_name = template_name
            template.subject = subject
            template.body = body
            data = {
                "id": str(template.id),
                "template_name": template.template_name,
                "subject": template.subject,
                "body": template.body,
            }
            return data, 204
        except IndexError:
            return {"status": "error", "message":"not found"}, 404
    
    if request.method == "DELETE":
        try:
            template = Template.objects(id=template_id)[0]
            template.delete()
            return {"status":"deleted"}
        except IndexError:
            return {"status": "error", "message":"not found"}, 404