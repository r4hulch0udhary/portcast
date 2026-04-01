# Module-level in-memory caches shared across all requests

# word -> definition (or None if not found)
definition_cache: dict[str, str | None] = {}

# Full result of the /dictionary endpoint. Set to None to signal "invalid".
dictionary_result_cache: list[dict] | None = None


def invalidate_dictionary_cache() -> None:
    """Call this whenever new paragraphs are added."""
    global dictionary_result_cache
    dictionary_result_cache = None
