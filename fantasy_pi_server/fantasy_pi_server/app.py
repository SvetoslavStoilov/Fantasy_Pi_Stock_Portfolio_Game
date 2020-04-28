from flask import Flask
from fantasy_pi_server.config import development_config
from flask_cors import CORS
from fantasy_pi_server.views import data, portfolios

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(development_config)
    CORS(app)

    app.register_blueprint(data)
    app.register_blueprint(portfolios)

    return app
