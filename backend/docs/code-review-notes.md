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
- Health checks now include lightweight case-provider and sample-data bootstrap
  diagnostics.
- Frontend integration docs now include concrete validation error examples,
  including production-like responses where validation details are hidden.
- Address masking now has an explicit false-positive test for road-name text
  followed by an amount expression or sequence-number expression.
- Paragraph sectioning now recognizes appeal and supreme-court procedure
  headings such as `항소취지`, `항소이유`, and `상고이유`.
- Paragraph sectioning also recognizes fixture-backed criminal and
  administrative headings such as `범죄사실`, `증거의 요지`, `법령의 적용`,
  `양형의 이유`, `처분의 경위`, `관계 법령`, and `판단`.
- Error codes now have an exported `ALL_ERROR_CODES` contract and a
  frontend-facing reference table.
- Health diagnostics now live in `HealthService` instead of being calculated
  directly inside the FastAPI route.
- Search similarity now has a free local hash-embedding provider in addition
  to keyword overlap.
- README and `.env.example` now refer to the free local hash similarity mode.
- Frontend TypeScript examples now include core search, detail, and
  simplification response contracts, with a unit test guarding against
  accidental removal.
- OpenAPI now exposes common `ApiResponse` and `ApiError` schemas and has
  integration tests for core frontend paths.
- README startup instructions include local health/OpenAPI checks and a sample
  search request.

Main residual risks:

- Case analysis is still rule-based and intentionally simple. It is safe for a
  free MVP, but recall and classification quality are limited.
- Legal-term extraction and simplification are deterministic MVP logic, not a
  legally complete interpretation engine.
- Validation details include Pydantic metadata only in development-like
  environments. Production-like environments return `details: null`.
- Frontend code should branch on stable error codes, not exact validation
  details.
- Address detection is intentionally conservative and currently covers clear
  Korean road-address patterns only. It avoids masking road-name text followed
  by amount expressions such as `123만 원`.
- Section splitting handles more fixture-backed judgment headings, but remains
  heuristic for unseen court document formats.
- Health checks are still intentionally lightweight and local; they do not call
  external paid services.
- Local hash embeddings are deterministic and free, but they are not a
  substitute for a legally tuned semantic retrieval model.
- The README run/test path has been checked by importing the app and running
  the documented pytest command.
- Existing sample text and some console output can appear garbled on Windows
  terminals if the shell encoding is not UTF-8, even when tests pass.
- A fully fresh dependency installation on a clean machine was not repeated in
  this local pass; the documented installed environment was verified.

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
- Later expanded the splitter to recognize simple numbered headings such as
  `1. 주문`, `2. 청구취지`, and `가. 이유`.
- Later added aliases for party-argument headings such as `원고의 주장` and
  `피고의 주장`.
- Later added aliases for law headings such as `적용법령`, normalized to
  `관련 법령`.
- Later added aliases for recognized-fact headings such as `기초사실` and
  `인정된 사실`, normalized to `인정 사실`.
- Later added aliases for judgment-order headings such as `판결 주문` and
  `주 문`, normalized to `주문`.

Why it matters:

- The requested user flow needs original judgment lookup before paragraph-level
  easy explanations.
- Stable paragraph IDs are necessary for re-simplifying one paragraph without
  regenerating the whole case.

Review notes:

- Good: Paragraph-level storage matches the frontend's likely interaction model.
- Good: Stored simplification state avoids unnecessary recomputation.
- Good: Numbered heading fixtures reduce the chance of only supporting one
  sample text format.
- Good: Party-argument fixture coverage helps keep claims and court reasoning
  separated for downstream simplification.
- Good: Law-heading fixture coverage keeps legal basis text out of conclusion
  paragraphs.
- Good: Recognized-fact fixture coverage helps distinguish facts accepted by
  the court from party arguments.
- Good: Judgment-order fixture coverage protects the most outcome-sensitive
  section from being treated as generic text.
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
- Good: Malformed JSON bodies and missing required fields are covered by
  regression tests for the common error format.
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

### 12. Frontend Validation Error Examples

Related commits:

- `1aa029f docs: add frontend handoff checklist`

What changed:

- Added concrete `INVALID_REQUEST` examples to the frontend integration guide.
- Documented missing-field, invalid-pagination, and production-like
  `details: null` responses.
