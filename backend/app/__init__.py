from flask import Flask
from flask_cors import CORS
from .config.config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Upload folder setup
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    CORS(app)  # Enable CORS

    # Register blueprints
    from .api.routes import api
    app.register_blueprint(api, url_prefix='/api')

    # Basic routes
    @app.route('/')
    def home():
        return {'message': 'Return Abuse Detection System API is running'}

    @app.route('/test')
    def test():
        return "Test route works!"

    return app
