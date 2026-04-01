from flask import Flask
from flask_alembic import Alembic
from app.models.paragraph import db
from app.api.fetch import fetch_bp
from app.api.search import search_bp
from app.api.dictionary import dictionary_bp
from app.docs import init_swagger_ui
from app.config import config

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config.database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.sqlalchemy_track_modifications
    app.config["DEBUG"] = config.debug
    app.config["ENV"] = config.env

    db.init_app(app)
    alembic = Alembic(app)

    init_swagger_ui(app)

    app.register_blueprint(fetch_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(dictionary_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=config.host, port=config.port, debug=config.debug)