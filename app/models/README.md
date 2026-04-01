# Models Layer

The model layer (`app/models`) defines the database schema using SQLAlchemy Core and Declarative mappings.

## 💾 `Paragraph` Model

Our central and sole data structure:

- **`id`** (`String`): Primary Key, UUID-v4 format, acting as the unique identifier.
- **`content`** (`Text`): The paragraph text itself, mapped to PostgreSQL's `TEXT` column type.
- **`content_hash`** (`String(64)`): Unique constraint, computed via an SHA-256 string hash generated in the constructor. This ensures no duplicate paragraphs are ever inserted.
- **`created_at`** (`DateTime`): Timestamp when the paragraph was saved, defaults to `datetime.now(UTC)`. Often indexed to easily grab the latest fetched paragraph.
