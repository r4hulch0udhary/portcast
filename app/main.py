"""
Main Application Entry Point.

This module initializes the asynchronous Flask application, configures the
database engine, registers API blueprints, and sets up CORS, logging, and Swagger UI.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from asgiref.wsgi import WsgiToAsgi

from app.models.paragraph import db
from app.api.fetch import fetch_bp
from app.api.search import search_bp
from app.api.dictionary import dictionary_bp
from app.docs import init_swagger_ui
from app.config import config
from app.app_logger import setup_logging


def create_app() -> Flask:
    """
    Application Factory for creating the Flask app instance.

    Sets up the application configuration, initializes the asynchronous database engine,
    registers blueprints for routes, and enables CORS and Swagger UI.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config.database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.sqlalchemy_track_modifications
    app.config["DEBUG"] = config.debug
    app.config["ENV"] = config.env

    # Create async engine
    async_db_url = config.database_url.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(async_db_url, poolclass=NullPool)
    app.engine = engine

    db.init_app(app)

    CORS(app)  # Enable CORS for all routes

    init_swagger_ui(app)

    app.register_blueprint(fetch_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(dictionary_bp)

    # Serve the HTML client at root
    @app.route("/")
    def index():
        return send_from_directory("../public", "index.html")

    # Set up logging
    setup_logging()
    app.logger.info("App started")

    return app


app = create_app()

asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run(host=config.host, port=config.port, debug=config.debug)
