# External Clients Layer

The external layer (`app/external`) manages outbound communication with third-party HTTP services. It abstracts away REST requests using the asynchronous `httpx` client.

## 🔌 API Integrations

### 1. `MetaphorpsumClient`
- **Target**: `http://metaphorpsum.com/paragraphs/1/1`
- **Purpose**: Retrieves a single random paragraph asynchronously. 

### 2. `DictionaryAPIClient`
- **Target**: `https://api.dictionaryapi.dev/api/v2/entries/en/{word}`
- **Purpose**: Retrieves dictionary definitions for given English words.
- **Fail-Safes**: Gracefully returns empty definitions if words are not found (HTTP 404), preventing backend failures.
