# API Endpoints Layer

The API layer (`app/api`) defines the REST endpoints for the service. It handles HTTP request parsing, input validation, and generating HTTP responses using asynchronous Flask Blueprints.

## 🚀 Endpoints

### 1. `GET /fetch`
- **Purpose**: Fetches a random paragraph from an external source and stores it.
- **Uniqueness Check**: It ensures it's not a duplicate by checking its SHA-256 hash.
- **Returns**: A JSON payload representing the newly stored paragraph.

### 2. `GET /search`
- **Purpose**: Searches through stored paragraphs using PostgreSQL Full-Text Search.
- **Query Params**:
  - `words` (required): Comma or space-separated list of words.
  - `operator` (required): `"and"` | `"or"`. Determines if the query matches all or any of the input words.
- **Returns**: A list of matching paragraphs.

### 3. `GET /dictionary`
- **Purpose**: Analyzes *all* saved paragraphs, extracts the top 10 most frequently used words across the database.
- **Feature**: Pulls word definitions via the Dictionary API.
- **Caching**: Results are cached in-memory to limit external calls.
