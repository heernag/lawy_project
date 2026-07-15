# Code Review Notes

This document records the backend chapters completed so far, what each chapter
changed, why the change matters, and the review notes to keep in mind before
moving toward a larger MVP release.

The project remains a free-only MVP backend. The current implementation uses
sample/public data, SQLite, local rule-based analysis, local keyword/similarity
logic, and local validation. No paid LLM, paid embedding API, paid vector
database, or paid case-data service has been added.

## Current Review Summary

Overall direction is sound for the requested MVP:

- API, service, provider, repository, schema, DB, and documentation concerns are
  split into separate modules instead of being placed in one file.
- Search, case detail, simplification, summary, legal-term, and validation flows
  are covered by automated tests.
- The backend only returns stored sample cases and does not invent judgments.
- Common API responses are used for success and error cases.
- Recent input-safety work improved privacy masking, prompt-injection warnings,
  search validation, date validation, and request validation errors.

Main residual risks:

- Case analysis is still rule-based and intentionally simple. It is safe for a
  free MVP, but recall and classification quality are limited.
- Legal-term extraction and simplification are deterministic MVP logic, not a
  legally complete interpretation engine.
- Validation details include Pydantic metadata only in development-like
  environments. Production-like environments return `details: null`.
- Address detection is intentionally conservative and currently covers clear
  Korean road-address patterns only.
- Existing sample text and some console output can appear garbled on Windows
  terminals if the shell encoding is not UTF-8, even when tests pass.

## Chapter Reviews

### 1. Sample Case Persistence

Related commits:

- `5a81aba feat: add sample case persistence`
- `04fd247 feat: load sample cases into sqlite provider`

What changed:

- Added sample judgment data loading for the MVP.
- Introduced SQLite-backed storage so the API searches and returns stored data
  instead of generating case results dynamically.
- Kept the data provider boundary so a future official public-data provider can
  replace the sample provider.

Why it matters:

- This directly supports the rule that the service must not create nonexistent
  judgments.
- It gives later search, detail, summary, and simplification features a stable
  data source.

Review notes:

- Good: Provider abstraction keeps the MVP free and replaceable.
- Good: Stored sample data gives integration tests a repeatable target.
- Risk: The project still needs a later official-data integration review before
  any real public-data ingestion is enabled.

### 2. Case Detail And Paragraph Sectioning

Related commits:

- `098ecee feat: add case detail and paragraph sectioning`
- `80478a5 feat: persist case sections and simplifications`

What changed:

- Added detailed case lookup.
- Split original judgment text into sections and paragraphs.
- Persisted sections and paragraph simplification state.

Why it matters:

- The requested user flow needs original judgment lookup before paragraph-level
  easy explanations.
- Stable paragraph IDs are necessary for re-simplifying one paragraph without
  regenerating the whole case.

Review notes:

- Good: Paragraph-level storage matches the frontend's likely interaction model.
- Good: Stored simplification state avoids unnecessary recomputation.
- Risk: Section splitting is still heuristic. More real judgment formats will
  need fixture-based tests.

### 3. Free Rule-Based Case Analysis

Related commits:

- `d79a89b feat: add free rule-based case analysis`

What changed:

- Added local natural-language case analysis for MVP categories, parties, facts,
  issues, keywords, and legal terms.

Why it matters:

- It gives users a useful first response without depending on a paid LLM.
- It respects the free-only direction and avoids hallucinated facts by relying
  on simple extraction rules.

Review notes:

- Good: No paid service dependency.
- Good: Tests check that user-unstated facts are not added.
- Risk: Rule coverage is narrow. It should be expanded through examples rather
  than broad guesses.

### 4. Free Local Search

Related commits:

- `a1caa89 feat: add free local case search`
- `49a3e1e fix: apply search decision date filters`
- `e58a606 feat: persist local case search indexes`

What changed:

- Added local keyword/similarity search.
- Added decision-date filtering.
- Persisted local search text in SQLite-backed search-index records.

Why it matters:

- The MVP can search stored judgments without paid embeddings or external vector
  services.
- Date filters make the search API closer to the requested legal-search
  behavior.

Review notes:

- Good: Search is deterministic and cheap to run locally.
- Good: Exact case-number matching has priority over fuzzy scoring.
- Risk: Local token overlap is not a substitute for robust legal semantic
  search. A later free embedding option can be considered if it runs locally.

### 5. Legal Terms And Summaries

Related commits:

- `289de56 feat: add legal terms and rule-based summaries`
- `f23d038 feat: persist and reuse case summaries`
- `f1a8732 feat: load legal terms into sqlite glossary`
- `d162186 feat: persist case legal term links`

What changed:

- Added legal-term definitions and case-term extraction.
- Added rule-based summaries.
- Stored summaries, glossary data, and case-term links in SQLite.

Why it matters:

- The frontend can show both general term definitions and context-linked terms.
- Reusing stored summaries keeps the MVP fast and predictable.

Review notes:

- Good: Glossary data is DB-backed instead of hardcoded only.
- Good: Case-term links make future UI highlighting easier.
- Risk: Definitions need source and licensing review before moving beyond sample
  MVP terms.

### 6. Simplification And Validation

Related commits:

- `7ddc8be feat: add free rule-based simplification validation`

What changed:

- Added rule-based paragraph simplification.
- Added validation for sensitive legal values such as amounts, dates, case
  numbers, rates, and judgment-result terms.

Why it matters:

- The service must not present changed amounts, dates, parties, or judgment
  outcomes as accurate simplifications.
- Validation warnings give the frontend a way to show review-required states.

Review notes:

- Good: Validation-first design matches the legal-safety requirement.
- Good: The system distinguishes generated explanation from verified text.
- Risk: Validation is not complete legal equivalence checking. It should be
  treated as a safety filter, not proof that a simplification is perfect.

