from pathlib import Path

from app.providers.sample_case_provider import SampleCaseProvider


def test_sample_provider_returns_only_cases_from_json():
    provider = SampleCaseProvider(Path("data/sample_cases.json"))

    results = provider.search_cases("노트북 환불", {})

    assert len(results) >= 1
    assert results[0]["case_id"].startswith("sample-")
    assert results[0]["source_name"] == "MVP sample data"


def test_sample_provider_get_case_returns_none_for_missing_id():
    provider = SampleCaseProvider(Path("data/sample_cases.json"))

    result = provider.get_case("missing")

    assert result is None
