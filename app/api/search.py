"""
Search API Routes.

Defines the endpoints associated with querying and retrieving stored paragraphs
using PostgreSQL full-text search capability.
"""

import re
from typing import Tuple, Any
from http import HTTPStatus
from flask import Blueprint, jsonify, request, current_app, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.search_service import SearchService
from app.repositories.paragraph_repository import ParagraphRepository


search_bp = Blueprint("search", __name__, url_prefix="/search")


@search_bp.route("", methods=["GET"])
async def search_paragraphs() -> Tuple[Response, int]:
    """
    Search currently stored paragraphs via given words and operator combining method.

    URL Arguments:
        words (str): The comma-separated words.
        operator (str): Search condition (e.g. 'and' or 'or').

    Returns:
        tuple: (JSON response listing matched paragraphs, HTTP status code).
    """
    try:
        words_str = request.args.get("words")
        operator = request.args.get("operator")

        if not words_str or not operator:
            return jsonify(
                {"error": "Missing words or operator"}
            ), HTTPStatus.BAD_REQUEST

        words = [w.strip() for w in re.split(r"[,\s]+", words_str) if w.strip()]
        if not words:
            return jsonify({"error": "No valid words provided"}), HTTPStatus.BAD_REQUEST

        if operator not in ["and", "or"]:
            return jsonify(
                {"error": "Operator must be 'and' or 'or'"}
            ), HTTPStatus.BAD_REQUEST

        async with AsyncSession(current_app.engine) as session:
            paragraph_repo = ParagraphRepository(session)
            search_service = SearchService(paragraph_repo)
            paragraphs = await search_service.search_paragraphs(
                session, words, operator
            )
            return jsonify({"paragraphs": paragraphs}), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Error in search: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