- Added a small TypeScript error-message helper showing how the frontend can
  branch on stable error codes instead of fragile validation-detail text.
- Added a matching validation-error example to the API spec.

Why it matters:

- Frontend code can handle invalid request bodies without parsing FastAPI's
  default 422 shape.
- UI behavior can remain stable when production hides validation internals.

Review notes:

- Good: The frontend is guided to use `error.code`, which is the stable API
  contract.
- Good: The examples do not expose raw user case text or require paid services.
- Risk: Exact `details` contents should still be treated as diagnostic metadata,
  not as a UI contract.

### 13. Address Masking False-Positive Guard

Related commits:

- `c6c06d0 feat: avoid address masking for amount expressions`
- `23c1cf4 test: add address masking false positive fixtures`

What changed:

- Added a unit test proving that `서울시 강남구 테헤란로 123만 원` is not masked
  as an address.
- Added a unit test proving that `서울시 강남구 테헤란로 3번 쟁점` is not masked
  as an address.
- Updated the road-address privacy pattern so a road-name number followed by a
  Korean amount expression such as `만 원` or `억 원` is not treated as an
  address number.
- Updated the road-address privacy pattern so a road-name number followed by
  `번` is treated as a sequence-number expression, not as a clear address.
- Kept the existing clear road-address masking behavior intact.

Why it matters:

- Legal dispute descriptions often contain place names and money amounts in the
  same sentence.
- Over-masking can make the frontend preview confusing and can hide facts that
  are not actually personal address data.

Review notes:

- Good: The change was driven by a failing regression test before production
  code was changed.
- Good: The rule remains local and free; no external privacy or paid service is
  used.
- Risk: Address detection is still heuristic. New address formats should be
  added with both positive and false-positive fixtures.

### 14. Appeal And Supreme Court Procedure Headings

Related commits:

- `67b2435 feat: recognize appeal procedure headings`

What changed:

- Added a unit test for `항소취지`, `항소이유`, and `상고이유` headings.
- Extended paragraph section heading recognition to normalize those headings to
  `항소 취지`, `항소 이유`, and `상고 이유`.
- Updated the API spec so frontend consumers know these section labels can be
  returned.

Why it matters:

- Public judgments can include procedure-specific sections, especially in
  appellate or supreme-court decisions.
- Keeping these sections separate helps later simplification preserve whether a
  paragraph is a party's appeal reason or a court's reasoning.

Review notes:

- Good: The change is covered by a failing-then-passing unit test.
- Good: The implementation is narrowly scoped to heading aliases and does not
  change paragraph ID generation.
- Risk: More procedure headings may appear in real judgments and should be
  added through fixture tests rather than broad guessing.

### 15. Error Code Contract And Frontend Reference

Related commits:

- `3e3b43c feat: expose stable error code contract`

What changed:

- Added `ALL_ERROR_CODES` to `app.core.errors` as the stable exported list of
  backend error codes.
- Added a unit test that locks the public error-code tuple to the existing
  string constants.
- Added a TypeScript `ApiErrorCode` union and an error-code handling table to
  the frontend integration guide.
- Added a short note to the API spec explaining that error codes are managed as
  backend string constants.

Why it matters:

- The frontend team can treat `error.code` as the stable API contract.
- New or renamed error codes are more likely to be caught in tests and docs
  before they surprise the UI.

Review notes:

- Good: The change keeps the existing response shape and does not alter any API
  behavior.
- Good: The contract is free/local and does not introduce external services.
- Risk: The TypeScript union in the docs is still manually copied. A later
  generated client could eliminate that duplication.

### 16. Health Diagnostics Service

Related commits:

- `a120ebf refactor: move health diagnostics into service`

What changed:

- Added `HealthService` to own case-provider health diagnostics.
- Added unit tests for available sample data, empty provider results, and
  provider failures.
- Updated the health route so it delegates diagnostic calculation to the
  service and only wraps the result in the common success response.
- Updated the API spec to note that health diagnostics are service-backed.

Why it matters:

- The route stays small as diagnostics grow.
- Provider exception details remain hidden behind the generic
  `case provider check failed` message.
- Startup and operations checks can expand later without mixing DB/provider
  logic into HTTP routing code.

Review notes:

