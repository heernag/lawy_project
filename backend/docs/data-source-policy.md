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

## Official Source Candidates

These candidates are not enabled in the MVP. They are review targets for a
future provider implementation.

### National Law Information Open Data

URL:

```text
https://open.law.go.kr/LSO/openApi/guideList.do
```

Observed from the official open-data guide:

- The guide lists judgment (`판례`) APIs for list lookup and body lookup.
- The guide also lists constitutional decisions, legal interpretations,
  administrative appeals, legal terms, and other legal information APIs.

Required before implementation:

- Apply for and manage the official API key if required.
- Confirm request parameters for judgment list and body lookup.
- Confirm call limits and acceptable usage.
- Confirm whether storing returned judgment text in the service database is
  allowed.
- Confirm whether displaying original text to end users is allowed.
- Confirm redistribution and commercial-use conditions.
- Confirm required source attribution text.

### Korean Court Judgment Access Pages

URL:

```text
https://www.scourt.go.kr/portal/information/finalruling/peruse/peruse_status.jsp
```

Required before implementation:

- Confirm whether there is an official API or only a user-facing reading page.
- Do not automate crawling unless the site terms clearly allow it.
- Do not bypass access restrictions, payment, authentication, CAPTCHA, or
  rate-limiting controls.
- Confirm whether any downloaded or viewed document can be stored, indexed,
  redisplayed, or used commercially.

## Provider Implementation Rule

Any real-data provider must be added behind the existing case-provider
interface. The MVP must keep working with `SampleCaseProvider` and the
SQLite-backed local provider even if an official provider is unavailable.

Allowed future shape:

```text
CaseProvider
├─ SampleCaseProvider
├─ DbCaseProvider
└─ OfficialPublicCaseProvider
```

Do not mix external API calls directly into route handlers.
