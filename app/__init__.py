from flask import Flask
from .config import Config
from .auth import auth
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)
    app.register_blueprint(auth)
    
    return app
    