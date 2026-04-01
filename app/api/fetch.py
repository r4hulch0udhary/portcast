from flask import Blueprint, jsonify
from http import HTTPStatus

fetch_bp = Blueprint("fetch", __name__, url_prefix="/fetch")


@fetch_bp.route("", methods=["GET"])
async def fetch_paragraph():
    # TODO: Implement fetch logic
    return jsonify(
        {"message": "Fetch endpoint not implemented yet"}
    ), HTTPStatus.NOT_IMPLEMENTED
