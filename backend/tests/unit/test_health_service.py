from app.services.health_service import HealthService


class WorkingProvider:
    def search_cases(self, query, filters):
        return [{"case_id": "sample-001"}, {"case_id": "sample-002"}]


class EmptyProvider:
    def search_cases(self, query, filters):
        return []


class FailingProvider:
    def search_cases(self, query, filters):
        raise RuntimeError("internal connection detail")


def test_health_service_reports_ok_when_cases_are_available():
    result = HealthService(WorkingProvider()).check()

    assert result == {
        "status": "ok",
        "checks": {
            "case_provider": "ok",
            "case_count": 2,
            "sample_data_loaded": True,
        },
    }


def test_health_service_reports_degraded_when_no_cases_are_available():
    result = HealthService(EmptyProvider()).check()

    assert result == {
        "status": "degraded",
        "checks": {
            "case_provider": "ok",
            "case_count": 0,
            "sample_data_loaded": False,
        },
    }


def test_health_service_hides_provider_exception_details():
    result = HealthService(FailingProvider()).check()

    assert result == {
        "status": "degraded",
        "checks": {
            "case_provider": "error",
            "case_count": 0,
            "sample_data_loaded": False,
            "message": "case provider check failed",
        },
    }
