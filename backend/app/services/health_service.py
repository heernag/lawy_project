from typing import Any

from app.providers.base_case_provider import CaseProvider


class HealthService:
    def __init__(self, provider: CaseProvider):
        self.provider = provider

    def check(self) -> dict[str, Any]:
        try:
            cases = self.provider.search_cases("", {})
        except Exception:
            return {
                "status": "degraded",
                "checks": {
                    "case_provider": "error",
                    "case_count": 0,
                    "sample_data_loaded": False,
                    "message": "case provider check failed",
                },
            }

        case_count = len(cases)
        return {
            "status": "ok" if case_count > 0 else "degraded",
            "checks": {
                "case_provider": "ok",
                "case_count": case_count,
                "sample_data_loaded": case_count > 0,
            },
        }
