from flask import Flask, jsonify
from flask_cors import CORS
import services.database
import services.banking

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='./flaskr.sqlite',
    )

    CORS(app)

    services.database.register_db(app)

    @app.post('/init-db')
    def init_db():
        services.database.init_db()
        return jsonify({
            'message': 'Database initialized'
        })

    app.register_blueprint(services.banking.bp)

    return app