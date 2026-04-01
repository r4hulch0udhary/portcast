from flask import Blueprint, jsonify
from http import HTTPStatus

dictionary_bp = Blueprint("dictionary", __name__, url_prefix="/dictionary")


@dictionary_bp.route("", methods=["GET"])
async def get_dictionary():
    # TODO: Implement dictionary logic
    return jsonify(
        {"message": "Dictionary endpoint not implemented yet"}
    ), HTTPStatus.NOT_IMPLEMENTED
