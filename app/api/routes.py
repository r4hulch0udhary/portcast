from flask import Blueprint

api_bp = Blueprint("api", __name__)


@api_bp.route("/")
async def hello():
    return {"message": "Hello World"}