- Good: Existing `/api/health` response shape stayed unchanged.
- Good: Failure behavior is now covered at both service and API levels.
- Risk: The health check still only proves the case provider can be queried; it
  does not yet check migrations, disk permissions, or search-index freshness.

### 17. Free Local Hash Embedding Provider

Related commits:

- `a56ed3d feat: add free local hash embeddings`

What changed:

- Added an `EmbeddingProvider` protocol.
- Added `LocalHashEmbeddingProvider`, which turns text into deterministic
  fixed-length vectors using local token hashing.
- Updated `LocalSimilarityService` to combine keyword overlap with local vector
  cosine similarity.
- Added unit tests for deterministic vector generation and embedding-backed
  similarity scoring.
- Updated API and frontend docs to state that search uses free local
  hash-embedding similarity and no paid embedding API.

Why it matters:

- The MVP now has an explicit embedding provider seam without introducing paid
  services.
- Search remains fully local while moving closer to the requested hybrid
  keyword/vector structure.

Review notes:

- Good: The implementation is deterministic, offline, and inexpensive.
- Good: The provider interface leaves room for a stronger free local model later
  without changing search routes.
- Risk: Hash embeddings only approximate lexical vector similarity. They should
  be treated as MVP relevance support, not legal semantic understanding.

### 18. README Run Verification

Related commits:

- `4cabfd2 docs: verify README local setup`
- `ba8b769 docs: verify README startup guide`

What changed:

- Updated README to mention the Bruno collection and Korean frontend flow guide.
- Updated README and `.env.example` from `local_tfidf` to `local_hash`.
- Updated the settings default similarity mode to `local_hash`.
- Added a settings unit test to lock that free local default.
- Verified the README test command with `python -m pytest -v`.
- Verified that the FastAPI app can be created from the documented backend
  environment.

Why it matters:

- A new developer following README sees the current free local search mode.
- The documented run/test path matches the codebase as it now stands.

Review notes:

- Good: The change keeps the project free-only and avoids paid embedding
  services.
- Good: The README now points frontend developers to the Bruno and flow docs.
- Good: `SIMILARITY_MODE=local_hash` is now validated by the search service;
  unsupported modes fail fast instead of silently using a default.
- Risk: A completely clean machine dependency install was not re-run because
  network/package installation is outside this local verification pass.

### 19. Frontend Handoff Checklist And Bruno Collection

Related commits:

- `1aa029f docs: add frontend handoff checklist`

What changed:

- Added a Bruno collection under `backend/bruno` for local API checks.
- Added Korean frontend screen-flow guidance in `frontend-flow-ko.md`.
- Added API checklist documentation for implemented endpoints and frontend
  expectations.

Why it matters:

- The frontend team can test the API without building request bodies from
  scratch.
- The flow guide clarifies that similarity scores are relevance signals, not
  win/loss probabilities.

Review notes:

- Good: Handoff docs match the current free MVP and point to local endpoints.
- Good: Error handling guidance tells the frontend to branch on `error.code`.
- Risk: Bruno files are examples, not a substitute for automated API contract
  tests; keep integration tests as the authoritative gate.

### 20. Official Data Source Policy Review

Related commits:

- `759ee3a docs: expand official data source review policy`

What changed:

- Documented official data-source candidates such as National Law Information
  Open Data and Korean Court judgment reading pages.
- Recorded that storage, redistribution, source display, commercial use, and
  original-text display conditions must be confirmed before implementing a real
  provider.
- Reaffirmed that MVP uses sample data and must not crawl restricted pages.

Why it matters:

- It protects the project from quietly drifting into unauthorized crawling or
  unverified redistribution.
- It preserves the provider boundary for a later official integration.

Review notes:

- Good: The policy is explicit that unknown terms block provider
  implementation.
- Good: Public provider work remains future work, not hidden MVP behavior.
- Risk: Before production with real cases, a fresh source/license review is
  still mandatory.

### 21. Judgment Section Heading Fixtures

Related commits:

- `6243972 test: add judgment section heading fixtures`

What changed:

- Added fixture coverage for criminal judgment headings:
  `범죄사실`, `증거의 요지`, `법령의 적용`, `양형의 이유`.
- Added fixture coverage for administrative judgment headings:
  `처분의 경위`, `관계 법령`, `판단`.
- Normalized those headings to existing section labels where useful.

