from flask import Blueprint, jsonify, request
from http import HTTPStatus
from app.services.search_service import SearchService
from app.repositories.paragraph_repository import ParagraphRepository
from app.models.paragraph import db

search_bp = Blueprint("search", __name__, url_prefix="/search")


@search_bp.route("", methods=["GET"])
async def search_paragraphs():
    try:
        words_str = request.args.get("words")
        operator = request.args.get("operator")
        
        if not words_str or not operator:
            return jsonify({"error": "Missing words or operator"}), HTTPStatus.BAD_REQUEST
        
        words = [w.strip() for w in words_str.split(",") if w.strip()]
        if not words:
            return jsonify({"error": "No valid words provided"}), HTTPStatus.BAD_REQUEST
        
        if operator not in ["and", "or"]:
            return jsonify({"error": "Operator must be 'and' or 'or'"}), HTTPStatus.BAD_REQUEST
        
        async with db.session() as session:
            paragraph_repo = ParagraphRepository(session)
            search_service = SearchService(paragraph_repo)
            paragraphs = await search_service.search_paragraphs(session, words, operator)
            return jsonify({"paragraphs": paragraphs}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
