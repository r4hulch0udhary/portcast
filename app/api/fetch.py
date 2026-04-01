from flask import Blueprint, jsonify
from http import HTTPStatus
from app.services.fetch_service import FetchService
from app.external.metaphorpsum import MetaphorpsumClient
from app.repositories.paragraph_repository import ParagraphRepository
from app.models.paragraph import db

fetch_bp = Blueprint("fetch", __name__, url_prefix="/fetch")


@fetch_bp.route("", methods=["GET"])
async def fetch_paragraph():
    try:
        async with db.session() as session:
            metaphorpsum_client = MetaphorpsumClient()
            paragraph_repo = ParagraphRepository(session)
            fetch_service = FetchService(metaphorpsum_client, paragraph_repo)
            content = await fetch_service.fetch_and_store_paragraph(session)
            return jsonify({"paragraph": content}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
