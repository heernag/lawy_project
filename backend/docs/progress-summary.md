# Backend Progress Summary

Updated: 2026-07-15

## Current State

The backend is a free-only FastAPI MVP. It uses local sample judgment data,
SQLite, local rule-based analysis, local keyword search, local validation, and
local documentation. It does not use paid LLM APIs, paid embedding APIs, paid
vector databases, paid case-data APIs, or unauthorized crawling.

Latest committed chapter:

- `a120ebf refactor: move health diagnostics into service`

Uncommitted but implemented and verified:

- Free local hash-embedding provider
- Embedding provider interface
- Local similarity scoring using keyword overlap plus local vector similarity
- Related tests and documentation updates

Latest verified test result:

```text
python -m pytest -q
84 passed, 1 warning
```

The warning is the existing FastAPI/Starlette TestClient deprecation warning.

## Completed Work

### Project Foundation

- FastAPI app structure
- API routes split by responsibility
- Common success/error response format
- CORS support through environment variable
- `.env.example`
- README with local run and test instructions
- Swagger/OpenAPI support through FastAPI

### Data And Persistence

- Sample judgment data loading
- SQLite-backed case document storage
- Case sections and paragraphs stored in DB
- Case summaries stored and reused
- Legal terms stored in SQLite glossary
- Case-to-legal-term links persisted
- Local search index text persisted

### Case Analysis

- Rule-based natural-language case analysis
- Category and sub-category extraction
- Parties, facts, legal issues, keywords, and legal terms extraction
- User-unstated facts are not intentionally added
- Input length validation
- Prompt-injection-like warning output

### Privacy And Input Safety

- Phone number masking
- Resident-registration-number pattern masking
- Email masking
- Clear Korean road-address pattern masking
- False-positive guard for road-name text followed by amount expressions
- Sanitized query returned for frontend preview
- Raw user case text is not intentionally stored long-term

### Search

- Exact case-number search priority
- Category filter
- Court/result metadata filter support
- Decision-date range filter
- Query normalization
- Stored search-index text search
- Keyword overlap similarity
- Similar case lookup
- Free local hash-embedding similarity implemented but not yet committed

### Case Detail And Paragraph Splitting

- Case detail lookup
- Section and paragraph response with stable paragraph IDs
- Common headings recognized: order, claim purpose, reason, recognized facts,
  party arguments, court reasoning, conclusion, and related laws
- Numbered headings recognized
- Appeal/supreme-court procedure headings recognized:
  `항소취지`, `항소이유`, `상고이유`

### Simplification And Validation

- Rule-based paragraph simplification
- Per-paragraph simplified text
- Validation status and warnings
- Checks for amounts, dates, case numbers, rates, legal article numbers,
  judgment-result terms, plaintiff/defendant role changes, obligation subject
  changes, missing negation, and added facts
- Failed validation is returned as review-required style output

### Legal Terms And Summaries

- Legal term lookup API
- Case legal-term extraction API
- Context-linked term extraction with paragraph IDs
- Rule-based case summary generation
- Summary reuse unless force regeneration is requested

### Error Handling And Frontend Contract

- Common request validation error format
- Malformed JSON and missing fields normalized to `INVALID_REQUEST`
- Production-like environments hide validation details
- Stable backend error-code constants
- `ALL_ERROR_CODES` exported for backend contract checks
- Frontend integration guide includes TypeScript examples
- Validation error examples documented

### Health And Operations

- `/api/health`
- Case provider diagnostics
- Sample data loaded check
- Provider failure returns degraded status without exposing exception details
- Health diagnostics moved into `HealthService`

### Tests

- Unit tests for analysis, search, similarity, embeddings, paragraph splitting,
  simplification, validation, legal terms, health, and error codes
- Integration tests for analysis, search, detail lookup, simplification, legal
  terms, DB bootstrap, CORS, health, request validation, and full user flow

## Git Status

Committed through:

- Health diagnostics service chapter

Pending commit:

- Free local hash-embedding search chapter

The pending commit could not be staged earlier because the Git write approval
was blocked by the current Codex usage limit.

## Remaining Work Estimate

Estimated backend MVP progress: about 75% complete.

Estimated remaining backend work: about 25%.

## Remaining Work

### Must Finish For MVP

- Commit the pending free local hash-embedding search work.
- Add or update frontend-facing docs for all final endpoint examples.
- Add Postman or Bruno test collection.
- Add final API endpoint checklist against the original MVP scope.
- Run final full test suite after all docs and pending code are committed.
- Confirm README can be followed from a clean local setup.

### Recommended Before MVP Handoff

- Add more address positive and false-positive fixtures.
- Add more paragraph heading fixtures from real public-format judgments.
- Add a small OpenAPI/TypeScript contract check if the frontend uses generated
  clients.
- Add health diagnostics for DB/search-index freshness only if needed.

### Later, Not Required For Free MVP

- Official public-data API provider integration after terms, storage, reuse,
  source display, and commercial-use conditions are verified.
- Stronger free local embedding backend after dependency size and runtime review.
- Alembic migration workflow hardening.
- Larger judgment fixture set.

## Remaining Amount Only

About 25% of the backend MVP remains.
