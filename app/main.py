from flask import Flask
from app.models.paragraph import db
from app.api.fetch import fetch_bp
from app.api.search import search_bp
from app.api.dictionary import dictionary_bp
from app.config import config

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config.database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.sqlalchemy_track_modifications
app.config["DEBUG"] = config.debug
app.config["ENV"] = config.env

db.init_app(app)

app.register_blueprint(fetch_bp)
app.register_blueprint(search_bp)
app.register_blueprint(dictionary_bp)

if __name__ == "__main__":
    app.run(host=config.host, port=config.port, debug=config.debug)