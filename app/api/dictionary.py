"""
Dictionary API Routes.

Features frequency analysis on top words inside paragraphs in DB
cross-referencing real meaning via external Dictionary APIs.
"""

from typing import Tuple, Any
from http import HTTPStatus
from flask import Blueprint, jsonify, current_app, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.dictionary_service import DictionaryService
from app.external.dictionary_api import DictionaryAPIClient
from app.repositories.paragraph_repository import ParagraphRepository


dictionary_bp = Blueprint("dictionary", __name__, url_prefix="/dictionary")


@dictionary_bp.route("", methods=["GET"])
async def get_dictionary() -> Tuple[Response, int]:
    """
    Executes a dictionary frequency count matching words with their definition.

    Returns:
        tuple: (JSON containing top words and definitions, HTTP status code).
    """
    try:
        async with AsyncSession(current_app.engine) as session:
            dictionary_client = DictionaryAPIClient()
            paragraph_repo = ParagraphRepository(session)
            dictionary_service = DictionaryService(dictionary_client, paragraph_repo)
            words_definitions = await dictionary_service.get_top_words_definitions(
                session
            )
            return jsonify({"words": words_definitions}), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Error in dictionary: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
