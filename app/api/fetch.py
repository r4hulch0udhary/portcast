"""
Fetch API Routes.

Handles fetching operations retrieving paragraphs from third-party sources
and storing them efficiently into the database while tracking uniqueness.
"""

from typing import Tuple
from http import HTTPStatus
from flask import Blueprint, jsonify, current_app, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.fetch_service import FetchService
from app.external.metaphorpsum import MetaphorpsumClient
from app.repositories.paragraph_repository import ParagraphRepository


fetch_bp = Blueprint("fetch", __name__, url_prefix="/fetch")


@fetch_bp.route("", methods=["GET"])
async def fetch_paragraph() -> Tuple[Response, int]:
    """
    Fetches a new paragraph from Metaphorpsum client and securely persists it natively in PostgreSQL.

    Returns:
        tuple: (JSON Object with returned paragraph, HTTP status code).
    """
    try:
        async with AsyncSession(current_app.engine) as session:
            metaphorpsum_client = MetaphorpsumClient()
            paragraph_repo = ParagraphRepository(session)
            fetch_service = FetchService(metaphorpsum_client, paragraph_repo)
            content = await fetch_service.fetch_and_store_paragraph(session)
            return jsonify({"paragraph": content}), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Error in fetch: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
