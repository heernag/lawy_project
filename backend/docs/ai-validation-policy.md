# AI Validation Policy

This MVP does not use a paid external LLM.

Case analysis, summaries, and simplification are rule-based and local. The simplifier performs conservative text replacement and then runs validation.

Validation checks:

- amounts
- dates
- rates
- legal article numbers
- sample case numbers
- plaintiff and defendant direction
- judgment result terms
- negative expressions

If a protected value changes or a role direction changes, the paragraph returns:

```json
{
  "validation_status": "review_required",
  "warnings": ["원문과 쉬운 설명의 금액이 일치하지 않습니다."]
}
```

The frontend must not display `review_required` text as verified legal translation.
