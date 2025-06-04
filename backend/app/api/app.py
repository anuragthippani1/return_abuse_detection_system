from flask import Flask, jsonify
from flask_cors import CORS
import pymongo
import os

from .routes import api  # or from routes import api depending on structure

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["amazon"]
    collection = db["return_cases"]

    app.register_blueprint(api, url_prefix='/api')

    @app.route('/api/return-case-statistics', methods=['GET'])
    def get_return_case_statistics():
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_cases": {"$sum": 1},
                    "avg_risk_score": {"$avg": "$risk_score"},
                    "avg_suspicion_score": {"$avg": "$suspicion_score"},
                    "high_risk_cases": {
                        "$sum": {
                            "$cond": [{"$gte": ["$risk_score", 80]}, 1, 0]
                        }
                    },
                    "medium_risk_cases": {
                        "$sum": {
                            "$cond": [
                                {"$and": [
                                    {"$gte": ["$risk_score", 50]},
                                    {"$lt": ["$risk_score", 80]}
                                ]},
                                1,
                                0
                            ]
                        }
                    },
                    "low_risk_cases": {
                        "$sum": {
                            "$cond": [{"$lt": ["$risk_score", 50]}, 1, 0]
                        }
                    }
                }
            }
        ]

        try:
            result = list(collection.aggregate(pipeline))
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

        if result:
            stats = result[0]
        else:
            stats = {
                "total_cases": 0,
                "avg_risk_score": 0,
                "avg_suspicion_score": 0,
                "high_risk_cases": 0,
                "medium_risk_cases": 0,
                "low_risk_cases": 0
            }

        return jsonify({
            "success": True,
            "statistics": {
                "total_cases": stats["total_cases"],
                "avg_risk_score": round(stats["avg_risk_score"] or 0, 2),
                "avg_suspicion_score": round(stats["avg_suspicion_score"] or 0, 2),
                "high_risk_cases": stats["high_risk_cases"],
                "medium_risk_cases": stats["medium_risk_cases"],
                "low_risk_cases": stats["low_risk_cases"],
            }
        })

    @app.route('/')
    def hello():
        return "Hello World!"

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
 