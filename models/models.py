from dotenv import load_dotenv, dotenv_values
from mongoengine import connect, Document, StringField, EmailField, ReferenceField

load_dotenv()

config = dotenv_values()
username = config["USERNAME"]
password = config["PASSWORD"]

CONNECTION_STRING = f"mongodb+srv://{username}:{password}@cluster0.dfgouuo.mongodb.net/?retryWrites=true&w=majority"

db = connect(host=CONNECTION_STRING)
class User(Document):
    email = EmailField(required = True, unique=True)
    first_name = StringField(required = True)
    last_name = StringField(required = True)
    password = StringField(required = True)

class Template(Document):
    user = ReferenceField(User)
    template_name = StringField(required=True)
    subject = StringField(required=True)
    body = StringField(required=True)