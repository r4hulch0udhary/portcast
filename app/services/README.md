# Services Layer

The service layer (`app/services`) contains the application's core business logic, acting as an intermediary between the API (Controllers), Database (Repositories), and External Applications.

## 🛠 Core Services

1. **`FetchService`**: Orchestrates fetching paragraphs from the external API, validating uniqueness by hashing the content (`SHA-256`), saving them via `ParagraphRepository`, and returning the result.
   
2. **`SearchService`**: Parses search queries and forwards them to the underlying `ParagraphRepository` to perform PostgreSQL Full-Text Search.

3. **`DictionaryService`**: 
   - Generates a frequency map for all stored paragraphs using `regex` filtering out punctuation and stop-words.
   - Determines the top 10 most common words across the system.
   - Asynchronously fetches definitions from the `DictionaryAPIClient`. 
   - Employs module-level caching (to prevent duplicate external requests and improve latency).
