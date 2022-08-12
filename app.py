import os
from flask import Flask
from .blueprints import register, login, templates
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY= config["SECRET_KEY"]
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route("/")
    def test():
        return "start"
    
    app.register_blueprint(register.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(templates.bp)
    
    return app