### 7. Documentation And Free Runtime Guide

Related commits:

- `60a1dbf docs: add frontend integration and free runtime guide`

What changed:

- Added API docs, frontend integration guidance, data-source policy, and
  AI-validation policy.

Why it matters:

- Frontend developers need stable request/response examples and TypeScript
  shapes.
- The data-source policy records the "do not crawl or invent" rule.

Review notes:

- Good: Documentation is close to the API implementation.
- Good: Free-only runtime expectations are written down.
- Risk: Documentation must keep being updated with every API response change.

### 8. Privacy Masking In Case Analysis

Related commits:

- `0ec8650 feat: add privacy masking to case analysis`

What changed:

- Added `sanitized_query` to the analysis response.
- Added `privacy_detections`.
- Locally masks phone numbers, resident-registration-number patterns, and email
  addresses with protection tokens.
- Later added conservative masking for clear Korean road-address patterns.

Why it matters:

- Users may paste sensitive real-case facts.
- The frontend can show a privacy-safe preview without echoing raw sensitive
  values.

Review notes:

- Good: Detection is local and free.
- Good: The original query is not added to long-term storage by this feature.
- Risk: Address masking is intentionally narrow. This avoids broad false
  positives, but it will not catch every Korean address form.

### 9. Case Analysis Input Safety

Related commits:

- `c7fc49c feat: add case analysis input safety warnings`

What changed:

- Restricted analysis input length to 5 to 2000 characters.
- Added `input_warnings`.
- Added local warnings for prompt-injection-like phrases such as instructions to
  ignore previous instructions.

Why it matters:

- It keeps the API from accepting meaningless or overly large analysis input.
- It avoids treating prompt-injection-like text as a system instruction.

Review notes:

- Good: Suspicious phrases are warnings, not legal conclusions.
- Good: The feature does not call any external moderation or security service.
- Risk: Warning pattern coverage is intentionally narrow. Expand only through
  concrete test cases.

### 10. Common Request Validation Errors

Related commits:

- `784be19 feat: normalize request validation errors`
- `d751836 feat: validate search date filters`

What changed:

- Converted FastAPI request-validation failures from default 422 responses into
  the project common error format.
- Added a JSON-safe validation error details conversion.
- Added search date validation for `YYYY-MM-DD` and date range ordering.

Why it matters:

- The frontend can handle invalid request bodies consistently.
- Search date filters no longer silently accept malformed date strings.

Review notes:

- Good: Common `INVALID_REQUEST` responses reduce frontend branching.
- Good: JSON-safe details fix prevents custom validators from breaking error
  responses.
- Good: Production-like environments hide internal validation metadata by
  returning `details: null`.
- Risk: Frontend code must treat `error.details` as optional.

### 11. Search Query Normalization

Related commits:

- `0d70833 feat: normalize search query input`

What changed:

- Search query input is trimmed.
- Repeated whitespace is collapsed to a single space.
- Normalized search queries must be 2 to 500 characters.

Why it matters:

- Search behavior is more predictable.
- Very short or overly long queries are rejected before hitting the search
  service.

Review notes:

- Good: Validation lives in the request schema, so the service receives cleaner
  input.
- Good: Tests cover both short-query rejection and whitespace normalization.
- Minor: The search route still has a defensive blank-query check that now
  overlaps with schema validation. It is harmless but could be removed later for
  clarity.

## Cross-Cutting Review

### Architecture

The architecture is moving in the right direction:

- `api/routes` handles HTTP boundaries.
- `schemas` define request and response contracts.
- `services` contain business logic.
- `providers` abstract data sources.
- `repositories` isolate DB access.
- `docs` tracks API and integration expectations.

This separation should continue. Avoid adding direct DB calls to routes or
putting AI/search/data-provider logic into API files.

### Testing

The test suite has grown chapter by chapter and currently covers:

- Case analysis
- Privacy warnings and masking
- Search filters
- Search input validation
- Date validation
- Case detail lookup
- Paragraph sectioning
- Simplification
- Validation warnings
- Legal terms
- DB bootstrap and repository behavior
- CORS
- Full flow

Review recommendation:

- Keep adding tests before every behavior change.
- Add more fixture-based tests before supporting real public judgment formats.
- Add explicit tests for malformed JSON and missing required fields if the
  frontend begins relying heavily on exact validation messages.

### Security And Privacy

Current strengths:

- No paid external LLM or privacy service is used.
- Sensitive-value detection is local.
- Full user input is not intentionally persisted for the MVP.
- Validation errors are normalized.

Review recommendations:

- Keep frontend error handling resilient when `error.details` is `null`.
- Expand address detection only with false-positive tests.
- Keep logs free of raw user case text.

### Legal Safety

Current strengths:

- The service does not predict win/loss probability.
- It does not generate fake case documents.
- Similarity scores are treated as search relevance, not outcome prediction.
- Simplification validation tracks legal-value preservation.

Review recommendations:

- Keep disclaimer text available to frontend surfaces.
- Avoid adding legal-strategy generation endpoints.
- Treat AI-generated text, if added later, as review-required unless validation
  passes.

## Suggested Next Chapters

Recommended order:

1. Add malformed JSON and missing-field API tests.
2. Add more section-splitting fixtures for different judgment formats.
3. Add address false-positive tests before expanding address detection.
4. Add a free local embedding adapter only if it can run without paid APIs.
5. Add a lightweight startup/data-bootstrap health diagnostic.

## Verification Snapshot

Latest verification before this document was written:

```text
python -m pytest -q
67 passed, 1 warning
```

The warning is the existing FastAPI/Starlette TestClient deprecation warning.
