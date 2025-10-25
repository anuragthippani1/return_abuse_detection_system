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
        return {'message': 'Return Abuse Detection System API is running', 'status': 'ok'}

    @app.route('/api')
    def api_root():
        return {
            'message': 'Amazon Return Abuse Detection System API',
            'version': '1.0',
            'endpoints': {
                'health': '/health',
                'get_cases': '/api/get-return-cases',
                'save_case': '/api/save-return-case',
                'statistics': '/api/return-case-statistics',
                'get_case_by_id': '/api/get-return-case/<case_id>',
                'update_case': '/api/update-return-case/<case_id>',
                'delete_case': '/api/delete-return-case/<case_id>',
                'upload_data': '/api/upload-data'
            }
        }

    @app.route('/test')
    def test():
        return "Test route works!"
    
    @app.route('/health')
    def health():
        return {'status': 'ok', 'message': 'Backend is running'}

    return app