Why it matters:

- Section splitting is central to paragraph-level simplification and frontend
  display.
- More fixture-backed headings reduce the chance that realistic public
  judgment formats collapse into a single `원문` section.

Review notes:

- Good: The change followed red-green TDD with failing tests first.
- Good: Normalization reuses existing frontend-friendly labels.
- Risk: The splitter is still heuristic and should keep growing through
  concrete fixtures, not broad pattern guesses.

### 22. Frontend TypeScript Contract Examples

Related commits:

- `ed1c273 docs: lock frontend TypeScript contract examples`

What changed:

- Added `CaseSearchResponse`, `CaseDetailResponse`,
  `SimplificationRequest`, `SimplifiedParagraph`, and
  `SimplifiedCaseResponse` TypeScript examples.
- Updated the fetch example to type the search response as
  `ApiResponse<CaseSearchResponse>`.
- Added a unit test that fails if core frontend response type snippets are
  accidentally removed from the guide.

Why it matters:

- The frontend team gets response-level contracts, not only item-level types.
- Manual docs now have a lightweight automated guard.

Review notes:

- Good: Type examples use `snake_case`, matching backend JSON.
- Good: The docs reflect common response wrapping with `ApiResponse<T>`.
- Risk: The TypeScript examples are still manually maintained. Generated
  clients from OpenAPI could reduce duplication later.

### 23. OpenAPI Contract Checks

Related commits:

- `86e2736 test: add OpenAPI contract checks`

What changed:

- Added integration tests that `/openapi.json` exposes core frontend paths.
- Added Pydantic `ApiResponse` and `ApiError` models for OpenAPI components.
- Documented `GET /api/cases/{case_id}` 200 and 404 responses with the common
  response schema.

Why it matters:

- Swagger/OpenAPI now better reflects the project-wide common response shape.
- Frontend contract drift is more likely to be caught by tests.

Review notes:

- Good: The tests verify real generated OpenAPI output through `TestClient`.
- Good: The runtime JSON response shape stayed unchanged.
- Good: Core frontend routes now have explicit common `ApiResponse` metadata
  for 200 responses and expected 400/404 error responses.
- Risk: `ApiResponse.data` is intentionally generic in OpenAPI for the MVP.
  Generated clients may still want endpoint-specific response wrappers later.

### 24. README Startup Guide Verification

Related commits:

- `ba8b769 docs: verify README startup guide`

What changed:

- Added local health and OpenAPI quick-check commands to README.
- Added a representative search API request example.
- Updated README with the latest verified test result:
  `94 passed, 1 warning`.
- Re-verified app creation and core OpenAPI paths from the documented backend
  environment.

Why it matters:

- A new developer can run the backend, check readiness, and try a search call
  with fewer missing steps.
- The README now reflects the current verified state.

Review notes:

- Good: README remains free-only and avoids paid API setup instructions.
- Good: Quick checks are simple enough for handoff.
- Risk: Fresh dependency installation on a brand-new machine was not performed
  because package installation may require network access.

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

### Operations

The health endpoint returns lightweight diagnostics:

- `case_provider`: whether the configured provider can be queried.
- `case_count`: how many stored cases are visible to the provider.
- `sample_data_loaded`: whether at least one MVP sample judgment is available.

This is intentionally lightweight and does not call external services.
Provider failures return `degraded` with a generic message so internal exception
details are not exposed.

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
- Frontend TypeScript documentation snippets
- OpenAPI core path and common response schema contracts

Review recommendation:

- Keep adding tests before every behavior change.
- Add more fixture-based tests before supporting real public judgment formats.
- Keep malformed JSON and missing required field tests focused on stable
  `error.code`, not exact framework detail text.

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

1. Add a generated OpenAPI/TypeScript contract check if the frontend starts
   depending on generated clients.
2. Add migration/search-index freshness checks to `HealthService` if operations
   needs deeper diagnostics.
3. Add more address positive/false-positive fixtures before widening masking.
4. Add more section-splitting fixtures for additional real public judgment
   formats.
5. Add a stronger free local embedding backend only after dependency and
   runtime-size review.

## Verification Snapshot

Latest verification before this document was written:

```text
python -m pytest -q
94 passed, 1 warning
```

The warning is the existing FastAPI/Starlette TestClient deprecation warning.
