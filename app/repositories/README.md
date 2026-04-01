# Repositories Layer

The repository layer (`app/repositories`) is responsible for direct database interactions using `Flask-SQLAlchemy` with asynchronous PostgreSQL (`asyncpg`).

## 🔍 `ParagraphRepository`

- **Save**: Saves paragraphs while returning existing ones natively if they already exist in the database.
- **Uniqueness Check**: Uses a pre-computed SHA-256 hash of paragraph content for O(1) duplicate prevention.

## PostgreSQL Full-Text Search (FTS)

For our `/search` endpoint, we use PostgreSQL's built-in FTS tools rather than basic `LIKE` queries:
- **`to_tsvector`**: Indexes and converts the text of the stored paragraphs into lexemes.
- **`to_tsquery`**: Matches and compares against search terms effectively.
- **Operators Support**: Handles the dynamic text queries with pipes (`|` for OR) and ampersands (`&` for AND).

### Example SQLAlchemy Syntax
```python
query = select(Paragraph.content).where(
    func.to_tsvector('english', Paragraph.content).op('@@')(
        func.to_tsquery('english', search_phrase)
    )
)
```
