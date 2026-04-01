from flask import Blueprint, jsonify
from http import HTTPStatus
from app.services.dictionary_service import DictionaryService
from app.external.dictionary_api import DictionaryAPIClient
from app.repositories.paragraph_repository import ParagraphRepository
from app.models.paragraph import db

dictionary_bp = Blueprint("dictionary", __name__, url_prefix="/dictionary")


@dictionary_bp.route("", methods=["GET"])
async def get_dictionary():
    try:
        async with db.session() as session:
            dictionary_client = DictionaryAPIClient()
            paragraph_repo = ParagraphRepository(session)
            dictionary_service = DictionaryService(dictionary_client, paragraph_repo)
            words_definitions = await dictionary_service.get_top_words_definitions(session)
            return jsonify({"words": words_definitions}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
