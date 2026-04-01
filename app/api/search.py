from flask import Blueprint, jsonify
from http import HTTPStatus

search_bp = Blueprint("search", __name__, url_prefix="/search")


@search_bp.route("", methods=["GET"])
async def search_paragraphs():
    # TODO: Implement search logic
    return jsonify(
        {"message": "Search endpoint not implemented yet"}
    ), HTTPStatus.NOT_IMPLEMENTED
