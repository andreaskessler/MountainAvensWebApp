from flask import Flask
from flask_cors import CORS
import os

def create_app():
    parentDir = os.path.abspath(os.path.join(os.path.dirname(__name__),".."))
    app = Flask(parentDir)
    if os.environ.get('FLASK_ENV') == 'development':
        CORS(app)
    from engine.api.routes import api_blueprint
    app.register_blueprint(api_blueprint)
    return app
