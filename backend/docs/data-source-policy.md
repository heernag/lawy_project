# Data Source Policy

This MVP uses only `MVP sample data` from `data/sample_cases.json`.

On application startup, the sample case JSON is loaded into SQLite through the repository layer. API services then read cases through the configured case provider rather than inventing or fetching external cases.

The MVP glossary is stored in `data/legal_terms.json` and loaded into the `legal_terms` table on startup. It is a built-in educational glossary, not an official legal dictionary.

When a case's legal terms are extracted, the case-term relationship and paragraph context are stored in `case_legal_terms`. This does not add new legal facts; it only records where built-in glossary terms appear in stored case text.

For MVP search, `case_embeddings` stores local search-index text, not paid external embeddings. The value is built from stored sample case metadata, summary, issues, and original text.

The sample data is for development and testing. It does not claim to be an official court judgment, and sample case numbers are intentionally marked as sample IDs.

The backend does not crawl websites.

Official data providers may be added only after confirming:

- API availability
- authentication method
- rate limits
- storage permission
- redistribution permission
- original text display permission
- commercial use permission
- source attribution requirements

Until those conditions are confirmed, official APIs remain documentation-only extension points.
