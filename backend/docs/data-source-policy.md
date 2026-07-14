# Data Source Policy

This MVP uses only `MVP sample data` from `data/sample_cases.json`.

On application startup, the sample JSON is loaded into SQLite through the repository layer. API services then read cases through the configured case provider rather than inventing or fetching external cases.

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
